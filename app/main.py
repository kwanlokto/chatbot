import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from chromadb import Client
from chromadb.config import Settings

app = FastAPI()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8000))

GEN_MODEL_NAME = "llama2:7b"
EMBED_MODEL_NAME = "nomic-embed-text"

# Connect to Chroma server (Docker)
chroma = Client(Settings(
    chroma_server_host=CHROMA_HOST,
    chroma_server_http_port=CHROMA_PORT,
))
collection = chroma.get_or_create_collection("docs")

# Request model for chat endpoint
class ChatRequest(BaseModel):
    message: str

@app.post("/rag")
def rag(query: str):
    # 1. Embed query using Ollama
    emb = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL_NAME, "prompt": query}
    ).json()["embedding"]

    # 2. Retrieve top docs
    results = collection.query(query_embeddings=[emb], n_results=3)
    context = " ".join(results["documents"][0])

    # 3. Generate answer with Ollama
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    res = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": GEN_MODEL_NAME, "prompt": prompt, "stream": False}
    ).json()

    return {"response": res["response"]}


@app.post("/chat")
def chat(request: ChatRequest):
    """
    Freeform chat endpoint that sends user message directly to Ollama.
    """
    # 1️⃣ Embed the query
    emb = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL_NAME, "prompt": request.message}
    ).json()["embedding"]

    # 2️⃣ Retrieve top docs from Chroma
    results = collection.query(query_embeddings=[emb], n_results=3)
    context = " ".join(results["documents"][0])  # concatenate top docs

    # 3️⃣ Generate answer using LLM with context
    prompt = f"Context:\n{context}\n\nQuestion: {request.message}\nAnswer:"

    res = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": GEN_MODEL_NAME, "prompt": prompt, "stream": False}
    ).json()

    return {"response": res["response"]}
