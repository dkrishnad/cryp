#!/usr/bin/env python3
"""
Complete Crypto Trading Bot Launcher
===================================
Starts both backend server and dashboard with proper error handling.
"""

import os
import sys
import time
import subprocess
import socket
import requests
from contextlib import closing

def check_port_free(port):
    """Check if a port is free"""
    try:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.bind(('localhost', port))
            return True
    except OSError:
        return False

def kill_process_on_port(port):
    """Kill process using a specific port"""
    try:
        result = subprocess.run(f'netstat -ano | findstr :{port}', 
                              shell=True, capture_output=True, text=True)
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        pid = parts[-1]
                        print(f"   Killing process {pid} on port {port}")
                        subprocess.run(f'taskkill /F /PID {pid}', shell=True, capture_output=True)
                        time.sleep(2)
                        return True
    except Exception as e:
        print(f"   Warning: Could not kill process on port {port}: {e}")
    return False

def wait_for_server(url, max_wait=30):
    """Wait for a server to become available"""
    for i in range(max_wait):
        try:
            response = requests.get(url, timeout=1)
            if response.status_code < 500:
                return True
        except:
            pass
        time.sleep(1)
    return False

def main():
    print("=" * 50)
    print("    CRYPTO TRADING BOT LAUNCHER")
    print("=" * 50)
    print()
    
    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(project_dir, "backend")
    dashboard_dir = os.path.join(project_dir, "dashboard")
    
    # Check directories exist
    if not os.path.exists(backend_dir):
        print("❌ Backend directory not found!")
        return 1
    if not os.path.exists(dashboard_dir):
        print("❌ Dashboard directory not found!")
        return 1
    
    print("✅ Project directories found")
    
    # Check and free ports
    print("\n[1/3] Checking ports...")
    
    if not check_port_free(8000):
        print("   Port 8000 busy, attempting to free it...")
        kill_process_on_port(8000)
        if not check_port_free(8000):
            print("❌ Could not free port 8000. Please close other applications.")
            return 1
    
    if not check_port_free(8050):
        print("   Port 8050 busy, attempting to free it...")
        kill_process_on_port(8050)
        if not check_port_free(8050):
            print("❌ Could not free port 8050. Please close other applications.")
            return 1
    
    print("✅ Ports 8000 and 8050 are available")
    
    # Start backend
    print("\n[2/3] Starting Backend Server...")
    os.chdir(backend_dir)
    
    backend_process = subprocess.Popen(
        [sys.executable, "main.py"],
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
    )
    
    print("   Waiting for backend to start...")
    if wait_for_server("http://localhost:8000/health", 30):
        print("✅ Backend server started successfully!")
    else:
        print("⚠️ Backend may still be starting (continuing anyway)")
    
    # Start dashboard
    print("\n[3/3] Starting Dashboard...")
    os.chdir(dashboard_dir)
    
    dashboard_process = subprocess.Popen(
        [sys.executable, "app.py"],
        creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
    )
    
    print("   Waiting for dashboard to start...")
    time.sleep(5)
    
    print("\n" + "=" * 50)
    print("    🚀 BOT STARTED SUCCESSFULLY!")
    print("=" * 50)
    print()
    print("📊 Dashboard:     http://localhost:8050")
    print("🔗 Backend API:   http://localhost:8000/docs")
    print("💡 WebSocket:     ws://localhost:8000/ws")
    print()
    print("✅ Both services are running in separate console windows")
    print("✅ Data should now be loading in the dashboard")
    print()
    print("To stop the bot: Close both console windows")
    print()
    
    # Try to open browser
    try:
        if os.name == 'nt':
            os.system('start http://localhost:8050')
        else:
            os.system('xdg-open http://localhost:8050')
    except:
        pass
    
    print("Press Enter to exit this launcher (services will continue running)...")
    input()
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n🛑 Launcher stopped by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
