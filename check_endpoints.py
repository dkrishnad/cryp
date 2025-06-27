#!/usr/bin/env python3
"""
Check what endpoints are available in the backend
"""
import requests
import json

try:
    # Get OpenAPI spec
    resp = requests.get("http://localhost:8000/openapi.json", timeout=5)
    if resp.status_code == 200:
        openapi = resp.json()
        paths = openapi.get("paths", {})
        
        print("Available Backend Endpoints:")
        print("=" * 40)
        
        for endpoint in sorted(paths.keys()):
            methods = list(paths[endpoint].keys())
            print(f"{endpoint} [{', '.join(methods).upper()}]")
        
        print(f"\nTotal endpoints: {len(paths)}")
        
        # Check for missing required endpoints
        required = [
            "/virtual_balance", "/trade", "/trades", "/trades/analytics", 
            "/backtest", "/backtest/results", "/model/predict_batch", 
            "/model/metrics", "/model/feature_importance", "/notifications"
        ]
        
        print(f"\nRequired by Dashboard:")
        print("=" * 40)
        
        missing = []
        for endpoint in required:
            if endpoint in paths:
                print(f"✅ {endpoint}")
            else:
                print(f"❌ {endpoint}")
                missing.append(endpoint)
        
        if missing:
            print(f"\n⚠️  Missing endpoints: {missing}")
        else:
            print(f"\n✅ All required endpoints are available!")
            
    else:
        print(f"Failed to get OpenAPI spec: {resp.status_code}")
        
except Exception as e:
    print(f"Error: {e}")
