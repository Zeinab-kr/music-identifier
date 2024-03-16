import boto3
from initials import access_key, secret_access_key, endpoint_url

s3 = boto3.client('s3', aws_access_key_id=access_key,
                  aws_secret_access_key=secret_access_key,
                  endpoint_url=endpoint_url)


def download_from_s3(voice_id):
    voice_data = s3.get_object(Bucket='song-storage', Key=voice_id)
    return voice_data
