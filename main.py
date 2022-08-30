from re import T
from devtools import debug
from dotenv import load_dotenv
from pydantic import BaseModel

from model import Champion, ChampionTag
load_dotenv()

import lol
import cache

cache.NAME = 'lol'
cache.ENABLE = True

class MatchResult(BaseModel):
  total: int = 0
  win: int = 0
  lose: int = 0

class PlayerStats(BaseModel):
  puuid: str
  summonerName: str
  playedWith: MatchResult = MatchResult()
  playedAgainst: MatchResult = MatchResult()

class ChampionStats(BaseModel):
  id: str
  name: str
  playedAs: MatchResult = MatchResult()
  playedWith: MatchResult = MatchResult()
  playedAgainst: MatchResult = MatchResult()
  tags: list[ChampionTag]

def findPlayer(players: list[PlayerStats], summonerName: str):
  return next(player for player in players if player.summonerName == summonerName)

def main():
  cache.load()
  
  me = lol.summoner('Toaxt')
  matches = lol.arams(me.puuid, max=500)

  print(f'{len(matches)} matches')

  players:dict[str, PlayerStats] = {}
  champions:dict[str, ChampionStats] = {}

  for match in matches:
    my_team = next(part.teamId for part in match.info.participants if part.puuid == me.puuid)
    # players
    for other in match.info.participants:
      if not other.puuid in players:
        players[other.puuid] = PlayerStats(**other.dict())
      player = players[other.puuid]
      # store player data
      # ally
      if other.teamId == my_team:
        player.playedWith.total += 1
        if other.win:
          player.playedWith.win += 1
        else:
          player.playedWith.lose += 1 
      # enemy
      else:
        player.playedAgainst.total += 1
        if other.win:
          player.playedAgainst.lose += 1 
        else: 
          player.playedAgainst.win += 1

    # champions
    for other in match.info.participants:
      champion = lol.champion(other.championName)
      if not other.championName in champions:
        champions[other.championName] = ChampionStats(**champion.dict())
      stats = champions[other.championName]
      
      # me 
      if other.puuid == me.puuid:
        stats.playedAs.total += 1
        if other.win:
          stats.playedAs.win += 1
        else:
          stats.playedAs.lose += 1
      # ally
      elif other.teamId == my_team:
        stats.playedWith.total += 1
        if other.win:
          stats.playedWith.win += 1
        else:
          stats.playedWith.lose += 1 
      # enemy
      else:
        stats.playedAgainst.total += 1
        if other.win:
          stats.playedAgainst.lose += 1 
        else: 
          stats.playedAgainst.win += 1
        
  # player_list = players.values()
  # top = 50
  # print(
  #   '\n'.join([f'{player.summonerName} (win with {player.playedWith.win/player.playedWith.win*100}%, games {player.playedWith.total+player.playedAgainst.total})' for player in sorted(player_list, key=lambda player: player.playedWith.total+player.playedAgainst.total, reverse=True)][:top])
  # )
  # repeats = len([player for player in player_list if player.playedWith.total+player.playedAgainst.total < 3 and player.playedWith.total+player.playedAgainst.total > 1])
  # print(f'{repeats} repeats')

  champion_list = champions.values()
  top = 10
  print(
    '\n'.join([f'{champ.name} (played {champ.playedAs.total}, win {champ.playedAs.win / champ.playedAs.total * 100 if champ.playedAs.total > 0 else 0}%)' for champ in sorted([c for c in champion_list], key=lambda c: c.playedAs.total, reverse=True)])
  )

  print()
  # doesnt work yet
  champion_classes = {}
  for tag in ChampionTag:
    champion_classes[tag.name] = len([tag2 for tag2 in next(c.tags for c in champion_list if c.playedAs.total > 0) if tag.name == tag2.name])

  for cls, count in champion_classes.items():
    print(f'{cls} (played {count})')

  # print(f'havent played {len([c for c in champion_list if c.playedAs.total == 0])} / {len(champion_list)} ({", ".join([c.name for c in sorted(champion_list, key=lambda c2: c2.name) if c.playedAs.total == 0])})')

  # print(findPlayer(player_list, "Toaxt"))

if __name__ == '__main__':
  main()