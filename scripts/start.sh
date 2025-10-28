#!/bin/bash
podman-compose down -v
podman-compose up --build -d

echo "Waiting for Qdrant..."
until podman exec qdrant curl -s http://localhost:6333/healthz | grep -q "OK"; do sleep 2; done

echo "Creating collection..."
curl -X PUT 'http://localhost:6333/collections/network_knowledge' \
  -H 'Content-Type: application/json' \
  -d '{"vectors": {"size": 384, "distance": "Cosine"}}'

echo "System ready!"
