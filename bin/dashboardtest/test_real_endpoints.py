#!/usr/bin/env python3
"""
Test the actual endpoints that exist in the backend
"""
import requests
import sys

API_URL = "http://localhost:8000"

def test_endpoint(path, method="GET", description=""):
    """Test a single endpoint"""
    try:
        if method == "GET":
            response = requests.get(f"{API_URL}{path}", timeout=5)
        elif method == "POST":
            response = requests.post(f"{API_URL}{path}", timeout=5)
        
        if response.status_code == 200:
            print(f"✅ {path}: WORKING ({response.status_code}) - {description}")
            return True
        elif response.status_code == 422:
            print(f"⚠️ {path}: REQUIRES PARAMS ({response.status_code}) - {description}")
            return True
        else:
            print(f"❌ {path}: FAILED ({response.status_code}) - {description}")
            return False
    except Exception as e:
        print(f"❌ {path}: ERROR ({e}) - {description}")
        return False

print("=== TESTING ACTUAL BACKEND ENDPOINTS ===")
print(f"Backend URL: {API_URL}")
print()

# Test basic endpoints
endpoints = [
    ("/health", "GET", "Health check"),
    ("/price", "GET", "Current price data"),
    ("/ml/predict", "GET", "ML prediction"),
    ("/ml/current_signal", "GET", "Current ML signal"),
    ("/advanced_auto_trading/status", "GET", "Auto trading status"),
    ("/advanced_auto_trading/positions", "GET", "Current positions"),
    ("/advanced_auto_trading/market_data", "GET", "Market data"),
    ("/notifications", "GET", "Notifications"),
    ("/model/versions", "GET", "Model versions"),
    ("/model/analytics", "GET", "Model analytics"),
    ("/ml/hybrid/status", "GET", "Hybrid ML status"),
    ("/risk_settings", "GET", "Risk settings"),
    ("/settings/email_notifications", "GET", "Email notification settings"),
]

working_count = 0
total_count = len(endpoints)

for path, method, description in endpoints:
    if test_endpoint(path, method, description):
        working_count += 1

print()
print(f"=== SUMMARY ===")
print(f"Working endpoints: {working_count}/{total_count}")
print(f"Success rate: {(working_count/total_count)*100:.1f}%")

if working_count > 0:
    print("✅ Backend is responding to some endpoints!")
else:
    print("❌ Backend is not responding to any endpoints!")
