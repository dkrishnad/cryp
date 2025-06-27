#!/usr/bin/env python3
"""
Quick Start Test
===============
Tests if the server can at least start without hanging
"""

import sys
import os
import time
import subprocess

# Change to backend directory
backend_dir = r"c:\Users\Hari\Desktop\Crypto bot\backend"
os.chdir(backend_dir)

print("🔍 Testing Server Startup...")

try:
    # Try to start main.py briefly
    print("Starting server process...")
    process = subprocess.Popen(
        [sys.executable, "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=backend_dir
    )
    
    # Wait 10 seconds to see if it starts
    time.sleep(10)
    
    if process.poll() is None:
        print("✅ SUCCESS: Server is running!")
        print("Terminating test process...")
        process.terminate()
        process.wait()
    else:
        # Process died, check errors
        stdout, stderr = process.communicate()
        print("❌ Server failed to start")
        print("STDOUT:", stdout[-500:] if stdout else "None")
        print("STDERR:", stderr[-500:] if stderr else "None")
        
except Exception as e:
    print(f"❌ Test failed: {e}")

print("Test complete!")
