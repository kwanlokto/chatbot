from fastapi import APIRouter, HTTPException
import requests
from definition import collection, OLLAMA_URL, GEN_MODEL_NAME, EMBED_MODEL_NAME, ChatRequest

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.get("/")
def chat(message: str):
    """
    Freeform chat endpoint that sends user message directly to Ollama.
    """
    # 1️⃣ Embed the query
    emb = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL_NAME, "prompt": message}
    ).json()

    query_emb = emb.get("embedding")
    if not query_emb:
        raise HTTPException(500, "Embedding model did not return 'embedding'")
    # 2️⃣ Retrieve top docs from Chroma
    results = collection.query(query_embeddings=[query_emb], n_results=3)
    context = " ".join(results["documents"][0])  # concatenate top docs

    # 3️⃣ Generate answer using LLM with context
    prompt = f"Context:\n{context}\n\nQuestion: {message}\nAnswer:"

    res = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": GEN_MODEL_NAME, "prompt": prompt, "stream": False}
    ).json()

    return {"response": res["response"]}
