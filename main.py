from fastapi import FastAPI, File, UploadFile, Form
from firstService.s3Handler import upload_to_s3
from firstService.dataBase import add_to_db
import pika
import json

app = FastAPI()


@app.get("/")
def home():
    return {"message": "works well"}


@app.post("/get-request")
def get_request(email: str = Form(...), voice: UploadFile = File(...)):
    upload_to_s3(voice)
    object_id = add_to_db(email, voice.filename)

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

    message = {'id': object_id}
    channel.basic_publish(exchange='', routing_key='myqueue', body=json.dumps(message))

    return {"message": "connection failed"}
