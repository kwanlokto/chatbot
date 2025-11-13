# Chatbot FastAPI Application

This project is a FastAPI application that utilizes the Anthropic API to provide chat functionality. Below are the details regarding the structure, setup, and usage of the application.

## Project Structure

```
chatbot
├── app
│   ├── main.py          # FastAPI application setup and chat endpoint
│   ├── api
│   │   ├── routes.py    # API routes and request handling
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
   ```

4. **Run the Application**
   You can run the application using Uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```

   Alternatively, you can use Docker:
   ```bash
   docker-compose up --build
   ```

## Usage

Once the application is running, you can send POST requests to the `/chat` endpoint with a JSON body containing messages. The expected format is as follows:

```json
{
    "messages": [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there!"}
    ]
}
```

The application will respond with a generated reply based on the input messages.

## License

This project is licensed under the MIT License. See the LICENSE file for details.