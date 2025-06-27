# Crypto Trading Bot - Windows Startup Script
# PowerShell script to start both backend and dashboard services

Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "🤖 CRYPTO TRADING BOT - SYSTEM STARTUP" -ForegroundColor Green
Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""

# Function to start backend
function Start-Backend {
    Write-Host "🚀 Starting Backend API Server..." -ForegroundColor Yellow
    $backend = Start-Process python -ArgumentList "backend/main.py" -PassThru -NoNewWindow
    return $backend
}

# Function to start dashboard
function Start-Dashboard {
    Write-Host "🚀 Starting Dashboard Web Server..." -ForegroundColor Yellow
    $dashboard = Start-Process python -ArgumentList "dashboard/app.py" -PassThru -NoNewWindow
    return $dashboard
}

try {
    # Start backend first
    $backendProcess = Start-Backend
    Write-Host "⏳ Waiting for backend to initialize..." -ForegroundColor Blue
    Start-Sleep -Seconds 3
    
    # Start dashboard
    $dashboardProcess = Start-Dashboard
    Write-Host "⏳ Waiting for dashboard to initialize..." -ForegroundColor Blue
    Start-Sleep -Seconds 3
    
    Write-Host ""
    Write-Host "✅ System startup complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📡 Backend API: http://localhost:8001" -ForegroundColor Cyan
    Write-Host "🌐 Dashboard:   http://localhost:8050" -ForegroundColor Cyan
    Write-Host "📚 API Docs:    http://localhost:8001/docs" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Press Ctrl+C to stop both services..." -ForegroundColor Yellow
    Write-Host ""
    
    # Keep monitoring processes
    while ($true) {
        if ($backendProcess.HasExited) {
            Write-Host "❌ Backend process stopped!" -ForegroundColor Red
            break
        }
        if ($dashboardProcess.HasExited) {
            Write-Host "❌ Dashboard process stopped!" -ForegroundColor Red
            break
        }
        Start-Sleep -Seconds 1
    }
}
catch {
    Write-Host "🛑 Shutting down services..." -ForegroundColor Red
    if ($backendProcess -and !$backendProcess.HasExited) {
        $backendProcess.Kill()
    }
    if ($dashboardProcess -and !$dashboardProcess.HasExited) {
        $dashboardProcess.Kill()
    }
    Write-Host "✅ All services stopped." -ForegroundColor Green
}
