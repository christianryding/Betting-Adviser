import os
import ast
import time
import requests
import json
import csv
import logging
from classes import Event
from classes import BetsCompleted

# logging
logging.basicConfig(filename='bets_api.log', level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s')

def get_ended_events():
    
    try:
        endedEventsUrl = "https://api.betsapi.com/v2/events/ended?sport_id=151&token={}&day=TODAY".format(os.environ.get('BETS_API_TOKEN'))
        endedEvents = requests.get(endedEventsUrl).json()
        results = endedEvents['results']
    except:
        logging.info("Couldnt get ended events")
    else:
        bets_completed = []
        bets_made = []
        with open('bets.csv','r') as csv_bets:
            csv_reader = csv.reader(csv_bets)
            for line in csv_reader: 
                event_exist = False
                for event_info in results:
                    # if event is completed add it to list 
                    if(line[0] == event_info['id'] and event_info['time_status'] == '3'):
                        bets_completed.append(BetsCompleted(event_info['id'],
                                                event_info['home']['name'],
                                                event_info['away']['name'],
                                                event_info['ss'],
                                                line[1],
                                                line[2],
                                                line[3]))
                        event_exist = True
                if(event_exist == False):
                    bets_made.append(line)

        with open('bets_summary.csv', 'a+', newline='') as f:
            for bets in bets_completed:
                event_result = bets.final_score.split('-')
                if(bets.team_betted_on == 'H' and event_result[0] > event_result[1]):
                    logging.info("won on H {} vs {} with id {}, betted on {}, final score {}!".format(bets.home_name, bets.away_name, bets.bets.eventID, bets.team_betted_on, bets.final_score))
                    sum = float(bets.money_bet) * float(bets.odds) 
                elif(bets.team_betted_on == 'A' and event_result[0] < event_result[1]):
                    logging.info("won on A {} vs {} with id {}, betted on {}, final score {}!".format(bets.home_name, bets.away_name, bets.bets.eventID, bets.team_betted_on, bets.final_score))
                    sum = float(bets.money_bet) * float(bets.odds)
                else:
                    logging.info("Lost on {}!".format(bets.eventID))
                    sum = -float(bets.money_bet)
                csvWriter = csv.writer(f)
                csvWriter.writerow([bets.eventID, bets.home_name, bets.away_name, bets.final_score, bets.team_betted_on, bets.odds, bets.money_bet, sum])

        with open('bets.csv', 'w+', newline='') as f:
            for bets in bets_made:
                csvWriter = csv.writer(f)
                csvWriter.writerow(bets)

# find good events with good odds
def find_events():   
    try:
        events_url = "https://api.betsapi.com/v2/events/upcoming?token={}&sport_id=151?day=TODAY".format(os.environ.get('BETS_API_TOKEN'))
        events = requests.get(events_url).json()
        events_list = []
        current_epoch_time = int(time.time())
        events_access = events['results']
    except:
        logging.info("Couldnt get upcoming events")
    else:
        for events_data in events_access:
            try:
                event_id = events_data['id']
                event_time = events_data['time']
                home_team = events_data['home']['name']
                away_team = events_data['away']['name']
                league = events_data['league']['name']
            except:
                logging.debug("Could not retrieve event id and time in find_events()")
            else:
                # get events within the next 2 hours (7200 sec)
                if((int(event_time)-int(current_epoch_time)) > 0 and (int(event_time)-int(current_epoch_time)) < 7200):
                    events_list.append(Event(event_id, event_time, home_team, away_team, league))  

    # if we find a good event/bet add it 
    for event in events_list:
        try:
            oddsUrl = "https://api.betsapi.com/v2/event/odds?token={}&event_id={}&odds_market=1&source=pinnaclesports".format(os.environ.get('BETS_API_TOKEN'), event.eventId)
            odds = requests.get(oddsUrl).json()
            odds_access = odds['results']['odds']['151_1']
            homeOddsNow = float(odds_access[0]['home_od'])
            homeOddsEarlier = float(odds_access[1]['home_od'])
            awayOddsNow = float(odds_access[0]['away_od'])
            awayOddsEarlier = float(odds_access[1]['away_od'])

            if(homeOddsNow < (homeOddsEarlier*0.99)):
                if(do_bet_exist(event.eventId) == False):
                    place_bet(event.eventId, 'H', homeOddsNow, 50)
                    logging.info("Placed bet on home team {} vs {} with id {}".format(event.home_team, event.away_team, event.eventId))

            if(awayOddsNow < (awayOddsEarlier*0.99)):
                if(do_bet_exist(event.eventId) == False):
                    place_bet(event.eventId, 'A', awayOddsNow, 50)
                    logging.info("Placed bet on away team {} vs {} with id {}".format(event.home_team, event.away_team, event.eventId))
        except:
            logging.debug("No event odds in find_events()")

# check if bet already exist
def do_bet_exist(event_id):
    with open('bets.csv','r') as csv_bets:
        event_exist = False
        csv_reader = csv.reader(csv_bets)
        for line in csv_reader:    
            if(line[0] == event_id):
                event_exist = True
                return event_exist
        return event_exist
    
# place a bet on a specific event
def place_bet(event_id, h_or_a, odds, money_bet):
    with open('bets.csv', 'a+', newline='') as f:
        csvWriter = csv.writer(f)
        csvWriter.writerow([event_id,h_or_a,odds,money_bet])
