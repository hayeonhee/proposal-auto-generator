@echo off
cd /d %~dp0

if not exist ".venv" (
    echo [Setup] Creating Python 3.12 Virtual Environment (.venv)...
    python -m venv .venv
    call .venv\Scripts\activate
    echo [Setup] Installing dependencies...
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate
)

echo [Run] Starting Gemini App...
python main.py
pause
