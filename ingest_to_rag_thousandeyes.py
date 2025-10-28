def ingest_te_agents(agents):
    points = []
    for a in agents:
        text = f"TE Agent: {a['agentName']} ({a['ipAddress']}) - {a['status']}"
        points.append({
            "id": f"te_{a['agentId']}",
            "vector": embedder.encode(text).tolist(),
            "payload": {
                "text": text,
                "metadata": {
                    "source": "te",
                    "agent_id": a['agentId'],
                    "location": a.get('location'),
                    "status": a['status']
                }
            }
        })
    requests.post(f"{RAG_URL}/ingest", json={"collection": "network_knowledge", "points": points})
