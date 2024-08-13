from Config import *

import requests
import json
from collections import deque
from Event import *

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# Now get a list of live & upcoming games for the sport you want, along with odds for different bookmakers
# This will deduct from the usage quota
# The usage quota cost = [number of markets specified] x [number of regions specified]
# For examples of usage quota costs, see https://the-odds-api.com/liveapi/guides/v4/#usage-quota-costs
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


odds_response = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
    params={
        'api_key': KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
        'commenceTimeFrom': Time.request_time(),
        'sport_key': SPORT
    }
)

if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

else:
    odds_json = odds_response.json()
    # print('Number of events:', len(odds_json))
    # print(odds_json)

    # sports_data = sports_response.json()

    # Iterate through each event


    pretty_sports_data = json.dumps(odds_json, indent=2)
    # print('List of in season sports:', pretty_sports_data)

    stack = deque()

    for event in odds_json:
        id = event['id']
        playerA = event['home_team']
        playerB = event['away_team']

        time = event['commence_time']
        stack.append(Event(id, playerA, playerB, time=time))

        bookmakers = event['bookmakers']

        for bookmaker in bookmakers:
            site = bookmaker['key']
            odds = bookmaker['markets'][0]['outcomes']     # list with odds

            playerA = odds[0]['name']
            playerB = odds[1]['name']
            oddsA = odds[0]['price']
            oddsB = odds[1]['price']

            event = stack.pop()
            event.add(Odds(site, float(oddsA), playerA), Odds(site, float(oddsB), playerB))
            stack.append(event)
    
    for event in stack:
        print(event)


    # # Check the usage quota
    # print('Remaining requests', odds_response.headers['x-requests-remaining'])
    # print('Used requests', odds_response.headers['x-requests-used'])