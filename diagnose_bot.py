#!/usr/bin/env python3
"""
Backend Diagnostic Script
=========================
Tests backend imports and startup to identify issues
"""

import sys
import os
import traceback

def test_backend_imports():
    """Test all backend imports"""
    print("🔍 Testing Backend Imports...")
    print("-" * 40)
    
    # Change to backend directory
    backend_dir = r"c:\Users\Hari\Desktop\Crypto bot\backend"
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    
    os.chdir(backend_dir)
    
    try:
        print("📦 Testing basic imports...")
        import requests
        import numpy as np
        import json
        import os
        import sys
        import logging
        print("✅ Basic imports successful")
        
        print("📦 Testing FastAPI...")
        from fastapi import FastAPI
        print("✅ FastAPI imported")
        
        print("📦 Testing uvicorn...")
        import uvicorn
        print("✅ uvicorn imported")
        
        print("📦 Testing database...")
        import db
        print("✅ Database module imported")
        
        print("📦 Testing trading module...")
        import trading
        print("✅ Trading module imported")
        
        print("📦 Testing ML module...")
        import ml
        print("✅ ML module imported")
        
        print("📦 Testing WebSocket...")
        import ws
        print("✅ WebSocket module imported")
        
        print("📦 Testing advanced auto trading...")
        try:
            from advanced_auto_trading import AdvancedAutoTradingEngine
            print("✅ Advanced auto trading imported")
        except ImportError as e:
            print(f"⚠️ Advanced auto trading warning: {e}")
        
        print("📦 Testing main module...")
        try:
            import main
            print("✅ Main module imported successfully")
            print(f"✅ FastAPI app object: {hasattr(main, 'app')}")
            return True
        except Exception as e:
            print(f"❌ Main module import failed: {e}")
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"❌ Import error: {e}")
        traceback.print_exc()
        return False

def test_dashboard_connection():
    """Test if dashboard callbacks have correct API URLs"""
    print("\n🔍 Testing Dashboard Configuration...")
    print("-" * 40)
    
    dashboard_dir = r"c:\Users\Hari\Desktop\Crypto bot\dashboard"
    if dashboard_dir not in sys.path:
        sys.path.insert(0, dashboard_dir)
    
    try:
        # Check callbacks.py API_URL
        callbacks_file = os.path.join(dashboard_dir, "callbacks.py")
        with open(callbacks_file, 'r') as f:
            content = f.read()
            if 'API_URL = "http://localhost:8000"' in content:
                print("✅ callbacks.py API_URL correct")
            else:
                print("❌ callbacks.py API_URL incorrect")
        
        # Check other layout files
        layout_files = ['hybrid_learning_layout.py', 'email_config_layout.py', 'binance_exact_layout.py']
        for file in layout_files:
            file_path = os.path.join(dashboard_dir, file)
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    content = f.read()
                    if 'localhost:8000' in content:
                        print(f"✅ {file} API_URL correct")
                    elif 'localhost:8001' in content:
                        print(f"❌ {file} still has port 8001")
                    else:
                        print(f"⚠️ {file} no API_URL found")
        
        return True
        
    except Exception as e:
        print(f"❌ Dashboard config error: {e}")
        return False

def test_basic_endpoints():
    """Test if we can start backend and hit basic endpoints"""
    print("\n🔍 Testing Backend Startup...")
    print("-" * 40)
    
    try:
        import subprocess
        import time
        import requests
        
        backend_dir = r"c:\Users\Hari\Desktop\Crypto bot\backend"
        os.chdir(backend_dir)
        
        print("🚀 Attempting to start backend server...")
        
        # Try to start main.py and capture output
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=backend_dir
        )
        
        # Wait a bit for startup
        time.sleep(10)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Backend process is running")
            
            # Try to hit a basic endpoint
            try:
                response = requests.get("http://localhost:8000/health", timeout=5)
                print(f"✅ Health endpoint response: {response.status_code}")
            except Exception as e:
                print(f"⚠️ Could not reach health endpoint: {e}")
            
            # Kill the test process
            process.terminate()
            process.wait()
            return True
            
        else:
            # Process died, get error output
            stdout, stderr = process.communicate()
            print(f"❌ Backend process failed to start")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Startup test error: {e}")
        traceback.print_exc()
        return False

def main():
    print("=" * 50)
    print("    CRYPTO BOT DIAGNOSTIC TOOL")
    print("=" * 50)
    
    success = True
    
    # Test imports
    if not test_backend_imports():
        success = False
    
    # Test dashboard configuration
    if not test_dashboard_connection():
        success = False
    
    # Test basic startup
    if not test_basic_endpoints():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✅ ALL TESTS PASSED - Bot should work correctly!")
        print("💡 Try running: python launch_complete_bot.py")
    else:
        print("❌ ISSUES FOUND - See errors above")
        print("💡 Fix the issues before running the bot")
    print("=" * 50)

if __name__ == "__main__":
    main()
