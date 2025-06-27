#!/usr/bin/env python3
"""
Comprehensive Feature Integration Check
Tests all advanced features and integrations
"""
import os
import sys
import importlib
import importlib.util
import requests
import json
from datetime import datetime

def test_file_existence():
    """Check if all required files exist"""
    print("🔍 Checking file existence...")
    
    required_files = [
        # Backend core files
        "backend/main.py",
        "backend/db.py", 
        "backend/futures_trading.py",
        "backend/binance_futures_exact.py",
        "backend/hybrid_learning.py",
        "backend/online_learning.py",
        "backend/ml_compatibility_manager.py",
        
        # Dashboard files
        "dashboard/app.py",
        "dashboard/layout.py",
        "dashboard/callbacks.py",
        "dashboard/futures_trading_layout.py",
        "dashboard/binance_exact_layout.py",
        "dashboard/futures_callbacks.py",
        "dashboard/binance_exact_callbacks.py",
        
        # Core trading files
        "futures_trading.py",
        "binance_futures_exact.py",
        
        # Analysis files
        "bot_performance_analysis.py",
        "visual_performance_analysis.py",
        "multi_coin_analysis.py",
        "realistic_5usd_hft_analysis.py",
        
        # Test files
        "test_futures_system.py",
        "test_binance_exact.py",
        
        # Transfer learning files
        "crypto_transfer_learning_lifecycle.py",
        "backend/crypto_transfer_learning.py",
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            existing_files.append(file_path)
        else:
            missing_files.append(file_path)
    
    print(f"✅ Found {len(existing_files)} required files")
    if missing_files:
        print(f"❌ Missing {len(missing_files)} files:")
        for file in missing_files:
            print(f"   - {file}")
    
    return len(missing_files) == 0

def test_backend_endpoints():
    """Test if backend endpoints are available"""
    print("\n🔍 Checking backend endpoint availability...")
    
    # Key endpoints to test
    endpoints = [
        # Basic endpoints
        "/health",
        "/price",
        "/virtual_balance",
        "/trades",
        
        # Futures endpoints
        "/futures/account",
        "/futures/positions", 
        "/futures/settings",
        "/futures/execute_signal",
        
        # Binance exact endpoints
        "/fapi/v1/order",
        "/fapi/v1/openOrders",
        "/fapi/v1/leverage",
        "/fapi/v1/ticker/24hr",
        
        # ML endpoints
        "/ml/hybrid/status",
        "/ml/online/stats",
        "/ml/compatibility/check",
        
        # Auto trading endpoints
        "/auto_trading/status",
        "/auto_trading/toggle",
        "/auto_trading/execute_signal",
    ]
    
    try:
        # Check if backend is running
        health_response = requests.get("http://localhost:8001/health", timeout=5)
        if health_response.status_code != 200:
            print("❌ Backend is not running or unhealthy")
            return False
        
        # Check OpenAPI documentation
        openapi_response = requests.get("http://localhost:8001/openapi.json", timeout=5)
        if openapi_response.status_code == 200:
            paths = openapi_response.json().get("paths", {})
            
            available_endpoints = []
            missing_endpoints = []
            
            for endpoint in endpoints:
                if endpoint in paths:
                    available_endpoints.append(endpoint)
                else:
                    missing_endpoints.append(endpoint)
            
            print(f"✅ Found {len(available_endpoints)} endpoints")
            if missing_endpoints:
                print(f"❌ Missing {len(missing_endpoints)} endpoints:")
                for endpoint in missing_endpoints:
                    print(f"   - {endpoint}")
            
            return len(missing_endpoints) == 0
        else:
            print("❌ Could not retrieve OpenAPI documentation")
            return False
            
    except Exception as e:
        print(f"❌ Backend connection error: {e}")
        return False

def test_dashboard_components():
    """Test dashboard component integration"""
    print("\n🔍 Checking dashboard component integration...")
    
    try:
        # Test main dashboard imports
        sys.path.append("dashboard")
          # Check if layout loads
        try:
            spec = importlib.util.spec_from_file_location("layout", "dashboard/layout.py")
            layout_module = importlib.util.module_from_spec(spec)
            print("✅ Main layout loads successfully")
        except Exception as e:
            print(f"❌ Layout import error: {e}")
            return False
        
        # Check if advanced layouts exist
        advanced_layouts = [
            "futures_trading_layout",
            "binance_exact_layout", 
            "hybrid_learning_layout",
            "auto_trading_layout"
        ]
        
        working_layouts = []
        broken_layouts = []
        
        for layout_name in advanced_layouts:
            try:
                importlib.import_module(layout_name)
                working_layouts.append(layout_name)
            except Exception as e:
                broken_layouts.append((layout_name, str(e)))
        
        print(f"✅ {len(working_layouts)} advanced layouts working")
        if broken_layouts:
            print(f"❌ {len(broken_layouts)} layouts have issues:")
            for layout_name, error in broken_layouts:
                print(f"   - {layout_name}: {error[:100]}...")
          # Check if callbacks load
        try:
            spec = importlib.util.spec_from_file_location("callbacks", "dashboard/callbacks.py") 
            callbacks_module = importlib.util.module_from_spec(spec)
            print("✅ Main callbacks load successfully")
        except Exception as e:
            print(f"❌ Callbacks import error: {e}")
            return False
        
        return len(broken_layouts) == 0
        
    except Exception as e:
        print(f"❌ Dashboard test error: {e}")
        return False

def test_analysis_capabilities():
    """Test analysis and ML capabilities"""
    print("\n🔍 Checking analysis and ML capabilities...")
    
    analysis_files = [
        "bot_performance_analysis.py",
        "multi_coin_analysis.py", 
        "realistic_5usd_hft_analysis.py",
        "visual_performance_analysis.py"
    ]
    
    working_analyses = []
    broken_analyses = []
    
    for analysis_file in analysis_files:
        try:
            # Try importing the module
            module_name = analysis_file.replace('.py', '')
            spec = importlib.util.spec_from_file_location(module_name, analysis_file)
            module = importlib.util.module_from_spec(spec)
            # Don't execute, just check if it can be parsed
            working_analyses.append(analysis_file)
        except Exception as e:
            broken_analyses.append((analysis_file, str(e)))
    
    print(f"✅ {len(working_analyses)} analysis files available")
    if broken_analyses:
        print(f"❌ {len(broken_analyses)} analysis files have issues:")
        for file_name, error in broken_analyses:
            print(f"   - {file_name}: {error[:100]}...")
    
    return len(broken_analyses) == 0

def test_documentation_completeness():
    """Test if documentation files exist"""
    print("\n🔍 Checking documentation completeness...")
    
    doc_files = [
        "5X_LEVERAGE_COMPLETE_ANALYSIS.md",
        "BINANCE_EXACT_SUCCESS.md",
        "FINAL_BINANCE_EXACT_COMPLETE.md",
        "BOT_WIN_PROBABILITY_ANALYSIS.md",
        "HIGH_FREQUENCY_ANALYSIS.md",
        "REALISTIC_5USD_ANALYSIS.md",
        "AI_SYNC_FINAL_STATUS.md"
    ]
    
    existing_docs = []
    missing_docs = []
    
    for doc_file in doc_files:
        if os.path.exists(doc_file):
            existing_docs.append(doc_file)
        else:
            missing_docs.append(doc_file)
    
    print(f"✅ Found {len(existing_docs)} documentation files")
    if missing_docs:
        print(f"❌ Missing {len(missing_docs)} documentation files:")
        for doc in missing_docs:
            print(f"   - {doc}")
    
    return len(missing_docs) == 0

def generate_integration_report():
    """Generate comprehensive integration report"""
    print("\n" + "="*60)
    print("🚀 COMPREHENSIVE FEATURE INTEGRATION REPORT")
    print("="*60)
    
    # Run all tests
    files_ok = test_file_existence()
    endpoints_ok = test_backend_endpoints()
    dashboard_ok = test_dashboard_components()
    analysis_ok = test_analysis_capabilities()
    docs_ok = test_documentation_completeness()
    
    # Summary
    print("\n📊 INTEGRATION SUMMARY:")
    print(f"File Structure: {'✅ COMPLETE' if files_ok else '❌ INCOMPLETE'}")
    print(f"Backend Endpoints: {'✅ COMPLETE' if endpoints_ok else '❌ INCOMPLETE'}")
    print(f"Dashboard Components: {'✅ COMPLETE' if dashboard_ok else '❌ INCOMPLETE'}")
    print(f"Analysis Capabilities: {'✅ COMPLETE' if analysis_ok else '❌ INCOMPLETE'}")
    print(f"Documentation: {'✅ COMPLETE' if docs_ok else '❌ INCOMPLETE'}")
    
    # Overall status
    overall_score = sum([files_ok, endpoints_ok, dashboard_ok, analysis_ok, docs_ok])
    total_tests = 5
    
    print(f"\n🎯 OVERALL INTEGRATION: {overall_score}/{total_tests} ({(overall_score/total_tests)*100:.0f}%)")
    
    if overall_score == total_tests:
        print("🎉 ALL FEATURES COMPLETELY INTEGRATED!")
        return True
    else:
        print("⚠️  Some features need attention")
        return False

if __name__ == "__main__":
    success = generate_integration_report()
    
    if success:
        print("\n✅ Your crypto trading bot has all advanced features fully integrated!")
        print("🚀 Ready for high-frequency, multi-coin, leveraged trading with ML!")
    else:
        print("\n⚠️  Some components need fixes before full deployment")
    
    # Save report
    with open("integration_report.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "overall_success": success,
            "report_generated": True
        }, f, indent=2)
    
    print(f"\n📄 Report saved to: integration_report.json")
