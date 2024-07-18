from pytube import YouTube
from pytube import Playlist

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import re
import os
import sys
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
youtube_api_key = os.getenv('YOUTUBE_API_KEY')


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

def get_playlist_tracks(playlist_link):
    print('hey')
    # Extraire l'ID de la playlist à partir du lien
    playlist_id = playlist_link.split('/')[-1].split('?')[0]

    results = sp.playlist_tracks(playlist_id)
    print(playlist_id)

    tracks = results['items']

    track_info_list = []

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    for idx, item in enumerate(tracks):
        track = item['track']
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        track_info_list.append(f"{track_name} - {artist_name}")

    return track_info_list


def search_youtube(track_name, artist_name):
    query = f"{track_name} {artist_name}"
    request = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=1
    )
    response = request.execute()
    video_id = response['items'][0]['id']['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    return video_url

def save_to_file(track_info_list, filename='tracks.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for track in track_info_list:
            track_name, artist_name = track.split('-')
            youtube_url = search_youtube(track_name, artist_name)
            f.write(f"{track_name} - {artist_name} - {youtube_url}\n")


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
    track = get_playlist_tracks("https://open.spotify.com/playlist/37i9dQZF1E36aSV6tJQQTm?si=2454b8591ba946c1")
    print(track)
    save_to_file(track, "aaa.txt")

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
