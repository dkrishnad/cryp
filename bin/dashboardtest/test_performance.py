#!/usr/bin/env python3
"""
Performance test for indicators with optimization
"""
import requests
import json
import time

API_URL = "http://localhost:8000"

print("Testing optimized indicators performance...")

# Test response times for different timeouts
timeouts = [1, 2, 3, 5]
test_symbols = ['btcusdt', 'kaiausdt', 'ethusdt']

for timeout in timeouts:
    print(f"\n=== Testing with {timeout}s timeout ===")
    
    for symbol in test_symbols:
        try:
            start_time = time.time()
            resp = requests.get(f"{API_URL}/features/indicators", 
                              params={"symbol": symbol}, 
                              timeout=timeout)
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            
            print(f"{symbol.upper()}: {response_time:.0f}ms - Status: {resp.status_code}")
            
            if resp.status_code == 200:
                data = resp.json()
                regime = data.get('regime', 'N/A')
                rsi = data.get('rsi', 'N/A')
                print(f"  → Regime: {regime}, RSI: {rsi}")
                
        except requests.exceptions.Timeout:
            print(f"{symbol.upper()}: TIMEOUT (>{timeout}s)")
        except Exception as e:
            print(f"{symbol.upper()}: ERROR - {e}")

print(f"\n=== Summary ===")
print("The dashboard now has:")
print("1. IMMEDIATE updates when symbols change (no waiting for interval)")
print("2. Periodic updates every 30 seconds for data refresh")
print("3. Reduced timeout to 2 seconds for faster error handling")
print("4. Explicit styling to ensure visibility")
print("\nTechnical indicators should now update instantly when changing symbols!")
