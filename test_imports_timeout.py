#!/usr/bin/env python3
"""
Minimal test to identify blocking imports
"""
import sys
import os
import signal
import threading
import time

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Set up timeout handler
def timeout_handler():
    """Called if import takes too long"""
    print("❌ Import timeout - something is still blocking!")
    os._exit(1)

# Start timeout timer
timer = threading.Timer(10.0, timeout_handler)
timer.start()

try:
    print("🔄 Testing import with timeout...")
    
    # Try importing step by step
    print("📦 Importing standard libraries...")
    import json
    import time as time_module
    import datetime
    print("✅ Standard libraries OK")
    
    print("📦 Importing FastAPI...")
    from fastapi import FastAPI
    print("✅ FastAPI OK")
    
    print("📦 Importing local modules...")
    import db
    print("✅ db module OK")
    
    import trading
    print("✅ trading module OK")
    
    import ml
    print("✅ ml module OK")
    
    import ws
    print("✅ ws module OK")
    
    print("📦 Testing problematic modules...")
    
    # Test futures_trading import directly
    try:
        print("📦 Testing futures_trading import...")
        import futures_trading
        print("✅ futures_trading module OK")
    except Exception as e:
        print(f"⚠️  futures_trading warning: {e}")
    
    # Test binance_futures_exact import directly
    try:
        print("📦 Testing binance_futures_exact import...")
        import binance_futures_exact
        print("✅ binance_futures_exact module OK")
    except Exception as e:
        print(f"⚠️  binance_futures_exact warning: {e}")
    
    print("📦 Now testing main.py import...")
    import main
    print("✅ main.py imported successfully!")
    
    # Cancel timeout
    timer.cancel()
    print("🎉 All imports completed successfully!")
    
except Exception as e:
    timer.cancel()
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
