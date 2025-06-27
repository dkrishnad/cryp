#!/usr/bin/env python3
"""
Direct server startup test with uvicorn
"""
import sys
import os
import subprocess
import time

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')

print("🚀 Testing direct server startup with uvicorn...")
print(f"📂 Backend directory: {backend_dir}")

# Change to backend directory
os.chdir(backend_dir)

# Use basic uvicorn command
cmd = [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--no-access-log"]

print(f"🔧 Running command: {' '.join(cmd)}")
print("⏱️  Starting server (will test for 10 seconds)...")

try:
    # Start the server
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=backend_dir
    )
    
    # Give it some time to start
    time.sleep(5)
    
    # Check if it's still running
    poll_result = process.poll()
    
    if poll_result is None:
        print("✅ Server appears to be running!")
        
        # Test a simple request
        try:
            import requests
            response = requests.get("http://127.0.0.1:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Health endpoint responded successfully!")
                print(f"📊 Response: {response.json()}")
            else:
                print(f"⚠️  Health endpoint returned status {response.status_code}")
        except Exception as e:
            print(f"⚠️  Could not test health endpoint: {e}")
        
        # Terminate the server
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        
        print("🎉 Server startup test successful!")
        
    else:
        print(f"❌ Server exited with code: {poll_result}")
        stdout, stderr = process.communicate()
        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")
        
except Exception as e:
    print(f"❌ Server startup failed: {e}")
    
    try:
        process.terminate()
    except:
        pass
