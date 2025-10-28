from fastapi import FastAPI, HTTPException
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from .models import QueryRequest, Document, IngestRequest
from .ingest import ingest_points
import os

app = FastAPI(title="MCP: RAG Server")

embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")
client = QdrantClient(host=os.getenv("QDRANT_HOST", "qdrant"), port=6333)
COLLECTION = "network_knowledge"

@app.post("/ingest")
async def ingest(data: IngestRequest):
    return ingest_points(data)

@app.post("/search", response_model=list[Document])
async def search(req: QueryRequest):
    vector = embedder.encode(req.query).tolist()

    filter_ = None
    if req.source:
        filter_ = {"must": [{"key": "metadata.source", "match": {"value": req.source}}]}

    try:
        results = client.search(
            collection_name=COLLECTION,
            query_vector=vector,
            limit=req.top_k,
            query_filter=filter_
        )
        return [
            Document(
                content=r.payload["text"],
                metadata=r.payload.get("metadata", {}),
                score=r.score
            )
            for r in results
        ]
    except Exception as e:
        raise HTTPException(500, str(e))
