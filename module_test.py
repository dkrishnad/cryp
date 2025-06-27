#!/usr/bin/env python3
"""
Module Import Test
==================
Tests each backend module individually
"""

import sys
import os

# Add backend to path
backend_dir = r"c:\Users\Hari\Desktop\Crypto bot\backend"
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

modules_to_test = [
    "db",
    "trading", 
    "ml",
    "ws",
    "hybrid_learning",
    "online_learning",
    "data_collection",
    "price_feed",
    "futures_trading"
]

print("🔍 Testing Individual Modules...")
print("-" * 40)

for module_name in modules_to_test:
    try:
        print(f"📦 Testing {module_name}...", end=" ")
        __import__(module_name)
        print("✅")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n🔍 Testing FastAPI creation...")
try:
    from fastapi import FastAPI
    app = FastAPI()
    print("✅ FastAPI app creation successful")
except Exception as e:
    print(f"❌ FastAPI error: {e}")

print("\n🔍 Testing uvicorn...")
try:
    import uvicorn
    print("✅ uvicorn import successful")
except Exception as e:
    print(f"❌ uvicorn error: {e}")

print("\nDone!")
