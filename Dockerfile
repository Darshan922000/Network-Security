# Use Python 3.10 as the base image
FROM python:3.10.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all files into the container
COPY . .

# Install Poetry (if using Poetry to manage pyproject.toml)
RUN pip install poetry

# Configure Poetry to Avoid Virtual Environments..all dependencies install globally not in virtual environment..
RUN poetry config virtualenvs.create false

# Install dependencies from pyproject.toml
RUN poetry install --no-root

RUN apt clean && apt update -y && apt install -y curl less && pip install awscli

RUN apt-get update

# Expose the port for FastAPI
EXPOSE 8080

# Default command: run FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]


