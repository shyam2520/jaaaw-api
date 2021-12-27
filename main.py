from typing import Optional

from fastapi import FastAPI,HTTPException,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from bson import json_util
import requests
import pymongo
import re
import json

client = pymongo.MongoClient("mongodb+srv://LowSpecGamer:upPGEx2uMXLpSytB@animescrape.msztw.mongodb.net/animeScrape?retryWrites=true&w=majority")
db=client['9anime']
# print(db.list_collection_names())
collection=db['Show_Name_Details']

app =FastAPI()

API_BASE_URL = 'https://gogoanime.mom/my-ajax'

# origins=['http://localhost:3000/']

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class animeException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.exception_handler(animeException)
async def unicorn_exception_handler(request: Request, exc: animeException):
    return JSONResponse(
        status_code=404,
        content={"message": f" {exc.name} isn't available as of now !!"},
    )



def getanime_gogoanime(paramters):

    api_res = requests.get(API_BASE_URL, params=paramters)
    anime_res = api_res.json()
    anime_res['source'] = 'GOGO'
    return anime_res


def getanime_JAAW(name, params):
    regex = re.compile(f'^{name}', re.IGNORECASE)
    res = list(collection.find({'title': regex}, params))
    if not(res) or len(res) == 0:
        raise animeException(name)
    return {'results': len(res), 'data': res, 'source': 'JAAW'}


@app.get('/anime')
def get_anime(name: str, genre: Optional[str] = None):
    paramters = {
        'character': name,
        'action': 'load_anime_list',
        'limit': 100
    }
    res = getanime_gogoanime(paramters)
    if(res['total_page'] == 0):
        return getanime_JAAW(name, {
            '_id': 0, 'episodes': 0, 'genre': 0})
    return res


@app.get('/episode')
def get_anime(title: str, id: Optional[str] = None):
    # regex=re.compile(f'^{title}',re.IGNORECASE)
    if id:
        paramters = {
            'movie_id': id,
            'action': 'load_list_episode',
            'limit': 100
        }
        return getanime_gogoanime(paramters)
    return getanime_JAAW(title,{'_id': 0})
