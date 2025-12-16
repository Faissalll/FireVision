FROM python:3.10-slim

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment Variables (Default)
ENV FLASK_APP=main.py

# Run with Gunicorn (or Python direct for threading)
# Using python direct because we rely on Threading for RTSP loop
CMD ["python", "main.py"]
