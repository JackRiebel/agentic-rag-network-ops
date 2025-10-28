from langchain_anthropic import ChatAnthropic
import requests
import os

RAG_URL = os.getenv("RAG_MCP_URL", "http://mcp-rag-server:8000")
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)

def rag_search(query: str, source: str = None, top_k: int = 5) -> str:
    payload = {"query": query, "top_k": top_k}
    if source:
        payload["source"] = source
    try:
        resp = requests.post(f"{RAG_URL}/search", json=payload, timeout=10)
        resp.raise_for_status()
        docs = resp.json()
        return "\n\n".join([f"[{d['metadata'].get('source','?')}] {d['content']}" for d in docs])
    except Exception as e:
        return f"RAG Error: {str(e)}"

def run_query(query: str) -> str:
    rag_results = rag_search(query, source="meraki") + "\n\n" + rag_search(query, source="te")
    prompt = f"""
    You are a network diagnostics agent.
    Use RAG results to diagnose: {query}
    
    RAG Context:
    {rag_results}
    
    Provide root cause and action.
    """
    response = llm.invoke(prompt)
    return response.content

if __name__ == "__main__":
    print(run_query("Why is Paris office slow?"))