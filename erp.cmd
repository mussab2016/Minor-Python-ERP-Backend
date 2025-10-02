@echo off
REM Navigate to your project folder if needed
cd /d %~dp0

REM Run Uvicorn server
uvicorn main:app --host 127.0.0.1 --port 8787 --reload --log-level debug

pause
