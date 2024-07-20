import os
import re
import sys

def check_file_exists(folder, file):
    file_path = os.path.join(folder, file)
    if os.path.exists(file_path):
        return True
    else:
        return False

def save_to_file(track_info_list, ytb, filename='tracks.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for track in track_info_list:
            track_name, artist_name = track.split('-')
            youtube_url = ytb.search_youtube(track_name, artist_name)
            f.write(f"{track_name} - {artist_name} - {youtube_url}\n")