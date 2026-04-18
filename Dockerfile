# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install required system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application package
COPY . .

# Install pip and dependencies
# The requirements.txt contains '-e .' so the current dir gets installed
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Create a non-root user for security
RUN useradd -m appuser \
    && chown -R appuser:appuser /app
USER appuser
