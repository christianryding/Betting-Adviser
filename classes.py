class BetsCompleted:  
    def __init__(self, eventID, home_name, away_name, final_score, team_betted_on, odds, money_bet):
        self.eventID = eventID   
        self.home_name = home_name
        self.away_name = away_name
        self.final_score = final_score
        self.team_betted_on = team_betted_on
        self.odds = odds
        self.money_bet = money_bet  


class Event:
    def __init__(self, eventId, time, home_team, away_team, league):
        self.eventId = eventId   
        self.time = time
        self.home_team = home_team
        self.away_team = away_team  
        self.league = league

    def getEventId(self):
        return '{}'.format(self.eventId)

    def set_home_team(self, home_team):
        self.home_team = home_team