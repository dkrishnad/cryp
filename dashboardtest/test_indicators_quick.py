#!/usr/bin/env python3
"""
Quick test of the indicators endpoint with timing
"""
import requests
import json
import time

API_URL = "http://localhost:8000"

print("Testing indicators endpoint with timing...")

# Test multiple symbols with timing
test_symbols = ['btcusdt', 'kaiausdt', 'ethusdt', 'solusdt']

for symbol in test_symbols:
    print(f"\n--- Testing {symbol.upper()} ---")
    try:
        start_time = time.time()
        resp = requests.get(f"{API_URL}/features/indicators", params={"symbol": symbol}, timeout=3)
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        print(f"Response time: {response_time:.2f}ms")
        print(f"Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"Data: {json.dumps(data, indent=2)}")
        else:
            print(f"Error: {resp.text}")
            
    except requests.exceptions.Timeout:
        print(f"TIMEOUT: Request took longer than 3 seconds")
    except Exception as e:
        print(f"Exception: {e}")

# Test health endpoint for comparison
print(f"\n--- Testing Health Endpoint ---")
try:
    start_time = time.time()
    resp = requests.get(f"{API_URL}/health", timeout=3)
    end_time = time.time()
    response_time = (end_time - start_time) * 1000
    
    print(f"Health response time: {response_time:.2f}ms")
    print(f"Health status: {resp.status_code}")
    if resp.status_code == 200:
        print(f"Health data: {resp.json()}")
except Exception as e:
    print(f"Health check failed: {e}")
