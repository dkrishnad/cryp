#!/usr/bin/env python3
"""
COMPLETE CRYPTO BOT LAUNCHER
Starts both backend API and dashboard UI
"""
import subprocess
import webbrowser
import time
import sys
import os
import threading
import requests

def check_server_health(url, max_attempts=10):
    """Check if server is healthy"""
    for i in range(max_attempts):
        try:
            response = requests.get(f"{url}/health", timeout=2)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False

def start_backend():
    """Start the backend API server"""
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    os.chdir(backend_dir)
    
    print("🔧 Starting FastAPI Backend Server...")
    print(f"📁 Backend directory: {os.getcwd()}")
    
    # Try main.py first with fallback to working version
    backend_file = "main.py"
    if not os.path.exists(backend_file):
        backend_file = "main_working.py"
        print("⚠️  main.py not found, using main_working.py")
    else:
        print("🔧 Using main.py (enhanced version)")
    
    # Start the backend server with better error capture
    backend_process = subprocess.Popen([
        sys.executable, backend_file
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    return backend_process

def start_dashboard():
    """Start the dashboard UI"""
    dashboard_dir = os.path.join(os.path.dirname(__file__), "dashboard")
    os.chdir(dashboard_dir)
    
    print("📊 Starting Dashboard UI...")
    print(f"📁 Dashboard directory: {os.getcwd()}")
    
    # Start the dashboard
    dashboard_process = subprocess.Popen([
        sys.executable, "app.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    return dashboard_process

def main():
    print("🚀 CRYPTO BOT COMPLETE LAUNCHER")
    print("=" * 50)
    
    try:
        # Start backend in a separate thread
        print("1. Starting Backend API Server...")
        backend_process = start_backend()
        
        # Wait for backend to be ready
        print("⏳ Waiting for backend to start...")
        if check_server_health("http://localhost:8000"):
            print("✅ Backend API is running!")
        else:
            print("⚠️  Backend might be starting slowly...")
        
        # Start dashboard
        print("\n2. Starting Dashboard UI...")
        dashboard_process = start_dashboard()
        
        # Wait for dashboard to start
        print("⏳ Waiting for dashboard to start...")
        time.sleep(5)
        
        if check_server_health("http://localhost:8050"):
            print("✅ Dashboard UI is running!")
        else:
            print("⚠️  Dashboard might be starting slowly...")
        
        # Open browser
        print("\n🌐 Opening browser...")
        time.sleep(2)
        
        # Open both interfaces
        webbrowser.open("http://localhost:8050")  # Dashboard
        webbrowser.open("http://localhost:8000/docs")  # API docs
        
        print("\n🎉 CRYPTO BOT IS RUNNING!")
        print("=" * 50)
        print("📊 Dashboard UI:     http://localhost:8050")
        print("🔗 Backend API:      http://localhost:8000")
        print("📚 API Docs:         http://localhost:8000/docs")
        print("❤️  Health Check:    http://localhost:8000/health")
        print("=" * 50)
        print("💡 Press Ctrl+C to stop both services")
        
        # Keep running until user stops
        try:
            while True:
                # Check if processes are still running
                backend_poll = backend_process.poll()
                dashboard_poll = dashboard_process.poll()
                
                if backend_poll is not None:
                    print(f"⚠️  Backend process stopped with exit code: {backend_poll}")
                    # Try to get error output
                    try:
                        stdout, stderr = backend_process.communicate(timeout=1)
                        if stdout:
                            print(f"📜 Backend stdout: {stdout}")
                        if stderr:
                            print(f"📜 Backend stderr: {stderr}")
                    except:
                        pass
                    break
                    
                if dashboard_poll is not None:
                    print(f"⚠️  Dashboard process stopped with exit code: {dashboard_poll}")
                    break
                    
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping Crypto Bot...")
            
        # Clean shutdown
        print("🔄 Terminating processes...")
        backend_process.terminate()
        dashboard_process.terminate()
        
        # Wait for clean shutdown
        try:
            backend_process.wait(timeout=5)
            dashboard_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("🔧 Force killing processes...")
            backend_process.kill()
            dashboard_process.kill()
            
        print("✅ Crypto Bot stopped successfully!")
        
    except Exception as e:
        print(f"❌ Error starting crypto bot: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
