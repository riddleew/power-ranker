

from datetime import datetime

# Placeholder class
class User:
    def __init__(self):
        self.user_id = ""
        self.gamer_tag = ""
        self.all_tournies = []
        self.ky_tournies = []

class Tournament:
    def __init__(self, tourney_dict):
        self.slug = tourney_dict['slug']
        self.name = tourney_dict['name']
        self.city = tourney_dict['city']
        self.state = tourney_dict['addrState']
        try:
            self.start_time =  datetime.fromtimestamp(tourney_dict['startAt'])
        except:
            print("Start date for " + tourney_dict['name'] + " is invalid.")
            self.start_time = datetime.fromtimestamp(0)
        self.start_time_str = self.start_time.strftime('%Y%m%d')
        self.is_online = tourney_dict['isOnline']
        self.events = []
        # Used to keep track of which tracked players traveled to out of state tournaments
        self.notable_entries = []

class Event:
    def __init__(self, event_dict):
        self.id = event_dict['id']
        self.slug = event_dict['slug']
        self.name = event_dict['name']
        self.num_entrants = event_dict['numEntrants']
        self.start_time =  datetime.fromtimestamp(event_dict['startAt'])
        self.start_time_str = self.start_time.strftime('%Y%m%d')
        self.is_teams_event = event_dict['teamRosterSize'] != None
        self.activity_state = event_dict['state']

    def __eq__(self, other):
        if (self.id == other.id and self.slug == other.slug and self.name == other.name
            and self.num_entrants == other.num_entrants and self.is_teams_event == other.is_teams_event):
            return True

        return False

    def __hash__(self):
        return (hash(self.id) ^ hash(self.slug) ^ hash(self.name) ^
                hash(self.num_entrants) ^ hash(self.is_teams_event))