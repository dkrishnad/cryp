#!/usr/bin/env python3
"""
Start Backend Server with Error Handling
"""
import sys
import os
import subprocess
import time

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
    safe_print("🚀 Starting Backend Server...")
    safe_print("=" * 50)
    
    backend_dir = os.path.join(os.path.dirname(__file__), 'backendtest')
    backend_script = os.path.join(backend_dir, 'app.py')
    
    if not os.path.exists(backend_script):
        safe_print(f"❌ Backend script not found: {backend_script}")
        return False
    
    safe_print(f"📂 Backend directory: {backend_dir}")
    safe_print(f"📄 Backend script: {backend_script}")
    
    try:
        # Start backend process
        safe_print("🔧 Starting backend process...")
        process = subprocess.Popen(
            [sys.executable, 'app.py'],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        safe_print(f"✅ Backend process started (PID: {process.pid})")
        safe_print("📊 Backend output:")
        safe_print("-" * 30)
        
        # Show initial output
        try:
            for i in range(10):  # Show first 10 lines of output
                line = process.stdout.readline()
                if line:
                    safe_print(f"   {line.strip()}")
                else:
                    break
                time.sleep(0.1)
        except:
            pass
        
        safe_print("-" * 30)
        safe_print("🌐 Backend should be running on http://localhost:5000")
        safe_print("💡 Keep this terminal open and start the dashboard in another terminal")
        
        # Keep the process running
        try:
            process.wait()
        except KeyboardInterrupt:
            safe_print("\n🛑 Stopping backend...")
            process.terminate()
            safe_print("✅ Backend stopped")
        
        return True
        
    except Exception as e:
        safe_print(f"❌ Failed to start backend: {e}")
        return False

if __name__ == "__main__":
    start_backend()
