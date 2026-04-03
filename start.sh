#!/usr/bin/env bash
# ============================================
#  PromptMaster Pro - AI Image Prompt Manager
# ============================================

set -e

echo "============================================"
echo "  PromptMaster Pro - AI Image Prompt Manager"
echo "============================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed or not in PATH."
    echo "Please install Python 3.10+ from https://www.python.org/downloads/"
    exit 1
fi

PYTHON=python3

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "[INFO] Creating virtual environment..."
    $PYTHON -m venv venv
    echo "[OK] Virtual environment created."
fi

# Activate virtual environment
echo "[INFO] Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "[INFO] Installing dependencies..."
pip install -r requirements.txt --quiet
echo "[OK] Dependencies installed."

# Launch application
echo ""
echo "[INFO] Starting PromptMaster Pro..."
echo "[INFO] Open your browser at http://localhost:8080"
echo "[INFO] Press Ctrl+C to stop the server."
echo ""
$PYTHON main.py
