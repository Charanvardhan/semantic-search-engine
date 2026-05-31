#!/bin/bash
set -e

# Semantic Search Engine setup script

echo "=== Semantic Search Engine Setup ==="
cd "$(dirname "$0")"

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "semanticsearchengine" ]; then
    echo "Creating virtual environment in semanticsearchengine/ using uv..."
    uv venv semanticsearchengine
fi

# Activate virtual environment
echo "Activating virtual environment..."
source semanticsearchengine/bin/activate

# Install dependencies using uv
echo "Installing dependencies from requirements.txt using uv..."
uv pip install -r requirements.txt

# Run server
echo "Starting FastAPI server..."
python -m uvicorn app.main:app --reload --port 8000
