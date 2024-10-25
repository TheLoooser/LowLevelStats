import os
import sys
import time
import requests
from halo import Halo
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

key = os.getenv('KEY')
api = 'https://euw1.api.riotgames.com'
api_match = 'https://europe.api.riotgames.com'

NR_OF_REQUESTS = 0
START = 0

spinner = Halo(text='Getting match data from Riot Games API...', text_color='cyan', color='blue', spinner='line')


def request(base_url, relative_url, parameters):
    global NR_OF_REQUESTS
    global START

    url = f'{base_url}/{relative_url}?{parameters}'
    result = requests.get(url)
    NR_OF_REQUESTS += 1

    # Limit requests per minute (max 50)
    if NR_OF_REQUESTS == 40:
        spinner.color = 'red'
        spinner.text_color = 'magenta'
        spinner.text = 'Pausing... (API Limit reached)'

        while time.time() - START <= 60:
            time.sleep(1)
        NR_OF_REQUESTS = 0
        START = time.time()

        spinner.color = 'blue'
        spinner.text_color = 'cyan'
        spinner.text = 'Getting match data from Riot Games API...'

    return result.json()


def get_information(summoner_name, tag_line, queue_type):
    global START
    global NR_OF_REQUESTS
    begin = time.time()
    START = begin
    summoner_info = {}
    queue_id = 420 if queue_type == 'RANKED_SOLO_5x5' else 440

    # GET SUMMONER
    account = request(api_match, f'riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}', f'api_key={key}')
    puuid = account['puuid']
    summoner = request(api, f'lol/summoner/v4/summoners/by-puuid/{puuid}', f'api_key={key}')
    summoner_info['level'] = summoner['summonerLevel']

    # GET RANK
    summoner_id = summoner['id']
    league_entry = request(api, f'lol/league/v4/entries/by-summoner/{summoner_id}', f'api_key={key}')

    nr_of_matches = 0
    for queue in league_entry:
        if queue['queueType'] == queue_type:
            nr_of_matches = queue['wins'] + queue['losses']
            summoner_info['rank'] = queue['tier']
            summoner_info['division'] = queue['rank']
            summoner_info['lp'] = queue['leaguePoints']
            summoner_info['games'] = nr_of_matches
            summoner_info['win'] = queue['wins'] / nr_of_matches * 100

    if nr_of_matches == 0:
        print("No matches haven been played by this player in the current split.")
        sys.exit(0)

    # GET MATCH IDs
    # assert nr_of_matches <= 100
    start = 0
    count = 100 if nr_of_matches > 100 else nr_of_matches
    all_match_ids = []
    while start < nr_of_matches:
        all_match_ids.extend(request(api_match,
                                     f'lol/match/v5/matches/by-puuid/{puuid}/ids',
                                     f'queue={queue_id}&start={start}&count={count}&api_key={key}'
                                     ))
        start += 100
        if nr_of_matches - start < 100:
            count = nr_of_matches - 100

    '''
    matches = {
        match_id1: [[puuid1, lvl, tier, rank, lp, win-%, lane], [], ...]
    }
    '''
    spinner.start()
    matches = {}
    for match_id in tqdm(all_match_ids, position=1):
        # GET MATCH
        match = request(api_match, f'lol/match/v5/matches/{match_id}', f'api_key={key}')

        player_info = []
        match_info = []
        if 'info' in match:
            for participant in match['info']['participants']:
                r = request(api, f"lol/league/v4/entries/by-summoner/{participant['summonerId']}", f'api_key={key}')

                for queue in r:
                    if queue['queueType'] == queue_type:
                        player_info = [participant['puuid'], participant['summonerLevel'], queue['tier'], queue['rank'],
                                       queue['leaguePoints'], queue['wins'] / (queue['losses'] + queue['wins']),
                                       participant['teamPosition']]

                match_info.append(player_info)

            matches[match_id] = match_info

    spinner.stop()
    print(f'Elapsed time: {time.time() - begin}')
    return summoner_info, matches
