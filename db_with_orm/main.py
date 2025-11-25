import os
import uvicorn
from fastapi import FastAPI, status, HTTPException, Response, Depends
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from database import get_db, engine
from sqlalchemy.orm import Session
import models, schemas, utils, config
from routers import chats, users, auth, vote



models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(chats.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World!"}




if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)