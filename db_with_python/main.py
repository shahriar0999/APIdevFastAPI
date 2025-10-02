import time
import uvicorn
from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import time


app = FastAPI()

class Post(BaseModel):
    id: int
    title: str
    date: datetime
    query: str

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastAPI', user='postgres', password='1212759382',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(3)

@app.get("/")
def root():
    return {"message": "Hello World!"}