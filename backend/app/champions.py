import logging
import lol
from fastapi import APIRouter
from model import ChampionStats
from db import db

router = APIRouter(prefix='/champions')

@router.get('/{summoner}/history')
def read_villians(summoner: str):
  p1 = lol.summoner(summoner)
  matches = lol.arams(p1.puuid, max=500)
  logging.info(f'getting champion history')

  champions = db.matches.aggregate([
    {
        '$match': {
            'info.participants.puuid': 'JrPytSmH-aI-GGazls-gTdUm9cI0ey7uj95LYZCSuV4g1maRBNt20HQbToh1AXPP_gweZloPHMTHQQ', 
            'info.gameMode': 'ARAM', 
            'info.participants.win': False
        }
    }, {
        '$unwind': {
            'path': '$info.participants'
        }
    }, {
        '$group': {
            '_id': {
                'championName': '$info.participants.championName', 
                'win': '$info.participants.win'
            }, 
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$sort': {
            'count': -1
        }
    }, {
        '$set': {
            'championName': '$_id.championName', 
            'win': {
                '$cond': [
                    {
                        '$eq': [
                            '$_id.win', True
                        ]
                    }, '$count', 0
                ]
            }, 
            'lose': {
                '$cond': [
                    {
                        '$eq': [
                            '$_id.win', False
                        ]
                    }, '$count', 0
                ]
            }
        }
    }, {
        '$group': {
            '_id': '$championName', 
            'championName': {
                '$first': '$championName'
            }, 
            'win': {
                '$sum': '$win'
            }, 
            'lose': {
                '$sum': '$lose'
            }
        }
    },
    {
        '$set': {
            'total': {
                '$add': [ '$win', '$lose' ]
            }
        }
    }
    ])
  
  logging.info('done')
  return list(champions)

@router.get('/{summoner}/top/{top}')
def read_top_champions(summoner: str, top: int):
  p1 = lol.summoner(summoner)
  matches = lol.arams(p1.puuid, max=500)
  logging.info(f'getting top {top} champions played')

  champions = db.matches.aggregate([
    {
        '$match': {
            'info.participants.puuid': p1.puuid,
            'info.gameMode': 'ARAM'
        }
    },
    {
        '$unwind': {
            'path': '$info.participants'
        }
    }, 
    {
        '$match': {
            'info.participants.puuid': p1.puuid
        }
    },
    {
       '$group': {
            '_id': '$info.participants.championId', 
            'championName': {
                '$first': '$info.participants.championName'
            }, 
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$sort': {
            'count': -1
        }
    }
  ])
  
  logging.info('done')
  return list(champions)[:top]