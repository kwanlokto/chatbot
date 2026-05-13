import os

import chromadb

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8001))

# "ollama" or "huggingface"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
GEN_MODEL_NAME = os.getenv("GEN_MODEL_NAME", "llama3.2")

HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_GEN_MODEL = os.getenv("HF_GEN_MODEL", "mistralai/Mixtral-8x7B-Instruct-v0.1")

chroma = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
collection = chroma.get_or_create_collection("docs")
