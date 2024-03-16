import requests


def detect_song(voice_data):
    response = voice_data['Body'].read()
    with open('voice.mp3', 'wb') as file:
        file.write(response)
    files = {"upload_file": open('voice.mp3', 'rb')}
    url = "https://shazam-api-free.p.rapidapi.com/shazam/recognize/"
    headers = {
        "X-RapidAPI-Key": "9180af86efmshf3c5b0a594242b7p12ce87jsn6333b750b986",
        "X-RapidAPI-Host": "shazam-api-free.p.rapidapi.com"
    }
    try:
        response = requests.post(url=url, files=files, headers=headers)
    except Exception as e:
        print("error in shazam detect:", e)

    res = response.json()
    if 'track' in res and 'title' in res['track']:
        song_title = res['track']['title']
        print("Song Title:", song_title)
        return song_title
    else:
        return "Not found"
