from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class QueryRequest(BaseModel):
    query: str

class Resource(BaseModel):
    id: str
    title: str
    type: str # 'ppt' or 'video'
    url: str
    description: Optional[str] = None
    tags: List[str] = []

class QueryResponse(BaseModel):
    answer: str
    resources: List[Resource]

class QueryLog(BaseModel):
    id: str
    user_id: Optional[str]
    query_text: str
    response_json: dict
    created_at: datetime
