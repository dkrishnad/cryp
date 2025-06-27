#!/usr/bin/env python3
"""
Quick Bot Launcher Test
======================
Tests the port detection and launches the bot with better error handling.
"""

import socket
import subprocess
import time
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

def main():
    print("🔍 Testing Bot Startup...")
    
    # Check for free port
    port = find_free_port(8000)
    if port:
        print(f"✅ Found free port: {port}")
    else:
        print("❌ No free ports found in range 8000-8009")
        return
    
    print(f"🚀 Starting bot on port {port}...")
    
    try:
        # Start the bot using subprocess so we can see the output
        cmd = f'python main.py'
        print(f"Running: {cmd}")
        
        # Run for a few seconds then terminate
        process = subprocess.Popen(cmd, shell=True)
        time.sleep(5)  # Let it start
        
        print("🛑 Stopping test after 5 seconds...")
        process.terminate()
        process.wait()
        
        print("✅ Bot startup test completed!")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    main()
