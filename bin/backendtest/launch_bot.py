#!/usr/bin/env python3
"""
Crypto Trading Bot Launcher
============================
This script starts the FastAPI backend server for the crypto trading bot.
Includes automatic port detection and conflict resolution.
"""

import os
import sys
import subprocess
import signal
import time
import socket
from contextlib import closing

def find_free_port(start_port=8000, max_attempts=10):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                sock.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def kill_process_on_port(port):
    """Kill any process using the specified port"""
    try:
        # Find process using the port
        result = subprocess.run(f'netstat -ano | findstr :{port}', 
                              shell=True, capture_output=True, text=True)
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        pid = parts[-1]
                        print(f"� Killing process {pid} on port {port}")
                        subprocess.run(f'taskkill /F /PID {pid}', shell=True)
                        time.sleep(2)
                        return True
    except Exception as e:
        print(f"⚠️ Could not kill process on port {port}: {e}")
    return False

def main():
    print("🚀 Starting Crypto Trading Bot Backend Server...")
    print("=" * 60)
    
    # Change to backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    
    # Try to find a free port
    port = find_free_port(8000)
    
    if port is None:
        print("🔄 Port 8000-8009 are all busy. Trying to free port 8000...")
        if kill_process_on_port(8000):
            port = 8000
        else:
            port = find_free_port(8010, 20)
    
    if port is None:
        print("❌ Could not find a free port. Please close other applications using ports 8000-8030")
        return 1
    
    print("📊 Dashboard will be available at: http://localhost:8050")
    print(f"🔗 API Documentation: http://localhost:{port}/docs")
    print(f"🌐 Backend API: http://localhost:{port}")
    print("=" * 60)
    
    try:
        # Import and start the FastAPI app
        import uvicorn
        import main
        
        print("✅ All modules imported successfully")
        print(f"🔄 Starting FastAPI server on port {port}...")
        
        # Start the server
        uvicorn.run(
            "main:app", 
            host="0.0.0.0", 
            port=port,
            reload=False,
            log_level="info",
            access_log=True
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except OSError as e:
        if "Address already in use" in str(e) or "10048" in str(e):
            print(f"❌ Port {port} is still in use. Please restart your computer.")
        else:
            print(f"❌ Server error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Server error: {e}")
        print("💡 Try running: pip install uvicorn[standard]")
        print("💡 Or run directly: python main.py")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
