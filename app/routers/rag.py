import os
import requests
import tempfile
import uuid

from definition import chroma, collection, EMBED_MODEL_NAME, OLLAMA_URL
from fastapi import APIRouter, File, HTTPException, UploadFile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings

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
        # -------------------------
        # Save uploaded PDF to temp file
        # -------------------------
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # -------------------------
        # Load PDF with LangChain
        # -------------------------
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()

        if not pages:
            raise HTTPException(400, "Could not extract text from PDF")

        # -------------------------
        # Split into chunks
        # -------------------------
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        docs = splitter.split_documents(pages)

        # -------------------------
        # LangChain Embeddings (Ollama)
        # -------------------------
        embeddings = OllamaEmbeddings(model=EMBED_MODEL_NAME, base_url=OLLAMA_URL)  # important

        # -------------------------
        # Insert documents into Chroma
        # Using your existing Chroma collection
        # -------------------------
        texts = [d.page_content for d in docs]
        metadatas = [d.metadata for d in docs]
        ids = [str(uuid.uuid4()) for _ in docs]

        collection.add(
            documents=texts,
            ids=ids,
            metadatas=metadatas,
            embeddings=embeddings.embed_documents(texts),
        )

        # Cleanup temp pdf
        os.remove(tmp_path)

        return {"message": "PDF uploaded", "chunks": len(texts)}

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
