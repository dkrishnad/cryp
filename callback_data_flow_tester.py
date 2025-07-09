#!/usr/bin/env python3
"""
Comprehensive Callback and Data Flow Test Script
Tests all interactive elements, callbacks, and real-time data flows
"""

import asyncio
import websockets
import json
import requests
import time
from datetime import datetime

class CallbackDataFlowTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []
        
    def log_test(self, test_name, success, details=""):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        
    async def test_websocket_connections(self):
        """Test all WebSocket connections for real-time data"""
        print("
=== TESTING WEBSOCKET CONNECTIONS ===")
        
        websocket_endpoints = [
            "/websocket/price_feed",
            "/websocket/trade_signals", 
            "/websocket/notifications"
        ]
        
        for endpoint in websocket_endpoints:
            try:
                ws_url = self.base_url.replace("http://", "ws://") + endpoint
                async with websockets.connect(ws_url) as websocket:
                    # Wait for a message
                    message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    data = json.loads(message)
                    self.log_test(f"WebSocket {endpoint}", True, f"Received: {type(data)}")
            except Exception as e:
                self.log_test(f"WebSocket {endpoint}", False, str(e))
                
    def test_callback_endpoints(self):
        """Test callback endpoints"""
        print("
=== TESTING CALLBACK ENDPOINTS ===")
        
        callback_tests = [
            {
                "endpoint": "/api/callbacks/button_click",
                "data": {"button_id": "start_trading", "action": "click"}
            },
            {
                "endpoint": "/api/callbacks/chart_update", 
                "data": {"chart_type": "candlestick", "timeframe": "1h", "symbol": "BTCUSDT"}
            },
            {
                "endpoint": "/api/callbacks/data_refresh",
                "data": {"component": "portfolio"}
            }
        ]
        
        for test in callback_tests:
            try:
                response = requests.post(
                    self.base_url + test["endpoint"],
                    json=test["data"],
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    success = data.get("status") == "success"
                    self.log_test(f"Callback {test['endpoint']}", success, f"Status: {response.status_code}")
                else:
                    self.log_test(f"Callback {test['endpoint']}", False, f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Callback {test['endpoint']}", False, str(e))
                
    def test_data_flow_endpoints(self):
        """Test real-time data flow endpoints"""
        print("
=== TESTING DATA FLOW ENDPOINTS ===")
        
        data_flow_endpoints = [
            "/api/realtime/prices",
            "/api/realtime/orderbook",
            "/api/portfolio/real_time_value",
            "/api/trading/active_orders",
            "/api/analytics/performance_metrics",
            "/api/charts/candlestick_stream"
        ]
        
        for endpoint in data_flow_endpoints:
            try:
                response = requests.get(self.base_url + endpoint, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    success = data.get("status") == "success"
                    self.log_test(f"Data Flow {endpoint}", success, f"Data received: {len(str(data))} chars")
                else:
                    self.log_test(f"Data Flow {endpoint}", False, f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Data Flow {endpoint}", False, str(e))
                
    def test_dashboard_button_callbacks(self):
        """Test all dashboard button callbacks"""
        print("
=== TESTING DASHBOARD BUTTON CALLBACKS ===")
        
        button_tests = [
            {"button_id": "start_auto_trading", "action": "start"},
            {"button_id": "stop_auto_trading", "action": "stop"},
            {"button_id": "refresh_portfolio", "action": "refresh"},
            {"button_id": "export_data", "action": "export"},
            {"button_id": "run_backtest", "action": "execute"},
            {"button_id": "send_alert", "action": "send"},
            {"button_id": "clear_notifications", "action": "clear"}
        ]
        
        for button in button_tests:
            try:
                response = requests.post(
                    self.base_url + "/api/callbacks/button_click",
                    json=button,
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    success = data.get("status") == "success"
                    self.log_test(f"Button {button['button_id']}", success, f"Action: {button['action']}")
                else:
                    self.log_test(f"Button {button['button_id']}", False, f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Button {button['button_id']}", False, str(e))
                
    async def run_comprehensive_test(self):
        """Run all callback and data flow tests"""
        print("🚀 STARTING COMPREHENSIVE CALLBACK AND DATA FLOW TESTS")
        print("="*60)
        
        # Test WebSocket connections
        await self.test_websocket_connections()
        
        # Test callback endpoints
        self.test_callback_endpoints()
        
        # Test data flow endpoints
        self.test_data_flow_endpoints()
        
        # Test dashboard button callbacks
        self.test_dashboard_button_callbacks()
        
        # Generate report
        return self.generate_test_report()
        
    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("
=== GENERATING TEST REPORT ===")
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        report = {
            "test_date": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": round(success_rate, 2)
            },
            "test_results": self.test_results,
            "status": "EXCELLENT" if success_rate >= 95 else "GOOD" if success_rate >= 85 else "NEEDS_WORK"
        }
        
        # Save report
        with open("CALLBACK_DATA_FLOW_TEST_REPORT.json", "w") as f:
            json.dump(report, f, indent=2)
            
        # Print summary
        print("\n" + "="*60)
        print("CALLBACK AND DATA FLOW TEST SUMMARY")
        print("="*60)
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        print(f"🎯 Status: {report['status']}")
        
        return report

async def main():
    """Main test execution"""
    tester = CallbackDataFlowTester()
    report = await tester.run_comprehensive_test()
    
    print("\n✅ CALLBACK AND DATA FLOW TESTING COMPLETED")
    print("📄 Report saved to: CALLBACK_DATA_FLOW_TEST_REPORT.json")
    
    return report

if __name__ == "__main__":
    asyncio.run(main())
