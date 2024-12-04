from typing import List, Dict, Optional
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    max_tokens: int = 256
    temperature: float = 0.7
    top_p: float = 0.9

class ChatResponseChoice(BaseModel):
    message: Dict[str, str]

class ChatResponse(BaseModel):
    choices: List[ChatResponseChoice]