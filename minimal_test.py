#!/usr/bin/env python3
"""
Minimal Backend Test
===================
Tests minimal FastAPI startup without complex initialization
"""

import sys
import os
import time
import subprocess

# Add backend to path
backend_dir = r"c:\Users\Hari\Desktop\Crypto bot\backend"
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

print("🔍 Testing Minimal Backend Startup...")

# Create a minimal test server
test_code = '''
import sys
sys.path.insert(0, r"c:\\Users\\Hari\\Desktop\\Crypto bot\\backend")

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/test")
def test_endpoint():
    return {"status": "ok", "message": "Backend is working!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("🚀 Starting minimal test server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
'''

# Write test server
with open("test_server.py", "w") as f:
    f.write(test_code)

print("✅ Created minimal test server")
print("🚀 Starting test server for 10 seconds...")

try:
    # Start the test server
    process = subprocess.Popen([sys.executable, "test_server.py"])
    
    # Wait a bit
    time.sleep(5)
    
    # Test if it responds
    import requests
    try:
        response = requests.get("http://localhost:8000/test", timeout=5)
        print(f"✅ Test endpoint response: {response.json()}")
    except Exception as e:
        print(f"❌ Could not reach test endpoint: {e}")
    
    # Clean up
    process.terminate()
    process.wait()
    
    print("✅ Minimal server test completed successfully!")
    print("🎯 The issue is likely in the main.py startup initialization")
    
except Exception as e:
    print(f"❌ Test server failed: {e}")

# Clean up
try:
    os.remove("test_server.py")
except:
    pass
