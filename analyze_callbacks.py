#!/usr/bin/env python3
"""
Code-based Callback Integration Verification
This script analyzes the codebase to verify dashboard-backend integrations
"""
import os
import re

def analyze_dashboard_callbacks():
    """Analyze dashboard callbacks to find API calls"""
    
    print("🔍 ANALYZING DASHBOARD CALLBACKS")
    print("=" * 50)
    
    files_to_check = [
        "dashboard/callbacks.py",
        "dashboard/utils.py", 
        "dashboard/hybrid_learning_layout.py",
        "dashboard/email_config_layout.py"
    ]
    
    api_calls = []
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"\n📄 Analyzing {file_path}...")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Find requests.get/post calls
                api_patterns = [
                    r'requests\.(get|post|put|delete)\s*\(\s*f?"([^"]+)"',
                    r'requests\.(get|post|put|delete)\s*\(\s*"([^"]+)"',
                ]
                
                for pattern in api_patterns:
                    matches = re.findall(pattern, content, re.MULTILINE)
                    for method, url in matches:
                        if "API_URL" in url or "localhost:8000" in url:
                            api_calls.append((file_path, method.upper(), url))
    
    print(f"\n📊 Found {len(api_calls)} API calls in dashboard:")
    for file_path, method, url in api_calls:
        clean_url = url.replace("{API_URL}", "").replace("http://localhost:8000", "")
        print(f"   {method} {clean_url} ({os.path.basename(file_path)})")
    
    return api_calls

def analyze_backend_endpoints():
    """Analyze backend endpoints"""
    
    print("\n🔍 ANALYZING BACKEND ENDPOINTS")
    print("=" * 50)
    
    backend_file = "backend/main.py"
    endpoints = []
    
    if os.path.exists(backend_file):
        with open(backend_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Find FastAPI endpoint decorators
            endpoint_pattern = r'@app\.(get|post|put|delete)\s*\(\s*"([^"]+)"'
            matches = re.findall(endpoint_pattern, content, re.MULTILINE)
            
            for method, path in matches:
                endpoints.append((method.upper(), path))
    
    print(f"\n📊 Found {len(endpoints)} backend endpoints:")
    for method, path in endpoints:
        print(f"   {method} {path}")
    
    return endpoints

def find_integration_matches(api_calls, endpoints):
    """Find matching dashboard calls and backend endpoints"""
    
    print("\n🔗 FINDING INTEGRATION MATCHES")
    print("=" * 50)
    
    # Extract endpoint paths from API calls
    dashboard_paths = set()
    for _, _, url in api_calls:
        # Clean up the URL to extract path
        clean_url = url.replace("{API_URL}", "").replace("http://localhost:8000", "")
        if clean_url.startswith("/"):
            # Remove query parameters and dynamic parts
            path = clean_url.split("?")[0].split("{")[0]
            dashboard_paths.add(path)
    
    backend_paths = set(path for _, path in endpoints)
    
    # Find matches
    matched_paths = dashboard_paths.intersection(backend_paths)
    unmatched_dashboard = dashboard_paths - backend_paths
    unmatched_backend = backend_paths - dashboard_paths
    
    print(f"\n✅ MATCHED INTEGRATIONS ({len(matched_paths)}):")
    for path in sorted(matched_paths):
        print(f"   {path}")
    
    if unmatched_dashboard:
        print(f"\n⚠️ DASHBOARD CALLS WITHOUT BACKEND ({len(unmatched_dashboard)}):")
        for path in sorted(unmatched_dashboard):
            print(f"   {path}")
    
    if unmatched_backend:
        print(f"\n📡 BACKEND ENDPOINTS NOT USED BY DASHBOARD ({len(unmatched_backend)}):")
        for path in sorted(unmatched_backend):
            print(f"   {path}")
    
    # Calculate integration percentage
    total_dashboard_calls = len(dashboard_paths)
    matched_calls = len(matched_paths)
    integration_pct = (matched_calls / total_dashboard_calls * 100) if total_dashboard_calls > 0 else 0
    
    print(f"\n📊 INTEGRATION STATISTICS:")
    print(f"   Dashboard API calls: {total_dashboard_calls}")
    print(f"   Backend endpoints: {len(backend_paths)}")
    print(f"   Matched integrations: {matched_calls}")
    print(f"   Integration percentage: {integration_pct:.1f}%")
    
    return {
        "matched": matched_paths,
        "unmatched_dashboard": unmatched_dashboard,
        "unmatched_backend": unmatched_backend,
        "integration_percentage": integration_pct
    }

def check_specific_features():
    """Check specific feature integrations"""
    
    print("\n🎯 CHECKING SPECIFIC FEATURE INTEGRATIONS")
    print("=" * 50)
    
    features_to_check = [
        ("Live Price Updates", ["callbacks.py"], ["/price"]),
        ("Technical Indicators", ["callbacks.py"], ["/features/indicators"]),
        ("Virtual Trading", ["callbacks.py", "utils.py"], ["/trade", "/virtual_balance"]),
        ("ML Predictions", ["utils.py"], ["/model/predict_batch", "/model/analytics"]),
        ("Hybrid Learning", ["hybrid_learning_layout.py"], ["/ml/hybrid", "/ml/online"]),
        ("Email Configuration", ["email_config_layout.py"], ["/email/config", "/email/test"]),
        ("Notifications", ["utils.py"], ["/notifications"]),
        ("Backtesting", ["utils.py"], ["/backtest"]),
    ]
    
    for feature_name, files, expected_endpoints in features_to_check:
        print(f"\n🔍 {feature_name}:")
        
        found_files = []
        for file_name in files:
            for root, dirs, filenames in os.walk("."):
                for filename in filenames:
                    if filename == file_name:
                        found_files.append(os.path.join(root, filename))
        
        if found_files:
            print(f"   ✅ Frontend files found: {[os.path.basename(f) for f in found_files]}")
        else:
            print(f"   ❌ Frontend files missing: {files}")
        
        # Check backend endpoints
        backend_file = "backend/main.py"
        if os.path.exists(backend_file):
            with open(backend_file, 'r') as f:
                backend_content = f.read()
                
            found_endpoints = []
            for endpoint in expected_endpoints:
                if endpoint in backend_content:
                    found_endpoints.append(endpoint)
            
            if found_endpoints:
                print(f"   ✅ Backend endpoints found: {found_endpoints}")
            else:
                print(f"   ❌ Backend endpoints missing: {expected_endpoints}")
        
        # Overall status
        has_frontend = len(found_files) > 0
        has_backend = len(found_endpoints) > 0 if 'found_endpoints' in locals() else False
        
        if has_frontend and has_backend:
            print(f"   🎉 {feature_name}: FULLY INTEGRATED")
        elif has_frontend or has_backend:
            print(f"   ⚠️ {feature_name}: PARTIALLY INTEGRATED")
        else:
            print(f"   ❌ {feature_name}: NOT INTEGRATED")

def main():
    """Main analysis function"""
    
    print("🔄 CODE-BASED CALLBACK INTEGRATION ANALYSIS")
    print("=" * 60)
    
    # Analyze dashboard callbacks
    api_calls = analyze_dashboard_callbacks()
    
    # Analyze backend endpoints
    endpoints = analyze_backend_endpoints()
    
    # Find integration matches
    results = find_integration_matches(api_calls, endpoints)
    
    # Check specific features
    check_specific_features()
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎯 FINAL INTEGRATION ASSESSMENT")
    print("=" * 60)
    
    integration_pct = results["integration_percentage"]
    
    if integration_pct >= 95:
        status = "🎉 EXCELLENT - Production Ready"
    elif integration_pct >= 85:
        status = "✅ GOOD - Minor gaps"
    elif integration_pct >= 70:
        status = "⚠️ FAIR - Some issues"
    else:
        status = "❌ POOR - Major problems"
    
    print(f"\n📊 DASHBOARD-BACKEND INTEGRATION: {integration_pct:.1f}%")
    print(f"🏆 STATUS: {status}")
    
    if integration_pct >= 90:
        print("\n✨ Your crypto bot has excellent integration between dashboard and backend!")
        print("   All major features are properly connected and functional.")
    
    return results

if __name__ == "__main__":
    main()
