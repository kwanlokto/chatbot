from typing import List, Optional

import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from definition import (
    GEN_MODEL_NAME,
    HF_GEN_MODEL,
    HF_TOKEN,
    LLM_PROVIDER,
    OLLAMA_URL,
    collection,
)

from .embeddings import embed

router = APIRouter(prefix="/chat", tags=["Chat"])


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []


def _ollama_generate(prompt: str) -> str:
    res = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": GEN_MODEL_NAME, "prompt": prompt, "stream": False},
        timeout=120,
    )
    res.raise_for_status()
    return res.json()["response"]


def _hf_generate(prompt: str) -> str:
    from huggingface_hub import InferenceClient

    client = InferenceClient(model=HF_GEN_MODEL, token=HF_TOKEN or None)
    return client.text_generation(prompt, max_new_tokens=512, temperature=0.7)


@router.post("/")
def chat(body: ChatRequest):
    query_emb = embed(body.message)

    results = collection.query(query_embeddings=[query_emb], n_results=3)
    docs = results["documents"][0] if results.get("documents") else []
    context = "\n\n".join(docs)

    history_str = "".join(
        f"{'Human' if m.role == 'user' else 'Assistant'}: {m.content}\n"
        for m in (body.history or [])
    )

    prompt = (
        "You are a helpful assistant. Use the provided context to answer questions accurately. "
        "If the context does not contain relevant information, say so.\n\n"
        f"Context:\n{context}\n\n"
        f"{history_str}"
        f"Human: {body.message}\nAssistant:"
    )

    try:
        if LLM_PROVIDER == "huggingface":
            response = _hf_generate(prompt)
        else:
            response = _ollama_generate(prompt)
    except Exception as e:
        raise HTTPException(500, f"LLM error: {str(e)}")

    return {"response": response}
