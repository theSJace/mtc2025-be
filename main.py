import logging, uvicorn, json
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from psycopg2 import pool
from ollama import Client
from util import *

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s')

app = FastAPI(title="MTC Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db_pool = pool.SimpleConnectionPool(
    minconn=1,  # Minimum number of connections
    maxconn=10,  # Maximum number of connections
    database="mtc",
    user="postgres",
    password="RSNQMuhRTHoqSOgZXmRWahhZHWZIbzeJ",
    host="shinkansen.proxy.rlwy.net",
    port=45600
)

class UserDTO(BaseModel):
    userId: str | None = ""
    userNickName: str | None = ""
    userEmail: str | None = ""
    userDob: str | None = ""
    userType: str | None = ""
    parentId: str | None = ""
    refCode: str | None = ""
    foodLikes: str | None = ""
    foodDislikes: str | None = ""
    hobbies: str | None = ""

class JournalDTO(BaseModel):
    journalId: str | None = ""
    journalEntry: str | None = ""
    sentiment: str | None = ""
    justification: str | None = ""
    emotion: str | None = ""
    updatedTs: str | None = ""
    userId: str | None = ""

class HobbyDTO(BaseModel):
    userId: str | None = ""

def getEmotions(createJournal:JournalDTO):
    client = Client(
    host='https://8d56-49-245-100-161.ngrok-free.app',
    )
    response = client.chat(model='llama3.2', messages=[
    {
        'role': 'user',
        'content': "you will assess the text given and return the sentiment (negative, positive, neutral) with emotions the user might be feeling as well as justification in a JSON compatible response. Keep the response to only be a JSON format",
    },
    {
        'role': 'user',
        'content': createJournal.journalEntry,
    },
    ])
    try:
        jsonRes = json.loads(response['message']['content'])
        sanitiseSentiment = jsonRes["sentiment"].replace("'", "")
        sanitiseEmotion = ','.join(jsonRes["emotions"]).replace("'", "")
        sanitiseJustification = jsonRes["justification"].replace("'", "")
        createJournal.sentiment = sanitiseSentiment
        createJournal.emotion = sanitiseEmotion
        createJournal.justification = sanitiseJustification
    except:
        print("Error getting response, trying again")
        getEmotions(createJournal)

def getActivityRecommendation(hobbyArr):
    client = Client(
    host='https://8d56-49-245-100-161.ngrok-free.app',
    )
    response = client.chat(model='llama3.2', messages=[
    {
        'role': 'system',
        'content': "you will be given a list of hobbies. Recommend activities for families that will be compatible with all or most of the hobbies if satisfying all is not possible with a short justification for each activity in less than 10 words. No extra note is required",
    },
    {
        'role': 'user',
        'content': ','.join(hobbyArr),
    },
    ])
    return response['message']['content']

@app.get("/", status_code=200)
def main():
    return '{"status":"Running"}'

@app.get("/user/{telegram_id}", status_code=200)
def checkUserExists(telegram_id:str, response: Response):
    print("Checking for user "+telegram_id)
    conn = db_pool.getconn()
    userExists, userData = checkUserImpl(telegram_id, conn)
    db_pool.putconn(conn)
    if(userExists):
        return userData
    response.status_code = status.HTTP_404_NOT_FOUND
    return None

@app.post("/user", status_code=200)
def createUserData(createUser:UserDTO, response:Response):
    conn = db_pool.getconn()
    success = createUserImpl(createUser, conn)
    db_pool.putconn(conn)
    if success == False:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return success

@app.get("/journal/{telegram_id}", status_code=200)
def getJournalByUser(telegram_id:str, response:Response):
    conn = db_pool.getconn()
    success, journalList = getJournalImpl(telegram_id, conn)
    db_pool.putconn(conn)
    if success == False:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return journalList

@app.post("/journal", status_code=200)
def createJournaldata(createJournal:JournalDTO, response:Response):
    conn = db_pool.getconn()
    getEmotions(createJournal)
    success = createJournalImpl(createJournal, conn)
    db_pool.putconn(conn)
    if success == False:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return success

@app.post("/journal/update", status_code=200)
def updateJournaldata(updateJournal:JournalDTO, response:Response):
    conn = db_pool.getconn()
    getEmotions(updateJournal)
    success = updateJournalImpl(updateJournal, conn)
    db_pool.putconn(conn)
    if success == False:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return success

@app.post("/hobby", status_code=200)
def getActivities(hobbyDto:HobbyDTO):
    conn = db_pool.getconn()
    hobbyList = getHobbyImpl(hobbyDto,conn)
    activityRecommendation = getActivityRecommendation(hobbyList)
    return activityRecommendation

if __name__ == '__main__':
    uvicorn.run(app, port=8000)