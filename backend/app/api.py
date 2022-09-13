from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from . import summoner, champions

app = FastAPI()
origins = [
  'http://localhost:3000',
  'localhost:3000'
]
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

@app.get('/', tags=['root'])
def read_root(request: Request):
  return {'message': 'welcome to hell'}

app.include_router(summoner.router, prefix='/api/v1')
app.include_router(champions.router, prefix='/api/v1')
