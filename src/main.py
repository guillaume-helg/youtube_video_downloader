import os
import re
from pytubeApi import PytubeApi

def print_menu():
    print("\n--- YouTube Downloader Pro ---")
    print("1. Download from YouTube (Video/Music/Playlist)")
    print("2. See Download History")
    print("3. Exit")
    print("------------------------------")

def main():
    ptb = PytubeApi()

    def download_from_youtube():
        print("\nPaste your link (video, music, or playlist):")
        url = input("> ").strip()
        if not url:
            return

        is_playlist = "playlist" in url.lower()

        if is_playlist:
            print("\n(Playlist) Choose format:")
            print("1 - Audio (.m4a + lyrics)")
            print("2 - Video (.mp4)")
            choice = input("> ")
            if choice == '1':
                ptb.download_playlist_music(url)
            else:
                ptb.download_playlist_video(url)
        else:
            print("\n(Single Video) Choose format:")
            print("1 - Audio (.m4a + lyrics)")
            print("2 - Video (.mp4)")
            choice = input("> ")
            if choice == '1':
                ptb.download_music(url)
            else:
                ptb.download_video(url)

    def see_my_history():
        history = ptb._get_history()
        if not history:
            print("\nYour history is empty.")
        else:
            print("\n--- Download History ---")
            for i, item in enumerate(history, 1):
                print(f"{i}. {item['title']} (ID: {item['id']})")
            print("------------------------")

    actions = {
        '1': download_from_youtube,
        '2': see_my_history,
    }

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '3':
            print("Exiting. Happy listening!")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()