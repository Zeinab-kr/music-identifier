import pika
from initials import *
from spotify_search import *
from shazam_detect import detect_song
from db_handler import *
from s3_download import download_from_s3


def consume_data():
    credentials = pika.PlainCredentials(cloudamqp_user, cloudamqp_password)
    parameters = pika.ConnectionParameters(cloudamqp_host, cloudamqp_port, cloudamqp_vhost, credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='myqueue')

    def callback(ch, method, properties, body):
        object_id, voice_id = find_in_db(body)
        voice_data = download_from_s3(voice_id)
        song_title = detect_song(voice_data)

        if song_title != "Not found":
            song_id = get_song_id_from_spotify(song_title)
            if song_id:
                print("Song ID from Spotify:", song_id)
            else:
                print("Song not found on Spotify")
        else:
            song_id = "Not found"

        update_in_db(object_id, song_id)

    channel.basic_consume(queue='myqueue', on_message_callback=callback, auto_ack=True)
    try:
        channel.start_consuming()
    except Exception as e:
        print("An error occurred:", e)

    channel.close()
    connection.close()
