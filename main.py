import os, logging, uvicorn
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from psycopg2 import pool
from datetime import datetime
from ollama import chat
from util import *

# DB_HOST = os.environ["DBHOST"]
# DB_PORT = os.environ["DBPORT"]
# DB_USER = os.environ["DBUSER"]
# DB_PASS = os.environ["DBPASSWORD"]

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s')

app = FastAPI(title="MTC Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# db_pool = pool.SimpleConnectionPool(
#     minconn=1,  # Minimum number of connections
#     maxconn=10,  # Maximum number of connections
#     database="mtc",
#     user=DB_USER,
#     password=DB_PASS,
#     host=DB_HOST,
#     port=DB_PORT
# )

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
    userFname: str | None = ""
    userLname: str | None = ""
    userEmail: str | None = ""
    userDob: str | None = ""
    userType: str | None = ""
    parentId: str | None = ""
    hobbies: str | None = ""
    foodLikes: str | None = ""
    foodDislikes: str | None = ""
    refCode: str | None = ""

class JournalDTO(BaseModel):
    journalId: str | None = ""
    journalEntry: str | None = ""
    sentiment: str | None = ""
    justification: str | None = ""
    userId: str | None = ""

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

@app.get("/journal", status_code=200)
def getJournalData(retrieveJournal:JournalDTO, response:Response):
    conn = db_pool.getconn()
    success = getJournalImpl(retrieveJournal, conn)
    db_pool.putconn(conn)
    if success == False:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return success

@app.post("/journal", status_code=200)
def createJournaldata(createJournal:JournalDTO, response:Response):
    conn = db_pool.getconn()
    success = createJournalImpl(createJournal, conn)
    db_pool.putconn(conn)
    if success == False:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return success

if __name__ == '__main__':
    uvicorn.run(app, port=8000)