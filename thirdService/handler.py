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
        message = f"Here are your music recommendations: {response}"

        send_email(user_email, subject, message)
        collection.update_one({"_id": doc["_id"]}, {"$set": {"Status": "done"}})


while True:
    process_data()
    time.sleep(20)

