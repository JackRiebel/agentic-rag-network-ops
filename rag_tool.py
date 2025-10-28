import requests
from langchain.tools import StructuredTool

RAG_URL = os.getenv("RAG_MCP_URL", "http://mcp-rag-server:8000")

def rag_search(query: str, source: str = None, top_k: int = 5) -> str:
    payload = {"query": query, "top_k": top_k}
    if source:
        payload["source"] = source
    docs = requests.post(f"{RAG_URL}/search", json=payload).json()
    return "\n\n".join([f"[{d['metadata'].get('source','?')}] {d['content']}" for d in docs])

rag_tool = StructuredTool.from_function(
    func=rag_search,
    name="RAG_Search",
    description="Search historical Meraki/TE/Splunk data. Use source: meraki, te, splunk"
)
