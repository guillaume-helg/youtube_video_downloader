from pytube import YouTube, Playlist
import utils

class PytubeApi:
    def __init__(self):
        pass
    

    # Allow to download playlist of music
    def download_playlist_music(self, playlist):
        for video in playlist.videos:
            if not utils.check_file_exists(f"DL_{playlist.title}", f"{video.title}.mp4"):
                print("Downloading : ", video.title)
                video.streams.get_by_itag(140).download(f"./DL_{playlist.title}")
        
    

    # Allow to download music
    def download_music(self, video):
        print("Downloading : ", video.title)
        stream = video.streams.get_by_itag(140)
        stream.download("./DL_music/")
    
    
    # Allow to download playlist of video
    def download_playlist_video(self, playlist):
        for video in playlist.videos:
            if not utils.check_file_exists(playlist.title, video.title):
                print("Downloading : ", video.title)
                video.streams.get_by_itag(22).download(f"./DL_{playlist.title}")
    
    # Allow to download video
    def download_video(self, video):
        print("Downloading : ", video.title)
        stream = video.streams.get_by_itag(22)
        stream.download("./DL_video/")
    

    # Allow to see each download mode enable
    def display_all_download_mode(self, url):
        ytb_object = YouTube(url)
        for stream in ytb_object.streams.fmt_streams:
            print(" ", stream)

    def download_spotify_tracks(self, tracks, ytb):
        for track in tracks:
            track_name, artist_name = track.split('-')
            youtube_url = ytb.search_youtube(track_name, artist_name)
            self.download_music(YouTube(youtube_url))
