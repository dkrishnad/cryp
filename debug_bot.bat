@echo off
echo ================================================================
echo STOPPING ALL PROCESSES AND RESTARTING CLEAN
echo ================================================================
echo.

REM Kill any existing processes
echo Stopping any existing bot processes...
taskkill /f /im python.exe 2>nul
taskkill /f /im uvicorn.exe 2>nul
timeout /t 3 /nobreak >nul

echo.
echo ================================================================
echo RUNNING DIAGNOSTIC
echo ================================================================
python diagnose.py

echo.
echo ================================================================
echo TESTING DASHBOARD DIRECTLY
echo ================================================================
python test_dashboard.py

pause
