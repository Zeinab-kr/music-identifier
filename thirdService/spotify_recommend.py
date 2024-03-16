import requests


def recommend_song(song_id):
    url = "https://spotify23.p.rapidapi.com/recommendations/"
    headers = {
        "X-RapidAPI-Key": "9180af86efmshf3c5b0a594242b7p12ce87jsn6333b750b986",
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }
    querystring = {"limit": "5", "seed_tracks": song_id}

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()
