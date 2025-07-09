#!/usr/bin/env python3
"""
Improved Port Mismatch and Data Flow Verification Script
Properly detects API_URL-based endpoint calls in dashboard
"""

import requests
import json
import os
import re
from pathlib import Path

def extract_backend_endpoints():
    """Extract all backend endpoints from main.py"""
    workspace_root = Path("c:/Users/Hari/Desktop/Testin dub")
    backend_endpoints = set()
    backend_main = workspace_root / "backendtest" / "main.py"
    
    if backend_main.exists():
        with open(backend_main, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find @app.get, @app.post, @app.delete endpoints
        endpoint_patterns = [
            r'@app\.get\(["\']([^"\']+)["\']',
            r'@app\.post\(["\']([^"\']+)["\']', 
            r'@app\.delete\(["\']([^"\']+)["\']',
            r'@app\.put\(["\']([^"\']+)["\']'
        ]
        
        for pattern in endpoint_patterns:
            matches = re.findall(pattern, content)
            backend_endpoints.update(matches)
    
    return backend_endpoints

def extract_dashboard_api_calls():
    """Extract API calls from dashboard files that use API_URL variable"""
    workspace_root = Path("c:/Users/Hari/Desktop/Testin dub")
    dashboard_calls = set()
    
    dashboard_files = [
        "dashboardtest/callbacks.py",
        "dashboardtest/futures_callbacks.py",
        "dashboardtest/binance_exact_layout.py", 
        "dashboardtest/utils.py",
        "dashboardtest/binance_exact_callbacks.py"
    ]
    
    for file_path in dashboard_files:
        full_path = workspace_root / file_path
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find API calls using API_URL variable
            api_call_patterns = [
                r'requests\.get\(f["\']{\s*API_URL\s*}([^"\']+)["\']',
                r'requests\.post\(f["\']{\s*API_URL\s*}([^"\']+)["\']',
                r'requests\.delete\(f["\']{\s*API_URL\s*}([^"\']+)["\']',
                r'requests\.put\(f["\']{\s*API_URL\s*}([^"\']+)["\']',
                r'api_session\.get\(f["\']{\s*API_URL\s*}([^"\']+)["\']',
                r'api_session\.post\(f["\']{\s*API_URL\s*}([^"\']+)["\']',
                r'api_session\.delete\(f["\']{\s*API_URL\s*}([^"\']+)["\']'
            ]
            
            for pattern in api_call_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    # Clean up endpoint path
                    endpoint = match.strip()
                    if endpoint and endpoint.startswith('/'):
                        dashboard_calls.add(endpoint)
            
            # Also check for direct localhost:8000 calls
            direct_patterns = [
                r'requests\.get\(["\']http://localhost:8000([^"\']+)["\']',
                r'requests\.post\(["\']http://localhost:8000([^"\']+)["\']',
                r'requests\.delete\(["\']http://localhost:8000([^"\']+)["\']'
            ]
            
            for pattern in direct_patterns:
                matches = re.findall(pattern, content)
                dashboard_calls.update(matches)
    
    return dashboard_calls

def normalize_endpoint(endpoint):
    """Normalize endpoint for comparison (remove path parameters)"""
    # Replace path parameters like {symbol} with placeholder
    normalized = re.sub(r'\{[^}]+\}', '{param}', endpoint)
    return normalized

def analyze_endpoint_coverage():
    """Analyze which endpoints are used and which are not"""
    print("🔍 IMPROVED ENDPOINT COVERAGE ANALYSIS")
    print("=" * 60)
    
    # Extract endpoints
    backend_endpoints = extract_backend_endpoints()
    dashboard_calls = extract_dashboard_api_calls()
    
    print(f"📊 Found {len(backend_endpoints)} backend endpoints")
    print(f"📞 Found {len(dashboard_calls)} dashboard API calls")
    
    # Show dashboard calls found
    if dashboard_calls:
        print(f"\n✅ DASHBOARD API CALLS DETECTED:")
        for call in sorted(dashboard_calls):
            print(f"   - {call}")
    
    # Normalize endpoints for comparison
    normalized_backend = {normalize_endpoint(ep) for ep in backend_endpoints}
    normalized_dashboard = {normalize_endpoint(ep) for ep in dashboard_calls}
    
    # Find matches and mismatches
    used_endpoints = []
    unused_endpoints = []
    missing_endpoints = []
    
    for backend_ep in backend_endpoints:
        normalized_backend_ep = normalize_endpoint(backend_ep)
        
        # Check if this backend endpoint is called by dashboard
        is_used = False
        for dashboard_ep in dashboard_calls:
            normalized_dashboard_ep = normalize_endpoint(dashboard_ep)
            if normalized_backend_ep == normalized_dashboard_ep:
                is_used = True
                break
        
        if is_used:
            used_endpoints.append(backend_ep)
        else:
            unused_endpoints.append(backend_ep)
    
    # Check for dashboard calls without backend endpoints
    for dashboard_ep in dashboard_calls:
        normalized_dashboard_ep = normalize_endpoint(dashboard_ep)
        
        is_implemented = False
        for backend_ep in backend_endpoints:
            normalized_backend_ep = normalize_endpoint(backend_ep)
            if normalized_dashboard_ep == normalized_backend_ep:
                is_implemented = True
                break
        
        if not is_implemented:
            missing_endpoints.append(dashboard_ep)
    
    # Display results
    print(f"\n📊 COVERAGE ANALYSIS:")
    print(f"   ✅ Used endpoints: {len(used_endpoints)}")
    print(f"   ⚠️  Unused endpoints: {len(unused_endpoints)}")
    print(f"   ❌ Missing endpoints: {len(missing_endpoints)}")
    
    if used_endpoints:
        print(f"\n✅ ENDPOINTS ACTIVELY USED BY DASHBOARD ({len(used_endpoints)}):")
        for endpoint in sorted(used_endpoints)[:20]:  # Show first 20
            print(f"   ✅ {endpoint}")
        if len(used_endpoints) > 20:
            print(f"   ... and {len(used_endpoints) - 20} more")
    
    if missing_endpoints:
        print(f"\n❌ DASHBOARD CALLS MISSING BACKEND IMPLEMENTATION ({len(missing_endpoints)}):")
        for endpoint in sorted(missing_endpoints):
            print(f"   ❌ {endpoint}")
    
    if unused_endpoints:
        print(f"\n⚠️  BACKEND ENDPOINTS NOT USED BY DASHBOARD ({len(unused_endpoints)}):")
        # Filter out some expected unused endpoints
        filtered_unused = []
        for ep in unused_endpoints:
            if not any(skip in ep for skip in ['/docs', '/openapi', '/redoc']):
                filtered_unused.append(ep)
        
        for endpoint in sorted(filtered_unused)[:30]:  # Show first 30
            print(f"   ⚠️  {endpoint}")
        if len(filtered_unused) > 30:
            print(f"   ... and {len(filtered_unused) - 30} more")
    
    # Generate summary
    coverage_percentage = (len(used_endpoints) / len(backend_endpoints)) * 100 if backend_endpoints else 0
    
    print(f"\n📈 COVERAGE SUMMARY:")
    print(f"   Coverage: {coverage_percentage:.1f}% of backend endpoints used")
    print(f"   Status: {'🎯 EXCELLENT' if coverage_percentage > 70 else '⚠️ NEEDS REVIEW' if coverage_percentage > 40 else '❌ POOR'}")
    
    return {
        "backend_endpoints": len(backend_endpoints),
        "dashboard_calls": len(dashboard_calls),
        "used_endpoints": len(used_endpoints),
        "unused_endpoints": len(unused_endpoints),
        "missing_endpoints": len(missing_endpoints),
        "coverage_percentage": coverage_percentage,
        "missing_list": missing_endpoints,
        "used_list": used_endpoints
    }

def check_port_alignment():
    """Check port alignment between backend and dashboard"""
    print("\n🔌 PORT ALIGNMENT CHECK:")
    print("=" * 30)
    
    workspace_root = Path("c:/Users/Hari/Desktop/Testin dub")
    issues = []
    
    # Check backend port
    backend_main = workspace_root / "backendtest" / "main.py"
    backend_port = None
    
    if backend_main.exists():
        with open(backend_main, 'r', encoding='utf-8') as f:
            content = f.read()
        
        uvicorn_match = re.search(r'uvicorn\.run\([^)]*port=(\d+)', content)
        if uvicorn_match:
            backend_port = uvicorn_match.group(1)
            print(f"   🖥️  Backend port: {backend_port}")
    
    # Check dashboard API_URL configurations
    dashboard_files = [
        "dashboardtest/callbacks.py",
        "dashboardtest/futures_callbacks.py",
        "dashboardtest/binance_exact_layout.py"
    ]
    
    for file_path in dashboard_files:
        full_path = workspace_root / file_path
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            api_url_matches = re.findall(r'API_URL\s*=\s*["\']([^"\']+)["\']', content)
            for url in api_url_matches:
                if backend_port and f":{backend_port}" in url:
                    print(f"   ✅ {file_path}: {url}")
                else:
                    print(f"   ❌ {file_path}: {url} (port mismatch)")
                    issues.append(f"Port mismatch in {file_path}")
    
    return issues

def main():
    """Main verification function"""
    print("🎯 IMPROVED PORT & ENDPOINT VERIFICATION")
    print("=" * 60)
    
    # Check port alignment
    port_issues = check_port_alignment()
    
    # Analyze endpoint coverage
    coverage_results = analyze_endpoint_coverage()
    
    # Overall assessment
    print(f"\n🎯 FINAL ASSESSMENT:")
    print("=" * 30)
    
    if port_issues:
        print(f"❌ Port Issues: {len(port_issues)} problems found")
        for issue in port_issues:
            print(f"   - {issue}")
    else:
        print("✅ Port Alignment: PERFECT")
    
    if coverage_results["missing_endpoints"]:
        print(f"❌ Missing Endpoints: {len(coverage_results['missing_endpoints'])} dashboard calls without backend")
    else:
        print("✅ Endpoint Implementation: COMPLETE")
    
    overall_status = "🎯 EXCELLENT" if not port_issues and not coverage_results["missing_endpoints"] else "⚠️ NEEDS ATTENTION"
    print(f"\n🏆 Overall Status: {overall_status}")
    
    # Save detailed report
    report = {
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "port_issues": port_issues,
        "coverage_results": coverage_results,
        "overall_status": overall_status.replace("🎯 ", "").replace("⚠️ ", "")
    }
    
    with open("improved_endpoint_verification_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: improved_endpoint_verification_report.json")

if __name__ == "__main__":
    main()
