import json
import os

import urllib.parse

NAME = 'lol'
ENABLE = True

cache = {}
if os.path.isfile(f'{NAME}.cache'):
    with open(f'{NAME}.cache') as f:
        cache = json.load(f)
        
def _get_key(url: str, params: dict):
    if params and len(params.keys()) > 0: 
        param_str = '&'.join([f'{k}={urllib.parse.quote(str(v))}' for k, v in params.items() if k != 'api_key'])
        return f"{url}?{param_str}"
    return url

def get(url: str, params: dict):
    key = _get_key(url, params)
    return cache[key]

def exists(url: str, params: dict):
    key = _get_key(url, params)
    return key in cache

def update(url: str, params: dict, data, remove=False):
    key = _get_key(url, params)

    if remove and key in cache:
        del cache[key]
    if not remove:
        cache[key] = data 

def save():
    if not ENABLE: 
        return
    with open(f'{NAME}.cache', 'w') as f:
        json.dump(cache, f, indent=4)