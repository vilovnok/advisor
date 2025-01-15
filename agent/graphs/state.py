from typing import List, Optional

from pydantic import BaseModel
from langchain_core.messages import BaseMessage


class State(BaseModel):
    activity_name: Optional[str] = None 
    category_name: Optional[str] = None
    similary_name: Optional[str] = None
    hallucination: List[float] = []
    history: List[BaseMessage]
