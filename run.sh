#!/usr/bin/env bash
set -e

# Change directory to the script's location
cd "$(dirname "$0")"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 could not be found."
    echo "Please install Python 3 (e.g., sudo apt install python3 python3-pip python3-tk ffmpeg)"
    exit 1
fi

# Function to run the app
run_app() {
    echo "[INFO] Starting TranscriPy..."
    "$1" transcripy.py
}

# 1. Check if dependencies are already installed globally or in current environment
if python3 -c "import customtkinter, faster_whisper" 2>/dev/null; then
    run_app python3
    exit 0
fi

# 2. Check if a local .venv exists and has dependencies
if [ -d ".venv" ] && .venv/bin/python -c "import customtkinter, faster_whisper" 2>/dev/null; then
    run_app .venv/bin/python
    exit 0
fi

# 3. First-time setup: install dependencies
echo "[INFO] Dependencies not found. Setting up environment..."

# Try installing directly or via automatic virtual environment
if python3 -m pip install -r requirements.txt 2>/dev/null; then
    run_app python3
    exit 0
else
    # Handle modern Linux (PEP 668 externally-managed-environment) with a local .venv
    echo "[INFO] Creating local virtual environment in .venv..."
    if ! python3 -m venv .venv 2>/dev/null; then
        echo "[ERROR] Failed to create virtual environment."
        echo "Please install python3-venv (e.g., sudo apt install python3-venv python3-tk ffmpeg)"
        exit 1
    fi
    .venv/bin/pip install --upgrade pip --quiet
    .venv/bin/pip install -r requirements.txt
    run_app .venv/bin/python
    exit 0
fi
