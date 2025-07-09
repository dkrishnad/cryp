#!/usr/bin/env python3
"""
Quick endpoint verification to check if missing endpoints are now registered
"""
import sys
import os
import re

def check_backend_endpoints():
    """Check how many endpoints are in the backend main.py"""
    try:
        with open("backendtest/main.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Find @app.get, @app.post, @app.delete endpoints
        patterns = [
            r'@app\.get\(["\']([^"\']+)["\']',
            r'@app\.post\(["\']([^"\']+)["\']', 
            r'@app\.delete\(["\']([^"\']+)["\']',
            r'@app\.put\(["\']([^"\']+)["\']'
        ]
        
        endpoints = set()
        for pattern in patterns:
            matches = re.findall(pattern, content)
            endpoints.update(matches)
        
        print(f"✅ Found {len(endpoints)} endpoints in backend main.py")
        return endpoints
    except Exception as e:
        print(f"❌ Error reading backend: {e}")
        return set()

def check_missing_endpoints():
    """Check how many endpoints are in missing_endpoints.py"""
    try:
        with open("backendtest/missing_endpoints.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Find @router.get, @router.post endpoints
        patterns = [
            r'@router\.get\(["\']([^"\']+)["\']',
            r'@router\.post\(["\']([^"\']+)["\']'
        ]
        
        endpoints = set()
        for pattern in patterns:
            matches = re.findall(pattern, content)
            endpoints.update(matches)
        
        print(f"✅ Found {len(endpoints)} endpoints in missing_endpoints.py:")
        for endpoint in sorted(endpoints):
            print(f"   - {endpoint}")
        return endpoints
    except Exception as e:
        print(f"❌ Error reading missing endpoints: {e}")
        return set()

def main():
    print("🔍 QUICK ENDPOINT CHECK")
    print("=" * 50)
    
    backend_endpoints = check_backend_endpoints()
    missing_endpoints = check_missing_endpoints()
    
    # Target missing endpoints
    target_missing = {
        "/backtest",
        "/backtest/results", 
        "/model/errors",
        "/model/logs",
        "/model/predict_batch",
        "/model/upload_and_retrain",
        "/safety/check",
        "/system/status",
        "/trades/analytics"
    }
    
    print(f"\n📋 TARGET MISSING ENDPOINTS CHECK:")
    covered = 0
    for endpoint in target_missing:
        if endpoint in missing_endpoints:
            print(f"   ✅ {endpoint} - IMPLEMENTED")
            covered += 1
        else:
            print(f"   ❌ {endpoint} - MISSING")
    
    print(f"\n📊 SUMMARY:")
    print(f"   Coverage: {covered}/{len(target_missing)} ({covered/len(target_missing)*100:.1f}%)")
    
    if covered == len(target_missing):
        print("   🎉 ALL MISSING ENDPOINTS ARE NOW IMPLEMENTED!")
    else:
        print("   ⚠️  Some endpoints still missing")

if __name__ == "__main__":
    main()
