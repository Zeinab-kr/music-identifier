from pymongo.mongo_client import MongoClient
from firstService.data import uri


def add_to_db(email, object_key):
    client = MongoClient(uri)
    db = client["DB1"]
    collection = db["request_data"]

    data = {
        "ID": object_key,
        "Email": email,
        "Status": "pending",
        "SongID": ""
    }

    result = collection.insert_one(data)
