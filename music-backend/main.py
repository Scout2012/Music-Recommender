import os
import re
import sys
import json
import uuid
import requests
from datetime import datetime
from typing import List, Tuple

################################################
#                  Helpers                     #
################################################

def find_regex_matches(expression: str, source: str) -> Tuple[str]:
        pattern = re.compile(expression)
        return re.findall(pattern, source)

def write_to(msg: str, filename: str, timestamp=True, indentation=0, is_json=False) -> None:
    ts = datetime.now()
    f = open(filename, "a")
    if is_json:
        if timestamp:
            f.write(f'\n{ts} {json.dumps(json.loads(msg), indent=indentation)}')
        else:
            f.write(json.dumps(json.loads(msg), indent=indentation))
    else:
        if timestamp:
            f.write(f'\n{ts} {msg}')
        else:
            f.write(msg)
    f.close()

def tag_playlist(playlist: dict) -> dict:
    tagged = {
        'tag': str(uuid.uuid4()),
        'content': playlist
    }
    return tagged

def save_playlist(playlist: dict) -> None:
    write_to(json.dumps(playlist), f'{playlist["tag"]}.json', timestamp=False, indentation=2, is_json=True)

################################################
#              Main Functions                  #
################################################

def get_playlist_json(playlist: str) -> dict:
    YT_INITIAL_DATA_RE = r'(window["ytInitialData"]|var\s*ytInitialData)\s*=\s*({.+?}.+?);'
    source = requests.get(playlist).text
    try:
        matched_intial_data = find_regex_matches(YT_INITIAL_DATA_RE, source)
        data = matched_intial_data[0][1]
        try:
            playlist_videos = json.loads(data)['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']
            return playlist_videos
        except TypeError as e:
            write_to(str(e), LOG_NAME)
            print(f'Error when attempting to load JSON data. Please inspect {LOG_NAME}')
            exit()
    except BaseException as e:
        write_to(str(e), LOG_NAME)
        print(f'Error when attempting to parse YT_INITIAL_DATA. Please inspect {LOG_NAME}')
        exit()


def get_playlist_titles(playlist_data: dict) -> List[str]:
    video_names = []
    for video in playlist_data:
        video_names.append(video['playlistVideoRenderer']['title']['runs'][0]['text'])
    return video_names

def find_candidates(seed: List[str]) -> List[str]:
    candidates = []
    
    for filename in os.listdir(os.getcwd() + '/pool/'):
        with open(os.path.join(os.getcwd() + '/pool/', filename), 'r') as f:
            # print(json.loads(f.read()))
            pass
    return candidates

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

playlist_json = get_playlist_json(seed_link)
seed_title = get_playlist_titles(playlist_json)
candidates = find_candidates(seed_title)
tagged_seed = tag_playlist(playlist_json)
print(f'Tagged your playlist. Your reference ID is {tagged_seed["tag"]}')
save_playlist(tagged_seed)