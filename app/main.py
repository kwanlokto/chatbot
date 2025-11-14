from fastapi import FastAPI
from routers import chat, rag

app = FastAPI()

# Register routers
app.include_router(chat.router)
app.include_router(rag.router)
