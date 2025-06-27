@echo off
echo ============================================================
echo   CRYPTO BOT BACKEND ONLY
echo ============================================================
echo.
echo Starting Backend API Server...
echo.
echo Backend API:  http://localhost:8000
echo API Docs:     http://localhost:8000/docs
echo Health Check: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

cd backend
python main.py

pause
