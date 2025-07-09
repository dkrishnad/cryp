#!/usr/bin/env python3
"""
Quick verification test for fixed backend
"""
import requests
import json
import time
from datetime import datetime

def test_fixed_backend():
    """Test the fixed backend endpoints"""
    backend_url = "http://localhost:5000"
    
    print("🔧 Starting backend verification test...")
    
    # Start backend and wait
    import subprocess
    import sys
    import os
    
    backend_process = subprocess.Popen(
        [sys.executable, "backendtest/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for backend to start
    time.sleep(3)
    
    # Critical endpoints to test
    test_endpoints = [
        ("/", "GET"),
        ("/data/live_prices", "GET"),
        ("/portfolio/balance", "GET"),
        ("/ml/predict", "POST"),
        ("/trade", "POST"),
        ("/notifications", "GET"),
        ("/auto_trading/status", "GET"),
        ("/futures/positions", "GET"),
        ("/ml/analytics", "GET"),
        ("/backtest/results", "GET")
    ]
    
    successful = 0
    failed = 0
    
    print(f"\n🧪 Testing {len(test_endpoints)} critical endpoints...")
    print("=" * 60)
    
    for endpoint, method in test_endpoints:
        try:
            start_time = time.time()
            
            if method == "GET":
                response = requests.get(f"{backend_url}{endpoint}", timeout=2)
            else:
                response = requests.post(f"{backend_url}{endpoint}", json={}, timeout=2)
            
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code < 400:
                print(f"✅ {endpoint:<25} {response.status_code} ({response_time:.0f}ms)")
                successful += 1
            else:
                print(f"❌ {endpoint:<25} {response.status_code} ({response_time:.0f}ms)")
                failed += 1
                
        except requests.exceptions.Timeout:
            print(f"⏱️ {endpoint:<25} TIMEOUT (>2s)")
            failed += 1
        except Exception as e:
            print(f"❌ {endpoint:<25} ERROR: {str(e)[:30]}")
            failed += 1
    
    print("=" * 60)
    print(f"📊 RESULTS: {successful}/{len(test_endpoints)} successful ({successful/len(test_endpoints)*100:.1f}%)")
    
    if successful == len(test_endpoints):
        print("🎉 ALL ENDPOINTS WORKING! Backend is now 100% functional!")
    else:
        print(f"❌ {failed} endpoints still failing")
    
    # Cleanup
    backend_process.terminate()
    
    return successful == len(test_endpoints)

if __name__ == "__main__":
    success = test_fixed_backend()
    print(f"\n🎯 BACKEND STATUS: {'✅ READY' if success else '❌ NEEDS MORE FIXES'}")
