#!/usr/bin/env python3
"""
Comprehensive Port Mismatch and Data Flow Verification Script
Checks for port alignment and data flow between backend and dashboard
"""

import requests
import json
import os
import re
from pathlib import Path

def check_port_alignment():
    """Check if all ports are aligned between backend and dashboard"""
    issues = []
    findings = []
    
    workspace_root = Path("c:/Users/Hari/Desktop/Testin dub")
    
    print("🔍 CHECKING PORT ALIGNMENT AND DATA FLOW...")
    print("=" * 60)
    
    # 1. Check backend port configuration
    print("\n1️⃣ BACKEND PORT CONFIGURATION:")
    backend_main = workspace_root / "backendtest" / "main.py"
    
    if backend_main.exists():
        with open(backend_main, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find uvicorn.run port
        uvicorn_match = re.search(r'uvicorn\.run\([^)]*port=(\d+)', content)
        if uvicorn_match:
            backend_port = uvicorn_match.group(1)
            print(f"   ✅ Backend configured to run on port: {backend_port}")
            findings.append(f"Backend port: {backend_port}")
        else:
            print("   ❌ Backend port configuration not found")
            issues.append("Backend port configuration missing")
    
    # 2. Check dashboard API_URL configurations
    print("\n2️⃣ DASHBOARD API_URL CONFIGURATIONS:")
    dashboard_files = [
        "dashboardtest/callbacks.py",
        "dashboardtest/futures_callbacks.py", 
        "dashboardtest/binance_exact_layout.py",
        "dashboardtest/utils.py"
    ]
    
    for file_path in dashboard_files:
        full_path = workspace_root / file_path
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find API_URL definitions
            api_url_matches = re.findall(r'API_URL\s*=\s*["\']([^"\']+)["\']', content)
            if api_url_matches:
                for url in api_url_matches:
                    print(f"   ✅ {file_path}: {url}")
                    findings.append(f"{file_path}: {url}")
                    
                    # Check if port matches backend
                    if ":8000" not in url:
                        issues.append(f"{file_path} uses wrong port: {url}")
            
            # Find direct localhost references
            localhost_matches = re.findall(r'http://localhost:(\d+)', content)
            for port in set(localhost_matches):
                if port != "8000":
                    print(f"   ⚠️  {file_path}: Direct reference to port {port}")
                    issues.append(f"{file_path} has direct port {port} reference")
    
    # 3. Check JavaScript/assets for hardcoded URLs
    print("\n3️⃣ JAVASCRIPT ASSETS URL CHECK:")
    assets_dir = workspace_root / "dashboardtest" / "assets"
    
    if assets_dir.exists():
        for js_file in assets_dir.glob("*.js"):
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find WebSocket and fetch URLs
            ws_matches = re.findall(r'ws://localhost:(\d+)', content)
            http_matches = re.findall(r'http://localhost:(\d+)', content)
            
            for port in set(ws_matches + http_matches):
                if port == "8000":
                    print(f"   ✅ {js_file.name}: Uses correct port {port}")
                    findings.append(f"{js_file.name}: Port {port}")
                else:
                    print(f"   ❌ {js_file.name}: Uses wrong port {port}")
                    issues.append(f"{js_file.name} uses wrong port {port}")
    
    return issues, findings

def check_endpoint_alignment():
    """Check if dashboard endpoints match backend endpoints"""
    print("\n4️⃣ ENDPOINT ALIGNMENT CHECK:")
    
    workspace_root = Path("c:/Users/Hari/Desktop/Testin dub")
    
    # Extract backend endpoints
    backend_endpoints = set()
    backend_main = workspace_root / "backendtest" / "main.py"
    
    if backend_main.exists():
        with open(backend_main, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find @app.get, @app.post, @app.delete endpoints
        endpoint_matches = re.findall(r'@app\.(get|post|delete)\(["\']([^"\']+)["\']', content)
        for method, endpoint in endpoint_matches:
            backend_endpoints.add(f"{method.upper()} {endpoint}")
    
    print(f"   📊 Found {len(backend_endpoints)} backend endpoints")
    
    # Extract dashboard API calls
    dashboard_calls = set()
    dashboard_files = [
        "dashboardtest/callbacks.py",
        "dashboardtest/futures_callbacks.py",
        "dashboardtest/binance_exact_layout.py", 
        "dashboardtest/utils.py"
    ]
    
    for file_path in dashboard_files:
        full_path = workspace_root / file_path
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find requests.get, requests.post, requests.delete calls
            request_matches = re.findall(r'requests\.(get|post|delete)\([^)]*["\']([^"\']+)["\']', content)
            for method, url in request_matches:
                # Extract endpoint from URL (remove API_URL part)
                if "API_URL" in url:
                    # This is a template, skip
                    continue
                endpoint = url.split('localhost:8000')[-1] if 'localhost:8000' in url else url
                if endpoint.startswith('/'):
                    dashboard_calls.add(f"{method.upper()} {endpoint}")
    
    print(f"   📞 Found {len(dashboard_calls)} dashboard API calls")
    
    # Find mismatched endpoints
    backend_paths = {ep.split(' ', 1)[1] for ep in backend_endpoints}
    dashboard_paths = {ep.split(' ', 1)[1] for ep in dashboard_calls}
    
    missing_endpoints = dashboard_paths - backend_paths
    unused_endpoints = backend_paths - dashboard_paths
    
    endpoint_issues = []
    if missing_endpoints:
        print(f"   ❌ {len(missing_endpoints)} endpoints called by dashboard but missing in backend:")
        for endpoint in sorted(missing_endpoints):
            print(f"      - {endpoint}")
            endpoint_issues.append(f"Missing backend endpoint: {endpoint}")
    
    if unused_endpoints:
        print(f"   ⚠️  {len(unused_endpoints)} backend endpoints not used by dashboard:")
        for endpoint in sorted(unused_endpoints):
            if not any(x in endpoint for x in ['{', 'docs', 'openapi']):  # Skip parametric and auto-generated
                print(f"      - {endpoint}")
    
    return endpoint_issues

def test_backend_connectivity():
    """Test if backend is running and accessible"""
    print("\n5️⃣ BACKEND CONNECTIVITY TEST:")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Backend is running and accessible on localhost:8000")
            
            # Test a few key endpoints
            test_endpoints = [
                "/model/analytics",
                "/ml/predict?symbol=btcusdt", 
                "/price/BTCUSDT",
                "/auto_trading/status"
            ]
            
            print("   🧪 Testing key endpoints:")
            for endpoint in test_endpoints:
                try:
                    resp = requests.get(f"http://localhost:8000{endpoint}", timeout=3)
                    status = "✅" if resp.status_code == 200 else f"❌ ({resp.status_code})"
                    print(f"      {status} {endpoint}")
                except Exception as e:
                    print(f"      ❌ {endpoint} - {str(e)}")
            
            return True
        else:
            print(f"   ❌ Backend returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Backend not accessible: {str(e)}")
        return False

def main():
    """Main verification function"""
    print("🎯 PORT MISMATCH & DATA FLOW VERIFICATION")
    print("=" * 60)
    
    # Check port alignment
    port_issues, port_findings = check_port_alignment()
    
    # Check endpoint alignment
    endpoint_issues = check_endpoint_alignment()
    
    # Test backend connectivity
    backend_running = test_backend_connectivity()
    
    # Generate summary report
    print("\n📋 VERIFICATION SUMMARY:")
    print("=" * 60)
    
    total_issues = len(port_issues) + len(endpoint_issues)
    
    if total_issues == 0:
        print("🎉 PERFECT ALIGNMENT! No port mismatches or data flow issues found.")
        print("\n✅ All systems properly configured:")
        for finding in port_findings:
            print(f"   ✅ {finding}")
    else:
        print(f"⚠️  Found {total_issues} issues that need attention:")
        
        if port_issues:
            print(f"\n🔌 Port Issues ({len(port_issues)}):")
            for issue in port_issues:
                print(f"   ❌ {issue}")
        
        if endpoint_issues:
            print(f"\n🔗 Endpoint Issues ({len(endpoint_issues)}):")
            for issue in endpoint_issues:
                print(f"   ❌ {issue}")
    
    print(f"\n🔧 Backend Status: {'✅ Running' if backend_running else '❌ Not Running'}")
    
    # Save detailed report
    report_data = {
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "port_issues": port_issues,
        "endpoint_issues": endpoint_issues,
        "port_findings": port_findings,
        "backend_running": backend_running,
        "total_issues": total_issues,
        "status": "PERFECT" if total_issues == 0 else "NEEDS_ATTENTION"
    }
    
    with open("port_and_dataflow_verification_report.json", "w") as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: port_and_dataflow_verification_report.json")
    
    return total_issues == 0

if __name__ == "__main__":
    main()
