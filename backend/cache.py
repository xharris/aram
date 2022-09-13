import json
import pickledb
import urllib.parse

NAME = 'data'
ENABLE = True
EXCLUDE_PARAM_KEYS = ['api_key']

cache:pickledb.PickleDB = None
changed = False 

def _name():
  return f'{NAME}.cache'
        
def _get_key(url: str, params: dict):
  params = params.copy()
  for k in EXCLUDE_PARAM_KEYS:
    if k in params:
      del params[k]
  if params and len(params.keys()) > 0: 
    param_str = '&'.join([f'{k}={urllib.parse.quote(str(v))}' for k, v in params.items() if k not in EXCLUDE_PARAM_KEYS])
    return f"{url}?{param_str}"
  return url

def load():
  if not ENABLE: return None
  global cache
  if not cache:
    cache = pickledb.load(_name(), auto_dump=True)

def get(url: str, params: dict):
  if not ENABLE: return None
  key = _get_key(url, params)
  return json.loads(cache.get(key))

def exists(url: str, params: dict):
  if not ENABLE: return False
  key = _get_key(url, params)
  return cache.get(key) is not False

def update(url: str, params: dict, data, remove=False):
  if not ENABLE: return None
  global changed
  key = _get_key(url, params)

  if remove and cache.get(key) is not None:
    cache.rem(key)
  if not remove:
    cache.set(key, json.dumps(data))
  changed = True

def save():
  # cache.auto_dump
  return 
  # if not ENABLE or not changed: 
  #   return
  # with open(f'{NAME}.cache', 'w') as f:
  #   json.dump(cache, f, indent=4)