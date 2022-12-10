

from datetime import datetime

# Placeholder class
class User:
    def __init__(self):
        self.user_id = ""
        self.tournaments = []

class Tournament:
    def __init__(self, tourney_dict):
        self.slug = tourney_dict['slug']
        self.name = tourney_dict['name']
        self.city = tourney_dict['city']
        self.state = tourney_dict['addrState']
        self.start_time =  datetime.fromtimestamp(tourney_dict['startAt'])
        self.start_time_str = self.start_time.strftime('%Y%m%d')
        self.is_online = tourney_dict['isOnline']
        #events_list_of_dict = tourney_dict['events']
        self.events = []

class Event:
    def __init__(self, event_dict):
        self.id = event_dict['id']
        self.num_entrants = event_dict['numEntrants']
        self.competition_tier = event_dict['competitionTier']