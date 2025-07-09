#!/usr/bin/env python3
"""
Comprehensive Frontend-Backend Synchronization Checker
This script checks API connections, endpoint availability, and functionality gaps
"""
import sys
import os
import requests
import json
import traceback
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add paths
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboardtest'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backendtest'))

def safe_print(msg):
    """Safe printing function"""
    try:
        print(msg)
        sys.stdout.flush()
    except UnicodeEncodeError:
        print(msg.encode('ascii', 'replace').decode('ascii'))
        sys.stdout.flush()

def check_backend_status():
    """Check if backend is running and accessible"""
    backend_urls = [
        'http://localhost:5000',
        'http://localhost:5000/api/status',
        'http://localhost:5000/health',
    ]
    
    safe_print("🔍 Checking Backend Connectivity...")
    safe_print("-" * 50)
    
    backend_running = False
    for url in backend_urls:
        try:
            response = requests.get(url, timeout=5)
            safe_print(f"✅ {url} - Status: {response.status_code}")
            if response.status_code == 200:
                backend_running = True
        except requests.exceptions.ConnectionError:
            safe_print(f"❌ {url} - Connection refused (backend not running)")
        except requests.exceptions.Timeout:
            safe_print(f"⚠️  {url} - Timeout")
        except Exception as e:
            safe_print(f"❌ {url} - Error: {e}")
    
    return backend_running

def discover_backend_endpoints():
    """Discover available backend endpoints"""
    safe_print("\n🔍 Discovering Backend Endpoints...")
    safe_print("-" * 50)
    
    # Check backend files for route definitions
    backend_files = [
        'backendtest/app.py',
        'backendtest/main.py',
        'backendtest/trading.py',
        'backendtest/ml.py',
        'backendtest/data_collection.py',
        'backendtest/futures_trading.py',
        'backendtest/advanced_auto_trading.py',
        'backendtest/ws.py',
        'backendtest/tasks.py',
        'backendtest/crypto_transfer_endpoints.py',
        'backendtest/missing_endpoints.py'
    ]
    
    endpoints = []
    
    for file_path in backend_files:
        if not os.path.exists(file_path):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find route definitions
            import re
            routes = re.findall(r'@app\.route\([\'"]([^\'"]+)[\'"]', content)
            routes.extend(re.findall(r'@bp\.route\([\'"]([^\'"]+)[\'"]', content))
            
            for route in routes:
                endpoints.append({
                    'endpoint': route,
                    'file': file_path,
                    'full_url': f'http://localhost:5000{route}'
                })
                
        except Exception as e:
            safe_print(f"❌ Error reading {file_path}: {e}")
    
    safe_print(f"📋 Found {len(endpoints)} endpoints:")
    for ep in endpoints[:10]:  # Show first 10
        safe_print(f"   {ep['endpoint']} ({ep['file']})")
    
    if len(endpoints) > 10:
        safe_print(f"   ... and {len(endpoints) - 10} more")
    
    return endpoints

def test_backend_endpoints(endpoints):
    """Test backend endpoints for accessibility"""
    safe_print("\n🧪 Testing Backend Endpoints...")
    safe_print("-" * 50)
    
    working_endpoints = []
    broken_endpoints = []
    
    def test_endpoint(ep):
        try:
            response = requests.get(ep['full_url'], timeout=3)
            return ep, response.status_code, 'working'
        except Exception as e:
            return ep, str(e), 'broken'
    
    # Test endpoints in parallel for speed
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(test_endpoint, ep) for ep in endpoints[:20]]  # Test first 20
        
        for future in as_completed(futures):
            ep, status, result = future.result()
            if result == 'working':
                working_endpoints.append(ep)
                safe_print(f"✅ {ep['endpoint']} - Status: {status}")
            else:
                broken_endpoints.append(ep)
                safe_print(f"❌ {ep['endpoint']} - Error: {status}")
    
    safe_print(f"\n📊 Endpoint Summary:")
    safe_print(f"   Working: {len(working_endpoints)}")
    safe_print(f"   Broken: {len(broken_endpoints)}")
    
    return working_endpoints, broken_endpoints

def check_frontend_api_calls():
    """Check frontend callbacks for API calls"""
    safe_print("\n🔍 Analyzing Frontend API Calls...")
    safe_print("-" * 50)
    
    callback_files = [
        'dashboardtest/callbacks.py',
        'dashboardtest/futures_callbacks.py',
        'dashboardtest/binance_exact_callbacks.py'
    ]
    
    api_calls = []
    
    for file_path in callback_files:
        if not os.path.exists(file_path):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find API calls
            import re
            # Look for requests calls
            requests_calls = re.findall(r'requests\.(get|post|put|delete)\([\'"]([^\'"]+)[\'"]', content)
            
            # Look for localhost URLs
            localhost_urls = re.findall(r'[\'"]http://localhost:(\d+)([^\'"]+)[\'"]', content)
            
            for method, url in requests_calls:
                api_calls.append({
                    'method': method,
                    'url': url,
                    'file': file_path,
                    'type': 'requests_call'
                })
            
            for port, path in localhost_urls:
                api_calls.append({
                    'method': 'unknown',
                    'url': f'http://localhost:{port}{path}',
                    'file': file_path,
                    'type': 'localhost_url'
                })
                
        except Exception as e:
            safe_print(f"❌ Error reading {file_path}: {e}")
    
    safe_print(f"📋 Found {len(api_calls)} API calls in frontend:")
    for call in api_calls:
        safe_print(f"   {call['method'].upper()} {call['url']} ({call['file']})")
    
    return api_calls

def check_callback_errors():
    """Check for common callback errors that cause Internal Server Error"""
    safe_print("\n🔍 Checking for Callback Errors...")
    safe_print("-" * 50)
    
    try:
        # Import without executing callbacks
        sys.path.insert(0, 'dashboardtest')
        
        # Check for common issues in callbacks
        with open('dashboardtest/callbacks.py', 'r', encoding='utf-8') as f:
            callback_content = f.read()
        
        issues = []
        
        # Check for undefined variables
        import re
        
        # Look for potential undefined variables in return statements
        return_statements = re.findall(r'return ([^#\n]+)', callback_content)
        
        # Look for missing imports
        if 'import requests' not in callback_content and 'requests.' in callback_content:
            issues.append("Missing 'import requests' statement")
        
        # Look for hardcoded URLs that might not work
        hardcoded_urls = re.findall(r'http://localhost:\d+[^\s\'"]+', callback_content)
        for url in hardcoded_urls:
            issues.append(f"Hardcoded URL found: {url}")
        
        # Look for try-catch blocks - missing ones might cause errors
        callback_functions = re.findall(r'def\s+(\w+)\([^)]*\):', callback_content)
        try_blocks = len(re.findall(r'\btry\s*:', callback_content))
        
        if len(callback_functions) > try_blocks * 2:  # Rough heuristic
            issues.append(f"Found {len(callback_functions)} callback functions but only {try_blocks} try blocks - missing error handling")
        
        if issues:
            safe_print("❌ Potential callback issues found:")
            for issue in issues:
                safe_print(f"   - {issue}")
        else:
            safe_print("✅ No obvious callback issues detected")
            
        return issues
        
    except Exception as e:
        safe_print(f"❌ Error checking callbacks: {e}")
        return [f"Error checking callbacks: {e}"]

def check_missing_functionality():
    """Check for missing functionality between frontend and backend"""
    safe_print("\n🔍 Checking for Missing Functionality...")
    safe_print("-" * 50)
    
    # Frontend button IDs that need backend endpoints
    frontend_buttons = []
    
    try:
        with open('dashboardtest/layout.py', 'r', encoding='utf-8') as f:
            layout_content = f.read()
        
        # Find button IDs
        import re
        button_ids = re.findall(r'id=[\'"]([^"\']*btn[^\'"]*)[\'"]', layout_content)
        frontend_buttons = list(set(button_ids))
        
        safe_print(f"📋 Found {len(frontend_buttons)} buttons in frontend")
        
    except Exception as e:
        safe_print(f"❌ Error reading layout: {e}")
    
    # Expected backend functionality based on button names
    expected_endpoints = []
    for btn_id in frontend_buttons:
        # Convert button ID to expected endpoint
        endpoint_name = btn_id.replace('-btn', '').replace('-', '_')
        expected_endpoints.append(f'/api/{endpoint_name}')
    
    safe_print(f"📋 Expected {len(expected_endpoints)} corresponding backend endpoints")
    
    return frontend_buttons, expected_endpoints

def check_infinite_loops():
    """Check for potential infinite loops in callbacks"""
    safe_print("\n🔍 Checking for Infinite Loop Patterns...")
    safe_print("-" * 50)
    
    try:
        with open('dashboardtest/callbacks.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        
        # Look for while True loops
        while_loops = len(re.findall(r'while\s+True\s*:', content))
        if while_loops > 0:
            issues.append(f"Found {while_loops} 'while True' loops")
        
        # Look for recursive callback patterns
        callback_names = re.findall(r'def\s+(\w+)\([^)]*\):', content)
        for name in callback_names:
            if name in content.count(name) > 2:  # Function name appears more than twice
                issues.append(f"Function '{name}' might be called recursively")
        
        # Look for interval callbacks that might be too frequent
        intervals = re.findall(r'interval=(\d+)', content)
        for interval in intervals:
            if int(interval) < 1000:  # Less than 1 second
                issues.append(f"Very frequent interval found: {interval}ms")
        
        if issues:
            safe_print("⚠️  Potential infinite loop issues:")
            for issue in issues:
                safe_print(f"   - {issue}")
        else:
            safe_print("✅ No obvious infinite loop patterns detected")
            
        return issues
        
    except Exception as e:
        safe_print(f"❌ Error checking for loops: {e}")
        return [f"Error checking loops: {e}"]

def main():
    """Main comprehensive check function"""
    safe_print("🚀 Comprehensive Frontend-Backend Synchronization Check")
    safe_print("=" * 70)
    
    # 1. Check backend status
    backend_running = check_backend_status()
    
    # 2. Discover and test backend endpoints
    endpoints = discover_backend_endpoints()
    if backend_running and endpoints:
        working_endpoints, broken_endpoints = test_backend_endpoints(endpoints)
    else:
        working_endpoints, broken_endpoints = [], []
    
    # 3. Check frontend API calls
    frontend_api_calls = check_frontend_api_calls()
    
    # 4. Check callback errors
    callback_issues = check_callback_errors()
    
    # 5. Check missing functionality
    frontend_buttons, expected_endpoints = check_missing_functionality()
    
    # 6. Check for infinite loops
    loop_issues = check_infinite_loops()
    
    # Summary and recommendations
    safe_print("\n" + "=" * 70)
    safe_print("📊 COMPREHENSIVE ANALYSIS SUMMARY")
    safe_print("=" * 70)
    
    safe_print(f"Backend Status: {'✅ Running' if backend_running else '❌ Not Running'}")
    safe_print(f"Backend Endpoints: {len(endpoints)} discovered, {len(working_endpoints)} working")
    safe_print(f"Frontend API Calls: {len(frontend_api_calls)} found")
    safe_print(f"Frontend Buttons: {len(frontend_buttons)} found")
    safe_print(f"Callback Issues: {len(callback_issues)} found")
    safe_print(f"Loop Issues: {len(loop_issues)} found")
    
    # Critical issues
    critical_issues = []
    
    if not backend_running:
        critical_issues.append("Backend server is not running")
    
    if len(broken_endpoints) > len(working_endpoints):
        critical_issues.append("More broken endpoints than working ones")
    
    if len(callback_issues) > 0:
        critical_issues.append("Callback errors detected")
    
    if len(loop_issues) > 0:
        critical_issues.append("Potential infinite loop patterns detected")
    
    if critical_issues:
        safe_print("\n❌ CRITICAL ISSUES TO FIX:")
        for i, issue in enumerate(critical_issues, 1):
            safe_print(f"   {i}. {issue}")
    else:
        safe_print("\n✅ No critical issues detected")
    
    # Recommendations
    safe_print("\n📋 RECOMMENDATIONS:")
    if not backend_running:
        safe_print("   1. Start the backend server first: python backendtest/app.py")
    
    if len(broken_endpoints) > 0:
        safe_print("   2. Fix broken backend endpoints")
    
    if len(callback_issues) > 0:
        safe_print("   3. Add error handling to callbacks")
    
    if len(loop_issues) > 0:
        safe_print("   4. Review callback logic for infinite loops")
    
    safe_print("   5. Enable debug mode in dashboard for better error messages")

if __name__ == "__main__":
    main()
