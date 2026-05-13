from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import chat, rag

app = FastAPI(title="PDF Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(rag.router)


@app.on_event("startup")
async def load_models():
    from routers.embeddings import get_model
    get_model()


@app.get("/health")
def health():
    return {"status": "ok"}
