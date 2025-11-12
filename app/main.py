from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

app = FastAPI()
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

class Message(BaseModel):
    messages: list[dict]

@app.post("/chat")
async def chat(request: Message):
    prompt = ""
    for m in request.messages:
        if m["role"] == "user":
            prompt += f"{HUMAN_PROMPT} {m['content']}"
        else:
            prompt += f"{AI_PROMPT} {m['content']}"

    response = client.completions.create(
        model="claude-3.5-sonnet",
        prompt=prompt,
        max_tokens_to_sample=500
    )

    return {"reply": response.completion}