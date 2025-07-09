@echo off
echo ============================================================
echo   CRYPTO BOT DASHBOARD ONLY
echo ============================================================
echo.
echo Starting Dashboard Server...
echo.
echo Dashboard:    http://localhost:8050
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

cd dashboard
python start_dashboard.py

pause
