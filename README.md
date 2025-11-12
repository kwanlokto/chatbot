# Claude Chatbot with Python Backend

A simple chatbot backend powered by **Claude (Anthropic)** using **Python FastAPI**. This backend exposes an API endpoint that your frontend (e.g., Next.js or any client) can call to interact with Claude.

---

## Features

* Chat with Claude LLM (3.5 Sonnet model)
* FastAPI backend handling Claude API requests
* Supports multiple messages (chat history)
* Easy to deploy locally or to a cloud provider

---

## Tech Stack

* **Backend**: Python 3.11+, FastAPI, Anthropic SDK
* **Server**: Uvicorn ASGI server
* **Environment Management**: `python-dotenv`

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/claude-chatbot-backend.git
cd claude-chatbot-backend
```

### 2. Setup Python Backend

1. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root:

```
ANTHROPIC_API_KEY=sk-ant-xxxxxx
```

4. Run the FastAPI server:

```bash
uvicorn main:app --reload --port 8000
```

The backend will run at `http://localhost:8000`.

---

## API Usage

Send a POST request to `/chat` with the following JSON body:

```json
{
  "messages": [
    { "role": "user", "content": "Hello Claude!" }
  ]
}
```

The response will be:

```json
{
  "reply": "Claude's response here"
}
```

You can use this endpoint with any frontend or client.

---

## Deployment

### Recommended Hosting

* **FastAPI backend**: Vercel (serverless Python), Render, Railway, Fly.io, or any Python hosting.

> Note: GitHub Pages cannot host the backend API — you need a live Python server.

---

## Optional Enhancements

* Add **streaming responses** for live typing effect.
* Persist chat history using SQLite, PostgreSQL, or Supabase.
* Integrate **RAG (Retrieval-Augmented Generation)** with your own docs.
* Add authentication for secure API access.

---

## Folder Structure (Example)

```
backend/
├─ main.py
├─ requirements.txt
└─ .env
```

---

## License

MIT License © [Your Name]

---

## References

* [Claude API Documentation](https://console.anthropic.com/docs/)
* [FastAPI Documentation](https://fastapi.tiangolo.com/)
