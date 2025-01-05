from pydantic import BaseModel
from fastapi import UploadFile
from typing import List, Optional

class AdviceSchemas(BaseModel):
    file: UploadFile 
    fileType: str
    # recommendations: Optional[List]=None
