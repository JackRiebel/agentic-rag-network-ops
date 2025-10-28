from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from .models import IngestRequest

client = QdrantClient(host="qdrant", port=6333)
COLLECTION = "network_knowledge"

def ingest_points(data: IngestRequest):
    points = [
        PointStruct(id=p.id, vector=p.vector, payload=p.payload)
        for p in data.points
    ]
    client.upsert(collection_name=data.collection, points=points)
    return {"status": "success", "ingested": len(points)}
