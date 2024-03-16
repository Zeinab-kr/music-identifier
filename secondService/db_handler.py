import json

from bson import ObjectId
from pymongo import MongoClient
from initials import uri

client = MongoClient(uri)
db = client["DB1"]
collection = db["request_data"]


def find_in_db(body):
    message = json.loads(body)
    object_id = message.get('id')
    data = collection.find_one({"_id": ObjectId(object_id)})
    voice_id = data["ID"]
    return object_id, voice_id


def update_in_db(object_id, song_id):
    filter_query = {"_id": ObjectId(object_id)}
    if song_id != "Not found":
        collection.update_one(filter_query, {"$set": {"Status": "ready", "SongID": song_id}})
    else:
        collection.update_one(filter_query, {"$set": {"Status": "failed", "SongID": song_id}})
