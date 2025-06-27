#!/usr/bin/env python3
"""
Minimal Main.py Test
===================
Minimal version to identify blocking imports
"""

print("Starting minimal main test...")

# Basic imports
print("1. Basic imports...")
import requests
import numpy as np
import random
print("   ✅ Basic imports OK")

# FastAPI imports
print("2. FastAPI imports...")
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
import time
import json
import os
import sys
print("   ✅ FastAPI imports OK")

# Database import
print("3. Database import...")
try:
    import db
    print("   ✅ Database import OK")
except Exception as e:
    print(f"   ❌ Database import failed: {e}")

# Trading import
print("4. Trading import...")
try:
    import trading
    print("   ✅ Trading import OK")
except Exception as e:
    print(f"   ❌ Trading import failed: {e}")

# ML import
print("5. ML import...")
try:
    import ml
    print("   ✅ ML import OK")
except Exception as e:
    print(f"   ❌ ML import failed: {e}")

# WebSocket import
print("6. WebSocket import...")
try:
    import ws
    print("   ✅ WebSocket import OK")
except Exception as e:
    print(f"   ❌ WebSocket import failed: {e}")

print("All basic imports completed!")

# Create minimal FastAPI app
print("7. Creating FastAPI app...")
app = FastAPI()

@app.get("/test")
def test():
    return {"status": "working"}

print("   ✅ FastAPI app created")

print("✅ All tests passed - ready to start server!")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting minimal server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
