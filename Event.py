import datetime

import requests

from Config import KEY


class Event:
    def __init__(self, event_id: str, playerA: str, playerB: str, oddsA: 'Odds'=None, oddsB: 'Odds'=None, time: str=None):
        self.event_id = event_id
        self.playerA = playerA
        self.playerB = playerB
        self.oddsA = Odds('', 0, '')
        self.oddsB = Odds('', 0, '')
        self.time = time
    
    def add(self, newOddsA: 'Odds', newOddsB: 'Odds'):
        if newOddsA > self.oddsA:
            self.oddsA = newOddsA
        if newOddsB > self.oddsB:
            self.oddsB = newOddsB

    def score(self) -> float:
        if self.oddsA.odds == 0 or self.oddsB.odds == 0:
            return 0
        return (1 / self.oddsA.odds) + (1 / self.oddsB.odds)
    
    def isArbitrage(self) -> bool:
        return self.score() < 1

    def __str__(self) -> str:
        if self.isArbitrage():
            return f'{self.playerA} vs {self.playerB} {self.time} is an arbitrage opportunity! \n {self.oddsA} {self.oddsB}\nThis adds up to {self.score()}\n--------------------------\n'
        else:
            return f'{self.playerA} vs {self.playerB} is not an arbitrage opportunity with odds {self.oddsA.odds} and {self.oddsB.odds} = {self.score()}\n--------------------------\n'

    def __gt__(self, other: 'Event') -> bool:
        if isinstance(other, Event):
            return self.score() > other.score()
    
    @staticmethod
    def from_json(json: dict) -> 'Event':
        id = json['id']
        playerA = json['home_team']
        playerB = json['away_team']
        time = json['commence_time']
        return Event(id, playerA, playerB, time=time)
    
    @staticmethod
    def possible_events(key: str, will_print: bool=False, url: str=None) -> 'requests.models.Response':
        if url is None:
            return None
        
        sports_response = requests.get(
            'https://api.the-odds-api.com/v4/sports', 
            params={
                'api_key': key
            }
        )
        if will_print:
            if sports_response.status_code != 200:
                print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')
            else:
                print('List of in season sports:', sports_response.json())
        return sports_response
        
    

class Odds:
    def __init__(self, site: str, odds: float, player: str):
        self.site = site
        self.odds = odds
        self.player = player
    
    def __gt__(self, other: 'Odds') -> bool:
        if isinstance(other, Odds):
            return self.odds > other.odds
        
    def __str__(self) -> str:
        return self.player + "\n    " + self.site + ": " +str(self.odds) + "\n\n"
    
class Time:
    
    @staticmethod
    def request_time() -> str:
        time_string = str(datetime.datetime.now() + datetime.timedelta(hours=4))
        year = time_string[:4]
        month = time_string[5:7]
        day = time_string[8:10]
        hour = time_string[11:13]
        minute = time_string[14:16]
        seconds = time_string[17:19]
        print(f'{year}-{month}-{day}T{hour}:{minute}:{seconds}Z')
        return f'{year}-{month}-{day}T{hour}:{minute}:{seconds}Z'
    
