@echo off
cd /d "%~dp0"
echo.
echo ================================================================
echo    🚀 CRYPTO TRADING BOT - COMPLETE LAUNCHER
echo    🔧 Starting Backend + Dashboard
echo ================================================================
echo.

echo 🛑 Stopping any existing processes...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo 🚀 Starting Backend Server...
start "Backend" cmd /k "python -m backend.main"

echo ⏳ Waiting for backend to start...
timeout /t 8 /nobreak >nul

echo.
echo 📊 Starting Dashboard...
start "Dashboard" cmd /k "cd dashboard && python start_app.py"

echo.
echo ================================================================
echo 🎉 CRYPTO TRADING BOT LAUNCHED!
echo 📊 Dashboard: http://localhost:8050
echo 🔗 API Docs: http://localhost:8000/docs
echo 🔧 API Health: http://localhost:8000/health
echo ================================================================
echo.
echo ⚠️  Both backend and dashboard are running in separate windows
echo 🛑 Close both windows to stop the bot
pause
