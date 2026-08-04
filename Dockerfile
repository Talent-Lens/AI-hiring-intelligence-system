FROM python:3.11-slim

WORKDIR /app

# Install Linux system dependencies required by OpenCV and audio/video processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port 7860 (Hugging Face Spaces default port)
EXPOSE 7860

# Run uvicorn server with correct case matching Backend folder
CMD ["uvicorn", "Backend.main:app", "--host", "0.0.0.0", "--port", "7860"]