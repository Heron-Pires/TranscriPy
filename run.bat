@echo off
cd /d "%~dp0"

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not found in PATH.
    echo Please install Python from https://www.python.org/downloads/ and check "Add Python to PATH".
    pause
    exit /b 1
)

:: Try running the app directly
python transcriPy.py >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] First time setup: Installing required libraries...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    echo.
    echo [INFO] Starting TranscriPy...
    python transcriPy.py
)
