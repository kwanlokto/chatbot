import os
import requests
from fastapi import FastAPI
from chromadb import HttpClient

app = FastAPI()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
CHROMA_URL = os.getenv("CHROMA_URL", "http://localhost:8001")

# Connect to Chroma using URL (more flexible)
chroma = HttpClient.from_url(CHROMA_URL)
collection = chroma.get_or_create_collection("docs")

@app.post("/rag")
def rag(query: str):
    # 1. Embed query using Ollama
    emb = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": query}
    ).json()["embedding"]

    # 2. Retrieve top docs
    results = collection.query(query_embeddings=[emb], n_results=3)
    context = " ".join(results["documents"][0])

    # 3. Generate answer with Ollama
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    res = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False}
    ).json()

    return {"response": res["response"]}
