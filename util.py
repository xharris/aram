from typing import Callable


def dict_get(d: dict, key: str, fn: Callable[[], any]):
  if not key in d:
    d[key] = fn()
  return d[key]