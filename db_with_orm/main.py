import os
from typing import List, Optional
import uvicorn
from fastapi import FastAPI, status, HTTPException, Response, Depends
from pydantic import BaseModel
from datetime import datetime
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from dotenv import load_dotenv
from database import get_db, engine
from sqlalchemy.orm import Session
import models, schemas, utils



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


@app.get("/chats", response_model=List[schemas.PostBase])
def get_posts(db: Session = Depends(get_db)):
    chats = db.query(models.Chat).all()
    return chats


@app.post("/chats", status_code=status.HTTP_201_CREATED, response_model=schemas.PostBase)
def create_chat(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_chat = models.Chat(query=post.query, response=post.response)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat

# get a specific chat
@app.get("/chats/{id}", response_model=schemas.PostBase)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Chat).filter(models.Chat.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post

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
@app.put("/chats/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostBase)
def update_chat(id: int, updated_post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Chat).filter(models.Chat.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"chat with id: {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

# create users
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # has the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# get user
@app.get("/users/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")
    return user

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)