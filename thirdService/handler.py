import time
from initials import uri
from pymongo import MongoClient
from spotify_recommend import recommend_song
from mail_handler import send_email


client = MongoClient(uri)
db = client["DB1"]
collection = db["request_data"]


def process_data():
    data = collection.find({"Status": "ready"})

    for doc in data:
        song_id = doc.get("SongID")

        response = recommend_song(song_id)
        collection.update_one({"_id": doc["_id"]}, {"$set": {"recommendations": response}})

        print("Recommendations saved for SongID:", song_id)

        # Send email to user with the response
        user_email = doc.get("Email")
        subject = "Your Music Recommendations"
        message = (f"Here are your music recommendations:\n"
                   f"1)\n"
                   f"Track name: {response['tracks'][0]['name']}\n"
                   f"Spotify Link: {response['tracks'][0]['external_urls']['spotify']}\n"
                   f"2)\n"
                   f"Track name: {response['tracks'][1]['name']}\n"
                   f"Spotify Link: {response['tracks'][1]['external_urls']['spotify']}\n"
                   f"3)\n"
                   f"Track name: {response['tracks'][2]['name']}\n"
                   f"Spotify Link: {response['tracks'][2]['external_urls']['spotify']}\n"
                   f"4)\n"
                   f"Track name: {response['tracks'][3]['name']}\n"
                   f"Spotify Link: {response['tracks'][3]['external_urls']['spotify']}\n"
                   f"5)\n"
                   f"Track name: {response['tracks'][4]['name']}\n"
                   f"Spotify Link: {response['tracks'][4]['external_urls']['spotify']}")

        send_email(user_email, subject, message)
        collection.update_one({"_id": doc["_id"]}, {"$set": {"Status": "done"}})


while True:
    process_data()
    time.sleep(20)

