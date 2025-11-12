# Use a small official image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build deps, install python deps, then remove build deps to keep image small
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

EXPOSE 8000

# Run uvicorn pointing to main:app (your file is main.py)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]