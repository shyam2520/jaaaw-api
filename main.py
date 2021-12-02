from typing import Optional

from fastapi import FastAPI
from bson import json_util
import pymongo
import re
import json

client = pymongo.MongoClient("mongodb+srv://LowSpecGamer:upPGEx2uMXLpSytB@animescrape.msztw.mongodb.net/animeScrape?retryWrites=true&w=majority")
db=client['9anime']
# print(db.list_collection_names())
collection=db['Show_Name_Details']

app =FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}

@app.get('/anime/{anime}')
def find_anime(anime:str):
    regex=re.compile(f'^{anime}',re.IGNORECASE)
    # res= [i for i in collection.find({'title':regex},{'_id': 0})]
    res=list(collection.find({'title':regex},{'_id': 0}))
    # print(type(res[0]))
    # response ={"status":200,"Shows":len(res),"data":dumps(res)}
    #     # print(res[i],end='\n\n')
    return res