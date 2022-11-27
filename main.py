import json

from graphqlclient import GraphQLClient

authToken = 'c4a231a21516bbe65650002b27d2dbeb'
apiVersion = 'alpha'
ultimateId = '1386'
# Make sure your sheet share link settings are 'anyone with the link'

client = GraphQLClient('https://api.smash.gg/gql/' + apiVersion)
client.inject_token('Bearer ' + authToken)
result = client.execute('''
query GetTournamentsByUser($userId: ID!) {
  user(id: $userId, slug: null) {
    name
    player {
      id
    }
    tournaments(query: {
      perPage: 500
      page: 1
      filter: {
        videogameId: [''' + ultimateId + ''']
        past: true
      }
    }) {
      nodes {
        name
        slug
      }
    }
  }
}
''',
{
  "userId": "603872"
})
resData = json.loads(result)
if 'errors' in resData:
    print('Error:')
    print(resData['errors'])
else:
    print(resData)