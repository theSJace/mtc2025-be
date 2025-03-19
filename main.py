import os, logging, uvicorn
from fastapi import FastAPI, HTTPException
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
    password="s9740499b",
    host="localhost",
    port=5432
)

@app.get("/", status_code=200)
def main():
    return '{"status":"Running"}'

@app.get("/test", status_code=200)
def ollamaTest():
    startTime = datetime.now()
    
    stream = chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
        stream=True,
    )

    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
    endTime = datetime.now()
    elapsedTime = endTime - startTime
    print("\n"+str(elapsedTime.total_seconds()))
    return '{"status":"Running"}'

if __name__ == '__main__':
    uvicorn.run(app, port=8000)