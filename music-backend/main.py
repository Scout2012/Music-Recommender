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

def find_regex_matches(expression: str, source: str or List[str]) -> Tuple[str]:
        pattern = re.compile(expression)
        search = None
        if(type(source) is type([])):
            for text in source:
                search = re.search(pattern, text)
                if search is not None:
                    return search
            return search
        else:
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
        'tag': str(uuid.uuid4().urn[9:]),
        'content': playlist
    }
    return tagged

def lookup_playlist(uuid: str) -> dict:
    playlist_ref_re = uuid + '.json'
    matched_playlist = find_regex_matches(playlist_ref_re, os.listdir(os.getcwd() + '/pool/'))
    
    if matched_playlist is not None:
        print('Found playlist!')
        return open(os.path.join(os.getcwd() + '/pool/', matched_playlist.group(0)), 'r')
    else:
        print(f'Could find playlist with ID {uuid}')
        return None

def save_playlist(playlist: dict) -> None:
    write_to(json.dumps(playlist), f'pool/{playlist["tag"]}.json', timestamp=False, indentation=2, is_json=True)

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
        try:
            video_names.append(video['playlistVideoRenderer']['title']['runs'][0]['text'])
        except KeyError:
            continue
    return video_names

def find_candidates(seed: List[str]) -> List[str]:
    candidates = []
    
    for filename in os.listdir(os.getcwd() + '/pool/'):
        with open(os.path.join(os.getcwd() + '/pool/', filename), 'r') as f:
            # print(json.loads(f.read()))
            pass
    return candidates

################################################
#              Driver Code                     #
################################################

LOG_NAME = 'log.txt'
VALID_YOUTUBE_PLAYLIST_LINK_RE = r'https://www.youtube.com/playlist\?list=PL[^\s]+'
VALID_UUID_REFERENCE = r'([(0-9a-z)]{8}\-[(0-9a-z)]{4}\-[(0-9a-z)]{4}\-[(0-9a-z)]{4}\-[(0-9a-z)]{12})'

# Optional UUID reference to old playlist
uuid_match = find_regex_matches(VALID_UUID_REFERENCE, sys.argv)
ref_uuid = None

if uuid_match is not None:
    ref_uuid = uuid_match.group(0)
    print(f'Searching for playlist with ID {ref_uuid}')
    playlist_file = lookup_playlist(ref_uuid)
    if playlist_file is not None:
        playlist_data = json.loads(playlist_file.read())["content"]
        playlist_file.close()
        # print(type(playlist_data))
        seed_title = get_playlist_titles(playlist_data)
        candidates = find_candidates(seed_title)
    else:
        print(f'Invalid reference ID given, exiting program.')
        exit()
else:
    youtube_link_match = find_regex_matches(VALID_YOUTUBE_PLAYLIST_LINK_RE, sys.argv)
    
    if youtube_link_match is None:
        print('Missing or invalid Youtube playlist parameter')
        print('Usage: python main.py [REFERENCE-ID | YOUTUBE_PLAYLIST_LINK]')
        exit()

    seed_link = youtube_link_match.group(0)
    playlist_json = get_playlist_json(seed_link)
    seed_title = get_playlist_titles(playlist_json)
    candidates = find_candidates(seed_title)
    tagged_seed = tag_playlist(playlist_json)
    save_playlist(tagged_seed)

    print(f'\nSaved your playlist. Your reference ID is {tagged_seed["tag"]}.')
    print('\nSave this ID if you would like to save time and look your playlist up again.')