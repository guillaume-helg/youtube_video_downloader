import os
import re

from pytubefix import Playlist, YouTube

from pytubeApi import PytubeApi


def print_menu():
    print("\nChoose an option:")
    print("1. Download from youtube")
    print("2. Download from spotify")
    print("3. See my history")
    print("6. Exit")

def main():


    ptb = PytubeApi()

    def download_from_youtube():
        print("Paste your link (video, music, playlist) : ")
        url = input()

        x = re.search(".*playlist.*", url)

        if x:
            print("(Playlist) Choose your format : \n1 - audio\n2 - video")
            reponse = int(input())
            ptb.download_playlist_music(Playlist(url)) if reponse == 1 else ptb.download_playlist_video(Playlist(url))
        else:
            print("(Video) Choose your format : \n1 - audio\n2 - video")
            reponse = int(input())
            ptb.download_music(YouTube(url)) if reponse == 1 else ptb.download_video(YouTube(url), use_oauth=True, allow_oauth_cache=True, use_po_token=True)

    # def download_from_spotify():
    #     print("Paste your link (spotify playlist) : ")
    #     url = input()
    #
    #     tracks = stf.get_playlist_tracks(url)
    #
    #     ptb.download_spotify_tracks(tracks, ytb)


    def see_my_history():
        print("Not available yet")


    actions = {
        '1': download_from_youtube,
        #'2': download_from_spotify,
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