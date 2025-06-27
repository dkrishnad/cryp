# Crypto Trading Bot PowerShell Launcher
# Run this with: powershell -ExecutionPolicy Bypass -File LAUNCH_BOT.ps1

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "   CRYPTO TRADING BOT LAUNCHER" -ForegroundColor Cyan  
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "Working directory: $ScriptDir" -ForegroundColor Green
Write-Host ""

# Check if launch_bot.py exists
if (Test-Path "launch_bot.py") {
    Write-Host "[OK] launch_bot.py found" -ForegroundColor Green
} else {
    Write-Host "[ERROR] launch_bot.py not found!" -ForegroundColor Red
    Write-Host "Current directory contents:" -ForegroundColor Yellow
    Get-ChildItem | Select-Object Name | Format-Table -HideTableHeaders
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Python installation
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python detected: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found in PATH!" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Starting Crypto Trading Bot..." -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Start the launcher
try {
    python launch_bot.py
    $exitCode = $LASTEXITCODE
    
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Cyan
    
    if ($exitCode -eq 0) {
        Write-Host "[SUCCESS] Bot completed normally (Exit code: $exitCode)" -ForegroundColor Green
    } else {
        Write-Host "[WARNING] Bot exited with code: $exitCode" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[ERROR] Failed to start launcher: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press Enter to exit..."
Read-Host
