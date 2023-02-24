from pytube import YouTube
from pytube import Playlist
import re

#fonction permettant d'afficher le pourcentage
def on_download_progress(stream, chunk, bytes_remaining):
    bytes_downloading = stream.filesize - bytes_remaining
    percent = bytes_downloading * 100 / stream.filesize
    print(f"progression du téléchargement {int(percent)}%")

# fonction pour telecharger une playlist au format musique
def dlPlaylistMusic():
    for video in p.videos:
        print("telechargement de : ", video.title)
        video.streams.get_by_itag(140).download()
    
# fonction pour telecharger une musique
def dlOneMusic():
    print("telechargement musical de ", yt.title)
    stream = yt.streams.get_by_itag(140)
    stream.download()
    print("fini")

# fonction pour telecharger une playlist au format video
def dlPlaylistVideo():
    for video in p.videos:
        print("telechargement de : ", video.title)
        video.streams.get_by_itag(22).download()

# fonction pour telecharger une video
def dlOneVideo():
    print("telechargement de la video ", yt.title)
    stream = yt.streams.get_by_itag(22)
    stream.download()
    print("fini")

# fonction pour voir tout les modeles de telechargement
def voirModeleDl():
    yt = YouTube(url)
    for stream in yt.streams.fmt_streams:
        print(" ", stream)

# programme qui demande directement à l'utilisateur le lien de dl
print("Collez le lien de votre playlist, de votre vidéo ou de votre musique")
url = input()
x = re.search(".*playlist.*", url)

if x:
    print("Vous avez mis le lien d'une playlist\ntaper 1 format audio, taper 2 format video")
    p = Playlist(url)
    reponse = int(input())
    dlPlaylistMusic() if reponse == 1 else dlPlaylistVideo()
else:
    print("Vous avez mis le lien d'une video\ntaper 1 format audio, taper 2 format video")
    yt = YouTube(url)
    yt.register_on_progress_callback(on_download_progress)
    reponse = int(input())
    dlOneMusic() if reponse == 1 else dlOneVideo()