from fastapi import FastAPI, File, UploadFile, Form
from pymongo.mongo_client import MongoClient
from firstService.s3Handler import upload_to_s3
import pika
import json

app = FastAPI()


@app.get("/")
def home():
    return {"message": "works well"}


@app.post("/get-request")
def get_request(email: str = Form(...), voice: UploadFile = File(...)):
    upload_to_s3(voice)

    # Save the generated ID and email to MongoDB
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
    id = str(result.inserted_id)

    # rabbitmq

    # RabbitMQ connection details
    cloudamqp_host = 'rattlesnake-01.rmq.cloudamqp.com'
    cloudamqp_port = 5672
    cloudamqp_user = 'acjmobwi'
    cloudamqp_password = '93u_0kC7qeaGMDeSSCPaQcT3zHZZ_bkM'
    cloudamqp_vhost = 'acjmobwi'

    # Establish RabbitMQ connection
    credentials = pika.PlainCredentials(cloudamqp_user, cloudamqp_password)
    parameters = pika.ConnectionParameters(cloudamqp_host, cloudamqp_port, cloudamqp_vhost, credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='myqueue')

    message = {'id': id}
    channel.basic_publish(exchange='', routing_key='myqueue', body=json.dumps(message))

    return {"message": "connection failed"}
