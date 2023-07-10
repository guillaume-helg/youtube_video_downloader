from pytube import YouTube
from pytube import Playlist
import re


# Avant de lancé le programme pour la 1ere fois il faut :
# - vérifier que vous ayez la librairie python
# - vérifier que vous ayez la librairie pytube
# - si vous téléchargez une playlist, vérifiez qu'elle soit publique


# fonction pour telecharger une playlist au format musique
def download_playlist_music(playlist):
    for video in playlist.videos:
        print("Downloading : ", video.title)
        video.streams.get_by_itag(140).download()
    

# fonction pour telecharger une musique
def download_music(video):
    print("Downloading : ", video.title)
    stream = video.streams.get_by_itag(140)
    stream.download()


# fonction pour telecharger une playlist au format video
def download_playlist_video(playlist):
    for video in playlist.videos:
        print("Downloading : ", video.title)
        video.streams.get_by_itag(22).download()


# fonction pour telecharger une video
def download_video(video):
    print("telechargement de la video ", video.title)
    stream = video.streams.get_by_itag(22)
    stream.download()


# fonction pour voir tout les modeles de telechargement
def display_all_download_mode():
    ytb_object = YouTube(url)
    for stream in ytb_object.streams.fmt_streams:
        print(" ", stream)


if __name__ == '__main__':
    print("Collez le lien de votre playlist, de votre vidéo ou de votre musique")
    url = input()
    x = re.search(".*playlist.*", url)

    if x:
        print("Vous avez mis le lien d'une playlist\ntaper 1 format audio, taper 2 format video")
        reponse = int(input())
        download_playlist_music(Playlist(url)) if reponse == 1 else download_playlist_video(Playlist(url))
    else:
        print("Vous avez mis le lien d'une video\ntaper 1 format audio, taper 2 format video")
        reponse = int(input())
        download_music(YouTube(url)) if reponse == 1 else download_video(YouTube(url))
