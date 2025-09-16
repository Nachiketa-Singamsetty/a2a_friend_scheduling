FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml ./
COPY app/ ./app/
COPY __init__.py ./

# Install dependencies
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install -e .

# Expose port
EXPOSE 10005

# Set environment variables
ENV PORT=10005
ENV PYTHONPATH=/app

# Run the application
CMD [".venv/bin/python", "-m", "app"]
