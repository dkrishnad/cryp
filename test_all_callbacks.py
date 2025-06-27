#!/usr/bin/env python3
"""
Comprehensive Dashboard-Backend Callback Integration Test
This script tests all major callbacks between the dashboard and backend to ensure full integration.
"""
import requests
import json
from datetime import datetime
import time

API_URL = "http://localhost:8000"

def test_endpoint(endpoint_url, method="GET", data=None, files=None, expected_status=200, description=""):
    """Test a single endpoint and return results"""
    try:
        start_time = time.time()
        
        if method == "GET":
            response = requests.get(endpoint_url, params=data, timeout=5)
        elif method == "POST":
            if files:
                response = requests.post(endpoint_url, files=files, timeout=10)
            else:
                response = requests.post(endpoint_url, json=data, timeout=5)
        elif method == "DELETE":
            response = requests.delete(endpoint_url, timeout=5)
        else:
            return {"status": "error", "message": f"Unsupported method: {method}"}
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        
        result = {
            "endpoint": endpoint_url,
            "method": method,
            "description": description,
            "status_code": response.status_code,
            "response_time": f"{response_time:.2f}ms",
            "expected_status": expected_status,
            "success": response.status_code == expected_status
        }
        
        try:
            result["response_data"] = response.json()
        except:
            result["response_data"] = response.text[:200] + "..." if len(response.text) > 200 else response.text
            
        return result
        
    except Exception as e:
        return {
            "endpoint": endpoint_url,
            "method": method,
            "description": description,
            "status": "error",
            "message": str(e),
            "success": False
        }

def test_all_backend_endpoints():
    """Test all backend endpoints to ensure they're working"""
    
    print("🧪 TESTING ALL BACKEND ENDPOINTS")
    print("=" * 60)
    
    endpoints_to_test = [
        # Core System
        (f"{API_URL}/health", "GET", None, "Health check"),
        
        # Trading & Risk Management
        (f"{API_URL}/virtual_balance", "GET", None, "Get virtual balance"),
        (f"{API_URL}/risk_settings", "GET", None, "Get risk settings"),
        (f"{API_URL}/trades", "GET", None, "Get trades list"),
        (f"{API_URL}/trades/analytics", "GET", None, "Get trade analytics"),
        
        # Price & Market Data  
        (f"{API_URL}/price", "GET", {"symbol": "btcusdt"}, "Get current price"),
        (f"{API_URL}/features/indicators", "GET", {"symbol": "btcusdt"}, "Get technical indicators"),
        
        # ML Traditional
        (f"{API_URL}/model/versions", "GET", None, "Get model versions"),
        (f"{API_URL}/model/active_version", "GET", None, "Get active model version"),
        (f"{API_URL}/model/analytics", "GET", None, "Get model analytics"),
        (f"{API_URL}/model/metrics", "GET", None, "Get model metrics"),
        (f"{API_URL}/model/feature_importance", "GET", None, "Get feature importance"),
        (f"{API_URL}/model/logs", "GET", None, "Get model logs"),
        (f"{API_URL}/model/errors", "GET", None, "Get model errors"),
        (f"{API_URL}/model/upload_status", "GET", None, "Get upload status"),
        
        # Notifications
        (f"{API_URL}/notifications", "GET", None, "Get notifications"),
        
        # Backtesting
        (f"{API_URL}/backtest/results", "GET", None, "Get backtest results"),
        
        # Settings
        (f"{API_URL}/settings/email_notifications", "GET", None, "Get email notification settings"),
        (f"{API_URL}/settings/email_address", "GET", None, "Get email address"),
        
        # Hybrid Learning System
        (f"{API_URL}/ml/hybrid/status", "GET", None, "Get hybrid learning status"),
        (f"{API_URL}/ml/online/stats", "GET", None, "Get online learning stats"),
        (f"{API_URL}/ml/data_collection/stats", "GET", None, "Get data collection stats"),
        (f"{API_URL}/ml/performance/history", "GET", None, "Get performance history"),
        (f"{API_URL}/ml/hybrid/predict", "GET", {"symbol": "btcusdt"}, "Get hybrid prediction"),
        
        # Email System (New)
        (f"{API_URL}/email/config", "GET", None, "Get email configuration"),
    ]
    
    results = []
    passed = 0
    failed = 0
    
    for endpoint_data in endpoints_to_test:
        if len(endpoint_data) == 4:
            url, method, params, description = endpoint_data
        else:
            url, method, params, description = endpoint_data[0], endpoint_data[1], endpoint_data[2], endpoint_data[3]
            
        result = test_endpoint(url, method, params, description=description)
        results.append(result)
        
        status_icon = "✅" if result.get("success", False) else "❌"
        print(f"{status_icon} {description}: {result.get('status_code', 'ERROR')} ({result.get('response_time', 'N/A')})")
        
        if result.get("success", False):
            passed += 1
        else:
            failed += 1
            if "message" in result:
                print(f"   Error: {result['message']}")
    
    print(f"\n📊 BACKEND ENDPOINT RESULTS: {passed} passed, {failed} failed")
    return results

def test_dashboard_callbacks():
    """Test critical dashboard callbacks that use backend endpoints"""
    
    print("\n🎮 TESTING DASHBOARD CALLBACK INTEGRATIONS")
    print("=" * 60)
    
    # Test the key endpoints that dashboard callbacks rely on
    callback_tests = [
        # Dashboard Tab Callbacks
        ("Technical Indicators Display", f"{API_URL}/features/indicators", "GET", {"symbol": "btcusdt"}),
        ("Live Price Display", f"{API_URL}/price", "GET", {"symbol": "btcusdt"}),
        ("Virtual Balance Display", f"{API_URL}/virtual_balance", "GET", None),
        ("Trade List Display", f"{API_URL}/trades", "GET", None),
        ("Notifications Display", f"{API_URL}/notifications", "GET", None),
        
        # ML Tab Callbacks
        ("Model Version Dropdown", f"{API_URL}/model/versions", "GET", None),
        ("Model Analytics Display", f"{API_URL}/model/analytics", "GET", None),
        ("Feature Importance Chart", f"{API_URL}/model/feature_importance", "GET", None),
        ("Model Metrics Display", f"{API_URL}/model/metrics", "GET", None),
        
        # Hybrid Learning Tab Callbacks
        ("Hybrid System Status", f"{API_URL}/ml/hybrid/status", "GET", None),
        ("Online Learning Stats", f"{API_URL}/ml/online/stats", "GET", None),
        ("Data Collection Stats", f"{API_URL}/ml/data_collection/stats", "GET", None),
        ("Performance History Chart", f"{API_URL}/ml/performance/history", "GET", None),
        ("Hybrid Predictions", f"{API_URL}/ml/hybrid/predict", "GET", {"symbol": "btcusdt"}),
        
        # Email Config Tab Callbacks (New)
        ("Email Config Display", f"{API_URL}/email/config", "GET", None),
        
        # Settings Callbacks
        ("Email Settings Display", f"{API_URL}/settings/email_notifications", "GET", None),
        ("Email Address Display", f"{API_URL}/settings/email_address", "GET", None),
    ]
    
    callback_results = []
    cb_passed = 0
    cb_failed = 0
    
    for test_name, url, method, params in callback_tests:
        result = test_endpoint(url, method, params, description=test_name)
        callback_results.append(result)
        
        status_icon = "✅" if result.get("success", False) else "❌"
        print(f"{status_icon} {test_name}: {result.get('status_code', 'ERROR')}")
        
        if result.get("success", False):
            cb_passed += 1
        else:
            cb_failed += 1
            if "message" in result:
                print(f"   Error: {result['message']}")
    
    print(f"\n📊 CALLBACK INTEGRATION RESULTS: {cb_passed} passed, {cb_failed} failed")
    return callback_results

def test_critical_workflows():
    """Test end-to-end workflows that span multiple endpoints"""
    
    print("\n🔄 TESTING CRITICAL WORKFLOWS")
    print("=" * 60)
    
    workflows = []
    
    # Workflow 1: Trading Workflow
    print("\n1. Testing Trading Workflow...")
    workflow_1 = []
    
    # Get current price
    price_result = test_endpoint(f"{API_URL}/price", "GET", {"symbol": "btcusdt"}, description="Get price for trading")
    workflow_1.append(price_result)
    
    # Get technical indicators  
    indicators_result = test_endpoint(f"{API_URL}/features/indicators", "GET", {"symbol": "btcusdt"}, description="Get indicators for trading")
    workflow_1.append(indicators_result)
    
    # Safety check before trade
    if price_result.get("success") and "response_data" in price_result:
        current_price = price_result["response_data"].get("price", 50000)
        safety_result = test_endpoint(f"{API_URL}/safety/check", "POST", {
            "symbol": "btcusdt",
            "direction": "long", 
            "amount": 100,
            "entry_price": current_price,
            "tp_pct": 2.0,
            "sl_pct": 1.0
        }, description="Safety check for trade")
        workflow_1.append(safety_result)
    
    workflows.append(("Trading Workflow", workflow_1))
    
    # Workflow 2: ML Prediction Workflow
    print("\n2. Testing ML Prediction Workflow...")
    workflow_2 = []
    
    # Get model versions
    versions_result = test_endpoint(f"{API_URL}/model/versions", "GET", None, description="Get available models")
    workflow_2.append(versions_result)
    
    # Get hybrid prediction
    hybrid_pred_result = test_endpoint(f"{API_URL}/ml/hybrid/predict", "GET", {"symbol": "btcusdt"}, description="Get hybrid prediction")
    workflow_2.append(hybrid_pred_result)
    
    # Get model metrics
    metrics_result = test_endpoint(f"{API_URL}/model/metrics", "GET", None, description="Get model performance")
    workflow_2.append(metrics_result)
    
    workflows.append(("ML Prediction Workflow", workflow_2))
    
    # Workflow 3: Data Collection & Learning Workflow  
    print("\n3. Testing Data Collection Workflow...")
    workflow_3 = []
    
    # Get data collection stats
    dc_stats_result = test_endpoint(f"{API_URL}/ml/data_collection/stats", "GET", None, description="Get data collection status")
    workflow_3.append(dc_stats_result)
    
    # Get online learning stats
    ol_stats_result = test_endpoint(f"{API_URL}/ml/online/stats", "GET", None, description="Get online learning status")
    workflow_3.append(ol_stats_result)
    
    # Get hybrid system status
    hybrid_status_result = test_endpoint(f"{API_URL}/ml/hybrid/status", "GET", None, description="Get hybrid system status")
    workflow_3.append(hybrid_status_result)
    
    workflows.append(("Data Collection Workflow", workflow_3))
    
    # Summary
    for workflow_name, workflow_results in workflows:
        passed = sum(1 for r in workflow_results if r.get("success", False))
        total = len(workflow_results)
        status_icon = "✅" if passed == total else "⚠️" if passed > 0 else "❌"
        print(f"{status_icon} {workflow_name}: {passed}/{total} steps successful")
    
    return workflows

def generate_integration_report(backend_results, callback_results, workflow_results):
    """Generate a comprehensive integration report"""
    
    print("\n" + "=" * 80)
    print("📋 COMPREHENSIVE INTEGRATION REPORT")
    print("=" * 80)
    
    # Backend Summary
    backend_passed = sum(1 for r in backend_results if r.get("success", False))
    backend_total = len(backend_results)
    backend_pct = (backend_passed / backend_total * 100) if backend_total > 0 else 0
    
    # Callback Summary
    callback_passed = sum(1 for r in callback_results if r.get("success", False))
    callback_total = len(callback_results)
    callback_pct = (callback_passed / callback_total * 100) if callback_total > 0 else 0
    
    # Workflow Summary
    workflow_passed = 0
    workflow_total = 0
    for _, workflow in workflow_results:
        for result in workflow:
            workflow_total += 1
            if result.get("success", False):
                workflow_passed += 1
    workflow_pct = (workflow_passed / workflow_total * 100) if workflow_total > 0 else 0
    
    print(f"\n🎯 OVERALL INTEGRATION STATUS:")
    print(f"   Backend Endpoints:    {backend_passed}/{backend_total} ({backend_pct:.1f}%)")
    print(f"   Dashboard Callbacks:  {callback_passed}/{callback_total} ({callback_pct:.1f}%)")
    print(f"   Critical Workflows:   {workflow_passed}/{workflow_total} ({workflow_pct:.1f}%)")
    
    overall_passed = backend_passed + callback_passed + workflow_passed
    overall_total = backend_total + callback_total + workflow_total
    overall_pct = (overall_passed / overall_total * 100) if overall_total > 0 else 0
    
    print(f"\n📊 TOTAL INTEGRATION:   {overall_passed}/{overall_total} ({overall_pct:.1f}%)")
    
    if overall_pct >= 95:
        status = "🎉 EXCELLENT - Production Ready"
    elif overall_pct >= 85:
        status = "✅ GOOD - Minor fixes needed"
    elif overall_pct >= 70:
        status = "⚠️ FAIR - Some issues to address"
    else:
        status = "❌ POOR - Major issues need fixing"
    
    print(f"\n🏆 INTEGRATION STATUS: {status}")
    
    # Failed endpoints
    failed_endpoints = []
    for result in backend_results + callback_results:
        if not result.get("success", False):
            failed_endpoints.append(result)
    
    if failed_endpoints:
        print(f"\n❌ FAILED ENDPOINTS ({len(failed_endpoints)}):")
        for failed in failed_endpoints[:10]:  # Show first 10
            print(f"   • {failed.get('description', 'Unknown')}: {failed.get('message', 'Error')}")
        if len(failed_endpoints) > 10:
            print(f"   ... and {len(failed_endpoints) - 10} more")
    
    return {
        "backend_integration": backend_pct,
        "callback_integration": callback_pct, 
        "workflow_integration": workflow_pct,
        "overall_integration": overall_pct,
        "status": status,
        "failed_count": len(failed_endpoints)
    }

def main():
    """Main test function"""
    
    print("🚀 STARTING COMPREHENSIVE DASHBOARD-BACKEND INTEGRATION TEST")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Testing backend at: {API_URL}")
    
    try:
        # Test 1: All backend endpoints
        backend_results = test_all_backend_endpoints()
        
        # Test 2: Dashboard callbacks
        callback_results = test_dashboard_callbacks()
        
        # Test 3: Critical workflows
        workflow_results = test_critical_workflows()
        
        # Generate comprehensive report
        report = generate_integration_report(backend_results, callback_results, workflow_results)
        
        print(f"\n⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎉 Integration test completed!")
        
        return report
        
    except requests.exceptions.ConnectionError:
        print("\n❌ CRITICAL ERROR: Cannot connect to backend!")
        print("   Please ensure the backend is running on http://localhost:8000")
        print("   Start with: python backend/main.py")
        return None
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return None

if __name__ == "__main__":
    main()
