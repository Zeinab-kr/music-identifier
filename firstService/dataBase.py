from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://Zeinab_kr:Zeinab801224@cluster0.oyi9kzk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


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
