import logging
import lol
from fastapi import APIRouter
from db import db

router = APIRouter(prefix='/match')

@router.get('/{summoner}/count')
def read_match_count(summoner: str):
  p1 = lol.summoner(summoner)
  matches = lol.arams(p1.puuid, max=500)
  
  return { 'count': len(matches), 'start': matches[0].info.gameStartTimestamp }