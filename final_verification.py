#!/usr/bin/env python3
"""
Final Verification and Status Report
Tests all components and generates comprehensive status
"""

import os
import sys
import json
import importlib
from datetime import datetime

def test_backend_components():
    """Test all backend components"""
    
    print("🧪 TESTING BACKEND COMPONENTS")
    print("=" * 40)
    
    # Add backend to path
    backend_path = r"c:\Users\Hari\Desktop\Test.binnew\Testin dub\backendtest"
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)
    
    test_results = {}
    
    # Test 1: Main module
    try:
        import main
        test_results["main.py"] = {"status": "SUCCESS", "details": "Imports without errors"}
        print("✅ main.py - SUCCESS")
    except Exception as e:
        test_results["main.py"] = {"status": "ERROR", "details": str(e)}
        print(f"❌ main.py - ERROR: {e}")
    
    # Test 2: Router modules
    router_modules = [
        "routes.advanced_auto_trading_routes",
        "routes.ml_prediction_routes",
        "routes.system_routes", 
        "routes.hft_analysis_routes",
        "routes.data_collection_routes",
        "routes.futures_trading_routes",
        "routes.settings_notifications_routes"
    ]
    
    for module_name in router_modules:
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, 'router'):
                test_results[module_name] = {"status": "SUCCESS", "details": "Router available"}
                print(f"✅ {module_name} - SUCCESS")
            else:
                test_results[module_name] = {"status": "WARNING", "details": "No router found"}
                print(f"⚠️ {module_name} - WARNING: No router")
        except Exception as e:
            test_results[module_name] = {"status": "ERROR", "details": str(e)}
            print(f"❌ {module_name} - ERROR: {e}")
    
    # Test 3: Core modules
    core_modules = ["db", "trading", "ml", "data_collection", "futures_trading"]
    
    for module_name in core_modules:
        try:
            module = importlib.import_module(module_name)
            test_results[module_name] = {"status": "SUCCESS", "details": "Core module available"}
            print(f"✅ {module_name} - SUCCESS")
        except Exception as e:
            test_results[module_name] = {"status": "ERROR", "details": str(e)}
            print(f"❌ {module_name} - ERROR: {e}")
    
    return test_results

def check_endpoint_coverage():
    """Check endpoint coverage and missing functionality"""
    
    print("\n🔍 CHECKING ENDPOINT COVERAGE")
    print("=" * 40)
    
    # Critical dashboard endpoints that must exist
    critical_endpoints = {
        "Basic Operations": [
            "/", "/health", "/balance", "/trades", "/portfolio"
        ],
        "Auto Trading": [
            "/auto_trading/status", "/auto_trading/toggle", "/auto_trading/settings"
        ],
        "Advanced Auto Trading": [
            "/advanced_auto_trading/status", "/advanced_auto_trading/start", "/advanced_auto_trading/stop"
        ],
        "ML & Prediction": [
            "/ml/predict", "/ml/online/stats", "/ml/performance/history"
        ],
        "HFT Analysis": [
            "/hft/status", "/hft/start", "/hft/stop", "/hft/analytics"
        ],
        "Data Collection": [
            "/data/collection/start", "/data/collection/stop", "/features/indicators"
        ],
        "Futures Trading": [
            "/futures/positions", "/futures/execute", "/fapi/v2/account"
        ],
        "Risk Management": [
            "/risk/portfolio_metrics", "/risk/calculate_position_size"
        ],
        "Notifications": [
            "/notifications", "/api/email/config", "/api/alerts/history"
        ]
    }
    
    # Try to check if endpoints exist by testing main module
    endpoint_status = {}
    
    try:
        # Import the main module to check its app
        import main
        
        if hasattr(main, 'app'):
            app = main.app
            routes = []
            
            # Extract routes from FastAPI app
            for route in app.routes:
                if hasattr(route, 'path'):
                    routes.append(route.path)
            
            for category, endpoints in critical_endpoints.items():
                category_status = {}
                for endpoint in endpoints:
                    if endpoint in routes:
                        category_status[endpoint] = "AVAILABLE"
                    else:
                        category_status[endpoint] = "MISSING"
                endpoint_status[category] = category_status
        else:
            endpoint_status = {"error": "No FastAPI app found in main module"}
    
    except Exception as e:
        endpoint_status = {"error": f"Could not check endpoints: {e}"}
    
    # Print endpoint status
    for category, endpoints in endpoint_status.items():
        if category == "error":
            print(f"❌ ERROR: {endpoints}")
            continue
            
        available = sum(1 for status in endpoints.values() if status == "AVAILABLE")
        total = len(endpoints)
        print(f"📊 {category}: {available}/{total} endpoints available")
        
        for endpoint, status in endpoints.items():
            if status == "AVAILABLE":
                print(f"   ✅ {endpoint}")
            else:
                print(f"   ❌ {endpoint}")
    
    return endpoint_status

def check_dashboard_compatibility():
    """Check dashboard compatibility"""
    
    print("\n🎯 CHECKING DASHBOARD COMPATIBILITY")
    print("=" * 40)
    
    dashboard_path = r"c:\Users\Hari\Desktop\Test.binnew\Testin dub\dashboardtest"
    
    compatibility_status = {}
    
    # Check if dashboard files exist
    critical_dashboard_files = [
        "app.py", "layout.py", "callbacks.py",
        "auto_trading_layout.py", "futures_trading_layout.py",
        "hybrid_learning_layout.py"
    ]
    
    for file in critical_dashboard_files:
        file_path = os.path.join(dashboard_path, file)
        if os.path.exists(file_path):
            compatibility_status[file] = "AVAILABLE"
            print(f"✅ {file} - AVAILABLE")
        else:
            compatibility_status[file] = "MISSING"
            print(f"❌ {file} - MISSING")
    
    return compatibility_status

def generate_comprehensive_status_report():
    """Generate comprehensive status report"""
    
    print("\n📄 GENERATING COMPREHENSIVE STATUS REPORT")
    print("=" * 50)
    
    # Run all tests
    backend_results = test_backend_components()
    endpoint_coverage = check_endpoint_coverage()
    dashboard_compatibility = check_dashboard_compatibility()
    
    # Calculate overall status
    backend_success = sum(1 for r in backend_results.values() if r["status"] == "SUCCESS")
    backend_total = len(backend_results)
    
    overall_status = "EXCELLENT" if backend_success == backend_total else "GOOD" if backend_success > backend_total * 0.8 else "NEEDS_ATTENTION"
    
    # Create comprehensive report
    report = {
        "report_date": datetime.now().isoformat(),
        "overall_status": overall_status,
        "backend_components": {
            "total_tested": backend_total,
            "successful": backend_success,
            "success_rate": f"{backend_success/backend_total*100:.1f}%",
            "details": backend_results
        },
        "endpoint_coverage": endpoint_coverage,
        "dashboard_compatibility": dashboard_compatibility,
        "recommendations": [],
        "next_steps": []
    }
    
    # Add recommendations based on results
    if overall_status == "EXCELLENT":
        report["recommendations"] = [
            "🎉 All systems operational!",
            "Ready for production testing",
            "Consider load testing"
        ]
        report["next_steps"] = [
            "Start backend: python backendtest/main.py",
            "Start dashboard: python dashboardtest/app.py", 
            "Test all functionality"
        ]
    elif overall_status == "GOOD":
        report["recommendations"] = [
            "⚠️ Minor issues detected",
            "Fix any missing components",
            "Test critical functionality"
        ]
        report["next_steps"] = [
            "Review error details",
            "Fix critical components",
            "Re-run verification"
        ]
    else:
        report["recommendations"] = [
            "🚨 Significant issues detected",
            "Critical components need attention",
            "Do not deploy until fixed"
        ]
        report["next_steps"] = [
            "Fix all ERROR status components",
            "Re-run comprehensive fix",
            "Verify all functionality"
        ]
    
    # Save report
    report_path = r"c:\Users\Hari\Desktop\Test.binnew\Testin dub\FINAL_VERIFICATION_STATUS_REPORT.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print("\n" + "=" * 60)
    print("FINAL COMPREHENSIVE STATUS REPORT")
    print("=" * 60)
    print(f"🎯 Overall Status: {overall_status}")
    print(f"📊 Backend Success Rate: {report['backend_components']['success_rate']}")
    print(f"📅 Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n🔍 RECOMMENDATIONS:")
    for rec in report["recommendations"]:
        print(f"   {rec}")
    
    print("\n📋 NEXT STEPS:")
    for step in report["next_steps"]:
        print(f"   • {step}")
    
    print(f"\n📄 Detailed report saved to: FINAL_VERIFICATION_STATUS_REPORT.json")
    
    return report

if __name__ == "__main__":
    print("🚀 FINAL COMPREHENSIVE VERIFICATION")
    print("=" * 60)
    
    report = generate_comprehensive_status_report()
    
    print("\n✅ VERIFICATION COMPLETE!")
