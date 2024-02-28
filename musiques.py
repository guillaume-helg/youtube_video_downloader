from pytube import YouTube
from pytube import Playlist
import re
import os


# Before run the code for the first time :
# - check if you have python library
# - check if you have pytube library
# - check if your playlist is public


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


def check_file_exists(folder, file):
    file_path = os.path.join(folder, file)
    if os.path.exists(file_path):
        return True
    else:
        return False


if __name__ == '__main__':
    print("Paste your link (video, music, playlist) : ")
    url = input()

    # true if this is a playlist, false if this is not
    x = re.search(".*playlist.*", url)

    if x:
        print("(Playlist) Choose your format : \n1 - audio\n2 - video")
        reponse = int(input())
        download_playlist_music(Playlist(url)) if reponse == 1 else download_playlist_video(Playlist(url))
    else:
        print("(Video) Choose your format : \n1 - audio\n2 - video")
        reponse = int(input())
        download_music(YouTube(url)) if reponse == 1 else download_video(YouTube(url))
