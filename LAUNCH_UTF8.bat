@echo off
REM UTF-8 Console Launch Script for Crypto Trading Bot
REM Handles emoji characters properly

echo Setting UTF-8 encoding...
chcp 65001 >nul

echo Setting Python encoding environment...
set PYTHONIOENCODING=utf-8
set PYTHONLEGACYWINDOWSFSENCODING=0

echo.
echo ======================================================================
echo     🚀 CRYPTO TRADING BOT - UTF-8 LAUNCHER
echo     🔧 Starting with proper emoji character support
echo ======================================================================
echo.

cd /d "%~dp0"

REM Start the complete application
python start_complete_app.py

pause
