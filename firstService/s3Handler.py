import boto3

s3 = boto3.client('s3', aws_access_key_id='d1206a55-bc96-4bb1-8ff1-096215c53136',
                  aws_secret_access_key='2ebbce30a131c09cdc842133c26161360d2a679d7879f39b919add7ad6fad6c9',
                  endpoint_url='https://song-storage.s3.ir-thr-at1.arvanstorage.ir')


def upload_to_s3(voice):
    bucket_name = 'song-storage'
    object_key = str(voice.filename)
    with voice.file as data:
        s3.upload_fileobj(data, bucket_name, object_key)
