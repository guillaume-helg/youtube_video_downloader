import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyApi:
    def __init__(self, client_id, client_secret):
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))

    def get_playlist_tracks(self, playlist_link):
        playlist_id = playlist_link.split('/')[-1].split('?')[0]

        results = self.sp.playlist_tracks(playlist_id)

        tracks = results['items']

        track_info_list = []

        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])

        for idx, item in enumerate(tracks):
            track = item['track']
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            track_info_list.append(f"{track_name} - {artist_name}")

        return track_info_list