#!/bin/bash
set -e

podman-compose down -v || true
podman-compose up --build -d

until podman exec qdrant curl -s http://localhost:6333/healthz | grep -q "OK"; do
  sleep 2
done

curl -X PUT 'http://localhost:6333/collections/network_knowledge' \
  -H 'Content-Type: application/json' \
  -d '{"vectors": {"size": 384, "distance": "Cosine"}}' || true

echo "System ready!"