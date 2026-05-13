# PDF Chatbot

A full-stack RAG chatbot that lets you upload PDFs and ask questions about them. Uses open-source LLMs — no OpenAI required.

## Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15 + Tailwind CSS |
| Backend | FastAPI (Python) |
| Embeddings | fastembed (`all-MiniLM-L6-v2`, runs on CPU) |
| LLM (local) | Ollama (`llama3.2`) |
| LLM (cloud) | HuggingFace Inference API (`Mixtral-8x7B`) |
| Vector DB | ChromaDB |

## Project Structure

```
chatbot/
├── app/                        # FastAPI backend
│   ├── main.py                 # App entry point, CORS, startup
│   ├── definition.py           # Config and ChromaDB client
│   └── routers/
│       ├── chat.py             # POST /chat/ — RAG chat with history
│       ├── rag.py              # POST /rag/doc — PDF upload; DELETE /rag/file/{name}
│       └── embeddings.py       # fastembed singleton
├── frontend/                   # Next.js frontend
│   └── src/
│       ├── app/                # Next.js App Router (layout, page)
│       ├── components/         # Sidebar, ChatWindow, MessageBubble, ChatInput
│       └── lib/api.ts          # Typed fetch helpers
├── docker-compose.yml          # Ollama + ChromaDB services
├── Dockerfile                  # Backend container
├── requirements.txt
└── .env.example
```

## Running Locally

Everything runs via Docker — one command starts all four services.

```bash
docker compose up --build
```

| Service | URL |
|---|---|
| Frontend (Next.js) | http://localhost:3000 |
| Backend (FastAPI) | http://localhost:8000 |
| API docs (Swagger) | http://localhost:8000/docs |
| ChromaDB | http://localhost:8001 |

**First run only** — pull the Ollama model after the containers are up:

```bash
docker exec ollama ollama pull llama3.2
```

> The backend will return LLM errors until the model is pulled. Embeddings and PDF upload work immediately.

### Running without Docker (optional)

If you prefer to run services individually:

```bash
# 1. Start Ollama + ChromaDB only
docker compose up ollama chromadb -d
docker exec ollama ollama pull llama3.2

# 2. Backend
pip install -r requirements.txt
cd app && uvicorn main:app --reload

# 3. Frontend
cd frontend
cp .env.local.example .env.local
npm install && npm run dev
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/chat/` | Send a message; returns AI response |
| `POST` | `/rag/doc` | Upload a PDF for RAG |
| `GET` | `/rag/docs` | List all indexed chunks |
| `DELETE` | `/rag/file/{filename}` | Remove all chunks for a file |
| `GET` | `/rag/query` | Raw vector search |
| `GET` | `/health` | Health check |

## Deploying to the Cloud

### Frontend → Vercel (free)

1. Push the repo to GitHub and import it in [Vercel](https://vercel.com)
2. Set **Root Directory** to `frontend`
3. Add environment variable: `NEXT_PUBLIC_API_URL=https://your-backend.onrender.com`

### Backend → Render.com (free tier)

1. New **Web Service** → connect repo, root directory `.`
2. **Build command:** `pip install -r requirements.txt`
3. **Start command:** `cd app && uvicorn main:app --host 0.0.0.0 --port 8000`
4. Set environment variables:

```
LLM_PROVIDER=huggingface
HF_TOKEN=hf_your_token_here
HF_GEN_MODEL=mistralai/Mixtral-8x7B-Instruct-v0.1
CHROMA_HOST=<your-chromadb-host>
CHROMA_PORT=8000
```

> Get a free HuggingFace token at https://huggingface.co/settings/tokens

### ChromaDB in the cloud

For persistent vector storage in production, run ChromaDB as a second Render service (or any server) using the `chromadb/chroma` Docker image, then point `CHROMA_HOST` / `CHROMA_PORT` at it.

## Environment Variables

Copy `.env.example` to `.env` for the backend and `frontend/.env.local.example` to `frontend/.env.local` for the frontend.

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `ollama` | `ollama` or `huggingface` |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama base URL |
| `GEN_MODEL_NAME` | `llama3.2` | Ollama model name |
| `HF_TOKEN` | — | HuggingFace API token |
| `HF_GEN_MODEL` | `mistralai/Mixtral-8x7B-Instruct-v0.1` | HF model ID |
| `CHROMA_HOST` | `localhost` | ChromaDB host |
| `CHROMA_PORT` | `8001` | ChromaDB port |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Frontend → backend URL |
