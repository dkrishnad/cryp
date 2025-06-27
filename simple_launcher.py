#!/usr/bin/env python3
"""
🚀 PROFESSIONAL CRYPTO TRADING BOT - ENHANCED LAUNCHER v2.1
Reliable startup with advanced error handling and monitoring
"""

import subprocess
import time
import sys
import os
import requests
import json
from datetime import datetime
import threading
import webbrowser
import signal
import atexit

# Global process tracking
processes = []

def print_status(message, status="INFO"):
    """Enhanced status printing with colors and timestamps"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    status_colors = {
        "INFO": "\033[94m",     # Blue
        "SUCCESS": "\033[92m",  # Green
        "ERROR": "\033[91m",    # Red
        "WARNING": "\033[93m",  # Yellow
        "HEADER": "\033[95m"    # Magenta
    }
    reset_color = "\033[0m"
    icons = {
        "INFO": "ℹ️",
        "SUCCESS": "✅",
        "ERROR": "❌",
        "WARNING": "⚠️",
        "HEADER": "🔥"
    }
    icon = icons.get(status, "•")
    color = status_colors.get(status, "")
    print(f"{color}{timestamp} [{icon} {status}] {message}{reset_color}")

def cleanup_all():
    """Clean up all processes on exit"""
    global processes
    print_status("🧹 Cleaning up processes...", "WARNING")
    
    for proc in processes:
        try:
            if proc and proc.poll() is None:
                proc.terminate()
                time.sleep(2)
                if proc.poll() is None:
                    proc.kill()
                print_status(f"Process {proc.pid} terminated", "INFO")
        except Exception as e:
            print_status(f"Error terminating process: {e}", "WARNING")

def signal_handler(signum, frame):
    """Handle interrupt signals"""
    print_status("\n🛑 Interrupt received, shutting down...", "WARNING")
    cleanup_all()
    sys.exit(0)

# Register cleanup
atexit.register(cleanup_all)
signal.signal(signal.SIGINT, signal_handler)

def check_port_available(port):
    """Check if a port is available"""
    try:
        response = requests.get(f"http://localhost:{port}/health" if port == 8001 else f"http://localhost:{port}", timeout=3)
        return response.status_code == 200
    except:
        return False

def start_backend():
    """Start the backend service"""
    global processes
    
    print_status("🚀 Starting Backend API Server...", "HEADER")
    
    if check_port_available(8001):
        print_status("Backend already running on port 8001", "SUCCESS")
        return True
    
    backend_path = os.path.join(os.getcwd(), "backend")
    if not os.path.exists(backend_path):
        print_status("Backend directory not found", "ERROR")
        return False
    
    try:
        # Start backend with hidden window on Windows
        startup_info = None
        if os.name == 'nt':
            startup_info = subprocess.STARTUPINFO()
            startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startup_info.wShowWindow = subprocess.SW_HIDE
        
        proc = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app",
            "--host", "127.0.0.1", "--port", "8001"
        ], cwd=backend_path, startupinfo=startup_info)
        
        processes.append(proc)
        print_status(f"Backend process started (PID: {proc.pid})", "INFO")
        
        # Wait for backend to be ready
        for i in range(30):
            time.sleep(2)
            if proc.poll() is not None:
                print_status("Backend process died", "ERROR")
                return False
            
            if check_port_available(8001):
                print_status("🎉 Backend API server is ready!", "SUCCESS")
                return True
            
            print_status(f"Waiting for backend... ({i+1}/30)", "INFO")
        
        print_status("Backend startup timeout", "ERROR")
        return False
        
    except Exception as e:
        print_status(f"Error starting backend: {e}", "ERROR")
        return False

def start_dashboard():
    """Start the dashboard service"""
    global processes
    
    print_status("🎨 Starting Dashboard Interface...", "HEADER")
    
    if check_port_available(8050):
        print_status("Dashboard already running on port 8050", "SUCCESS")
        return True
    
    dashboard_path = os.path.join(os.getcwd(), "dashboard")
    if not os.path.exists(dashboard_path):
        print_status("Dashboard directory not found", "ERROR")
        return False
    
    # Find dashboard start file
    start_files = ['start_dashboard.py', 'start_app.py', 'app.py']
    start_file = None
    
    for file in start_files:
        if os.path.exists(os.path.join(dashboard_path, file)):
            start_file = file
            break
    
    if not start_file:
        print_status("No dashboard start file found", "ERROR")
        return False
    
    print_status(f"Using start file: {start_file}", "INFO")
    
    try:
        # Start dashboard with hidden window on Windows
        startup_info = None
        if os.name == 'nt':
            startup_info = subprocess.STARTUPINFO()
            startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startup_info.wShowWindow = subprocess.SW_HIDE
        
        proc = subprocess.Popen([
            sys.executable, start_file
        ], cwd=dashboard_path, startupinfo=startup_info)
        
        processes.append(proc)
        print_status(f"Dashboard process started (PID: {proc.pid})", "INFO")
        
        # Wait for dashboard to be ready
        for i in range(40):
            time.sleep(2)
            if proc.poll() is not None:
                print_status("Dashboard process died", "ERROR")
                return False
            
            if check_port_available(8050):
                print_status("🎉 Dashboard interface is ready!", "SUCCESS")
                return True
            
            print_status(f"Waiting for dashboard... ({i+1}/40)", "INFO")
        
        print_status("Dashboard startup timeout", "ERROR")
        return False
        
    except Exception as e:
        print_status(f"Error starting dashboard: {e}", "ERROR")
        return False

def open_browser():
    """Open browser to dashboard"""
    time.sleep(3)
    try:
        webbrowser.open("http://localhost:8050")
        print_status("🌐 Browser opened to dashboard", "SUCCESS")
    except Exception as e:
        print_status(f"Could not open browser: {e}", "WARNING")

def display_success():
    """Display success information"""
    success_info = """
╔══════════════════════════════════════════════════════════════════╗
║                     🎉 LAUNCH SUCCESSFUL!                        ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  📊 Dashboard:     http://localhost:8050                         ║
║  🔌 Backend API:   http://localhost:8001                         ║
║  📚 API Docs:      http://localhost:8001/docs                    ║
║                                                                  ║
║  🚀 Status: READY FOR PROFESSIONAL TRADING                      ║
║                                                                  ║
║  Press Ctrl+C to stop all services                              ║
╚══════════════════════════════════════════════════════════════════╝
    """
    print(success_info)

def main():
    """Main launcher function"""
    # Print banner
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║              🚀 CRYPTO TRADING BOT LAUNCHER v2.1                ║
║                   Professional-Grade Platform                    ║
╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)
    
    # Set working directory
    bot_dir = r"c:\Users\Hari\Desktop\Crypto bot"
    if os.path.exists(bot_dir):
        os.chdir(bot_dir)
        print_status(f"📁 Working directory: {bot_dir}", "INFO")
    
    # Start services
    print_status("🎯 Initializing services...", "HEADER")
    
    # Start backend
    if not start_backend():
        print_status("❌ Backend startup failed", "ERROR")
        return False
    
    # Start dashboard
    if not start_dashboard():
        print_status("❌ Dashboard startup failed", "ERROR")
        return False
    
    # Success!
    print_status("🚀 ALL SERVICES STARTED SUCCESSFULLY!", "SUCCESS")
    display_success()
    
    # Open browser
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Keep running
    try:
        print_status("🔄 Monitoring services... Press Ctrl+C to stop", "INFO")
        while True:
            time.sleep(30)
            
            # Basic health check
            backend_ok = check_port_available(8001)
            dashboard_ok = check_port_available(8050)
            
            if not backend_ok:
                print_status("⚠️ Backend health check failed", "WARNING")
            if not dashboard_ok:
                print_status("⚠️ Dashboard health check failed", "WARNING")
            
            if not backend_ok or not dashboard_ok:
                print_status("💡 Some services may need attention", "WARNING")
    
    except KeyboardInterrupt:
        print_status("\n🛑 Shutdown requested", "WARNING")
        cleanup_all()
        print_status("👋 All services stopped. Goodbye!", "SUCCESS")
    
    return True

if __name__ == "__main__":
    main()
