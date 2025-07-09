#!/usr/bin/env python3
"""
Simple launcher script to start both backend and frontend servers
"""
import os
import sys
import subprocess
import time
import threading

def start_backend():
    """Start the backend server"""
    print("🚀 Starting backend server...")
    os.chdir("backendtest")
    
    # Use the virtual environment Python
    python_path = r"c:/Users/Hari/Desktop/Testin dub/.venv/Scripts/python.exe"
    
    try:
        result = subprocess.run([python_path, "main.py"], 
                              capture_output=True, text=True, timeout=30)
        print("Backend output:", result.stdout)
        if result.stderr:
            print("Backend errors:", result.stderr)
    except subprocess.TimeoutExpired:
        print("✅ Backend server started (running in background)")
    except Exception as e:
        print(f"❌ Backend server error: {e}")

def start_frontend():
    """Start the frontend server"""
    print("🚀 Starting frontend server...")
    os.chdir("../dashboardtest")
    
    # Use the virtual environment Python
    python_path = r"c:/Users/Hari/Desktop/Testin dub/.venv/Scripts/python.exe"
    
    try:
        result = subprocess.run([python_path, "app.py"], 
                              capture_output=True, text=True, timeout=30)
        print("Frontend output:", result.stdout)
        if result.stderr:
            print("Frontend errors:", result.stderr)
    except subprocess.TimeoutExpired:
        print("✅ Frontend server started (running in background)")
    except Exception as e:
        print(f"❌ Frontend server error: {e}")

def main():
    """Main launcher function"""
    print("🎯 Crypto Trading Bot Launcher")
    print("=" * 40)
    
    original_dir = os.getcwd()
    
    try:
        # Start backend in a separate thread
        backend_thread = threading.Thread(target=start_backend)
        backend_thread.daemon = True
        backend_thread.start()
        
        # Give backend time to start
        time.sleep(5)
        
        # Change back to original directory
        os.chdir(original_dir)
        
        # Start frontend in a separate thread
        frontend_thread = threading.Thread(target=start_frontend)
        frontend_thread.daemon = True
        frontend_thread.start()
        
        print("\n🎉 Both servers are starting...")
        print("📊 Backend: http://localhost:8000")
        print("🎛️  Frontend: http://localhost:8050")
        print("\n⚡ Press Ctrl+C to stop both servers")
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
    except Exception as e:
        print(f"❌ Launcher error: {e}")
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    main()
