import requests


def get_song_id_from_spotify(song_title):
    url = "https://spotify23.p.rapidapi.com/search/"
    headers = {
        "X-RapidAPI-Key": "9180af86efmshf3c5b0a594242b7p12ce87jsn6333b750b986",
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }

    querystring = {"q": song_title, "type": "multi", "offset": "0", "limit": "10", "numberOfTopResults": "5"}

    try:
        response = requests.get(url, headers=headers, params=querystring)
    except Exception as e:
        print("error in spotify search:", e)
        response = None

    data = response.json()

    if 'tracks' in data and data['tracks']['totalCount'] != 0:
        song_id = data['tracks']['items'][0]['data']['id']
        return song_id
    else:
        return None
