FROM python:3.11-slim

# Install FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY main.py .
COPY officeambience.mp3 .

# Run the script
CMD ["python", "main.py"]
