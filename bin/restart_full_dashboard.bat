@echo off
chcp 65001 >nul
echo.
echo ===============================================
echo 🚀 RESTARTING WITH FULL-FEATURED DASHBOARD 🚀
echo ===============================================
echo.

cd /d "c:\Users\Hari\Desktop\Crypto bot"

echo [INFO] 🛑 Stopping any existing services...
taskkill /F /IM python.exe >nul 2>&1

echo [INFO] ⏳ Waiting for cleanup...
timeout /t 3 /nobreak >nul

echo [INFO] 🚀 Starting backend...
start "Crypto Bot Backend" cmd /c "chcp 65001 && cd /d backend && python -m uvicorn main:app --host 127.0.0.1 --port 8001"

echo [INFO] ⏳ Waiting for backend...
timeout /t 8 /nobreak >nul

echo [INFO] 💎 Starting FULL-FEATURED dashboard with ALL tabs...
start "Crypto Bot Dashboard - Full Features" cmd /c "chcp 65001 && cd /d dashboard && python app.py"

echo [INFO] ⏳ Waiting for dashboard...
timeout /t 8 /nobreak >nul

echo [INFO] 🌐 Opening browser...
start http://localhost:8050

echo.
echo ===============================================
echo 🎉 FULL-FEATURED DASHBOARD SHOULD BE READY! 🎉
echo 💎 All tabs and features enabled
echo 📊 Dashboard: http://localhost:8050
echo 🔧 Backend: http://localhost:8001
echo ===============================================
echo.
echo Press any key to exit...
pause >nul
