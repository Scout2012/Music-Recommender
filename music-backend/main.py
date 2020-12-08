import re
import json
import requests
from typing import List

def get_playlist_titles(playlist: str) -> List[str]:

    video_names = []
    source = requests.get(playlist).text

    pattern = re.compile("window\\[\"ytInitialData\"\\]\\s*=\\s*(\\{.*?\\});")
    data = re.findall(pattern, source)[0]

    playlist_videos = json.loads(data)['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']
    # print(json.dumps(playlist_videos, indent=2))

    for video in playlist_videos:
        video_names.append(video['playlistVideoRenderer']['title']['runs'][0]['text'])

    return video_names

print(get_playlist_titles('https://www.youtube.com/playlist?list=PLDIoUOhQQPlXr63I_vwF9GD8sAKh77dWU'))