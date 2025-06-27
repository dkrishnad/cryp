@echo off
cd /d "%~dp0"
echo.
echo ================================================================
echo    🚀 CRYPTO TRADING BOT - COMPLETE LAUNCHER
echo    🔧 Backend API + Dashboard UI + All Features
echo ================================================================
echo.
echo Working directory: %CD%
echo.

REM Kill any existing processes first
echo 🛑 Stopping any existing bot processes...
taskkill /f /im python.exe 2>nul
taskkill /f /im uvicorn.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo 🚀 Starting the complete crypto bot...
python START_CRYPTO_BOT.py

echo.
echo ================================================================
echo If the launcher failed, try the diagnostic:
echo python diagnose.py
echo ================================================================
pause