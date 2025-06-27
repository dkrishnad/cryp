#!/usr/bin/env python3
"""
Test backend indicators endpoint for different symbols
"""
import requests
import json

API_URL = "http://localhost:8000"

# Test symbols
test_symbols = ['btcusdt', 'ethusdt', 'solusdt', 'dogeusdt']

print("Testing indicators endpoint for different symbols...")

for symbol in test_symbols:
    print(f"\n--- Testing {symbol.upper()} ---")
    try:
        resp = requests.get(f"{API_URL}/features/indicators", params={"symbol": symbol})
        print(f"Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error response: {resp.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

# Also test health endpoint
print(f"\n--- Testing Health Endpoint ---")
try:
    resp = requests.get(f"{API_URL}/health")
    print(f"Health Status: {resp.status_code}")
    if resp.status_code == 200:
        print(f"Health Response: {resp.json()}")
except Exception as e:
    print(f"Health check failed: {e}")
