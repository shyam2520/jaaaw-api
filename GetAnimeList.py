
from math import ceil
from pymongo import MongoClient


client = MongoClient(
    "mongodb+srv://LowSpecGamer:upPGEx2uMXLpSytB@animescrape.msztw.mongodb.net/animeScrape?retryWrites=true&w=majority")

db = client['GoGoAnime']

collection = db['gogoanime_anime_list']


def GetAnimeList(collection, params):
    name = params['character'] if params['character'] else ''
    limits = params['limit'] if params['limit'] else 100
    pageno = params['page'] if params['page'] else 1
    skip_val = (pageno-1)*(limits)
    res = collection.aggregate([
        {"$facet": {
            "totalData": [
                {"$match": {"post_title": {
                    "$regex": f"^{name}",
                    "$options": "im"}},
                 },
                {"$project": {"_id": 0}},
                {"$skip": skip_val},
                {"$limit": limits}
            ],
            "totalCount": [
                {"$match": {"post_title": {
                    "$regex": f"^{name}",
                    "$options": "im"
                }}},
                {"$count": "count"}
            ]
        }}
    ])
    response = {}
    for i in res:
        response['data'] = (i['totalData'])
        response['total_page'] = (
            ceil(i['totalCount'][0]['count']/limits)) if i['totalCount'] else 0
        response['character'] = name
        response['page'] = pageno
    return response





def GetEpisodeList(collection, params):
    movie_id = params['movie_id'] if params['movie_id'] else ''
    limits = params['limit'] if params['limit'] else 100
    pageno = params['page'] if params['page'] else 1
    skip_val = (pageno-1)*(limits)
    res = collection.aggregate([
        {"$facet": {
            "totalData": [
                {"$match": {"movie_id": movie_id}},
                {"$skip": skip_val},
                {"$limit": limits},
                {"$project": {"_id": False}}
            ],
            "totalCount": [
                {"$match": {"movie_id": movie_id}},
                {"$count": "Total_Count"}
            ]
        }}
    ])
    response = {}
    for i in res:
        response['total_page'] = int(
            ceil((i['totalCount'][0]['Total_Count'])/limits) if i['totalCount'] else 0)
        response["data"] = i['totalData']
        response["limit"] = limits
        response["page"] = pageno
    return response
