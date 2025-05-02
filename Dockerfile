# Use the official Python 3.10 image from Dev Containers base
FROM mcr.microsoft.com/devcontainers/python:3.10

# Set work directory
WORKDIR /workspace

# Install system packages
RUN apt-get update && apt-get install -y \
    curl \
    git \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies (optional here)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Default command
CMD ["bash"]