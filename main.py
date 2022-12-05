from datetime import datetime, timezone
import json

from graphqlclient import GraphQLClient

import queries

def get_tournaments():
  for user_id, player_name in user_dict.items():
    print("Processing " + player_name + "'s tournaments...")
    result = client.execute(queries.get_tournies_by_user, {"userId": user_id})
    res_data = json.loads(result)
    if 'errors' in res_data:
        print('Error:')
        print(res_data['errors'])

    for tournament in res_data['data']['user']['tournaments']['nodes']:
      cut_off_date_start = datetime(2022, 10, 1)
      cut_off_date_end = datetime(2022, 12, 31)
      
      #print(tournament)
      #timestamp = datetime.utcfromtimestamp(tournament['startAt']).strftime('%Y-%m-%d %H:%M:%S')
      dt_ts1 = datetime.fromtimestamp(tournament['startAt'], tz=timezone.utc).strftime('%m-%d-%Y %H:%M:%S')

      tourney_start = datetime.fromtimestamp(tournament['startAt'])#.strftime('%m-%d-%Y %H:%M:%S')
      str_date = tourney_start.strftime('%m-%d-%Y')

      if tourney_start >= cut_off_date_start and tourney_start <= cut_off_date_end:
        print(tournament['name'] + '\t' + str_date)
        tour_set.add(tournament['slug'])
      elif tourney_start < cut_off_date_start:
        print('Tournament outside of season window --- ' + tournament['name'] + '\t' + str_date)
        break

auth_token = 'c4a231a21516bbe65650002b27d2dbeb'
api_version = 'alpha'
ultimate_id = '1386'


tour_set = set()
user_dict = dict()

with open('user-ids.txt', 'r') as file:
  delimiter = '---'
  for line in file:
    # Get player name
    name_idx = line.index(delimiter)
    player_name = line[:name_idx]
    
    # Get user id
    id_idx = name_idx + 3
    user_id = line[id_idx:].strip()
    user_dict[user_id] = player_name 
    

client = GraphQLClient('https://api.smash.gg/gql/' + api_version)
client.inject_token('Bearer ' + auth_token)

get_tournaments()




