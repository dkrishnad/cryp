#!/usr/bin/env python3
"""
Simple test script to diagnose the server issue
"""
import sys
import os

# Add paths
backend_dir = os.path.join(os.getcwd(), "backendtest")
sys.path.insert(0, backend_dir)

print("🔍 Testing backend components...")

try:
    print("1. Testing database import...")
    from backendtest.db import initialize_database
    print("   ✅ Database import successful")
    
    print("2. Testing database initialization...")
    initialize_database()
    print("   ✅ Database initialization successful")
    
except Exception as e:
    print(f"   ❌ Database error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("3. Testing trading import...")
    from backendtest.trading import open_virtual_trade
    print("   ✅ Trading import successful")
    
except Exception as e:
    print(f"   ❌ Trading error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("4. Testing ML import...")
    from backendtest.ml import real_predict
    print("   ✅ ML import successful")
    
except Exception as e:
    print(f"   ❌ ML error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("5. Testing FastAPI import...")
    from fastapi import FastAPI
    print("   ✅ FastAPI import successful")
    
except Exception as e:
    print(f"   ❌ FastAPI error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("6. Testing Dash import...")
    import dash
    print("   ✅ Dash import successful")
    
except Exception as e:
    print(f"   ❌ Dash error: {e}")
    import traceback
    traceback.print_exc()

print("\n🎉 Component testing complete!")
