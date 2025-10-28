from pydantic import BaseModel
from typing import List, Dict, Optional

class Point(BaseModel):
    id: str
    vector: List[float]
    payload: Dict

class IngestRequest(BaseModel):
    collection: str
    points: List[Point]

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    source: Optional[str] = None

class Document(BaseModel):
    content: str
    metadata: Dict
    score: float
