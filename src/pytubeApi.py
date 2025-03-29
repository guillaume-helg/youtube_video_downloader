import os
import json
import subprocess
import lyricsgenius
import yt_dlp
from mutagen.mp4 import MP4
from mutagen.flac import FLAC
import utils
from dotenv import load_dotenv

load_dotenv()

class PytubeApi:
    def __init__(self):
        self.history_file = os.path.join(os.path.dirname(__file__), "data", "history.json")
        self.genius_token = os.getenv("GENIUS_ACCESS_TOKEN")
        self.genius = lyricsgenius.Genius(self.genius_token) if self.genius_token else None
        self._ensure_history_exists()
        self.ffmpeg_available = self._check_ffmpeg()

        # yt-dlp logger to silence some output if desired, or keep it default
        self.ydl_opts_base = {
            'noplaylist': True,
            'quiet': False,
            'windowsfilenames': True,
        }

    def _check_ffmpeg(self):
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("WARNING: FFmpeg not found. Downloading audio as m4a with metadata may fail or behave incorrectly.")
            print("Please install FFmpeg to enable these features.")
            return False

    def _ensure_history_exists(self):
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        if not os.path.exists(self.history_file) or os.path.getsize(self.history_file) == 0:
            with open(self.history_file, 'w') as f:
                json.dump([], f)

    def _get_history(self):
        self._ensure_history_exists()
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("WARNING: History file corrupted. Resetting.")
            with open(self.history_file, 'w') as f:
                json.dump([], f)
            return []

    def _add_to_history(self, video_id, title):
        history = self._get_history()
        if video_id not in [item['id'] for item in history]:
            history.append({"id": video_id, "title": title})
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=4)

    def is_already_downloaded(self, video_id):
        history = self._get_history()
        return any(item['id'] == video_id for item in history)

    def download_playlist_music(self, playlist_url):
        print(f"Fetching playlist info: {playlist_url}")
        ydl_opts = {
            'extract_flat': True,
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            if 'entries' in info:
                for entry in info['entries']:
                    self.download_music(entry['url'])
                    
    def download_music(self, url):
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            video_id = info.get('id')
            title = info.get('title')

        if self.is_already_downloaded(video_id):
            print(f"Skipping (already downloaded): {title}")
            return

        print(f"Downloading Audio: {title}")

        # Best audio, then extract to m4a (alac)
        ydl_opts = dict(self.ydl_opts_base)
        ydl_opts.update({
            'format': 'bestaudio/best',
            'outtmpl': './DL_music/%(title)s.%(ext)s',
        })
        
        if self.ffmpeg_available:
            ydl_opts.update({
                'writethumbnail': True,
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'm4a',
                        'preferredquality': '192',
                    },
                    {
                        'key': 'EmbedThumbnail',
                        'already_have_thumbnail': False,
                    },
                    {
                        'key': 'FFmpegMetadata',
                        'add_metadata': True,
                    }
                ],
            })

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                download_path = ydl.prepare_filename(info_dict)
                
                if self.ffmpeg_available:
                    # The postprocessor changes the extension to .m4a
                    base, _ = os.path.splitext(download_path)
                    final_file = base + ".m4a"
                else:
                    final_file = download_path

                self._add_metadata(final_file, info_dict)
                self._add_to_history(video_id, title)
                print(f"Finished: {final_file}")

        except Exception as e:
            print(f"Error downloading music: {e}")

    def _add_metadata(self, filepath, info_dict):
        if not os.path.exists(filepath):
            return

        title = info_dict.get('track', info_dict.get('title', 'Unknown Title'))
        artist = info_dict.get('artist', info_dict.get('uploader', 'Unknown Artist'))
        album = info_dict.get('album', '')

        if filepath.endswith(".m4a"):
            try:
                audio = MP4(filepath)
                
                # Check if yt-dlp's FFmpegMetadata already provided better tags
                # We only overwrite if missing, or if we need to explicitly inject missing info.
                
                if not audio.get("\xa9nam"):
                    audio["\xa9nam"] = title
                if not audio.get("\xa9ART"):
                    audio["\xa9ART"] = artist
                if album and not audio.get("\xa9alb"):
                    audio["\xa9alb"] = album
                
                if self.genius:
                    print(f"Fetching lyrics for: {title} by {artist}")
                    try:
                        song = self.genius.search_song(title, artist)
                        if song:
                            audio["\xa9lyr"] = song.lyrics
                    except Exception as e:
                        print(f"Could not fetch lyrics: {e}")
                
                audio.save()
            except Exception as e:
                print(f"Error adding ALAC metadata to {filepath}: {e}")

    def download_playlist_video(self, playlist_url):
         print(f"Fetching playlist info: {playlist_url}")
         ydl_opts = {
            'extract_flat': True,
            'quiet': True
         }
         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            playlist_title = info.get('title', 'playlist')
            if 'entries' in info:
                for entry in info['entries']:
                    self.download_video(entry['url'], folder=playlist_title)

    def download_video(self, url, folder="video"):
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            video_id = info.get('id')
            title = info.get('title')

        if self.is_already_downloaded(video_id):
            print(f"Skipping (already downloaded): {title}")
            return
            
        print(f"Downloading Video: {title}")
        
        ydl_opts = dict(self.ydl_opts_base)
        if self.ffmpeg_available:
            ydl_opts.update({
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': f'./DL_{folder}/%(title)s.%(ext)s',
                'merge_output_format': 'mp4',
            })
        else:
            ydl_opts.update({
                'format': 'best',
                'outtmpl': f'./DL_{folder}/%(title)s.%(ext)s',
            })

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                self._add_to_history(video_id, title)
        except Exception as e:
            print(f"Error downloading video: {e}")

    def display_all_download_mode(self, url):
        ydl_opts = {
            'listformats': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=False)

    def download_spotify_tracks(self, tracks, ytb):
        # Implementation skipped
        pass
