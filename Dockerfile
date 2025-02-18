# Use an official lightweight Python base image
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

ENV LOG_FILE_DIR=/home/tdt/logs

# Install required dependencies for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY . /home/tdt
VOLUME /home/tdt
WORKDIR /home/tdt

RUN python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt



RUN chmod +x entrypoint.sh

ENTRYPOINT ["/home/tdt/entrypoint.sh"]