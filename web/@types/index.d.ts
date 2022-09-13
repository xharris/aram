declare namespace Aram {
  namespace Riot {
    type puuid = string

    interface Summoner {
      id: string
      accountId: string
      puuid: puuid
      name: string
      profileIconId: number
      revisionDate: number
      summonerLevel: number
    }
  }
}
