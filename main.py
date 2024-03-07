from fastapi import FastAPI, File, UploadFile, Form
import boto3
from pymongo.mongo_client import MongoClient

app = FastAPI()
s3 = boto3.client('s3', aws_access_key_id='d1206a55-bc96-4bb1-8ff1-096215c53136',
                  aws_secret_access_key='2ebbce30a131c09cdc842133c26161360d2a679d7879f39b919add7ad6fad6c9',
                  endpoint_url='https://song-storage.s3.ir-thr-at1.arvanstorage.ir')


# get email and voice file
@app.get("/")
def home():
    return {"message": "works well"}


@app.post("/get-request")
def get_request(email: str = Form(...), voice: UploadFile = File(...)):
    bucket_name = 'song-storage'
    object_key = str(voice.filename)

    with voice.file as data:
        s3.upload_fileobj(data, bucket_name, object_key)

    # Save the generated ID and email to MongoDB (code from previous step)
    uri = "mongodb+srv://Zeinab_kr:Zeinab801224@cluster0.oyi9kzk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
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
    return {"message": "connection failed"}
