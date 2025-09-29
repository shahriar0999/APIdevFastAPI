from fastapi import FastAPI, HTTPException, status, Body, Response
from pydantic import BaseModel


app = FastAPI()

class Chat(BaseModel):
    name: str
    description: str

chats = [
    {"id": 1, "name": "Advance MLOPS Roadmap", "description": "This is a chat about MLOPS"},
    {"id": 2, "name": "Data Science", "description": "This is a chat about Data Science"}
]

# get post
def find_chat(id: int):
    for chat in chats:
        if chat['id'] == id:
            return chat
        
# find index
def find_chat_index(id: int):
    for i, chat in enumerate(chats):
        if chat['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "Welcome to FastApi Basics 2.0"}


# get all chats using crud operration retrieve method
@app.get("/chats")
def get_chats():
    return {'chats': chats}

# get a single chat
@app.get("/chats/{id}")
def get_chat(id: int):
    chat = find_chat(id)
    if not chat:
        raise HTTPException(status_code=404, detail=f"Chat with id {id} not found")
    return {'chat': chat}

# # create a chat but have data validation problem
# @app.post("/chats")
# def create_chat(chat: dict = Body(...)):
#     return {"message": "this works"}

@app.post("/chats")
def create_chat(chat: Chat):
    chat = chat.dict()
    chat['id'] = len(chats) + 1
    chats.append(chat)
    return {"chat": chat}


# delete a chat
@app.delete("/chats/{id}")
def delete_chat(id: int):
    index = find_chat_index(id)
    if index == None:
        raise HTTPException(status_code=404, detail=f"Chat with id {id} not found")
    chats.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)