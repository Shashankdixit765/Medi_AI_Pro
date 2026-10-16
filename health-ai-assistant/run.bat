@echo off
title MediAI Pro - AI Healthcare Diagnosis Assistant [Created by Shashank Dixit]
color 0b
echo =========================================================================
echo       MediAI Pro - AI-Powered Healthcare Diagnosis Assistant
echo                  Created by Shashank Dixit
echo =========================================================================
echo.
echo [*] Starting FastAPI Backend on http://127.0.0.1:8000 ...
echo [*] Press Ctrl+C anytime to stop the server.
echo.

python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload

pause
