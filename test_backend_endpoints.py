#!/usr/bin/env python3
"""
Comprehensive backend endpoint testing for dashboard issues
"""

import requests
import json
import time
import sys
import os

API_URL = "http://localhost:8001"

def test_endpoint(endpoint, method="GET", data=None):
    """Test a backend endpoint"""
    try:
        url = f"{API_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url, timeout=3)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=3)
            
        return {
            "status": response.status_code,
            "response": response.json() if response.status_code == 200 else response.text,
            "working": response.status_code == 200
        }
    except Exception as e:
        return {
            "status": "ERROR", 
            "response": str(e),
            "working": False
        }
                    else:
                        print(f"✗ Missing expected key: {key}")
            return True
        else:
            print(f"✗ Failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Test the new endpoints"""
    base_url = "http://localhost:8000"
    
    print("=== Testing Backend Endpoints ===\n")
    
    # Test health endpoint first
    if not test_endpoint(f"{base_url}/health"):
        print("Backend is not running. Please start it first with: uvicorn main:app --reload")
        return
    
    print("\n" + "="*50 + "\n")
    
    # Test new endpoints
    endpoints = [
        ("/price/BTCUSDT", ["symbol", "price"]),
        ("/balance", ["balance", "currency"]),
        ("/trades/recent", ["trades"]),
    ]
    
    for endpoint, expected_keys in endpoints:
        test_endpoint(f"{base_url}{endpoint}", expected_keys)
        print("\n" + "-"*30 + "\n")
    
    print("Test completed!")

if __name__ == "__main__":
    main()
