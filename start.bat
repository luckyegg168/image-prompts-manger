@echo off
title PromptMaster Pro - AI Image Prompt Manager
echo ============================================
echo   PromptMaster Pro - AI Image Prompt Manager
echo ============================================
echo.

:: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Create virtual environment if not exists
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created.
)

:: Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies
echo [INFO] Installing dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo [OK] Dependencies installed.

:: Launch application
echo.
echo [INFO] Starting PromptMaster Pro...
echo [INFO] Open your browser at http://localhost:8080
echo [INFO] Press Ctrl+C to stop the server.
echo.
python main.py

:: Deactivate on exit
call venv\Scripts\deactivate.bat 2>nul
pause
