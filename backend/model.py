from enum import Enum, IntEnum, auto
from typing import Literal, Union
from pydantic import BaseModel

class _AutoName(Enum):
  def _generate_next_value_(name, _start, _count, _lastval):
    return name

puuid = str

class Summoner(BaseModel):
  id: str 
  accountId: str
  puuid: puuid
  name: str
  profileIconId: int
  revisionDate: int
  summonerLevel: int

class Metadata(BaseModel):
  dataVersion: str 
  matchId: str 
  participants: list[str]

class GameMode(_AutoName):
  CLASSIC = auto() 
  ODIN = auto() 
  ARAM = auto() 
  TUTORIAL = auto() 
  URF = auto() 
  DOOMBOTSTEEMO = auto() 
  ONEFORALL = auto() 
  ASCENSION = auto() 
  FIRSTBLOOD = auto() 
  KINGPORO = auto() 
  SIEGE = auto() 
  ASSASSINATE = auto() 
  ARSR = auto() 
  DARKSTAR = auto() 
  STARGUARDIAN = auto() 
  PROJECT = auto() 
  GAMEMODEX = auto() 
  ODYSSEY = auto() 
  NEXUSBLITZ = auto() 
  ULTBOOK = auto()

class GameType(_AutoName):
  CUSTOM_GAME = auto()
  TUTORIAL_GAME = auto()
  MATCHED_GAME = auto()

class Participant(BaseModel):
  puuid: puuid
  kills: int 
  deaths: int 
  assists: int
  championId: int 
  champLevel: int 
  champExperience: int 
  summonerName: str
  teamId: int
  win: bool
  championName: str

class Info(BaseModel):
  gameDuration: int
  gameStartTimestamp: int 
  gameEndTimestamp: int 
  gameMode: GameMode
  gameType: GameType
  participants: list[Participant]

class Match(BaseModel):
  metadata: Metadata
  info: Info

class ChampionTag(_AutoName):
  Fighter = auto()
  Mage = auto()
  Marksman = auto()
  Assassin = auto()
  Tank = auto()
  Support = auto()

class Champion(BaseModel):
  id: str 
  name: str 
  tags: list[ChampionTag]