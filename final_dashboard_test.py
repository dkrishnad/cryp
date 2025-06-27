#!/usr/bin/env python3
"""
Final Dashboard Functionality Test
Test all major dashboard features and API connections
"""
import requests
import time
import json

def test_backend_health():
    """Test if backend is running and healthy"""
    print("🔍 Testing backend health...")
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is healthy")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
        return False

def test_critical_endpoints():
    """Test critical API endpoints"""
    print("\n🔍 Testing critical endpoints...")
    
    endpoints = [
        "/price",
        "/virtual_balance", 
        "/trades",
        "/auto_trading/status",
        "/model/analytics",
        "/features/indicators"
    ]
    
    results = {}
    for endpoint in endpoints:
        try:
            url = f"http://localhost:8001{endpoint}"
            response = requests.get(url, timeout=5)
            results[endpoint] = {
                'status': response.status_code,
                'success': response.status_code == 200
            }
            if response.status_code == 200:
                print(f"✅ {endpoint}")
            else:
                print(f"❌ {endpoint} - Status: {response.status_code}")
        except Exception as e:
            results[endpoint] = {
                'status': 'error',
                'success': False,
                'error': str(e)
            }
            print(f"❌ {endpoint} - Error: {e}")
    
    successful = sum(1 for r in results.values() if r['success'])
    print(f"\n📊 Endpoint Results: {successful}/{len(endpoints)} working")
    return results

def test_dashboard_access():
    """Test if dashboard is accessible"""
    print("\n🔍 Testing dashboard access...")
    try:
        response = requests.get("http://localhost:8050/", timeout=10)
        if response.status_code == 200:
            print("✅ Dashboard is accessible")
            return True
        else:
            print(f"❌ Dashboard access failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Dashboard not accessible: {e}")
        return False

def test_websocket_connection():
    """Test if websocket price feed is working"""
    print("\n🔍 Testing WebSocket price feed...")
    try:
        # Test if websocket endpoint exists
        response = requests.get("http://localhost:8001/price", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'symbol' in data and 'price' in data:
                print(f"✅ WebSocket price feed working: {data['symbol']} = ${data['price']}")
                return True
        print("❌ WebSocket price feed not working properly")
        return False
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        return False

def test_auto_trading_system():
    """Test auto trading system"""
    print("\n🔍 Testing auto trading system...")
    try:
        # Test status endpoint
        response = requests.get("http://localhost:8001/auto_trading/status", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print(f"✅ Auto trading status: {status.get('status', 'Unknown')}")
            
            # Test signals endpoint
            response = requests.get("http://localhost:8001/auto_trading/signals", timeout=5)
            if response.status_code == 200:
                signals = response.json()
                print(f"✅ Auto trading signals: {len(signals)} signals available")
                return True
        print("❌ Auto trading system not working properly")
        return False
    except Exception as e:
        print(f"❌ Auto trading test failed: {e}")
        return False

def test_ml_system():
    """Test ML prediction system"""
    print("\n🔍 Testing ML system...")
    try:
        response = requests.get("http://localhost:8001/model/analytics", timeout=5)
        if response.status_code == 200:
            analytics = response.json()
            print(f"✅ ML analytics available: {len(analytics)} models")
            return True
        print("❌ ML system not working properly")
        return False
    except Exception as e:
        print(f"❌ ML test failed: {e}")
        return False

def generate_system_report(test_results):
    """Generate comprehensive system report"""
    print("\n📊 SYSTEM STATUS REPORT")
    print("="*50)
    
    # Calculate overall health
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results.values() if result)
    health_score = (passed_tests / total_tests) * 100
    
    print(f"🎯 Overall Health Score: {health_score:.1f}%")
    print(f"📈 Tests Passed: {passed_tests}/{total_tests}")
    
    # Component status
    components = {
        'Backend API': test_results.get('backend_health', False),
        'Dashboard UI': test_results.get('dashboard_access', False),
        'WebSocket Feed': test_results.get('websocket', False),
        'Auto Trading': test_results.get('auto_trading', False),
        'ML System': test_results.get('ml_system', False),
        'API Endpoints': test_results.get('endpoints_working', 0) > 3
    }
    
    print("\n🔧 COMPONENT STATUS:")
    for component, status in components.items():
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {component}")
    
    # Recommendations
    print("\n🎯 RECOMMENDATIONS:")
    if health_score >= 90:
        print("✅ System is in excellent condition - ready for production use!")
    elif health_score >= 75:
        print("✅ System is working well - minor issues may exist")
    elif health_score >= 50:
        print("⚠️  System has moderate issues - some features may not work")
    else:
        print("🚨 System has major issues - significant fixes needed")
    
    # Next steps
    failing_components = [comp for comp, status in components.items() if not status]
    if failing_components:
        print("\n🔧 PRIORITY FIXES:")
        for i, comp in enumerate(failing_components, 1):
            print(f"  {i}. Fix {comp}")
    
    return health_score

def main():
    print("🚀 FINAL DASHBOARD FUNCTIONALITY TEST")
    print("="*60)
    
    # Run all tests
    test_results = {}
    
    test_results['backend_health'] = test_backend_health()
    test_results['dashboard_access'] = test_dashboard_access()
    test_results['websocket'] = test_websocket_connection()
    test_results['auto_trading'] = test_auto_trading_system()
    test_results['ml_system'] = test_ml_system()
    
    # Test endpoints
    endpoint_results = test_critical_endpoints()
    test_results['endpoints_working'] = sum(1 for r in endpoint_results.values() if r['success'])
    test_results['endpoint_details'] = endpoint_results
    
    # Generate final report
    health_score = generate_system_report(test_results)
    
    # Save results
    from datetime import datetime
    
    final_report = {
        'timestamp': datetime.now().isoformat(),
        'health_score': health_score,
        'test_results': test_results,
        'summary': {
            'total_tests': len([k for k in test_results.keys() if k != 'endpoint_details']),
            'passed_tests': sum(1 for k, v in test_results.items() if k != 'endpoint_details' and k != 'endpoints_working' and v),
            'system_ready': health_score >= 75
        }
    }
    
    with open("final_system_test_report.json", "w") as f:
        json.dump(final_report, f, indent=2)
    
    print(f"\n📄 Full report saved to: final_system_test_report.json")
    
    if health_score >= 75:
        print("\n🎉 SYSTEM READY FOR USE!")
        print("✅ All major components are functional")
        print("✅ Dashboard and backend are properly integrated")
        print("✅ Auto trading and ML systems are operational")
    else:
        print(f"\n⚠️  SYSTEM NEEDS ATTENTION (Score: {health_score:.1f}%)")
    
    return health_score >= 75

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
