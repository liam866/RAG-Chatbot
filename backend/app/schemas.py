from pydantic import BaseModel
from typing import List

class DocumentChunk(BaseModel):
    file: str
    heading: str
    text: str
    start_line: int
    end_line: int

class ChatRequest(BaseModel):
    question: str

class Source(BaseModel):
    file: str
    heading: str
    start_line: int
    end_line: int
    
class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]
