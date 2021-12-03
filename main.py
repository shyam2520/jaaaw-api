from typing import Optional

from fastapi import FastAPI,HTTPException,Request
from fastapi.responses import JSONResponse
from bson import json_util
import pymongo
import re
import json

client = pymongo.MongoClient("mongodb+srv://LowSpecGamer:upPGEx2uMXLpSytB@animescrape.msztw.mongodb.net/animeScrape?retryWrites=true&w=majority")
db=client['9anime']
# print(db.list_collection_names())
collection=db['Show_Name_Details']

app =FastAPI()


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

@app.get('/anime')
def get_anime(name:str,genre:Optional[str]=None):
    regex=re.compile(f'^{name}',re.IGNORECASE)
    res=list(collection.find({'title':regex},{'_id': 0}))
    if not(res) or len(res)==0:
        raise animeException(name)
    return {'status':200,'results':len(res),'data':res}