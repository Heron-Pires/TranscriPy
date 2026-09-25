@echo off
setlocal
cd /d "%~dp0"
title TranscriPy

REM Determine the best Python command (try 'py -3' first, then 'python')
set "PYTHON_CMD="

py -3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=py -3"
) else (
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON_CMD=python"
    )
)

if "%PYTHON_CMD%"=="" (
    echo [ERROR] Python was not found on your system.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check the option "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM Check if required packages are installed
%PYTHON_CMD% -c "import customtkinter, faster_whisper" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] First-time setup: installing required packages...
    %PYTHON_CMD% -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
)

REM Launch the application
echo [INFO] Starting TranscriPy...
%PYTHON_CMD% transcriPy.py

REM If the app closed with an error, keep the console open
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] TranscriPy closed with an error.
    pause
)
