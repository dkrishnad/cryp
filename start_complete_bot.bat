@echo off
echo ========================================
echo    CRYPTO TRADING BOT LAUNCHER
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/3] Checking for required ports...
netstat -ano | findstr :8000 >nul
if not errorlevel 1 (
    echo WARNING: Port 8000 is already in use. Attempting to free it...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
        taskkill /F /PID %%a >nul 2>&1
    )
    timeout /t 2 >nul
)

netstat -ano | findstr :8050 >nul
if not errorlevel 1 (
    echo WARNING: Port 8050 is already in use. Attempting to free it...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8050') do (
        taskkill /F /PID %%a >nul 2>&1
    )
    timeout /t 2 >nul
)

echo [2/3] Starting Backend Server (Port 8000)...
cd /d "c:\Users\Hari\Desktop\Crypto bot\backend"
start "Backend Server" cmd /c "python main.py & pause"
echo Waiting for backend to start...
timeout /t 5 >nul

echo [3/3] Starting Dashboard (Port 8050)...
cd /d "c:\Users\Hari\Desktop\Crypto bot\dashboard"
start "Dashboard" cmd /c "python app.py & pause"
echo Waiting for dashboard to start...
timeout /t 3 >nul

echo.
echo ========================================
echo    BOT STARTED SUCCESSFULLY!
echo ========================================
echo.
echo Dashboard: http://localhost:8050
echo Backend API: http://localhost:8000/docs
echo.
echo Press any key to open dashboard in browser...
pause >nul

start http://localhost:8050

echo.
echo Both services are now running in separate windows.
echo Close those windows to stop the bot.
pause
