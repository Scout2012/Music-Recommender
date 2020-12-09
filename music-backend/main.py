import re
import sys
import json
import requests
from datetime import datetime
from typing import List, Tuple

def find_regex_matches(expression: str, source: str) -> Tuple[str]:
        pattern = re.compile(expression)
        return re.findall(pattern, source)

def get_playlist_titles(playlist: str) -> List[str]:

    video_names = []
    source = requests.get(playlist).text

    YT_INITIAL_DATA_RE = r'(window["ytInitialData"]|var\s*ytInitialData)\s*=\s*({.+?}.+?);'
    
    matched_intial_data = find_regex_matches(YT_INITIAL_DATA_RE, source)
    try:
        data = matched_intial_data[0][1]
        try:
            playlist_videos = json.loads(data)['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']
        except TypeError as e:
            write_to(str(e), LOG_NAME)
            print(f'Error when attempting to load JSON data. Please inspect {LOG_NAME}')
            exit()
        for video in playlist_videos:
            video_names.append(video['playlistVideoRenderer']['title']['runs'][0]['text'])
    except BaseException as e:
        write_to(str(e), LOG_NAME)
        print(f'Error when attempting to parse YT_INITIAL_DATA. Please inspect {LOG_NAME}')
        exit()
    return video_names

def find_candidates(seed: List[str]) -> int:
    print(seed)

def write_to(msg: str, filename: str) -> None:
    ts = datetime.now()
    f = open(filename, "a")
    f.write(f'\n{ts} {msg}')
    f.close()

LOG_NAME = 'log.txt'
VALID_YOUTUBE_PLAYLIST_LINK_RE = r'https://www.youtube.com/playlist\?list=[^\s]+'

try:
    seed_link = sys.argv[1]
except IndexError:
    print('Missing Youtube playlist parameter')
    print('Usage: python main.py YOUTUBE_PLAYLIST_LINK')
    exit()

youtube_link_match = find_regex_matches(VALID_YOUTUBE_PLAYLIST_LINK_RE, seed_link)
if len(youtube_link_match) != 1:
    print('Invalid Youtube playlist link')
    exit()

seed_title = get_playlist_titles(seed_link)
find_candidates(seed_title)