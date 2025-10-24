from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from typing import List
import database
from sqlalchemy.orm import Session
import models, schemas, oauth2


router = APIRouter(
    prefix="/chats",
    tags=["Chats"]
)


@router.get("/", response_model=List[schemas.PostBase])
def get_posts(db: Session = Depends(database.get_db)):
    chats = db.query(models.Chat).all()
    return chats


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostBase)
def create_chat(post: schemas.PostCreate, db: Session = Depends(database.get_db), user_id: int = Depends(oauth2.get_current_user)):
    new_chat = models.Chat(query=post.query, response=post.response)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat

# get a specific chat
@router.get("/{id}", response_model=schemas.PostBase)
def get_post(id: int, db: Session = Depends(database.get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Chat).filter(models.Chat.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post

# delete a specific chat
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Chat).filter(models.Chat.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"chat with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update a existing chat
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostBase)
def update_chat(id: int, updated_post: schemas.PostCreate, db: Session = Depends(database.get_db), user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Chat).filter(models.Chat.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"chat with id: {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
