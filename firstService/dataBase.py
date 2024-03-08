from pymongo.mongo_client import MongoClient
from data import uri


def add_to_db(email, object_key):
    # Create a new client and connect to the server
    client = MongoClient(uri)
    db = client["DB1"]
    collection = db["request_data"]

    # Define the data structure
    data = {
        "ID": object_key,
        "Email": email,
        "Status": "pending",
        "SongID": ""
    }

    # Insert the data into MongoDB
    result = collection.insert_one(data)
    return str(result.inserted_id)
