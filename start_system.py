#!/usr/bin/env python3
"""
Complete launch script for the crypto bot system
"""

import sys
import os
import subprocess
import time
import threading
import webbrowser

def launch_backend():
    """Launch the backend API server"""
    try:
        print("🔧 Starting Backend API Server...")
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
        os.chdir(backend_dir)
        result = subprocess.run([sys.executable, 'main.py'], check=False)
        print(f"Backend process ended with code: {result.returncode}")
    except Exception as e:
        print(f"❌ Backend error: {e}")

def launch_dashboard():
    """Launch the dashboard server"""
    try:
        print("🎨 Starting Dashboard Server...")
        dashboard_dir = os.path.join(os.path.dirname(__file__), 'dashboard')
        os.chdir(dashboard_dir)
        result = subprocess.run([sys.executable, 'start_dashboard.py'], check=False)
        print(f"Dashboard process ended with code: {result.returncode}")
    except Exception as e:
        print(f"❌ Dashboard error: {e}")

def check_backend_health():
    """Check if backend is responding"""
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Main launcher function"""
    print("=" * 60)
    print("🚀 CRYPTO BOT SYSTEM LAUNCHER")
    print("=" * 60)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=launch_backend, daemon=True)
    backend_thread.start()
    
    # Wait a bit for backend to start
    print("⏳ Waiting for backend to start...")
    time.sleep(3)
    
    # Check backend health
    for i in range(10):
        if check_backend_health():
            print("✅ Backend is running and healthy!")
            break
        time.sleep(1)
    else:
        print("⚠️  Backend may not be responding, continuing anyway...")
    
    # Start dashboard in a separate thread
    dashboard_thread = threading.Thread(target=launch_dashboard, daemon=True)
    dashboard_thread.start()
    
    # Wait a bit for dashboard to start
    print("⏳ Waiting for dashboard to start...")
    time.sleep(3)
    
    print("\n" + "=" * 60)
    print("🎉 CRYPTO BOT SYSTEM STATUS")
    print("=" * 60)
    print("📡 Backend API:  http://localhost:8000")
    print("📊 API Docs:     http://localhost:8000/docs")
    print("❤️  Health:      http://localhost:8000/health")
    print("🎨 Dashboard:    http://localhost:8050")
    print("=" * 60)
    
    # Open browser
    try:
        print("🌐 Opening dashboard in browser...")
        webbrowser.open("http://localhost:8050")
    except:
        print("⚠️  Could not open browser automatically")
    
    print("\n📝 Press Ctrl+C to stop all services")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down crypto bot system...")
        sys.exit(0)

if __name__ == "__main__":
    main()
