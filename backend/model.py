from enum import Enum, auto
from pydantic import BaseModel

class _AutoName(Enum):
  def _generate_next_value_(name, _start, _count, _lastval):
    return name

# RIOT API

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
  PRACTICETOOL = auto()

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

# ARAM

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