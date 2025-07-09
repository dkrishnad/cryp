#!/usr/bin/env python3
"""
Comprehensive Frontend vs Backend Endpoint Analysis
Step-by-step matching of callbacks.py vs main.py
"""

import re
import os

def extract_frontend_endpoints():
    """Extract all API endpoints called from callbacks.py"""
    frontend_file = "dashboardtest/callbacks.py"
    
    if not os.path.exists(frontend_file):
        print(f"❌ Frontend file not found: {frontend_file}")
        return []
    
    with open(frontend_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match API calls
    patterns = [
        r'api_session\.get\([^,]*["\']([^"\']+)["\']',  # api_session.get calls
        r'api_session\.post\([^,]*["\']([^"\']+)["\']', # api_session.post calls
        r'requests\.get\([^,]*["\']http://[^/]+([^"\']+)["\']', # direct requests.get
        r'requests\.post\([^,]*["\']http://[^/]+([^"\']+)["\']', # direct requests.post
        r'f["\'][^"\']*\{API_URL\}([^"\']*)["\']',  # f-string API calls
    ]
    
    endpoints = set()
    for pattern in patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            if match.startswith('/'):
                # Clean up dynamic parts
                clean_endpoint = re.sub(r'\{[^}]+\}', '{param}', match)
                endpoints.add(clean_endpoint)
    
    return sorted(list(endpoints))

def extract_backend_endpoints():
    """Extract all API endpoints provided by main.py"""
    backend_file = "backendtest/main.py"
    
    if not os.path.exists(backend_file):
        print(f"❌ Backend file not found: {backend_file}")
        return []
    
    with open(backend_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match FastAPI route decorators
    patterns = [
        r'@app\.get\(["\']([^"\']+)["\']',
        r'@app\.post\(["\']([^"\']+)["\']',
        r'@app\.put\(["\']([^"\']+)["\']',
        r'@app\.delete\(["\']([^"\']+)["\']',
    ]
    
    endpoints = set()
    for pattern in patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            # Clean up dynamic parts
            clean_endpoint = re.sub(r'\{[^}]+\}', '{param}', match)
            endpoints.add(clean_endpoint)
    
    return sorted(list(endpoints))

def analyze_mismatches():
    """Compare frontend calls vs backend endpoints"""
    print("=" * 80)
    print("🔍 COMPREHENSIVE ENDPOINT ANALYSIS")
    print("=" * 80)
    
    frontend_endpoints = extract_frontend_endpoints()
    backend_endpoints = extract_backend_endpoints()
    
    print(f"\n📊 SUMMARY:")
    print(f"   Frontend calls: {len(frontend_endpoints)} unique endpoints")
    print(f"   Backend provides: {len(backend_endpoints)} endpoints")
    
    print(f"\n📋 FRONTEND ENDPOINTS (callbacks.py calls):")
    for i, endpoint in enumerate(frontend_endpoints, 1):
        print(f"   {i:2d}. {endpoint}")
    
    print(f"\n🔧 BACKEND ENDPOINTS (main.py provides):")
    for i, endpoint in enumerate(backend_endpoints, 1):
        print(f"   {i:2d}. {endpoint}")
    
    # Find mismatches
    print(f"\n❌ MISMATCHED ENDPOINTS (Frontend calls but Backend doesn't provide):")
    mismatches = []
    for endpoint in frontend_endpoints:
        if endpoint not in backend_endpoints:
            mismatches.append(endpoint)
            print(f"   ❌ {endpoint}")
    
    print(f"\n✅ MATCHED ENDPOINTS (Both have):")
    matches = []
    for endpoint in frontend_endpoints:
        if endpoint in backend_endpoints:
            matches.append(endpoint)
            print(f"   ✅ {endpoint}")
    
    print(f"\n🔧 UNUSED BACKEND ENDPOINTS (Backend provides but Frontend doesn't use):")
    unused = []
    for endpoint in backend_endpoints:
        if endpoint not in frontend_endpoints:
            unused.append(endpoint)
            print(f"   🔧 {endpoint}")
    
    print(f"\n📊 MISMATCH ANALYSIS:")
    print(f"   Mismatched: {len(mismatches)}")
    print(f"   Matched: {len(matches)}")
    print(f"   Unused backend: {len(unused)}")
    
    if mismatches:
        print(f"\n🎯 PRIORITY FIXES NEEDED:")
        for i, endpoint in enumerate(mismatches, 1):
            print(f"   {i}. Fix frontend calls to '{endpoint}'")
    
    return {
        'frontend': frontend_endpoints,
        'backend': backend_endpoints,
        'mismatches': mismatches,
        'matches': matches,
        'unused': unused
    }

if __name__ == "__main__":
    results = analyze_mismatches()
