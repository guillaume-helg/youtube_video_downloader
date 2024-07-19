import os
from dotenv import load_dotenv
import spotifyApi

load_dotenv()

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
youtube_api_key = os.getenv('YOUTUBE_API_KEY')

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
