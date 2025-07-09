#!/usr/bin/env python3
"""
Launcher script to start both backend and frontend with proper error handling
"""
import subprocess
import sys
import time
import requests
import os
from threading import Thread

def safe_print(msg):
    """Safe printing function"""
    try:
        print(msg)
        sys.stdout.flush()
    except UnicodeEncodeError:
        print(msg.encode('ascii', 'replace').decode('ascii'))
        sys.stdout.flush()

def start_backend():
    """Start the backend server"""
    safe_print("🔧 Starting backend server...")
    try:
        # Change to backend directory
        backend_dir = os.path.join(os.path.dirname(__file__), 'backendtest')
        backend_script = os.path.join(backend_dir, 'app.py')
        
        # Start backend process
        process = subprocess.Popen(
            [sys.executable, backend_script],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give it time to start
        time.sleep(3)
        
        # Check if backend is running
        try:
            response = requests.get('http://localhost:5000/api/status', timeout=5)
            if response.status_code == 200:
                safe_print("✅ Backend server started successfully")
                return process
            else:
                safe_print(f"❌ Backend returned status {response.status_code}")
                return None
        except Exception as e:
            safe_print(f"❌ Backend connection test failed: {e}")
            return None
            
    except Exception as e:
        safe_print(f"❌ Failed to start backend: {e}")
        return None

def start_dashboard():
    """Start the dashboard with proper error handling"""
    safe_print("🔧 Starting dashboard...")
    try:
        # Change to dashboard directory
        dashboard_dir = os.path.join(os.path.dirname(__file__), 'dashboardtest')
        dashboard_script = os.path.join(dashboard_dir, 'app.py')
        
        # Start dashboard
        subprocess.run([sys.executable, dashboard_script], cwd=dashboard_dir)
        
    except Exception as e:
        safe_print(f"❌ Failed to start dashboard: {e}")

def main():
    """Main launcher function"""
    safe_print("🚀 Starting Crypto Trading Bot...")
    safe_print("=" * 50)
    
    # Start backend first
    backend_process = start_backend()
    
    if backend_process is None:
        safe_print("❌ Backend failed to start. Starting dashboard anyway...")
    
    # Start dashboard (this will block)
    safe_print("🔧 Starting dashboard on http://localhost:8050")
    start_dashboard()

if __name__ == "__main__":
    main()
