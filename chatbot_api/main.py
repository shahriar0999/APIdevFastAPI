from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import uuid
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from loading import load_dotenv


load_dotenv()


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Chatbot API!"}



