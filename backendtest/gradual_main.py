#!/usr/bin/env python3
"""
Gradual main.py to identify blocking imports
"""
import sys
import os

# Add backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(backend_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

print("✅ Step 1: Basic imports")

# Import statements
import requests
import numpy as np
import random
import time
import json
import logging
import uuid
from datetime import datetime

print("✅ Step 2: FastAPI imports")
from fastapi import FastAPI, UploadFile, File, Request, Body, Query, APIRouter
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, TYPE_CHECKING
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse

print("✅ Step 3: Local module imports")
# Test each local import one by one
try:
    import db
    print("✅ db imported")
except Exception as e:
    print(f"❌ db failed: {e}")

try:
    from trading import open_virtual_trade
    print("✅ trading imported")
except Exception as e:
    print(f"❌ trading failed: {e}")

try:
    from ml import real_predict
    print("✅ ml imported")
except Exception as e:
    print(f"❌ ml failed: {e}")

try:
    from ws import router as ws_router
    print("✅ ws imported")
except Exception as e:
    print(f"❌ ws failed: {e}")

try:
    from price_feed import get_binance_price
    print("✅ price_feed imported")
except Exception as e:
    print(f"❌ price_feed failed: {e}")

print("✅ Step 4: Create FastAPI app")
app = FastAPI(title="Crypto Bot API")

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Gradual server is running"}

print("✅ All basic functionality working!")
print("🚀 Ready to start server...")

if __name__ == "__main__":
    import uvicorn
    print("🌟 Starting gradual server on http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)
