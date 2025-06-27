#!/usr/bin/env python3
"""
Bot Startup Test
================
This script tests all imports and initializations before starting the bot.
"""

import sys
import os

def test_imports():
    print("🔍 Testing Bot Imports...")
    print("-" * 40)
    
    try:
        print("📦 Testing FastAPI...")
        from fastapi import FastAPI
        print("✅ FastAPI imported successfully")
        
        print("📦 Testing uvicorn...")
        import uvicorn
        print("✅ uvicorn imported successfully")
        
        print("📦 Testing main module...")
        import main
        print("✅ main module imported successfully")
        
        print("📦 Testing advanced auto trading...")
        from advanced_auto_trading import AdvancedAutoTradingEngine
        print("✅ Advanced auto trading imported successfully")
        
        print("📦 Testing database...")
        import db
        print("✅ Database module imported successfully")
        
        print("📦 Testing trading module...")
        import trading
        print("✅ Trading module imported successfully")
        
        print("📦 Testing ML module...")
        import ml
        print("✅ ML module imported successfully")
        
        print("\n🎉 All imports successful!")
        print("🚀 Ready to launch bot!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    # Change to backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    
    success = test_imports()
    if success:
        print("\n🔥 Starting bot now...")
        print("💡 Run: python launch_bot.py")
    else:
        print("\n❌ Fix import errors before launching")
        sys.exit(1)
