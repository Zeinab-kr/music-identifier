from fastapi import FastAPI, File, UploadFile, Form
from firstService.s3Handler import upload_to_s3
from firstService.dataBase import add_to_db
from firstService.rabbitMQ import add_to_queue

app = FastAPI()


@app.get("/")
def home():
    return {"message": "works well"}


@app.post("/get-request")
def get_request(email: str = Form(...), voice: UploadFile = File(...)):
    upload_to_s3(voice)
    object_id = add_to_db(email, voice.filename)
    add_to_queue(object_id)

    return {"message": "connection failed"}
