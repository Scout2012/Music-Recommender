import os
import re
import sys
import json
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

################################################
#              Main Functions                  #
################################################

def source_songs(candidates: List[List], seed_titles: List[str], desired_playlist_size=25) -> List[str]:
    songs = []

    for candidate in candidates:
        while(candidate[0] > 0):
            for song in candidate[2]:
                if song not in seed_titles:
                    if len(songs) < desired_playlist_size:
                        songs.append(song)
                        candidate[0] -= 1
                    else:
                        return songs
    return songs

def tag_playlist(playlist: dict, playlist_id: str) -> dict:
    tagged = {
        'tag': playlist_id,
        'content': playlist
    }
    return tagged

def lookup_playlist(playlist_id: str) -> dict:
    playlist_ref_re = playlist_id + '.json'
    matched_playlist = find_regex_matches(playlist_ref_re, os.listdir(os.getcwd() + '/pool/'))
    
    if matched_playlist is not None:
        print('Found playlist!')
        return open(os.path.join(os.getcwd() + '/pool/', matched_playlist.group(0)), 'r')
    else:
        print(f'Could not find playlist with ID {playlist_id}')
        return None

def save_playlist(playlist: dict) -> None:
    write_to(json.dumps(playlist), f'pool/{playlist["tag"]}.json', timestamp=False, indentation=2, is_json=True)

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

def find_candidates(seed: List[str], seed_id: str='') -> List[str]:
    candidates = []
    priority = 0
    current_playlist_names = None
    for filename in os.listdir(os.getcwd() + '/pool/'):
        priority = 0
        current_playlist_names = None
        # We don't want to use our own playlist as a source.
        # 36 is length of uuid4, the uuid we use.
        if filename[:-5] != seed_id:
            with open(os.path.join(os.getcwd() + '/pool/', filename), 'r') as f:
                playlist = json.loads(f.read())
                tag = playlist["tag"]
                videos = playlist["content"]
                current_playlist_names = get_playlist_titles(videos)
                for video in seed:
                    if video in current_playlist_names:
                        priority += 1
                if priority > 0:
                    candidates.append([priority, tag, current_playlist_names])
    return sorted(candidates, reverse=True)

################################################
#              Driver Code                     #
################################################

LOG_NAME = 'log.txt'
VALID_YOUTUBE_PLAYLIST_LINK_RE = r'https://www.youtube.com/playlist\?list=PL[^\s]+'
YOUTUBE_ID_RE = r'(PL[a-zA-Z0-9].+)\S'
# VALID_UUID_REFERENCE = r'([(0-9a-z)]{8}\-[(0-9a-z)]{4}\-[(0-9a-z)]{4}\-[(0-9a-z)]{4}\-[(0-9a-z)]{12})'

id_match = find_regex_matches(YOUTUBE_ID_RE, sys.argv)
youtube_link_match = find_regex_matches(VALID_YOUTUBE_PLAYLIST_LINK_RE, sys.argv)

if id_match is not None:
    ref_id = id_match.group(0)
    print(f'Searching for playlist with ID {ref_id}')
    playlist_file = lookup_playlist(ref_id)
    if playlist_file is not None:
        playlist_data = json.loads(playlist_file.read())["content"]
        playlist_file.close()
        seed_titles = get_playlist_titles(playlist_data)
        candidates = find_candidates(seed_titles, ref_id)
        songs = source_songs(candidates, seed_titles)
        print(songs)

    elif youtube_link_match is not None:
        seed_link = youtube_link_match.group(0)
        playlist_json = get_playlist_json(seed_link)
        seed_titles = get_playlist_titles(playlist_json)
        candidates = find_candidates(seed_titles)
        songs = source_songs(candidates, seed_titles)
        print(songs)

        # Finishing touches, tag and save the playlist in the pool
        tagged_seed = tag_playlist(playlist_json, ref_id)
        save_playlist(tagged_seed)

        print(f'\nSaved your playlist. Your reference ID is {tagged_seed["tag"]}.')
        print('\nSave this ID if you would like to save time and look your playlist up again.')
    else:
        print('Playlist with that ID does not exist in our system.')
        exit()
else:
    print('Missing or invalid Youtube playlist parameter')
    print('Usage: python main.py [YOUTUBE_PLAYLIST_LINK | YOUTUBE_PLAYLIST_LINK_ID]')
    exit()