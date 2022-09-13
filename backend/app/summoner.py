import lol
from fastapi import APIRouter

router = APIRouter(prefix='/summoner')

@router.get('/{summoner}')
def read_summoner(summoner: str):
  return lol.summoner(summoner)