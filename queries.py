get_tournies_by_user = '''
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
        videogameId: [1386]
        past: true
      }
    }) {
      nodes {
        name
        slug
        startAt
        isOnline
      }
    }
  }
}
'''
