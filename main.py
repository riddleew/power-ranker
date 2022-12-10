from datetime import datetime
import json
from urllib.error import URLError

from graphqlclient import GraphQLClient

import queries
from datamodels import *


def get_tokens():
  """Retrieves oauth tokens from a text file."""
  
  tokens = []
  with open('token.txt', 'r') as file:
    for token in file:
      tokens.append(token.strip())

  return tokens


def reset_client():
  """Before reaching request limit, inject a fresh auth token to reset request count."""
  
  global current_token_index
  global request_count 
  request_count = 0

  client.inject_token('Bearer ' + auth_tokens[current_token_index])
  if current_token_index == len(auth_tokens) - 1:
    current_token_index = 0
  else:
    current_token_index += 1


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

    result = execute_query(queries.get_tournies_by_user, query_variables)
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


def execute_query(query, variables):
  """Executes GraphQL queries. Implements a retry system if a bad connection occurs."""
  
  try_attempt_ctr = 1
  total_attempts = 3
  global request_count

  while try_attempt_ctr <= total_attempts:
    if request_count == request_threshold:
      reset_client()
    try:
      request_count += 1
      result = client.execute(query, variables)
      return result
    except URLError:
      try_attempt_ctr += 1

  raise URLError(f'Max number of attempts ({total_attempts}) exceeded.')


def write_tourney_names_to_files(tournies):
  """Writes tourney names/slugs with dates to text files.
  Allows for a simple overview summary of tournaments.
  """
  i = 1
  with open('tourney_names.txt', 'w') as names, open('tourney_slugs.txt', 'w') as slugs:
    
    for tourney in tournies.values():
      names.write(f'{tourney.start_time} --- {tourney.name} --- {tourney.city}, {tourney.state}\n')
      slugs.write(f'{tourney.start_time} --- {tourney.slug} --- {tourney.city}, {tourney.state}\n')
      
      print(f'{i}: {tourney.slug}')
      i = i + 1


def set_events(tournies):
  """Queries events per tournaments. Attempts to filter out non-Singles events.
  Adds results to collection.
  """
  global client
  filter_names = {'squad strike', 'crew battle', 'redemption', 'ladder', 'doubles', 'amateur'}
  
  for tourney_slug, tourney_obj in tournies.items():
    print(f'\n{tourney_obj.name}')
    query_variables = {"slug": tourney_slug}
    result = execute_query(queries.get_event_by_tournament, query_variables)
    res_data = json.loads(result)
    if 'errors' in res_data:
        print('Error:')
        print(res_data['errors'])

    for event_json in res_data['data']['tournament']['events']:
      event = Event(event_json)

      # Filter out events that are most likely not Singles events
      if event.is_teams_event:
        continue
      is_not_singles = 1 in [name in event.name.lower() for name in filter_names]
      if is_not_singles:
        continue
      
      tournies[tourney_slug].events.append(event)
      print(f'---{event.name}')

def write_events_to_file(tournies):
  with open('tourney_events.txt', 'w') as file:
    for tourney in tournies.values():
      file.write(f'{tourney.name}\n')
      for event in tourney.events:
        file.write(f'---{event.name}\n')

auth_tokens = get_tokens()
current_token_index = 0
api_version = 'alpha'
request_count = 0
client = GraphQLClient('https://api.smash.gg/gql/' + api_version)
reset_client()
ultimate_id = '1386'
user_dict = dict()
tourney_to_events = dict()

request_threshold = 79

collect_user_ids_from_file()

tournies = dict(sorted(set_tournaments().items(), key=lambda item: item[1].start_time))

write_tourney_names_to_files(tournies)
set_events(tournies)

write_events_to_file(tournies)

# Add all_events_removed_from_tourney idea