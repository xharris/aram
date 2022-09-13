import logging
import lol
from fastapi import APIRouter
from model import ChampionStats
from db import db

router = APIRouter(prefix='/champions')

@router.get('/{summoner}/top/{top}')
def read_top_champions(summoner: str, top: int):
  p1 = lol.summoner(summoner)
  matches = lol.arams(p1.puuid, max=500)
  logging.info(f'analyzing {len(matches)} arams')

  champions = db.matches.aggregate([
    {
        '$unwind': {
            'path': '$info.participants'
        }
    }, {
        '$match': {
            'info.participants.puuid': p1.puuid
        }
    }, {
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