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

ENDPOINT = 'https://na1.api.riotgames.com/lol/' # might need na. for older summoners
KEY = cfg.DEV_KEY
API_KEY = 'api_key=' + KEY
MATCHES = []
myTeammates = []
matchPlayers = []
DIR = os.path.dirname(__file__)
CHAMP_LIST = {}
#pylint: disable=E0001, E1101, C0111, C0103

def load_champ_data():
     with open(os.path.join(DIR, 'Data\\champ_list.txt')) as data_file:
        global CHAMP_LIST
        CHAMP_LIST = json.load(data_file)

# Returns true if champ_list.txt is current
def check_version():
    r = requests.get(ENDPOINT + 'static-data/v3/versions?' + API_KEY)
    return(r.json()[0] == CHAMP_LIST['version'])

def get_champ_list():
    if check_version() == True:
        return(CHAMP_LIST['data'])
    else:
        r = requests.get(ENDPOINT + 'static-data/v3/champions?locale=en_US&dataById=true&' + API_KEY)
        print(r.headers)
        with open(os.path.join(DIR, 'Data\\champ_list.txt'), 'w') as f:
            json.dump(r.json(), f)

def get_champ_name(id):
    return(get_champ_list()[str(id)]['name'])

def main():
    load_champ_data()
    print(get_champ_name(60))

if __name__ == "__main__":
    main()
