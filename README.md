# Chatbot FastAPI Application

This project is a FastAPI application that utilizes the Anthropic API to provide chat functionality. Below are the details regarding the structure, setup, and usage of the application.

## Project Structure

```
chatbot
├── app
│   ├── main.py          # FastAPI application setup and chat endpoint
│   ├── routers          # API routes and request handling
│   │   └── __init__.py  # Marks the api directory as a Python package
│   └── __init__.py      # Marks the app directory as a Python package
├── Dockerfile            # Instructions to build the Docker image
├── docker-compose.yml    # Defines services and configurations for Docker
├── requirements.txt      # Lists Python dependencies
├── .env                  # Environment variables (e.g., API keys)
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd chatbot
   ```

2. **Create a Virtual Environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ollama pull llama2:7b
   ollama pull nomic-embed-text
   ```

   Alternatively, you can use Docker:
   ```bash
   ./docker_build.sh
   ```

4. **Run the Application**
   You can run the application using Uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```

   Alternatively, you can use Docker:
   ```bash
   docker compose up -d
   ```

## Usage

We are using FastAPI so you can reference the docs via localhost:8000/docs

## License

This project is licensed under the MIT License. See the LICENSE file for details.