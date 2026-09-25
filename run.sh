#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed."
    echo "Please install it using your package manager (e.g. sudo apt install python3 python3-pip python3-tk)."
    exit 1
fi

# Try running the app directly, install requirements if it fails
if ! python3 transcriPy.py 2>/dev/null; then
    echo "[INFO] First time setup: Installing required libraries..."
    python3 -m pip install -r requirements.txt --quiet
    echo "[INFO] Starting TranscriPy..."
    python3 transcriPy.py
fi
