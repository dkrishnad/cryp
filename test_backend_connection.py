#!/usr/bin/env python3
"""
Test backend connection and API endpoints
"""
import requests
import json

print("🔍 Testing backend connection...")

try:
    # Test if backend is running
    response = requests.get("http://localhost:8000/", timeout=5)
    print(f"✅ Backend is running: {response.status_code}")
except Exception as e:
    print(f"❌ Backend connection failed: {e}")
    print("   Make sure the backend is running on port 8000")

try:
    # Test a simple API endpoint
    response = requests.get("http://localhost:8000/test", timeout=5)
    print(f"✅ Test endpoint: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {response.text[:100]}")
except Exception as e:
    print(f"⚠️  Test endpoint failed: {e}")

try:
    # Test balance endpoint
    response = requests.get("http://localhost:8000/balance", timeout=5)
    print(f"✅ Balance endpoint: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {response.text[:100]}")
except Exception as e:
    print(f"⚠️  Balance endpoint failed: {e}")

try:
    # Test prediction endpoint
    response = requests.post("http://localhost:8000/predict", 
                           json={"symbol": "BTCUSDT"}, 
                           timeout=5)
    print(f"✅ Prediction endpoint: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {response.text[:100]}")
except Exception as e:
    print(f"⚠️  Prediction endpoint failed: {e}")

print("\n🎉 Backend connection test complete!")
