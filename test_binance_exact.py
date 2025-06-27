#!/usr/bin/env python3
"""
Test script for Binance-exact API compatibility
Tests all endpoints to ensure 1:1 compatibility with Binance Futures API
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8001"

class BinanceExactTester:
    def __init__(self):
        self.session = requests.Session()
        self.results = []
        
    def log_test(self, name, success, message, data=None):
        """Log test result"""
        result = {
            "test": name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        self.results.append(result)
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {name} - {message}")
        
    def test_account_endpoints(self):
        """Test account information endpoints"""
        print("\n" + "="*60)
        print("TESTING ACCOUNT ENDPOINTS")
        print("="*60)
        
        # Test account info
        try:
            response = self.session.get(f"{BASE_URL}/fapi/v2/account")
            if response.status_code == 200:
                data = response.json()
                if "totalWalletBalance" in data and "availableBalance" in data:
                    self.log_test("Account Info", True, "Successfully retrieved account data", data)
                else:
                    self.log_test("Account Info", False, "Missing required fields in account data")
            else:
                self.log_test("Account Info", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Account Info", False, f"Exception: {str(e)}")
            
        # Test balance info
        try:
            response = self.session.get(f"{BASE_URL}/fapi/v2/balance")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Balance Info", True, f"Retrieved {len(data)} balance entries", data)
                else:
                    self.log_test("Balance Info", False, "Balance data should be a list")
            else:
                self.log_test("Balance Info", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Balance Info", False, f"Exception: {str(e)}")
            
    def test_position_endpoints(self):
        """Test position information endpoints"""
        print("\n" + "="*60)
        print("TESTING POSITION ENDPOINTS")
        print("="*60)
        
        # Test position risk (all positions)
        try:
            response = self.session.get(f"{BASE_URL}/fapi/v2/positionRisk")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Position Risk (All)", True, f"Retrieved {len(data)} positions", data)
                else:
                    self.log_test("Position Risk (All)", False, "Position data should be a list")
            else:
                self.log_test("Position Risk (All)", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Position Risk (All)", False, f"Exception: {str(e)}")
            
        # Test position risk for specific symbol
        try:
            response = self.session.get(f"{BASE_URL}/fapi/v2/positionRisk?symbol=BTCUSDT")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Position Risk (BTCUSDT)", True, f"Retrieved {len(data)} BTCUSDT positions", data)
                else:
                    self.log_test("Position Risk (BTCUSDT)", False, "Position data should be a list")
            else:
                self.log_test("Position Risk (BTCUSDT)", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Position Risk (BTCUSDT)", False, f"Exception: {str(e)}")
            
    def test_order_endpoints(self):
        """Test order management endpoints"""
        print("\n" + "="*60)
        print("TESTING ORDER ENDPOINTS")
        print("="*60)
        
        # Test placing a market buy order
        try:
            order_data = {
                "symbol": "BTCUSDT",
                "side": "BUY",
                "type": "MARKET",
                "quantity": "0.001",
                "positionSide": "BOTH"
            }
            response = self.session.post(f"{BASE_URL}/fapi/v1/order", data=order_data)
            if response.status_code == 200:
                data = response.json()
                if "orderId" in data and "status" in data:
                    order_id = data["orderId"]
                    self.log_test("Market Buy Order", True, f"Order placed with ID {order_id}", data)
                    
                    # Test getting open orders
                    time.sleep(0.1)  # Small delay
                    response2 = self.session.get(f"{BASE_URL}/fapi/v1/openOrders")
                    if response2.status_code == 200:
                        orders = response2.json()
                        self.log_test("Get Open Orders", True, f"Retrieved {len(orders)} open orders", orders)
                    else:
                        self.log_test("Get Open Orders", False, f"HTTP {response2.status_code}")
                        
                else:
                    self.log_test("Market Buy Order", False, "Missing orderId or status in response")
            else:
                self.log_test("Market Buy Order", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Market Buy Order", False, f"Exception: {str(e)}")
            
        # Test placing a limit sell order
        try:
            order_data = {
                "symbol": "BTCUSDT",
                "side": "SELL",
                "type": "LIMIT",
                "quantity": "0.001",
                "price": "110000.00",
                "timeInForce": "GTC",
                "positionSide": "BOTH"
            }
            response = self.session.post(f"{BASE_URL}/fapi/v1/order", data=order_data)
            if response.status_code == 200:
                data = response.json()
                if "orderId" in data and "status" in data:
                    order_id = data["orderId"]
                    self.log_test("Limit Sell Order", True, f"Order placed with ID {order_id}", data)
                    
                    # Test canceling the order
                    time.sleep(0.1)  # Small delay
                    cancel_data = {"symbol": "BTCUSDT", "orderId": order_id}
                    response2 = self.session.delete(f"{BASE_URL}/fapi/v1/order", params=cancel_data)
                    if response2.status_code == 200:
                        cancel_result = response2.json()
                        if "status" in cancel_result and cancel_result["status"] == "CANCELED":
                            self.log_test("Cancel Order", True, f"Order {order_id} canceled", cancel_result)
                        else:
                            self.log_test("Cancel Order", False, f"Order not properly canceled: {cancel_result}")
                    else:
                        self.log_test("Cancel Order", False, f"HTTP {response2.status_code}")
                        
                else:
                    self.log_test("Limit Sell Order", False, "Missing orderId or status in response")
            else:
                self.log_test("Limit Sell Order", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Limit Sell Order", False, f"Exception: {str(e)}")
            
    def test_leverage_margin(self):
        """Test leverage and margin endpoints"""
        print("\n" + "="*60)
        print("TESTING LEVERAGE & MARGIN ENDPOINTS")
        print("="*60)
        
        # Test changing leverage
        try:
            leverage_data = {"symbol": "BTCUSDT", "leverage": 20}
            response = self.session.post(f"{BASE_URL}/fapi/v1/leverage", data=leverage_data)
            if response.status_code == 200:
                data = response.json()
                if "leverage" in data:
                    self.log_test("Change Leverage", True, f"Leverage set to {data['leverage']}x", data)
                else:
                    self.log_test("Change Leverage", False, "Missing leverage in response")
            else:
                self.log_test("Change Leverage", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Change Leverage", False, f"Exception: {str(e)}")
            
        # Test changing margin type
        try:
            margin_data = {"symbol": "BTCUSDT", "marginType": "ISOLATED"}
            response = self.session.post(f"{BASE_URL}/fapi/v1/marginType", data=margin_data)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Change Margin Type", True, "Margin type changed to ISOLATED", data)
            else:
                self.log_test("Change Margin Type", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Change Margin Type", False, f"Exception: {str(e)}")
            
    def test_market_data(self):
        """Test market data endpoints"""
        print("\n" + "="*60)
        print("TESTING MARKET DATA ENDPOINTS")
        print("="*60)
        
        # Test 24hr ticker (all symbols)
        try:
            response = self.session.get(f"{BASE_URL}/fapi/v1/ticker/24hr")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    self.log_test("24hr Ticker (All)", True, f"Retrieved {len(data)} tickers", data)
                else:
                    self.log_test("24hr Ticker (All)", False, "No ticker data received")
            else:
                self.log_test("24hr Ticker (All)", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("24hr Ticker (All)", False, f"Exception: {str(e)}")
            
        # Test 24hr ticker (specific symbol)
        try:
            response = self.session.get(f"{BASE_URL}/fapi/v1/ticker/24hr?symbol=BTCUSDT")
            if response.status_code == 200:
                data = response.json()
                if "symbol" in data and data["symbol"] == "BTCUSDT":
                    self.log_test("24hr Ticker (BTCUSDT)", True, "Retrieved BTCUSDT ticker", data)
                else:
                    self.log_test("24hr Ticker (BTCUSDT)", False, "Invalid ticker data")
            else:
                self.log_test("24hr Ticker (BTCUSDT)", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("24hr Ticker (BTCUSDT)", False, f"Exception: {str(e)}")
            
        # Test exchange info
        try:
            response = self.session.get(f"{BASE_URL}/fapi/v1/exchangeInfo")
            if response.status_code == 200:
                data = response.json()
                if "symbols" in data and "timezone" in data:
                    symbol_count = len(data["symbols"])
                    self.log_test("Exchange Info", True, f"Retrieved exchange info with {symbol_count} symbols", 
                                {"symbol_count": symbol_count, "timezone": data["timezone"]})
                else:
                    self.log_test("Exchange Info", False, "Invalid exchange info format")
            else:
                self.log_test("Exchange Info", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Exchange Info", False, f"Exception: {str(e)}")
            
    def test_auto_trading(self):
        """Test auto trading integration"""
        print("\n" + "="*60)
        print("TESTING AUTO TRADING INTEGRATION")
        print("="*60)
        
        # Test auto signal execution
        try:
            signal_data = {
                "symbol": "BTCUSDT",
                "direction": "BUY",
                "confidence": 0.8,
                "price": 107000.0
            }
            response = self.session.post(f"{BASE_URL}/binance/auto_execute", 
                                       json=signal_data,
                                       headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    self.log_test("Auto Signal Execution", True, "Signal executed successfully", data)
                else:
                    self.log_test("Auto Signal Execution", False, f"Execution failed: {data.get('message')}")
            else:
                self.log_test("Auto Signal Execution", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Auto Signal Execution", False, f"Exception: {str(e)}")
            
    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🚀 STARTING BINANCE-EXACT API COMPATIBILITY TESTS")
        print("="*80)
        
        start_time = time.time()
        
        # Run all test suites
        self.test_account_endpoints()
        self.test_position_endpoints()
        self.test_order_endpoints()
        self.test_leverage_margin()
        self.test_market_data()
        self.test_auto_trading()
        
        end_time = time.time()
        
        # Generate summary
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r["success"]])
        failed_tests = total_tests - passed_tests
        
        print("\n" + "="*80)
        print("🎯 TEST SUMMARY")
        print("="*80)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print(f"Duration: {end_time - start_time:.2f} seconds")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['message']}")
        else:
            print("\n✅ ALL TESTS PASSED!")
            
        # Save detailed results
        with open("binance_exact_test_results.json", "w") as f:
            json.dump({
                "summary": {
                    "total_tests": total_tests,
                    "passed_tests": passed_tests,
                    "failed_tests": failed_tests,
                    "success_rate": (passed_tests/total_tests)*100,
                    "duration": end_time - start_time,
                    "timestamp": datetime.now().isoformat()
                },
                "results": self.results
            }, f, indent=2)
            
        print(f"\n📄 Detailed results saved to: binance_exact_test_results.json")
        
        return passed_tests == total_tests

if __name__ == "__main__":
    print("🧪 BINANCE FUTURES API EXACT COMPATIBILITY TEST")
    print("Make sure the backend is running on http://localhost:8000")
    print()
    
    # Check if backend is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ Backend not responding. Please start the backend first.")
            exit(1)
    except:
        print("❌ Cannot connect to backend. Please start the backend first.")
        exit(1)
        
    # Run tests
    tester = BinanceExactTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 ALL BINANCE-EXACT TESTS PASSED! System is ready for real trading.")
    else:
        print("\n⚠️  Some tests failed. Please review and fix before proceeding.")
        
    exit(0 if success else 1)
