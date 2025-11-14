from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Message(BaseModel):
    messages: list[dict]


@router.post("/chat")
async def chat(request: Message):
    # This function will be implemented in main.py
    pass


# Additional routes can be added here in the future.
