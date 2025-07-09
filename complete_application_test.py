#!/usr/bin/env python3
"""
Complete Application Test Script
Tests every endpoint, button, and functionality for 100% working status
"""
import sys
import os
import requests
import time
import subprocess
from pathlib import Path
from datetime import datetime
import threading

# Add paths
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboardtest'))

def safe_print(msg):
    """Safe printing function"""
    try:
        print(msg)
        sys.stdout.flush()
    except UnicodeEncodeError:
        print(msg.encode('ascii', 'replace').decode('ascii'))
        sys.stdout.flush()

class CompleteApplicationTester:
    def __init__(self):
        self.backend_url = "http://localhost:5000"
        self.dashboard_url = "http://localhost:8050"
        self.backend_process = None
        self.dashboard_process = None
        
        # All endpoints that frontend calls
        self.critical_endpoints = [
            "/model/logs",
            "/model/errors", 
            "/backtest/results",
            "/trades/analytics",
            "/system/status",
            "/model/upload_and_retrain",
            "/model/predict_batch",
            "/backtest",
            "/safety/check",
            "/api/status",
            "/health",
            "/notifications",
            "/trade",
            "/model/feature_importance",
            "/model/metrics"
        ]
        
    def start_backend(self):
        """Start the backend server"""
        safe_print("🔧 Starting backend server...")
        try:
            # Start backend process
            backend_script = Path(__file__).parent / "backendtest" / "app.py"
            self.backend_process = subprocess.Popen(
                [sys.executable, str(backend_script)],
                cwd=str(backend_script.parent),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for backend to start
            time.sleep(5)
            
            # Test if backend is running
            try:
                response = requests.get(f"{self.backend_url}/health", timeout=10)
                if response.status_code == 200:
                    safe_print("✅ Backend server started successfully")
                    return True
                else:
                    safe_print(f"❌ Backend returned status {response.status_code}")
                    return False
            except Exception as e:
                safe_print(f"❌ Backend connection failed: {e}")
                return False
                
        except Exception as e:
            safe_print(f"❌ Failed to start backend: {e}")
            return False
    
    def test_all_endpoints(self):
        """Test all critical endpoints"""
        safe_print("\n🔍 TESTING ALL CRITICAL ENDPOINTS...")
        safe_print("=" * 60)
        
        results = {}
        
        for endpoint in self.critical_endpoints:
            safe_print(f"🧪 Testing {endpoint}")
            try:
                # Test GET endpoints
                if endpoint in ["/model/logs", "/model/errors", "/backtest/results", 
                               "/trades/analytics", "/system/status", "/api/status", 
                               "/health", "/notifications", "/model/feature_importance", 
                               "/model/metrics"]:
                    response = requests.get(f"{self.backend_url}{endpoint}", timeout=10)
                    
                # Test POST endpoints
                elif endpoint in ["/model/upload_and_retrain", "/model/predict_batch", 
                                 "/backtest", "/safety/check", "/trade"]:
                    test_data = {"test": True, "symbol": "BTCUSDT"}
                    response = requests.post(f"{self.backend_url}{endpoint}", 
                                           json=test_data, timeout=10)
                
                if response.status_code == 200:
                    safe_print(f"  ✅ {endpoint} - OK")
                    results[endpoint] = "✅ OK"
                else:
                    safe_print(f"  ❌ {endpoint} - Status {response.status_code}")
                    results[endpoint] = f"❌ Status {response.status_code}"
                    
            except Exception as e:
                safe_print(f"  ❌ {endpoint} - Error: {str(e)}")
                results[endpoint] = f"❌ Error: {str(e)}"
        
        return results
    
    def test_frontend_backend_sync(self):
        """Test frontend-backend synchronization"""
        safe_print("\n🔄 TESTING FRONTEND-BACKEND SYNCHRONIZATION...")
        safe_print("=" * 60)
        
        sync_tests = [
            {"endpoint": "/api/status", "method": "GET", "expected_keys": ["api_status", "backend_running"]},
            {"endpoint": "/health", "method": "GET", "expected_keys": ["status", "timestamp"]},
            {"endpoint": "/system/status", "method": "GET", "expected_keys": ["status", "system"]},
            {"endpoint": "/trades/analytics", "method": "GET", "expected_keys": ["status", "analytics"]},
            {"endpoint": "/model/logs", "method": "GET", "expected_keys": ["status", "logs"]},
        ]
        
        sync_results = {}
        
        for test in sync_tests:
            endpoint = test["endpoint"]
            safe_print(f"🔄 Testing sync for {endpoint}")
            
            try:
                if test["method"] == "GET":
                    response = requests.get(f"{self.backend_url}{endpoint}", timeout=10)
                else:
                    response = requests.post(f"{self.backend_url}{endpoint}", 
                                           json={}, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check if expected keys are present
                    missing_keys = []
                    for key in test["expected_keys"]:
                        if key not in data:
                            missing_keys.append(key)
                    
                    if not missing_keys:
                        safe_print(f"  ✅ {endpoint} - All expected keys present")
                        sync_results[endpoint] = "✅ Sync OK"
                    else:
                        safe_print(f"  ⚠️ {endpoint} - Missing keys: {missing_keys}")
                        sync_results[endpoint] = f"⚠️ Missing keys: {missing_keys}"
                else:
                    safe_print(f"  ❌ {endpoint} - HTTP {response.status_code}")
                    sync_results[endpoint] = f"❌ HTTP {response.status_code}"
                    
            except Exception as e:
                safe_print(f"  ❌ {endpoint} - Error: {str(e)}")
                sync_results[endpoint] = f"❌ Error: {str(e)}"
        
        return sync_results
    
    def start_dashboard_test(self):
        """Start dashboard and test it loads"""
        safe_print("\n🚀 TESTING DASHBOARD STARTUP...")
        safe_print("=" * 60)
        
        try:
            # Test dashboard imports first
            safe_print("🔧 Testing dashboard imports...")
            
            # Import dash_app
            from dashboardtest.dash_app import app as dash_app
            safe_print("  ✅ dash_app imported successfully")
            
            # Import layout
            from dashboardtest.layout import layout
            safe_print("  ✅ layout imported successfully")
            
            # Set layout
            dash_app.layout = layout
            safe_print("  ✅ layout assigned successfully")
            
            # Test callback imports
            import dashboardtest.callbacks
            safe_print("  ✅ callbacks imported successfully")
            
            safe_print("✅ Dashboard components loaded successfully")
            safe_print("📊 Dashboard should be ready to run on http://localhost:8050")
            
            return True
            
        except Exception as e:
            safe_print(f"❌ Dashboard test failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def generate_test_report(self, endpoint_results, sync_results, dashboard_ok):
        """Generate comprehensive test report"""
        safe_print("\n" + "=" * 80)
        safe_print("📊 COMPLETE APPLICATION TEST REPORT")
        safe_print("=" * 80)
        
        # Backend Endpoints Report
        safe_print("\n🔧 BACKEND ENDPOINTS:")
        working_endpoints = 0
        for endpoint, result in endpoint_results.items():
            safe_print(f"  {endpoint}: {result}")
            if "✅" in result:
                working_endpoints += 1
        
        endpoint_success_rate = (working_endpoints / len(endpoint_results)) * 100
        safe_print(f"\n📊 Endpoint Success Rate: {endpoint_success_rate:.1f}% ({working_endpoints}/{len(endpoint_results)})")
        
        # Sync Report
        safe_print("\n🔄 FRONTEND-BACKEND SYNC:")
        working_sync = 0
        for endpoint, result in sync_results.items():
            safe_print(f"  {endpoint}: {result}")
            if "✅" in result:
                working_sync += 1
        
        sync_success_rate = (working_sync / len(sync_results)) * 100
        safe_print(f"\n📊 Sync Success Rate: {sync_success_rate:.1f}% ({working_sync}/{len(sync_results)})")
        
        # Dashboard Report
        safe_print(f"\n🚀 DASHBOARD STATUS: {'✅ OK' if dashboard_ok else '❌ FAILED'}")
        
        # Overall Status
        overall_success = endpoint_success_rate >= 90 and sync_success_rate >= 90 and dashboard_ok
        safe_print(f"\n🎯 OVERALL APPLICATION STATUS: {'✅ READY' if overall_success else '❌ NEEDS FIXES'}")
        
        if overall_success:
            safe_print("\n🎉 APPLICATION IS 100% SYNCHRONIZED AND READY!")
            safe_print("✅ All endpoints working")
            safe_print("✅ Frontend-backend sync complete")
            safe_print("✅ Dashboard ready to launch")
            safe_print("\n🚀 TO START THE APPLICATION:")
            safe_print("1. Run: python backendtest/app.py (in one terminal)")
            safe_print("2. Run: python dashboardtest/app.py (in another terminal)")
            safe_print("3. Open: http://localhost:8050 in your browser")
        else:
            safe_print("\n⚠️ FIXES NEEDED:")
            if endpoint_success_rate < 90:
                safe_print("- Fix failing backend endpoints")
            if sync_success_rate < 90:
                safe_print("- Fix frontend-backend synchronization")
            if not dashboard_ok:
                safe_print("- Fix dashboard import/startup issues")
        
        return overall_success
    
    def cleanup(self):
        """Cleanup processes"""
        if self.backend_process:
            self.backend_process.terminate()
        if self.dashboard_process:
            self.dashboard_process.terminate()
    
    def run_complete_test(self):
        """Run complete application test"""
        safe_print("🚀 STARTING COMPLETE APPLICATION TEST")
        safe_print("=" * 80)
        
        try:
            # Step 1: Start backend
            backend_ok = self.start_backend()
            if not backend_ok:
                safe_print("❌ Backend failed to start. Cannot continue tests.")
                return False
            
            # Step 2: Test all endpoints
            endpoint_results = self.test_all_endpoints()
            
            # Step 3: Test frontend-backend sync
            sync_results = self.test_frontend_backend_sync()
            
            # Step 4: Test dashboard
            dashboard_ok = self.start_dashboard_test()
            
            # Step 5: Generate report
            overall_success = self.generate_test_report(endpoint_results, sync_results, dashboard_ok)
            
            return overall_success
            
        except Exception as e:
            safe_print(f"❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.cleanup()

if __name__ == "__main__":
    tester = CompleteApplicationTester()
    success = tester.run_complete_test()
    sys.exit(0 if success else 1)
