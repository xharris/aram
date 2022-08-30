import os
from string import Template 
import requests
import cache
import model
from datetime import date, datetime
import time

RATE_LIMIT = 20 # requests allowed per second
API_KEY = os.getenv('RIOT_API_KEY')
BASE_URL = 'https://$region.api.riotgames.com'

last_call: datetime = None
def _call(url: str, params: dict = {}, method = 'get', region = 'americas', noCache = False):
  global last_call
  if not 'api_key' in params or not params['api_key']:
    params['api_key'] = API_KEY
  if not noCache and cache.exists(url, params):
    return cache.get(url, params)
  # rate limiting: avoid making queries too fast
  now = datetime.now()
  if last_call is not None:
    diff = (now - last_call).total_seconds()
    last_call = None
    if diff > (1/RATE_LIMIT):
      # going too fast. wait {diff} seconds
      time.sleep(diff)
  else:
    last_call = datetime.now()

  r = requests.request(method, f'{Template(BASE_URL).substitute(region=region)}/{url}', params=params)

  if r.status_code >= 200 and r.status_code < 300:
    data = r.json()
    if not noCache:
      cache.update(url, params, data)
    return data

  # service unavailable, just retry
  if r.status_code == 503:
    return _call(url, params, method, region, noCache)

  # rate limit exceeded
  if r.status_code == 429 and 'Retry-After' in r.headers:
    wait = int(r.headers['Retry-After'])
    print(f'Rate limit exceeded. Waiting {wait}s')
    last_call = None
    time.sleep(wait)
    return _call(url, params, method, region, noCache)

  raise Exception(r.text, r.headers)

def _get(url: str, params: dict = {}):
  if cache.exists(url, params):
    return cache.get(url, params)
  r = requests.get(url, params=params)

  if r.status_code >= 200 and r.status_code < 300:
    data = r.json()
    cache.update(url, params, data)
    return data

  # service unavailable, just retry
  if r.status_code == 503:
    return _get(url, params)
  raise Exception(r.status_code, r.text, r.headers)

# routes

def summoner(username: str):
  print(f'GET summoner {username}')
  summoner = model.Summoner(**_call(f'lol/summoner/v4/summoners/by-name/{username}', region='na1'))
  cache.save()
  return summoner

def arams(puuid: model.puuid, max = 300):
  print('GET arams ', end='')
  # get ids
  ids: list[str] = []
  ret: list[str] = None
  while ret is None or (len(ret) == 100 and len(ids) <= max):
    ret = _call(f'lol/match/v5/matches/by-puuid/{puuid}/ids', {
      'type': 'normal',
      'start': len(ids),
      'count': 100
    }, noCache=True) or []
    print('|', end='', flush=True)
    ids.extend(ret)
  ids = ids[:max]
  print(f'({len(ids)})')
  # turn ids into match data
  matches = [print('.', end='', flush=True) or model.Match(**_call(f'lol/match/v5/matches/{id}')) for id in ids]
  print()  
  cache.save()
  return [match for match in matches if match.info.gameMode == model.GameMode.ARAM][:max]

def champion(name: str):
  # print(f'GET champion {name}')
  if name.lower() == 'fiddlesticks':
    name = 'Fiddlesticks'
  data = _get(f'http://ddragon.leagueoflegends.com/cdn/12.16.1/data/en_US/champion.json')['data'][name]
  cache.save()
  data = data.copy()
  data['tags'] = [model.ChampionTag(tag) for tag in data['tags']]
  return model.Champion(**data)