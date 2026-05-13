import os
import tempfile
import uuid
from urllib.parse import unquote

from fastapi import APIRouter, File, HTTPException, UploadFile
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

from definition import chroma, collection

from .embeddings import embed, embed_batch

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.get("/collections")
def list_collections():
    return {"collections": [c.name for c in chroma.list_collections()]}


@router.get("/docs")
def get_all_docs():
    return collection.get(include=["metadatas", "documents"])


@router.post("/doc")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(400, "Only PDF files are allowed")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        loader = PyPDFLoader(tmp_path)
        pages = loader.load()
        os.remove(tmp_path)

        if not pages:
            raise HTTPException(400, "Could not extract text from PDF")

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = splitter.split_documents(pages)

        texts = [d.page_content for d in docs]
        metadatas = [
            {"source": file.filename, **{k: str(v) for k, v in d.metadata.items()}}
            for d in docs
        ]
        ids = [str(uuid.uuid4()) for _ in docs]
        embeddings = embed_batch(texts)

        collection.add(documents=texts, ids=ids, metadatas=metadatas, embeddings=embeddings)

        return {"message": "PDF uploaded successfully", "chunks": len(texts), "filename": file.filename}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error processing PDF: {str(e)}")


@router.delete("/file/{filename:path}")
def delete_file(filename: str):
    filename = unquote(filename)
    collection.delete(where={"source": filename})
    return {"message": f"Deleted all chunks for {filename}"}


@router.get("/query")
def query_docs(query: str, n: int = 3):
    query_emb = embed(query)
    return collection.query(query_embeddings=[query_emb], n_results=n)
