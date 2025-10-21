import os
import uvicorn
from fastapi import FastAPI, status, HTTPException, Response, Depends
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from dotenv import load_dotenv
from database import get_db, engine
from sqlalchemy.orm import Session
import models, schemas, utils
from routers import chats, users



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

app.include_router(chats.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Hello World!"}




if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)