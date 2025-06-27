#!/usr/bin/env python3
"""
Import Test Tool
================
Tests each import individually to identify blocking imports
"""

import sys
import os

# Add backend to path
backend_dir = r"c:\Users\Hari\Desktop\Crypto bot\backend"
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

imports_to_test = [
    ("Basic imports", "import requests, numpy, json, os, sys, logging"),
    ("FastAPI", "from fastapi import FastAPI"),
    ("Database", "import db"),
    ("Trading", "from trading import open_virtual_trade"),
    ("ML", "from ml import real_predict"),
    ("WebSocket", "from ws import router as ws_router"),
    ("Price Feed", "from price_feed import get_binance_price"),
    ("Futures Trading", "from futures_trading import futures_engine"),
    ("Binance Exact", "from binance_futures_exact import binance_futures_engine"),
    ("Minimal Transfer", "from minimal_transfer_endpoints import get_minimal_transfer_router"),
    ("ML Compatibility", "from ml_compatibility_manager import MLCompatibilityManager")
]

print("🔍 Testing Each Import Individually...")
print("=" * 50)

for name, import_statement in imports_to_test:
    try:
        print(f"📦 Testing {name}...", end=" ", flush=True)
        exec(import_statement)
        print("✅")
    except Exception as e:
        print(f"❌ ERROR: {e}")

print("\n🔍 Testing FastAPI App Creation...")
try:
    from fastapi import FastAPI
    app = FastAPI()
    print("✅ FastAPI app creation successful")
except Exception as e:
    print(f"❌ FastAPI app creation failed: {e}")

print("\nTest complete!")
