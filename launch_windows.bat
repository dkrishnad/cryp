@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM Windows Batch Launcher for Crypto Trading Bot
REM UTF-8 Support for Emoji Display

echo.
echo ==============================================================
echo     🚀 CRYPTO TRADING BOT - BATCH LAUNCHER 🚀
echo     📊 Windows UTF-8 Emoji Support 📊  
echo ==============================================================
echo.

REM Set UTF-8 environment variables
set PYTHONIOENCODING=utf-8
set PYTHONLEGACYWINDOWSFSENCODING=0

REM Change to bot directory
cd /d "c:\Users\Hari\Desktop\Crypto bot"
if errorlevel 1 (
    echo ❌ ERROR: Could not change to bot directory
    pause
    exit /b 1
)

echo [INFO] 📁 Working in: %CD%

REM Check if backend is already running
echo [INFO] 🔍 Checking if backend is running...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8001' -TimeoutSec 2 -ErrorAction Stop; exit 0 } catch { exit 1 }" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] ✅ Backend already running
) else (
    echo [INFO] 🔧 Starting backend server...
    if not exist "backend" (
        echo [ERROR] ❌ Backend directory not found
        pause
        exit /b 1
    )
    
    REM Start backend in new window
    start "Crypto Bot Backend" cmd /c "chcp 65001 && cd /d backend && python -m uvicorn main:app --host 127.0.0.1 --port 8001"
    
    echo [INFO] ⏳ Waiting for backend to start...
    timeout /t 5 /nobreak >nul
    
    REM Wait for backend to be ready
    set /a attempts=0
    :wait_backend
    set /a attempts+=1
    if !attempts! gtr 30 (
        echo [ERROR] ❌ Backend failed to start after 60 seconds
        pause
        exit /b 1
    )
    
    powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8001' -TimeoutSec 2 -ErrorAction Stop; exit 0 } catch { exit 1 }" >nul 2>&1
    if %errorlevel% neq 0 (
        echo [INFO] ⏳ Waiting... (!attempts!/30)
        timeout /t 2 /nobreak >nul
        goto wait_backend
    )
    
    echo [INFO] ✅ Backend started successfully!
)

REM Check if dashboard is already running
echo [INFO] 🔍 Checking if dashboard is running...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8050' -TimeoutSec 2 -ErrorAction Stop; exit 0 } catch { exit 1 }" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] ✅ Dashboard already running
) else (
    echo [INFO] 🎨 Starting beautiful dashboard...
    if not exist "dashboard" (
        echo [ERROR] ❌ Dashboard directory not found
        pause
        exit /b 1
    )
    
    if not exist "dashboard\start_beautiful.py" (
        echo [ERROR] ❌ start_beautiful.py not found
        pause
        exit /b 1
    )
    
    REM Start dashboard in new window
    start "Crypto Bot Dashboard" cmd /c "chcp 65001 && cd /d dashboard && python -u start_beautiful.py"
    
    echo [INFO] ⏳ Waiting for dashboard to start...
    timeout /t 5 /nobreak >nul
    
    REM Wait for dashboard to be ready
    set /a attempts=0
    :wait_dashboard
    set /a attempts+=1
    if !attempts! gtr 45 (
        echo [ERROR] ❌ Dashboard failed to start after 90 seconds
        pause
        exit /b 1
    )
    
    powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8050' -TimeoutSec 2 -ErrorAction Stop; exit 0 } catch { exit 1 }" >nul 2>&1
    if %errorlevel% neq 0 (
        echo [INFO] ⏳ Waiting... (!attempts!/45)
        timeout /t 2 /nobreak >nul
        goto wait_dashboard
    )
    
    echo [INFO] 🎉 Beautiful dashboard started successfully!
)

REM Check data collection
echo [INFO] 🎯 Checking data collection...
timeout /t 3 /nobreak >nul

powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:8001/ml/data_collection/stats' -TimeoutSec 5; if ($response.status -eq 'success') { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] 🎯 Data collection is running automatically!
) else (
    echo [INFO] ⚠️ Data collection status unknown
)

REM Final verification
echo [INFO] 🔍 Final system verification...

powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8001' -TimeoutSec 2 -ErrorAction Stop; exit 0 } catch { exit 1 }" >nul 2>&1
set backend_ok=%errorlevel%

powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8050' -TimeoutSec 2 -ErrorAction Stop; exit 0 } catch { exit 1 }" >nul 2>&1
set dashboard_ok=%errorlevel%

if %backend_ok% equ 0 if %dashboard_ok% equ 0 (
    echo.
    echo ==============================================================
    echo     🎉 CRYPTO TRADING BOT READY! 🎉
    echo.
    echo     🌐 Dashboard:  http://localhost:8050
    echo     🔧 Backend:    http://localhost:8001
    echo     📚 API Docs:   http://localhost:8001/docs
    echo.
    echo     ✨ Features: AI/ML Trading + Auto Data Collection
    echo     💎 Beautiful Emoji-Rich Interface  
    echo     🎯 Windows Batch UTF-8 Support
    echo ==============================================================
    echo.
    
    echo [INFO] 🌐 Opening browser to dashboard...
    start http://localhost:8050
    
    echo [INFO] 🚀 All systems operational! Services running in separate windows.
    echo [INFO] 🛑 Press any key to exit launcher (services will continue)
    pause >nul
    
    echo [INFO] 👋 Launcher stopped. Services continue running.
) else (
    echo [ERROR] ❌ FAILED: System health check failed
    echo [ERROR] Backend OK: %backend_ok%, Dashboard OK: %dashboard_ok%
    pause
    exit /b 1
)

endlocal
