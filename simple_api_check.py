#!/usr/bin/env python3
"""
Simple API Endpoint Checker - Find ALL missing endpoints
"""
import re
import os

def find_frontend_api_calls():
    """Find all API calls in frontend files"""
    print("🔍 Finding frontend API calls...")
    
    frontend_files = [
        "dashboardtest/callbacks.py",
        "dashboardtest/utils.py", 
        "dashboardtest/futures_callbacks.py",
        "dashboardtest/binance_exact_callbacks.py"
    ]
    
    api_calls = set()
    
    for file_path in frontend_files:
        if os.path.exists(file_path):
            print(f"  📄 Checking {file_path}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find requests.get/post calls
                patterns = [
                    r'requests\.(?:get|post|put|delete)\(["\']([^"\']+)["\']',
                    r'make_api_call\(["\'][^"\']*["\'],\s*["\']([^"\']+)["\']'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        if 'localhost:5000' in match:
                            endpoint = match.split('localhost:5000')[-1]
                            api_calls.add(endpoint)
                        elif match.startswith('/'):
                            api_calls.add(match)
                            
            except Exception as e:
                print(f"    ❌ Error: {e}")
    
    print(f"  ✅ Found {len(api_calls)} unique API calls")
    return sorted(list(api_calls))

def find_backend_endpoints():
    """Find all endpoints in backend files"""
    print("🔍 Finding backend endpoints...")
    
    backend_files = [
        "backendtest/app.py",
        "backendtest/main.py",
        "backendtest/trading.py",
        "backendtest/ml.py",
        "backendtest/futures_trading.py"
    ]
    
    endpoints = set()
    
    for file_path in backend_files:
        if os.path.exists(file_path):
            print(f"  📄 Checking {file_path}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find @app.route decorators
                patterns = [
                    r'@app\.route\(["\']([^"\']+)["\']',
                    r'@app\.(?:get|post|put|delete)\(["\']([^"\']+)["\']'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        endpoints.add(match)
                        
            except Exception as e:
                print(f"    ❌ Error: {e}")
    
    print(f"  ✅ Found {len(endpoints)} backend endpoints")
    return sorted(list(endpoints))

def main():
    print("🚀 SIMPLE API SYNC CHECK")
    print("=" * 50)
    
    frontend_calls = find_frontend_api_calls()
    backend_endpoints = find_backend_endpoints()
    
    print(f"\n📊 FRONTEND API CALLS ({len(frontend_calls)}):")
    for call in frontend_calls:
        print(f"  - {call}")
    
    print(f"\n📊 BACKEND ENDPOINTS ({len(backend_endpoints)}):")
    for endpoint in backend_endpoints:
        print(f"  - {endpoint}")
    
    print(f"\n❌ MISSING ENDPOINTS:")
    missing = []
    for call in frontend_calls:
        if call not in backend_endpoints:
            # Check for dynamic routes
            found = False
            for endpoint in backend_endpoints:
                if '<' in endpoint:
                    # Convert to regex pattern
                    pattern = re.sub(r'<[^>]+>', r'[^/]+', endpoint)
                    if re.match(f"^{pattern}$", call):
                        found = True
                        break
            if not found:
                missing.append(call)
                print(f"  - {call}")
    
    print(f"\n📊 SUMMARY:")
    print(f"  Frontend calls: {len(frontend_calls)}")
    print(f"  Backend endpoints: {len(backend_endpoints)}")
    print(f"  Missing endpoints: {len(missing)}")
    
    return missing

if __name__ == "__main__":
    missing_endpoints = main()
