#!/bin/bash

if [ ! -d ".venv" ]; then
    echo "[Setup] Creating Python 3.12 Virtual Environment (.venv)..."
    python3.12 -m venv .venv
    source .venv/bin/activate
    echo "[Setup] Installing dependencies..."
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

echo "[Run] Starting Gemini App..."
python main.py
