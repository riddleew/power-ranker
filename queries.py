get_tournies_by_user = '''
query GetTournamentsByUser($userId: ID!) {
  user(id: $userId, slug: null) {
    name
    player {
      id
      gamerTag
    }
    tournaments(query: {
      perPage: 100
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
        city
        addrState
      }
    }
  }
}
'''

get_events_by_tournament = '''
query GetEventByTournament($slug: String!) {
  tournament(slug: $slug) {
  	events(filter: {videogameId: [1386]}) {
      id
      slug
      name
      numEntrants
      startAt
      competitionTier
      state
      teamRosterSize {
        minPlayers
      }
    }
  }
}
'''

get_events_by_user = '''
query GetEventsByUser($userId: ID!) {
  user(id: $userId, slug: null) {
    name
    player {
      id
      gamerTag
    }
    events(query: {
      perPage: 100
      page: 1
      sortBy: "startAt desc"
      filter: {
        videogameId: [1386]
        #eventType: 1
      }
    }) {
      nodes {
        id
      	slug
      	name
      	numEntrants
      	teamRosterSize {
        	minPlayers
      	}
        tournament {
          name
        	slug
        	startAt
        	isOnline
        	city
        	addrState
        }
      }
    }
  }
}
'''