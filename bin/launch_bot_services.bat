@echo off
echo ==============================================
echo Crypto Trading Bot - Launch Backend & Frontend
echo ==============================================
echo.
echo This will open two terminal windows:
echo 1. Backend Server (Port 8000)
echo 2. Frontend Dashboard (Port 8050)
echo.
echo Please wait while services start...
echo.

start cmd /k "cd /d %~dp0 && start_backend.bat"
timeout /t 5 > nul
start cmd /k "cd /d %~dp0 && start_frontend.bat"

echo.
echo Services are starting in separate windows.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8050
echo.
echo Press any key to exit this window...
pause > nul
