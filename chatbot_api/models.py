from pydantic import BaseModel
from typing import Dict, List


class CreateChatRequest(BaseModel):
    user_message: str

class UpdateChatRequest(BaseModel):
    title: str

class ChatResponse(BaseModel):
    chat_id: str
    title: str
    messages: List[Dict[str, str]]