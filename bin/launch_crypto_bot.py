#!/usr/bin/env python3
"""
CRYPTO BOT LAUNCHER
Starts backend and opens dashboard
"""
import subprocess
import webbrowser
import time
import sys
import os

def main():
    print("🚀 Starting Crypto Bot...")
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    os.chdir(backend_dir)
    
    print(f"📁 Working directory: {os.getcwd()}")
    
    try:
        # Start the backend server
        print("🔧 Starting FastAPI backend server...")
        server_process = subprocess.Popen([
            sys.executable, "main_working.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a bit for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(3)
        
        # Check if server is running
        print("🌐 Opening browser to dashboard...")
        webbrowser.open("http://localhost:8000/docs")
        
        print("\n✅ Crypto Bot is starting!")
        print("📍 Backend API: http://localhost:8000")
        print("📍 API Documentation: http://localhost:8000/docs")
        print("📍 Health Check: http://localhost:8000/health")
        print("\n💡 To stop the bot, press Ctrl+C")
        
        # Keep the launcher running
        try:
            server_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping Crypto Bot...")
            server_process.terminate()
            
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
