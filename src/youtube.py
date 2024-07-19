from googleapiclient.discovery import build

class YoutubeApi:
    def __init__(self, youtube_api_key):
        youtube = build('youtube', 'v3', developerKey=youtube_api_key)
        pass
    
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