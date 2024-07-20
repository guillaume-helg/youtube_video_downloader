import os
from dotenv import load_dotenv
import re

from pytube import Playlist, YouTube

from pytubeApi import PytubeApi
from spotifyApi import SpotifyApi
from youtube import YoutubeApi
import utils

load_dotenv()

def print_menu():
    print("\nChoose an option:")
    print("1. Download from youtube")
    print("2. Download from spotify")
    print("3. See my history")
    print("6. Exit")

def main():
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    youtube_api_key = os.getenv('YOUTUBE_API_KEY')

    stf = SpotifyApi(client_id, client_secret)
    ytb = YoutubeApi(youtube_api_key)
    ptb = PytubeApi()


    def download_from_youtube():
        print("Paste your link (video, music, playlist) : ")
        url = input()

        # true if this is a playlist, false if this is not
        x = re.search(".*playlist.*", url)

        if x:
            print("(Playlist) Choose your format : \n1 - audio\n2 - video")
            reponse = int(input())
            ptb.download_playlist_music(Playlist(url)) if reponse == 1 else ptb.download_playlist_video(Playlist(url))
        else:
            print("(Video) Choose your format : \n1 - audio\n2 - video")
            reponse = int(input())
            ptb.download_music(YouTube(url)) if reponse == 1 else ptb.download_video(YouTube(url))

    def download_from_spotify():
        print("Paste your link (spotify playlist) : ")
        url = input()

        track = stf.get_playlist_tracks("https://open.spotify.com/playlist/37i9dQZF1E36aSV6tJQQTm?si=2454b8591ba946c1")
        utils.save_to_file(track, ytb, "aaa.txt")


    def see_my_history():
        print("Not available yet")


    actions = {
        '1': download_from_youtube,
        '2': download_from_spotify,
        '3': see_my_history,
    }

    while True:
        print_menu()
        choice = input("Enter your choice (1-6) : ")

        if choice == '6':
            print("Exiting the program !")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Invalid choice ! Try again !")



if __name__ == "__main__":
    main()