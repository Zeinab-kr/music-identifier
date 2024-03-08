import boto3
from data import *

s3 = boto3.client('s3', aws_access_key_id=access_key,
                  aws_secret_access_key=secret_access_key,
                  endpoint_url=endpoint_url)


def upload_to_s3(voice):
    bucket_name = 'song-storage'
    object_key = str(voice.filename)
    with voice.file as data:
        s3.upload_fileobj(data, bucket_name, object_key)
