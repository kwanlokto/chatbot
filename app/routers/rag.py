from fastapi import APIRouter, HTTPException
import requests

from definition import chroma, collection, OLLAMA_URL

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.get("/collections")
def list_collections():
    return {"collections": chroma.list_collections()}


@router.get("/docs")
def get_all_docs():
    return collection.get()


@router.get("/doc/{doc_id}")
def get_doc(doc_id: str):
    result = collection.get(ids=[doc_id])
    if not result["documents"]:
        raise HTTPException(404, "Document not found")
    return result


@router.get("/query")
def query_docs(query: str, n: int = 3):

    emb = requests.post(
        f"{OLLAMA_URL}/api/embeddings", json={"model": "nomic-embed-text", "prompt": query}
    ).json()

    query_emb = emb.get("embedding")
    if not query_emb:
        raise HTTPException(500, "Embedding model did not return 'embedding'")

    results = collection.query(query_embeddings=[query_emb], n_results=n)
    return results
