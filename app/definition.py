import os
from chromadb import Client
from chromadb.config import Settings
from pydantic import BaseModel

# Environment variables with defaults
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8001))

# Model names
GEN_MODEL_NAME = "llama2:7b"
EMBED_MODEL_NAME = "nomic-embed-text"

# Initialize Chroma client
chroma = Client(
    Settings(
        chroma_server_host=CHROMA_HOST,
        chroma_server_http_port=CHROMA_PORT,
    )
)

# Get or create the "docs" collection
collection = chroma.get_or_create_collection("docs")


class ChatRequest(BaseModel):
    message: str
