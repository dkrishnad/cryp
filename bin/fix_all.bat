@echo off
echo ================================================================
echo 🔧 CRYPTO BOT COMPLETE FIX AND TEST SUITE
echo ================================================================
echo.

REM Step 1: Stop all processes
echo 🛑 Step 1: Stopping all existing processes...
taskkill /f /im python.exe 2>nul
taskkill /f /im uvicorn.exe 2>nul
timeout /t 3 /nobreak >nul

REM Step 2: Install dependencies
echo.
echo 📦 Step 2: Installing/checking dependencies...
python install_deps.py

REM Step 3: Run diagnostic
echo.
echo 🔍 Step 3: Running diagnostic...
python diagnose.py

REM Step 4: Test minimal backend
echo.
echo 🔧 Step 4: Testing minimal backend...
echo Starting test backend for 10 seconds...
start /B python backend\test_main.py
timeout /t 10 /nobreak >nul
taskkill /f /im python.exe 2>nul

REM Step 5: Test minimal dashboard
echo.
echo 🎨 Step 5: Testing minimal dashboard...
echo Starting test dashboard for 10 seconds...
start /B python dashboard\test_dashboard_minimal.py
timeout /t 10 /nobreak >nul
taskkill /f /im python.exe 2>nul

REM Step 6: Try the fixed launcher
echo.
echo 🚀 Step 6: Starting the complete fixed bot...
python launch_fixed.py

echo.
echo ================================================================
echo 🎯 Fix complete! Check the output above for any remaining issues.
echo ================================================================
pause
