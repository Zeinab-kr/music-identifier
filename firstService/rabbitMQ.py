import pika
import json
from firstService.data import *

credentials = pika.PlainCredentials(cloudamqp_user, cloudamqp_password)
parameters = pika.ConnectionParameters(cloudamqp_host, cloudamqp_port, cloudamqp_vhost, credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='myqueue')


def add_to_queue(object_id):
    message = {'id': object_id}
    channel.basic_publish(exchange='', routing_key='myqueue', body=json.dumps(message))
