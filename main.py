from datetime import datetime
import json

from graphqlclient import GraphQLClient

import queries
from datamodels import *

def get_token():
  """Retrieves oauth token from a text file."""
  with open('token.txt', 'r') as file:
    return file.readline()


def collect_user_ids_from_file():
  """Reads through a text file and compiles a dictionary of user_id -> player_name."""
  with open('user-ids.txt', 'r') as file:
    delimiter = '---'
    for line in file:
      if line.startswith('#'):
        continue
      # Get player name
      name_idx = line.index(delimiter)
      player_name = line[:name_idx]
      
      # Get user id
      id_idx = name_idx + 3
      user_id = line[id_idx:].strip()
      user_dict[user_id] = player_name


def set_tournaments():
  """Runs a tournament query for each user that was collected.
  Returns a dictonary of tourney_slug -> TourneyObj.
  """
  tourney_dict = dict()
  for user_id, player_name in user_dict.items():
    print("Processing " + player_name + "'s tournaments...")
    query_variables = {"userId": user_id}
    result = client.execute(queries.get_tournies_by_user, query_variables)
    res_data = json.loads(result)
    if 'errors' in res_data:
        print('Error:')
        print(res_data['errors'])

    for tourney_json in res_data['data']['user']['tournaments']['nodes']:
      cut_off_date_start = datetime(2022, 10, 1)
      cut_off_date_end = datetime(2022, 12, 31)
      
      tourney = Tournament(tourney_json)
    
      str_date = tourney.start_time.strftime('%m-%d-%Y')
      
      if tourney.start_time >= cut_off_date_start and tourney.start_time <= cut_off_date_end:
        if tourney.is_online:
          continue
        print(tourney.name + '\t' + str_date)
        tourney_dict[tourney.slug] = tourney
      elif tourney.start_time < cut_off_date_start:
        print('Tournament outside of season window --- ' + tourney.name + '\t' + str_date)
        break
  
  return tourney_dict


def write_tourney_names_to_files(tournies):
  """Writes tourney names/slugs with dates to text files.
  Allows for a simple overview summary of tournaments.
  """
  i = 1
  with open('tourney_names.txt', 'w') as names, open('tourney_slugs.txt', 'w') as slugs:
    
    for tourney in tournies:
      names.write(f'{tourney.start_time} --- {tourney.name} --- {tourney.city}, {tourney.state}\n')
      slugs.write(f'{tourney.start_time} --- {tourney.slug} --- {tourney.city}, {tourney.state}\n')
      
      print(f'{i}: {tourney.slug}')
      i = i + 1

auth_token = get_token()
api_version = 'alpha'
client = GraphQLClient('https://api.smash.gg/gql/' + api_version)
client.inject_token('Bearer ' + auth_token)
ultimate_id = '1386'
user_dict = dict()

collect_user_ids_from_file()
# Returns a dict of tournies, and then converts it to a sorted list of tournies.
# Dict is initially used to guard against duplicate tourney entries.
tournies = sorted(set_tournaments().values(), key=lambda tourney: tourney.start_time)
write_tourney_names_to_files(tournies)