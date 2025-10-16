import os
import time
import uvicorn
from fastapi import FastAPI, status, HTTPException, Response, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from dotenv import load_dotenv
from database import get_db, engine
from sqlalchemy.orm import Session
import time
import models

models.Base.metadata.create_all(bind=engine)

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
    query: str
    response: str

@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get("/chats")
def get_posts(db: Session = Depends(get_db)):
    chats = db.query(models.Chat).all()
    return {"chats": chats}


@app.post("/chats", status_code=status.HTTP_201_CREATED)
def create_chat(post: Post, db: Session = Depends(get_db)):
    new_chat = models.Chat(query=post.query, response=post.response)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return {"response": new_chat}

# get a specific chat
@app.get("/chats/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Chat).filter(models.Chat.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return ("chat", post)

# delete a specific chat
@app.delete("/chats/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Chat).filter(models.Chat.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"chat with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update a existing chat
@app.put("/chats/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_chat(id: int, updated_post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Chat).filter(models.Chat.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"chat with id: {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"chat": post_query.first()}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)