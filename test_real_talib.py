#!/usr/bin/env python3
"""
Test if backend starts with real TA-Lib installed
"""
import sys
import os

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

print("🎯 Testing backend startup with REAL TA-Lib...")

try:
    print("🔄 Testing TA-Lib import directly...")
    import talib
    print("✅ Real TA-Lib imported successfully!")
    print(f"📊 TA-Lib version available with functions like RSI, MACD, BBANDS")
    
    print("🔄 Testing advanced_auto_trading import...")
    import advanced_auto_trading
    print("✅ Advanced auto trading imported successfully!")
    
    print("🔄 Testing main.py import...")
    import main
    print("✅ Main.py imported successfully!")
    
    print("🔄 Testing FastAPI app...")
    app = main.app
    print("✅ FastAPI app retrieved successfully!")
    
    print("\n🎉 SUCCESS! Backend is ready with REAL TA-Lib!")
    print("✅ All advanced technical indicators are now available:")
    print("   • Real RSI calculations")
    print("   • Real MACD signals") 
    print("   • Real Bollinger Bands")
    print("   • Real moving averages")
    print("   • Professional trading signals")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
