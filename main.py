from devtools import debug
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

import lol
import cache

cache.ENABLE = True

class Player(BaseModel):
  puuid: str
  summonerName: str
  totalMatches: int = 0
  wonWith: int = 0
  wonAgainst: int = 0
  lostWith: int  = 0
  lostAgainst: int = 0

def main():
  me = lol.summoner('Toaxt')
  matches = lol.arams(me.puuid, max=500)

  print(f'{len(matches)} matches')

  players:dict[str, Player] = {}

  for match in matches:
    my_team = next(part.teamId for part in match.info.participants if part.puuid)
    for other in match.info.participants:
      if not other.puuid in players:
        players[other.puuid] = Player(**other.dict())
      player = players[other.puuid]
      # store player data
      player.totalMatches += 1
      # ally
      if other.teamId == my_team:
        if other.win:
          player.wonWith += 1
        else:
          player.lostWith += 1 
      # enemy
      else:
        if other.win:
          player.lostAgainst += 1 
        else: 
          player.wonAgainst += 1

  player_list = players.values()
  top = 50
  print(
    '\n'.join([f'{player.summonerName} (win with {player.wonWith/player.totalMatches*100}%, games {player.totalMatches})' for player in sorted(player_list, key=lambda player: player.totalMatches, reverse=True)][:top])
  )
  repeats = len([player for player in player_list if player.totalMatches < 3 and player.totalMatches > 1])
  print(f'{repeats} repeats')

  cache.save()

if __name__ == '__main__':
  main()