# PowerShell Launcher for Crypto Trading Bot
# Enhanced Windows support with proper UTF-8 handling

# Set UTF-8 encoding for PowerShell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [console]::InputEncoding = [console]::OutputEncoding = New-Object System.Text.UTF8Encoding

# Set environment variables for Python UTF-8 support
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONLEGACYWINDOWSFSENCODING = "0"

function Write-Status {
    param($Message)
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] $Message" -ForegroundColor Green
}

function Write-Error-Status {
    param($Message)
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] $Message" -ForegroundColor Red
}

function Test-Port {
    param($Port)
    try {
        $connection = Test-NetConnection -ComputerName "localhost" -Port $Port -WarningAction SilentlyContinue
        return $connection.TcpTestSucceeded
    }
    catch {
        return $false
    }
}

# Main script
Write-Host ""
Write-Host "=============================================================="
Write-Host "    🚀 CRYPTO TRADING BOT - POWERSHELL LAUNCHER 🚀"
Write-Host "    📊 Full UTF-8 Emoji Support on Windows 📊"
Write-Host "=============================================================="
Write-Host ""

# Change to bot directory
$BotDir = "c:\Users\Hari\Desktop\Crypto bot"
if (Test-Path $BotDir) {
    Set-Location $BotDir
    Write-Status "📁 Working in: $BotDir"
} else {
    Write-Error-Status "❌ Bot directory not found: $BotDir"
    exit 1
}

# Start Backend
Write-Status "🔧 Starting backend server..."

if (Test-Port 8001) {
    Write-Status "✅ Backend already running on port 8001"
} else {
    $BackendPath = Join-Path $BotDir "backend"
    if (Test-Path $BackendPath) {
        Write-Status "⚡ Launching backend with uvicorn..."
        
        # Start backend in new window with UTF-8 support
        $BackendCmd = "python -m uvicorn main:app --host 127.0.0.1 --port 8001"
        Start-Process -FilePath "cmd.exe" -ArgumentList "/c", "chcp 65001 && cd `"$BackendPath`" && $BackendCmd" -WindowStyle Normal
        
        # Wait for backend to start
        Write-Status "⏳ Waiting for backend to start..."
        $attempts = 0
        while (-not (Test-Port 8001) -and $attempts -lt 30) {
            Start-Sleep 2
            $attempts++
            Write-Status "⏳ Waiting... ($attempts/30)"
        }
        
        if (Test-Port 8001) {
            Write-Status "✅ Backend started successfully!"
        } else {
            Write-Error-Status "❌ Backend failed to start after 60 seconds"
            exit 1
        }
    } else {
        Write-Error-Status "❌ Backend directory not found: $BackendPath"
        exit 1
    }
}

# Start Dashboard
Write-Status "🎨 Starting beautiful dashboard..."

if (Test-Port 8050) {
    Write-Status "✅ Dashboard already running on port 8050"
} else {
    $DashboardPath = Join-Path $BotDir "dashboard"
    if (Test-Path $DashboardPath) {
        $DashboardFile = Join-Path $DashboardPath "start_beautiful.py"
        
        if (Test-Path $DashboardFile) {
            Write-Status "💎 Launching beautiful emoji dashboard..."
            
            # Start dashboard in new window with UTF-8 support
            $DashboardCmd = "python -u start_beautiful.py"
            Start-Process -FilePath "cmd.exe" -ArgumentList "/c", "chcp 65001 && cd `"$DashboardPath`" && $DashboardCmd" -WindowStyle Normal
            
            # Wait for dashboard to start
            Write-Status "⏳ Waiting for dashboard to start..."
            $attempts = 0
            while (-not (Test-Port 8050) -and $attempts -lt 45) {
                Start-Sleep 2
                $attempts++
                Write-Status "⏳ Waiting... ($attempts/45)"
            }
            
            if (Test-Port 8050) {
                Write-Status "🎉 Beautiful dashboard started successfully!"
            } else {
                Write-Error-Status "❌ Dashboard failed to start after 90 seconds"
                exit 1
            }
        } else {
            Write-Error-Status "❌ start_beautiful.py not found in dashboard directory"
            exit 1
        }
    } else {
        Write-Error-Status "❌ Dashboard directory not found: $DashboardPath"
        exit 1
    }
}

# Check data collection
Write-Status "🎯 Checking data collection status..."
Start-Sleep 3

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8001/ml/data_collection/stats" -TimeoutSec 5
    if ($response.status -eq "success") {
        Write-Status "🎯 Data collection is running automatically!"
    }
} catch {
    Write-Status "⚠️ Data collection status unknown"
}

# Final verification
Write-Status "🔍 Final system verification..."
$backendOk = Test-Port 8001
$dashboardOk = Test-Port 8050

if ($backendOk -and $dashboardOk) {
    Write-Host ""
    Write-Host "=============================================================="
    Write-Host "    🎉 CRYPTO TRADING BOT READY! 🎉"
    Write-Host ""
    Write-Host "    🌐 Dashboard:  http://localhost:8050"
    Write-Host "    🔧 Backend:    http://localhost:8001"
    Write-Host "    📚 API Docs:   http://localhost:8001/docs"
    Write-Host ""
    Write-Host "    ✨ Features: AI/ML Trading + Auto Data Collection"
    Write-Host "    💎 Beautiful Emoji-Rich Interface"
    Write-Host "    🎯 PowerShell UTF-8 Support"
    Write-Host "=============================================================="
    Write-Host ""
    
    # Open browser
    Write-Status "🌐 Opening browser to dashboard..."
    Start-Process "http://localhost:8050"
    
    Write-Status "🚀 All systems operational! Both services are running in separate windows."
    Write-Status "🛑 Close this window or press Ctrl+C to exit launcher (services will continue)"
    
    # Keep script running
    try {
        while ($true) {
            Start-Sleep 60
            # Quick health check
            if (-not (Test-Port 8001) -or -not (Test-Port 8050)) {
                Write-Status "⚠️ WARNING: Service health check failed"
            }
        }
    }
    catch {
        Write-Status "👋 Launcher stopped. Services continue running in their windows."
    }
} else {
    Write-Error-Status "❌ FAILED: System health check failed"
    Write-Error-Status "Backend OK: $backendOk, Dashboard OK: $dashboardOk"
    exit 1
}
