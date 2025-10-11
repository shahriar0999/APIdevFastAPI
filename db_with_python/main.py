import os
import time
import uvicorn
from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import time

# Load API key from .env
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq chat model
chat = ChatGroq(
    api_key=groq_api_key,
    model="openai/gpt-oss-20b"  # or any available Groq model
)


app = FastAPI()

class Post(BaseModel):
    title: str
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


@app.get("/chats")
def get_posts():
    cursor.execute("""SELECT * FROM chats """)
    chats = cursor.fetchall()
    return {"chats": chats}


@app.post("/chats", status_code=status.HTTP_201_CREATED)
def create_chat(post: Post):
    cursor.execute("""INSERT INTO chats (title, query) VALUES (%s, %s) RETURNING *""",
                   (post.title, post.query))
    new_post = cursor.fetchone()
    conn.commit()
    # Send a message
    messages = [
        HumanMessage(content=post.query)
    ]
    response = chat(messages)
    # conver that post into dict
    new_post = dict(new_post)
    new_post['response'] = response.content
    return {"response": new_post}

# get a specific chat
@app.get("/chats/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM chats WHERE id = %s""", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return ("chat", post)

# delete a specific chat
@app.delete("/chats/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM chats WHERE id = %s RETURNING *""", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"chat with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

  

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)