#!/usr/bin/env python3
"""
Simple backend server startup script
"""
import os
import sys
import subprocess

print("Crypto Bot Backend Startup")
print("=" * 40)

# Navigate to backend directory
backend_dir = r"c:\Users\Hari\Desktop\Crypto bot\backend"
os.chdir(backend_dir)
print(f"Working directory: {os.getcwd()}")

# Run the main.py file directly
try:
    print("Starting backend server...")
    result = subprocess.run([sys.executable, "main.py"], 
                          cwd=backend_dir, 
                          capture_output=False, 
                          text=True)
    print(f"Process exited with code: {result.returncode}")
except Exception as e:
    print(f"Error starting server: {e}")

print("Script completed.")
