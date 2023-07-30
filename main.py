from typing import Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import pymongo
import logging

from GetAnimeList import GetEpisodeList, GetAnimeList

logging.basicConfig(level=logging.DEBUG,filename="./log.log" ,format="%(asctime)s - %(levelname)s - %(message)s")

client = pymongo.MongoClient(
    "mongodb+srv://LowSpecGamer:upPGEx2uMXLpSytB@animescrape.msztw.mongodb.net/animeScrape?retryWrites=true&w=majority")
db = client['GoGoAnime']

anime_collection = db['gogoanime_anime_list']
episode_collection = db['anime_episode_data']

app = FastAPI()

API_BASE_URL = 'https://gogoanime.mom/my-ajax'

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class animeException(Exception):
    def __init__(self, name: str):
        self.name = name
        print(self.name)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.exception_handler(animeException)
async def unicorn_exception_handler(request: Request, exc: animeException):
    if exc.name == 'INVALID ACTION':
        return JSONResponse(
            status_code=500,
            content={
                "message": f" {exc.name} , query the appropriate action to retrieve data "},

        )
    else:
        return JSONResponse(
            status_code=404,
            content={
                "message": f"{exc.name} isn't avaiable as of now !! "},

        )


def getanime_gogoanime(paramters):

    api_res = requests.get(API_BASE_URL, params=paramters)
    anime_res = api_res.json()
    anime_res['source'] = 'GOGO'
    return anime_res


def getanime_JAAW(anime_collection, params):
    anime_res = GetAnimeList(anime_collection, params)
    anime_res['source'] = 'JAAW'
    return anime_res

def getepisode_JAAW(collection,params):
    episode_res=GetEpisodeList(collection,params)
    episode_res['source']='JAAW'
    return episode_res


@app.get('/anime')
def get_anime(keyword: str, action: Optional[str] = 'search', limit: Optional[int] = 100, page: Optional[int] = 1):
    params = {
        'keyword': keyword,
        'action': action,
        'limit': limit,
        'page': page
    }
    try:
        res = getanime_gogoanime(params)
    except Exception as GogoAnimeException:
        try:
            res = getanime_JAAW(anime_collection, params)
        except Exception as JAAWAPIException:
            raise animeException(f"{params['character']} ")

    return res


@app.get('/episode')
def get_anime(movie_id: str, action: Optional[str] = 'list_episode',lastidx:Optional[str]='', limit: Optional[int] = 100, page: Optional[int] = 0):
    params = {
        'movie_id': movie_id,
        'action': action,
        'limit': limit,
        'different_page': page,
        # 'lastidx':lastidx
    }

    try:
        res = getanime_gogoanime(params)
    except Exception as GogoAnimeException:
        try:
            res = getepisode_JAAW(episode_collection, params)
        except Exception as JAAWAPIException:
            raise animeException(f"{params['character']} ")

    return res

@app.get('/topanime')
def get_top_anime(action:str,type_of_view:str,limit:int,page:int):
    # logging.info("top anime endpoint ")
    logging.info(f"action : ${action}, type: ${type_of_view}")
    params = {
        'action':action,
        'top_view':type_of_view,
        'limit':limit,
        'page':page
    }
    try :
        res=getanime_gogoanime(params)
    except Exception as JAAWAPIException:
        raise animeException(f"{params['action']} ")

    return res 

@app.get('/popular_on_going')
def get_poppular_ongoing(page:int,limit:int,action:Optional[str]='popular_ongoing_update'):
    params={
        'action':action,
        'limit':limit,
        'page':page
    }
    try :
        res=getanime_gogoanime(params)
    except Exception as GogoAnimeException:
        raise animeException(f"{params['action']} ")
    return res

