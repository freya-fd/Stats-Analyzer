import os
import time
import threading
import requests
import json
import config as cfg
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.cell import cell
from functools import wraps
from pprint import pprint
from enum import Enum

ENDPOINT = 'https://na1.api.riotgames.com/lol/' # might need na. for older summoners
KEY = cfg.DEV_KEY
API_KEY = 'api_key=' + KEY
myTeammates = []
matchPlayers = []
DIR = os.path.dirname(__file__)
#pylint: disable=E0001, E1101, C0111, C0103

class Queue(Enum):
    ARAM = '65'
    INVASION = '990'
    FLEX = '440'
    SOLO = '420'

def update_match_data(data):
    with open(os.path.join(DIR, 'Data\\match_list.txt'), 'w') as f:
        json.dump(data, f)

def id_from_name(name):
    r = requests.get(ENDPOINT + 'summoner/v3/summoners/by-name/' + name + '?' + API_KEY)
    return r.json()['accountId']

def get_matchlist(summonerID, season, queue):
    begin_index = 0
    r = requests.get(ENDPOINT + 'match/v3/matchlists/by-account/' + summonerID + '?season=' + season + '&queue=' + queue + '&beginIndex=' + str(begin_index) + '&' + API_KEY)
    matches = r.json()['matches']
    total_games = r.json()['totalGames']
    remaining_games = total_games
    while remaining_games > 0:
        begin_index += 100
        remaining_games -= 100
        r = requests.get(ENDPOINT + 'match/v3/matchlists/by-account/' + summonerID + '?season=' + season + '&queue=' + queue + '&beginIndex=' + str(begin_index) + '&' + API_KEY)
        matches.extend(r.json()['matches'])

    return matches

def main():
    summonerName = 'Brimstoner'
    SUMID = id_from_name(summonerName)
    update_match_data(get_matchlist(str(SUMID), '9', Queue.SOLO.value))

if __name__ == "__main__":
    main()
