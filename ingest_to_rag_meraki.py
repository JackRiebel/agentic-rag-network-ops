import requests
import json
import os
from sentence_transformers import SentenceTransformer

RAG_URL = os.getenv("RAG_MCP_URL", "http://localhost:8001")
embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")

def ingest_meraki_events(events):
    points = []
    for e in events:
        text = f"Meraki: {e.get('description', 'Event')} in {e.get('networkName')}"
        points.append({
            "id": f"meraki_{e.get('occurrenceId')}",
            "vector": embedder.encode(text).tolist(),
            "payload": {
                "text": text,
                "metadata": {
                    "source": "meraki",
                    "network_id": e.get("networkId"),
                    "device": e.get("deviceSerial"),
                    "timestamp": e.get("occurredAt")
                }
            }
        })
    requests.post(f"{RAG_URL}/ingest", json={"collection": "network_knowledge", "points": points})
