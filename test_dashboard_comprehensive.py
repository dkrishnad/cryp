#!/usr/bin/env python3
"""
Comprehensive Dashboard Functionality Test
Tests all critical buttons, controls, and data displays across all tabs
"""

import requests
import json
import time
from typing import Dict, Any

class DashboardTester:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.results = {
            "tests_passed": 0,
            "tests_failed": 0,
            "errors": [],
            "details": {}
        }
    
    def test_endpoint(self, endpoint: str, method: str = "GET", data: Dict[Any, Any] = None, timeout: int = 5) -> Dict[str, Any]:
        """Test a backend endpoint"""
        url = f"{self.base_url}{endpoint}"
        try:
            if method == "GET":
                response = requests.get(url, timeout=timeout)
            elif method == "POST":
                response = requests.post(url, json=data or {}, timeout=timeout)
            
            return {
                "success": response.status_code in [200, 201],
                "status_code": response.status_code,
                "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            }
        except Exception as e:
            return {
                "success": False,
                "status_code": None,
                "error": str(e)
            }
    
    def run_tests(self):
        """Run comprehensive tests across all dashboard features"""
        print("🧪 COMPREHENSIVE DASHBOARD FUNCTIONALITY TEST")
        print("=" * 60)
        
        # Test Dashboard Tab Features
        print("\n📊 TESTING DASHBOARD TAB")
        print("-" * 30)
        
        # Test Price API
        result = self.test_endpoint("/price?symbol=BTCUSDT")
        self.log_test("Price API", result)
        
        # Test Technical Indicators
        result = self.test_endpoint("/features/indicators?symbol=BTCUSDT")
        self.log_test("Technical Indicators", result)
        
        # Test Virtual Balance
        result = self.test_endpoint("/virtual_balance")
        self.log_test("Virtual Balance Fetch", result)
        
        # Test ML Prediction Tab Features  
        print("\n🤖 TESTING ML PREDICTION TAB")
        print("-" * 30)
        
        # Test Model Analytics
        result = self.test_endpoint("/model/analytics")
        self.log_test("Model Analytics", result)
        
        # Test Batch Prediction
        sample_data = {
            "data": [
                {"open": 50000, "high": 51000, "low": 49000, "close": 50500, "volume": 1000}
            ]        }
        result = self.test_endpoint("/model/predict_batch", "POST", sample_data)
        self.log_test("Batch Prediction", result)
        
        # Test Auto Trading Tab Features
        print("\n🚀 TESTING AUTO TRADING TAB")
        print("-" * 30)
        
        # Test Auto Trading Status
        result = self.test_endpoint("/auto_trading/status")
        self.log_test("Auto Trading Status", result)
        
        # Test Current Signal
        result = self.test_endpoint("/auto_trading/current_signal")
        self.log_test("Current Trading Signal", result)
        
        # Test Auto Trading Settings
        settings_data = {
            "enabled": False,
            "symbol": "BTCUSDT",
            "entry_threshold": 0.7,
            "exit_threshold": 0.3,
            "max_positions": 3,
            "risk_per_trade": 0.02,
            "amount_config": {
                "type": "fixed",
                "value": 100
            }
        }
        result = self.test_endpoint("/auto_trading/settings", "POST", settings_data)
        self.log_test("Auto Trading Settings", result)
        
        # Test Trade-related endpoints
        print("\n📈 TESTING TRADE OPERATIONS")
        print("-" * 30)
        
        # Test Get Trades
        result = self.test_endpoint("/trades")
        self.log_test("Get Trades", result)
        
        # Test Trade Analytics
        result = self.test_endpoint("/trades/analytics")
        self.log_test("Trade Analytics", result)
        
        # Test Email Configuration
        print("\n📧 TESTING EMAIL CONFIGURATION")
        print("-" * 30)
        
        # Test Email Notifications Setting
        result = self.test_endpoint("/settings/email_notifications")
        self.log_test("Email Notifications Get", result)
        
        # Test Email Address Setting
        result = self.test_endpoint("/settings/email_address")
        self.log_test("Email Address Get", result)
        
        # Test Backtest Features
        print("\n🔄 TESTING BACKTEST FEATURES")
        print("-" * 30)
          # Test Regular Backtest
        backtest_data = {
            "symbol": "BTCUSDT",
            "days": 7,
            "initial_balance": 1000
        }
        result = self.test_endpoint("/backtest", "POST", backtest_data)
        self.log_test("Backtest", result)
        
        # Print Summary
        self.print_summary()
    
    def log_test(self, test_name: str, result: Dict[str, Any]):
        """Log test result"""
        if result.get("success", False):
            print(f"   ✅ {test_name}")
            self.results["tests_passed"] += 1
        else:
            error_msg = result.get('error', f'Status {result.get("status_code", "Unknown")}')
            print(f"   ❌ {test_name}: {error_msg}")
            self.results["tests_failed"] += 1
            self.results["errors"].append({
                "test": test_name,
                "error": result.get("error", result.get("response", "Unknown error"))
            })
        
        self.results["details"][test_name] = result
    
    def print_summary(self):
        """Print test summary"""
        total_tests = self.results["tests_passed"] + self.results["tests_failed"]
        success_rate = (self.results["tests_passed"] / total_tests * 100) if total_tests > 0 else 0
        
        print("\n" + "=" * 60)
        print("🎯 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {self.results['tests_passed']}")
        print(f"❌ Failed: {self.results['tests_failed']}")
        print(f"📊 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🏆 EXCELLENT - Dashboard is fully functional!")
        elif success_rate >= 75:
            print("🟡 GOOD - Most features working, minor issues detected")
        elif success_rate >= 50:
            print("🟠 FAIR - Significant issues detected")
        else:
            print("🔴 POOR - Major functionality problems")
        
        if self.results["errors"]:
            print("\n🐛 ERRORS DETECTED:")
            for error in self.results["errors"]:
                print(f"   • {error['test']}: {error['error']}")
        
        # Save detailed results
        with open("dashboard_test_results.json", "w") as f:
            json.dump(self.results, f, indent=2)
        print(f"\n📄 Detailed results saved to: dashboard_test_results.json")

def main():
    """Main test execution"""
    print("⏳ Waiting for backend to be ready...")
    time.sleep(2)
    
    tester = DashboardTester()
    tester.run_tests()
    
    print("\n🌐 Dashboard URL: http://127.0.0.1:8050")
    print("💡 Manual testing recommended for UI interactions and real-time updates")

if __name__ == "__main__":
    main()
