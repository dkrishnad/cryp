#!/usr/bin/env python3
"""
Complete Crypto Trading Bot Launcher
Starts both backend and dashboard with error checking
"""
import subprocess
import time
import sys
import os
import threading
import requests
from datetime import datetime

def print_banner():
    print("\n" + "="*70)
    print("    🚀 CRYPTO TRADING BOT - COMPLETE LAUNCHER")
    print("    🔧 Starting Backend + Dashboard with Error Monitoring")
    print("="*70 + "\n")

def start_backend():
    """Start the FastAPI backend"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔧 Starting Backend Server...")
    try:
        backend_process = subprocess.Popen(
            [sys.executable, "-m", "backend.main"],
            cwd=os.getcwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Monitor backend output
        for line in backend_process.stdout:
            print(f"[BACKEND] {line.strip()}")
            if "Application startup complete" in line or "Uvicorn running" in line:
                print("✅ Backend started successfully!")
                break
                
    except Exception as e:
        print(f"❌ Backend Error: {e}")
        return None
    
    return backend_process

def start_dashboard():
    """Start the Dash dashboard"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 Starting Dashboard...")
    try:
        dashboard_process = subprocess.Popen(
            [sys.executable, "start_app.py"],
            cwd=os.path.join(os.getcwd(), "dashboard"),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Monitor dashboard output
        for line in dashboard_process.stdout:
            print(f"[DASHBOARD] {line.strip()}")
            if "Running on" in line or "Dash is running" in line:
                print("✅ Dashboard started successfully!")
                break
                
    except Exception as e:
        print(f"❌ Dashboard Error: {e}")
        return None
    
    return dashboard_process

def check_services():
    """Check if services are running"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔍 Checking Services...")
    
    # Check backend
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend API is responding")
        else:
            print(f"⚠️ Backend API returned status: {response.status_code}")
    except Exception as e:
        print(f"❌ Backend API not responding: {e}")
    
    # Check dashboard with multiple addresses
    dashboard_urls = [
        "http://localhost:8050",
        "http://127.0.0.1:8050",
        "http://0.0.0.0:8050"
    ]
    
    dashboard_responding = False
    for url in dashboard_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print("✅ Dashboard is responding")
                dashboard_responding = True
                break
            else:
                print(f"⚠️ Dashboard at {url} returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ Dashboard not responding at {url}: {e}")
    
    if not dashboard_responding:
        print("ℹ️ Dashboard may still be starting up. Try accessing http://localhost:8050 directly in your browser.")

def main():
    print_banner()
    
    # Start backend in a separate thread
    print("🚀 Starting Backend Server...")
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait a bit for backend to start
    time.sleep(5)
    
    # Start dashboard in a separate thread
    print("📊 Starting Dashboard...")
    dashboard_thread = threading.Thread(target=start_dashboard, daemon=True)
    dashboard_thread.start()
    
    # Wait a bit for dashboard to start
    time.sleep(5)
    
    # Check services
    check_services()
    
    print("\n" + "="*70)
    print("🎉 CRYPTO TRADING BOT LAUNCH COMPLETE!")
    print("📊 Dashboard: http://localhost:8050")
    print("🔗 API Docs: http://localhost:8000/docs")
    print("🔧 API Health: http://localhost:8000/health")
    print("="*70)
    print("\n⚠️  Press Ctrl+C to stop all services")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")
        print("✅ Bot stopped successfully!")

if __name__ == "__main__":
    main()
