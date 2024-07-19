from pytube import YouTube
from pytube import Playlist

class PytubeApi:
    def __init__(self):
        pass
    
    # Allow to download playlist of music
    def download_playlist_music(playlist):
        for video in playlist.videos:
            if not check_file_exists(f"DL_{playlist.title}", f"{video.title}.mp4"):
                print("Downloading : ", video.title)
                video.streams.get_by_itag(140).download(f"./DL_{playlist.title}")
        
    
    # Allow to download music
    def download_music(video):
        print("Downloading : ", video.title)
        stream = video.streams.get_by_itag(140)
        stream.download("./DL_music/")
    
    
    # Allow to download playlist of video
    def download_playlist_video(playlist):
        for video in playlist.videos:
            if not check_file_exists(playlist.title, video.title):
                print("Downloading : ", video.title)
                video.streams.get_by_itag(22).download(f"./DL_{playlist.title}")
    
    # Allow to download video
    def download_video(video):
        print("Downloading : ", video.title)
        stream = video.streams.get_by_itag(22)
        stream.download("./DL_video/")
    
    # Allow to see each download mode enable
    def display_all_download_mode(url):
        ytb_object = YouTube(url)
        for stream in ytb_object.streams.fmt_streams:
            print(" ", stream)
