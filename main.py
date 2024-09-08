#!/usr/bin/python3

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

def find_regex_matches(expression: str, source: str | List[str]) -> Tuple[str]:
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
    with open(filename, "a+") as f:
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

################################################
#        Generic recommandation logic          #
################################################

def pick_candidates_from_hosts(candidate_hosts: List[List], seed_titles: List[str], desired_length=25) -> List[str]:
    picks = []

    for host in candidate_hosts:
        host_candidates_features = get_features(host['candidates'])
        if len(picks) >= desired_length:
                return picks
        if host['rank'] > 0:
            for pick in host_candidates_features:
                if pick not in seed_titles:
                    picks.append(pick)
                    host['rank'] -= 1

    return picks

def wrap_candidate_host_content(content: dict, id: str) -> dict:
    return {
        'id': id,
        'content': content
    }

def lookup_saved_candidate_host(candidate_id: str) -> dict:
    candidate_search_string = candidate_id + '.json'
    matches = find_regex_matches(candidate_search_string, get_candidate_hosts())
    
    if matches is None:
        print(f'Could not find host with ID {candidate_id}')
        return None

    print('Found host!')
    return json.load(open(os.path.join(get_pool_location(), matches.group(0)), 'r'))

def save_candidate_host(source: dict) -> None:
    id = source["id"]
    write_to(json.dumps(source), f'{get_pool_location()}/{id}.json', timestamp=False, indentation=2, is_json=True)
    print(f'\nSaved your entered source. Your reference ID is {id}.')
    print('\nSave this ID if you would like to generate a new recommendation based of .')

def find_suitable_hosts(seed: List[str], seed_id: str='') -> List[str]:
    hosts = []
    for candidate_host_location in get_candidate_hosts():
        # We don't want to use our own item as a host.
        if candidate_host_location.replace('.json', '') == seed_id:
            continue
        suitable_hosts = rank_candidates_from_candidate_host(candidate_host_location, seed)

        if suitable_hosts is not None:
            hosts.append(suitable_hosts)

    return sorted(hosts, key= lambda candidate: candidate['rank'], reverse=True)

def rank_candidates_from_candidate_host(candidate_host_location: str, seed: List[str]):
    with open(os.path.join(get_pool_location(), candidate_host_location), 'r') as candidate_host_buffer:
        candidate_host = json.loads(candidate_host_buffer.read())
        candidate_host_id = candidate_host["id"]
        potential_candidates = candidate_host["content"]
        ranking = get_ranking(seed, get_features(potential_candidates))
        if ranking > 0:
            return {'rank': ranking, 'host_id': candidate_host_id, 'candidates': potential_candidates}
        
def get_ranking(seed: List[str], candidate_features: List[str]):
    priority = 0
    for video in seed:
        if video in candidate_features:
            priority += 1
    return priority

def get_pool_location() -> str:
    return os.path.dirname(os.path.realpath(__file__)) + '/pool/'

def get_candidate_hosts() -> List[str]:
    return os.listdir(get_pool_location())

def get_recommendations(source_context: dict, source_context_id: str):
    source_features = get_features(source_context)
    hosts = find_suitable_hosts(source_features, source_context_id)
    return pick_candidates_from_hosts(hosts, source_features)

################################################
#           YouTube specific logic             #
################################################

def fetch_candidate_content(candidate_link: str) -> dict:
    YT_INITIAL_DATA_RE = r'(window["ytInitialData"]|var\s*ytInitialData)\s*=\s*({.+?}.+?);'
    source = requests.get(candidate_link).text
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

def get_features(candidate_content: dict, feature) -> List[str]:
    pool = []
    for content in candidate_content:
        try:
            pool.append(content['playlistVideoRenderer']['title']['runs'][0]['text'])
        except KeyError:
            continue
    return pool

def get_source_candidate_content(seed_link, ref_id):
    candidate_content = fetch_candidate_content(seed_link)
    save_candidate_host(wrap_candidate_host_content(candidate_content, ref_id))

    return candidate_content

def get_youtube_sourced_recommendations(recommend_from):
    VALID_YOUTUBE_PLAYLIST_LINK_RE = r'https://www.youtube.com/playlist\?list=PL[^\s]+'
    VALID_SAVED_CANDIDATE_ID_RE = r'(PL[a-zA-Z0-9].+)\S'

    # Ensure we were provided a valid 'recommended_from' source
    recommendation_source_id_regex_match = find_regex_matches(VALID_SAVED_CANDIDATE_ID_RE, recommend_from)

    if recommendation_source_id_regex_match is None or len(recommendation_source_id_regex_match) <= 0:
        print('Missing or invalid Youtube playlist parameter')
        print('Usage: python main.py [SOURCE_LINK | SAVED_CANDIDATE_ID]')
        return None

    recommendation_source_id = recommendation_source_id_regex_match[0]
    print(f'Searching for candidate with ID {recommendation_source_id}')

    # Get recommendations based off of existing candidate ID
    saved_recommendation_source = lookup_saved_candidate_host(recommendation_source_id)
    youtube_link_match = find_regex_matches(VALID_YOUTUBE_PLAYLIST_LINK_RE, recommend_from)

    if (saved_recommendation_source is None or len(saved_recommendation_source) <= 0) and (youtube_link_match is None or len(youtube_link_match) <= 0):
        print('Malformed source link or ID.')
        return []

    if saved_recommendation_source is not None:
        return get_recommendations(saved_recommendation_source["content"], recommendation_source_id)

    # Get recommendation based off of unsaved source
    if youtube_link_match is not None:
        print(youtube_link_match)
        return get_recommendations(get_source_candidate_content(youtube_link_match[0], recommendation_source_id), recommendation_source_id)

################################################
#         Recommendation entry point           #
################################################

def main(source_recommendation_id):
    return get_youtube_sourced_recommendations(source_recommendation_id)

################################################
#               Package entry                  #
################################################

LOG_NAME = os.environ['LOG_NAME'] or 'error.log'
if __name__ == '__main__':
    print(main(sys.argv[1]))