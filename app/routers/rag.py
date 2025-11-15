from fastapi import APIRouter, HTTPException,  UploadFile, File
from pypdf import PdfReader
import uuid
import requests
import io

from definition import chroma, collection, OLLAMA_URL, EMBED_MODEL_NAME

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


@router.post("/doc")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(400, "Only PDF files are allowed")

    try:
        # Read PDF bytes
        pdf_bytes = await file.read()
        reader = PdfReader(io.BytesIO(pdf_bytes))

        # Extract all text
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        if not text.strip():
            raise HTTPException(400, "PDF text extraction failed or PDF is empty")

        # Generate embeddings
        emb = requests.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": EMBED_MODEL_NAME, "prompt": text}
        ).json()

        embedding = emb.get("embedding")
        if not embedding:
            raise HTTPException(500, "Embedding model did not return 'embedding'")

        # Store document
        doc_id = str(uuid.uuid4())

        collection.add(
            ids=[doc_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[{"filename": file.filename}]
        )

        return {"message": "PDF uploaded", "doc_id": doc_id}

    except Exception as e:
        raise HTTPException(500, f"Error processing PDF: {str(e)}")

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
