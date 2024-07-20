from googleapiclient.discovery import build

class YoutubeApi:
    def __init__(self, youtube_api_key):
        self.ytb = build('youtube', 'v3', developerKey=youtube_api_key)
    
    def search_youtube(self, track_name, artist_name):
        query = f"{track_name} {artist_name}"
        request = self.ytb.search().list(
            q=query,
            part='snippet',
            maxResults=1
        )
        response = request.execute()
        video_id = response['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url