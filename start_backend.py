#!/usr/bin/env python3
"""
Launch script for the crypto bot backend
"""

import sys
import os

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

try:
    print("🚀 Starting Crypto Bot Backend...")
    import uvicorn
    from backend.main import app
    
    print("✅ Backend loaded successfully!")
    print("📍 Server URL: http://localhost:8000")
    print("📋 API Docs: http://localhost:8000/docs")
    print("❤️  Health Check: http://localhost:8000/health")
    print("🔥 Starting server...")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, log_level="info")
    
except Exception as e:
    print(f"❌ Error starting backend: {e}")
    print("📝 Check the backend/main.py file for issues")
    sys.exit(1)
