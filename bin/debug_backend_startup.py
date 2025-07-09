#!/usr/bin/env python3
"""
DEBUG VERSION - START BACKEND WITH DETAILED LOGGING
"""
import sys
import os
import traceback

def debug_start_backend():
    """Debug version of backend startup"""
    print("🔧 DEBUG: Starting backend import test...")
    
    try:
        # Add backend directory to Python path
        backend_dir = os.path.join(os.path.dirname(__file__), "backend")
        sys.path.insert(0, backend_dir)
        print(f"📁 Backend directory: {backend_dir}")
        
        # Test imports one by one
        print("📦 Testing basic imports...")
        import json
        import time
        print("✅ json, time imported")
        
        import uuid
        import logging
        print("✅ uuid, logging imported")
        
        import random
        import requests
        print("✅ random, requests imported")
        
        from fastapi import FastAPI
        print("✅ FastAPI imported")
        
        from pydantic import BaseModel
        print("✅ Pydantic imported")
        
        print("📦 Testing main.py import...")
        import main  # type: ignore
        print("✅ main.py imported successfully")
        
        print("📦 Testing app creation...")
        app = main.app
        print(f"✅ App created: {app.title}")
        
        print("📦 Testing health endpoint...")
        from fastapi.testclient import TestClient
        client = TestClient(app)
        response = client.get("/health")
        print(f"✅ Health endpoint: {response.status_code} - {response.json()}")
        
        print("🎉 ALL TESTS PASSED - Backend should work!")
        return True
        
    except Exception as e:
        print(f"❌ Error during debug: {e}")
        print(f"📍 Error type: {type(e).__name__}")
        print(f"📋 Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_start_backend()
    if success:
        print("\n🚀 Backend is ready to start!")
        print("💡 Try running: python main.py")
    else:
        print("\n⚠️  Backend has issues that need fixing")
        print("💡 Try running: python main_working.py")
