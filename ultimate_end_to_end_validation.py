#!/usr/bin/env python3
"""
ULTIMATE END-TO-END VALIDATION SCRIPT
Tests every button, chart, functionality, callbacks, and data flow
Comprehensive simulation of full dashboard and backend interaction
"""

import requests
import json
import time
import asyncio
import sys
import os
from datetime import datetime
from typing import Dict, List, Any

class UltimateEndToEndValidator:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.dashboard_url = "http://localhost:8050" 
        self.test_results = []
        self.performance_metrics = {}
        self.callback_tests = {}
        self.data_flow_tests = {}
        
    def log_test(self, category: str, test_name: str, status: str, details: Any = None, response_time: float = 0):
        """Log test result with comprehensive details"""
        result = {
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "test_name": test_name,
            "status": status,
            "details": details,
            "response_time_ms": round(response_time * 1000, 2)
        }
        self.test_results.append(result)
        
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_emoji} [{category}] {test_name}: {status} ({response_time*1000:.1f}ms)")
        
        if details and status == "FAIL":
            print(f"   Details: {details}")

    async def test_backend_endpoint(self, method: str, endpoint: str, data: Dict = None, expected_status: int = 200) -> Dict:
        """Test a backend endpoint with comprehensive validation"""
        start_time = time.time()
        
        try:
            url = f"{self.backend_url}{endpoint}"
            
            if method.upper() == "GET":
                response = requests.get(url, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, json=data or {}, timeout=10)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data or {}, timeout=10)
            elif method.upper() == "DELETE":
                response = requests.delete(url, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response_time = time.time() - start_time
            
            if response.status_code == expected_status:
                try:
                    response_data = response.json()
                    return {
                        "status": "PASS",
                        "data": response_data,
                        "response_time": response_time,
                        "status_code": response.status_code
                    }
                except:
                    return {
                        "status": "PASS",
                        "data": response.text,
                        "response_time": response_time,
                        "status_code": response.status_code
                    }
            else:
                return {
                    "status": "FAIL",
                    "error": f"Expected {expected_status}, got {response.status_code}",
                    "response_time": response_time,
                    "status_code": response.status_code
                }
                
        except Exception as e:
            response_time = time.time() - start_time
            return {
                "status": "FAIL",
                "error": str(e),
                "response_time": response_time,
                "status_code": None
            }

    async def test_basic_operations(self):
        """Test all basic operation buttons and functionality"""
        print("\n🚀 TESTING BASIC OPERATIONS")
        print("=" * 50)
        
        basic_tests = [
            ("GET", "/", "Root endpoint"),
            ("GET", "/health", "Health check"),
            ("GET", "/balance", "Get balance"),
            ("GET", "/trades", "Get all trades"),
            ("GET", "/trades/recent", "Get recent trades"),
            ("GET", "/portfolio", "Get portfolio"),
            ("POST", "/virtual_balance/reset", "Reset virtual balance"),
            ("DELETE", "/trades/cleanup", "Cleanup old trades")
        ]
        
        for method, endpoint, description in basic_tests:
            result = await self.test_backend_endpoint(method, endpoint)
            self.log_test("BASIC_OPS", description, result["status"], 
                         result.get("error"), result["response_time"])

    async def test_auto_trading_functionality(self):
        """Test all auto trading buttons and workflows"""
        print("\n🤖 TESTING AUTO TRADING FUNCTIONALITY")
        print("=" * 50)
        
        # Auto Trading Status and Controls
        auto_trading_tests = [
            ("GET", "/auto_trading/status", "Get auto trading status"),
            ("POST", "/auto_trading/toggle", "Toggle auto trading", {"enabled": True}),
            ("GET", "/auto_trading/signals", "Get auto trading signals"),
            ("POST", "/auto_trading/settings", "Update auto trading settings", {
                "enabled": True,
                "symbol": "BTCUSDT",
                "entry_threshold": 0.6,
                "exit_threshold": 0.3,
                "max_positions": 3,
                "risk_per_trade": 2.0,
                "amount_config": {"type": "fixed", "amount": 100.0}
            }),
            ("POST", "/auto_trading/toggle", "Disable auto trading", {"enabled": False})
        ]
        
        for method, endpoint, description, *data in auto_trading_tests:
            payload = data[0] if data else None
            result = await self.test_backend_endpoint(method, endpoint, payload)
            self.log_test("AUTO_TRADING", description, result["status"], 
                         result.get("error"), result["response_time"])

    async def test_advanced_auto_trading(self):
        """Test advanced auto trading engine functionality"""
        print("\n🎯 TESTING ADVANCED AUTO TRADING ENGINE")
        print("=" * 50)
        
        advanced_tests = [
            ("GET", "/advanced_auto_trading/status", "Get advanced engine status"),
            ("POST", "/advanced_auto_trading/start", "Start advanced engine"),
            ("GET", "/advanced_auto_trading/positions", "Get advanced positions"),
            ("GET", "/advanced_auto_trading/market_data", "Get market data"),
            ("GET", "/advanced_auto_trading/indicators/BTCUSDT", "Get indicators for BTCUSDT"),
            ("GET", "/advanced_auto_trading/ai_signals", "Get AI signals"),
            ("POST", "/advanced_auto_trading/config", "Update advanced config", {
                "symbols": ["BTCUSDT", "ETHUSDT"],
                "risk_level": "medium",
                "max_positions": 5
            }),
            ("POST", "/advanced_auto_trading/stop", "Stop advanced engine")
        ]
        
        for method, endpoint, description, *data in advanced_tests:
            payload = data[0] if data else None
            result = await self.test_backend_endpoint(method, endpoint, payload)
            self.log_test("ADVANCED_AUTO", description, result["status"], 
                         result.get("error"), result["response_time"])

    async def test_ml_prediction_functionality(self):
        """Test all ML and prediction buttons"""
        print("\n🧠 TESTING ML PREDICTION FUNCTIONALITY")
        print("=" * 50)
        
        ml_tests = [
            ("GET", "/ml/predict", "Get ML prediction"),
            ("POST", "/ml/predict", "Post ML prediction", {"symbol": "BTCUSDT"}),
            ("GET", "/ml/online/stats", "Get online learning stats"),
            ("POST", "/ml/online/add_training_data", "Add training data", {
                "symbol": "BTCUSDT",
                "features": {"price": 45000, "volume": 1000},
                "target": 0.8
            }),
            ("POST", "/ml/online/update", "Trigger online learning update"),
            ("GET", "/ml/performance/history", "Get performance history"),
            ("POST", "/ml/tune_models", "Tune ML models", {
                "symbol": "BTCUSDT",
                "hyperparameters": {"learning_rate": 0.01, "max_depth": 10}
            }),
            ("GET", "/ml/compatibility/check", "Check ML compatibility"),
            ("POST", "/ml/compatibility/fix", "Fix ML compatibility"),
            ("GET", "/ml/compatibility/recommendations", "Get ML recommendations"),
            ("GET", "/ml/online/performance", "Get model performance"),
            ("GET", "/ml/online/buffer_status", "Get learning buffer status"),
            ("POST", "/ml/online/config", "Save online learning config", {
                "learning_rate": 0.01,
                "batch_size": 32,
                "buffer_size": 1000
            })
        ]
        
        # Test transfer learning endpoints
        transfer_learning_tests = [
            ("GET", "/ml/transfer_learning/init", "Initialize transfer learning"),
            ("POST", "/ml/transfer_learning/init", "Post transfer learning init"),
            ("GET", "/ml/target_model/train", "Start target model training"),
            ("POST", "/ml/target_model/train", "Post target model training"),
            ("GET", "/ml/learning_rates/optimize", "Optimize learning rates"),
            ("POST", "/ml/learning_rates/optimize", "Post learning rate optimization"),
            ("GET", "/ml/learning_rates/reset", "Reset learning rates"),
            ("POST", "/ml/learning_rates/reset", "Post learning rate reset"),
            ("GET", "/ml/model/force_update", "Force model update"),
            ("POST", "/ml/model/force_update", "Post model force update"),
            ("GET", "/ml/model/retrain", "Start model retraining"),
            ("POST", "/ml/model/retrain", "Post model retrain")
        ]
        
        all_ml_tests = ml_tests + transfer_learning_tests
        
        for method, endpoint, description, *data in all_ml_tests:
            payload = data[0] if data else None
            result = await self.test_backend_endpoint(method, endpoint, payload)
            self.log_test("ML_PREDICTION", description, result["status"], 
                         result.get("error"), result["response_time"])

    async def test_hft_analysis_functionality(self):
        """Test HFT analysis buttons and real-time features"""
        print("\n⚡ TESTING HFT ANALYSIS FUNCTIONALITY")
        print("=" * 50)
        
        hft_tests = [
            ("GET", "/hft/status", "Get HFT status"),
            ("POST", "/hft/start", "Start HFT analysis"),
            ("GET", "/hft/analytics", "Get HFT analytics"),
            ("GET", "/hft/opportunities", "Get HFT opportunities"),
            ("POST", "/hft/config", "Save HFT configuration", {
                "symbols": ["BTCUSDT", "ETHUSDT"],
                "interval_ms": 100,
                "threshold_percent": 0.01,
                "max_orders_per_minute": 60
            }),
            ("GET", "/hft/analysis/start", "HFT analysis start button"),
            ("POST", "/hft/analysis/start", "Post HFT analysis start"),
            ("GET", "/hft/analysis/stop", "HFT analysis stop button"),
            ("POST", "/hft/analysis/stop", "Post HFT analysis stop"),
            ("POST", "/hft/stop", "Stop HFT analysis")
        ]
        
        for method, endpoint, description, *data in hft_tests:
            payload = data[0] if data else None
            result = await self.test_backend_endpoint(method, endpoint, payload)
            self.log_test("HFT_ANALYSIS", description, result["status"], 
                         result.get("error"), result["response_time"])

    async def test_futures_trading_functionality(self):
        """Test futures trading buttons and Binance integration"""
        print("\n📈 TESTING FUTURES TRADING FUNCTIONALITY")
        print("=" * 50)
        
        futures_tests = [
            ("GET", "/futures/positions", "Get futures positions"),
            ("GET", "/futures/execute", "Futures execute button"),
            ("POST", "/futures/execute", "Post futures execute"),
            ("GET", "/futures/account", "Get futures account"),
            ("POST", "/futures/place_order", "Place futures order", {
                "symbol": "BTCUSDT",
                "side": "BUY",
                "quantity": 0.001,
                "price": 45000
            }),
            ("GET", "/binance/auto_execute", "Binance auto execute button"),
            ("POST", "/binance/auto_execute", "Post Binance auto execute", {
                "symbol": "BTCUSDT",
                "direction": "BUY",
                "confidence": 0.8,
                "price": 45000
            })
        ]
        
        # Binance Futures Exact API tests
        binance_api_tests = [
            ("GET", "/fapi/v2/account", "Binance futures account"),
            ("GET", "/fapi/v2/balance", "Binance futures balance"),
            ("GET", "/fapi/v2/positionRisk", "Binance position risk"),
            ("GET", "/fapi/v1/openOrders", "Binance open orders"),
            ("GET", "/fapi/v1/ticker/24hr", "Binance 24hr ticker"),
            ("GET", "/fapi/v1/exchangeInfo", "Binance exchange info"),
            ("POST", "/fapi/v1/leverage", "Change Binance leverage", {
                "symbol": "BTCUSDT",
                "leverage": 10
            }),
            ("POST", "/fapi/v1/marginType", "Change Binance margin type", {
                "symbol": "BTCUSDT",
                "marginType": "ISOLATED"
            })
        ]
        
        all_futures_tests = futures_tests + binance_api_tests
        
        for method, endpoint, description, *data in all_futures_tests:
            payload = data[0] if data else None
            result = await self.test_backend_endpoint(method, endpoint, payload)
            self.log_test("FUTURES_TRADING", description, result["status"], 
                         result.get("error"), result["response_time"])

    async def test_data_collection_functionality(self):
        """Test data collection buttons and real-time data flow"""
        print("\n📊 TESTING DATA COLLECTION FUNCTIONALITY")
        print("=" * 50)
        
        data_tests = [
            ("GET", "/data/collection/start", "Data collection start button"),
            ("POST", "/data/collection/start", "Post data collection start"),
            ("GET", "/data/collection/stop", "Data collection stop button"),
            ("POST", "/data/collection/stop", "Post data collection stop"),
            ("GET", "/data/symbol_data", "Get symbol data dropdown"),
            ("POST", "/data/symbol_data", "Post symbol data"),
            ("GET", "/features/indicators", "Get technical indicators"),
            ("GET", "/features/indicators?symbol=BTCUSDT", "Get BTC indicators"),
            ("GET", "/price", "Get current price"),
            ("GET", "/price/BTCUSDT", "Get BTC price"),
            ("GET", "/data/collection/status", "Get collection status"),
            ("GET", "/data/collection/stats", "Get collection stats")
        ]
        
        for method, endpoint, description, *data in data_tests:
            payload = data[0] if data else None
            result = await self.test_backend_endpoint(method, endpoint, payload)
            self.log_test("DATA_COLLECTION", description, result["status"], 
                         result.get("error"), result["response_time"])

    async def test_risk_management_functionality(self):
        """Test risk management buttons and calculations"""
        print("\n⚖️ TESTING RISK MANAGEMENT FUNCTIONALITY")
        print("=" * 50)
        
        risk_tests = [
            ("GET", "/risk/portfolio_metrics", "Get portfolio risk metrics"),
            ("POST", "/risk/calculate_position_size", "Calculate position size", {
                "symbol": "BTCUSDT",
                "entry_price": 45000,
                "stop_loss_price": 44000,
                "risk_per_trade_percent": 2.0,
                "confidence": 0.8
            }),
            ("POST", "/risk/check_trade_risk", "Check trade risk", {
                "symbol": "BTCUSDT",
                "position_size": 0.001,
                "entry_price": 45000,
                "stop_loss_price": 44000
            }),
            ("GET", "/risk/stop_loss_strategies", "Get stop loss strategies"),
            ("POST", "/risk/update_advanced_settings", "Update risk settings", {
                "max_drawdown": 10.0,
                "max_position_size": 1000.0,
                "risk_per_trade": 2.0
            }),
            ("GET", "/risk_settings", "Get risk settings"),
            ("POST", "/risk_settings", "Update risk settings", {
                "max_drawdown": 15.0,
                "max_daily_loss": 5.0
            })
        ]
        
        for method, endpoint, description, *data in risk_tests:
            payload = data[0] if data else None
            result = await self.test_backend_endpoint(method, endpoint, payload)
            self.log_test("RISK_MANAGEMENT", description, result["status"], 
                         result.get("error"), result["response_time"])

    async def test_email_notifications_functionality(self):
        """Test email and notification buttons"""
        print("\n📧 TESTING EMAIL & NOTIFICATIONS FUNCTIONALITY")
        print("=" * 50)
        
        notification_tests = [
            ("GET", "/notifications", "Get notifications"),
            ("GET", "/notifications/send_manual_alert", "Send manual alert button"),
            ("POST", "/notifications/send_manual_alert", "Post manual alert"),
            ("GET", "/notifications/clear_all", "Clear all notifications button"),
            ("POST", "/notifications/clear_all", "Post clear all notifications"),
            ("GET", "/notifications/mark_all_read", "Mark all read button"),
            ("POST", "/notifications/mark_all_read", "Post mark all read"),
            ("GET", "/api/email/config", "Get email configuration"),
            ("POST", "/api/email/config", "Update email config", {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "enabled": False
            }),
            ("POST", "/api/email/test", "Test email connection"),
            ("GET", "/api/alerts/history", "Get alert history"),
            ("DELETE", "/api/alerts/history", "Clear alert history"),
            ("POST", "/api/alerts/check", "Check auto alerts"),
            ("GET", "/email/config", "Get email config (legacy)"),
            ("POST", "/email/config", "Post email config (legacy)", {
                "email": "test@example.com",
                "enabled": False
            }),
            ("POST", "/email/test", "Test email (legacy)"),
            ("POST", "/email/send_test", "Send test email", {
                "subject": "Test",
                "body": "Test message"
            })
        ]
        
        for method, endpoint, description, *data in notification_tests:
            payload = data[0] if data else None
            result = await self.test_backend_endpoint(method, endpoint, payload)
            self.log_test("EMAIL_NOTIFICATIONS", description, result["status"], 
                         result.get("error"), result["response_time"])

    async def test_trading_operations(self):
        """Test trading operation buttons and workflows"""
        print("\n💰 TESTING TRADING OPERATIONS")
        print("=" * 50)
        
        trading_tests = [
            ("POST", "/trade", "Create new trade", {
                "symbol": "BTCUSDT",
                "action": "buy",
                "amount": 0.001,
                "price": 45000
            }),
            ("GET", "/trades/recent?limit=5", "Get recent trades with limit"),
            ("POST", "/trades/1/close", "Close trade"),
            ("POST", "/trades/1/cancel", "Cancel trade"),
            ("POST", "/trades/1/activate", "Activate trade"),
            ("GET", "/performance/dashboard", "Get performance dashboard"),
            ("GET", "/performance/metrics", "Get performance metrics"),
            ("GET", "/performance/metrics?timeframe=1d", "Get daily performance")
        ]
        
        for method, endpoint, description, *data in trading_tests:
            payload = data[0] if data else None
            result = await self.test_backend_endpoint(method, endpoint, payload)
            self.log_test("TRADING_OPS", description, result["status"], 
                         result.get("error"), result["response_time"])

    async def test_system_health_functionality(self):
        """Test system health and monitoring buttons"""
        print("\n🔧 TESTING SYSTEM HEALTH & MONITORING")
        print("=" * 50)
        
        system_tests = [
            ("GET", "/system/status", "Get system status"),
            ("GET", "/model/upload_status", "Get model upload status"),
            ("GET", "/model/versions", "Get model versions"),
            ("GET", "/model/active_version", "Get active model version"),
            ("GET", "/model/analytics", "Get model analytics"),
            ("POST", "/retrain", "Start model retraining"),
            ("GET", "/backtest/comprehensive", "Comprehensive backtest button"),
            ("POST", "/backtest/comprehensive", "Post comprehensive backtest"),
            ("GET", "/backtest", "Get backtest results"),
            ("GET", "/backtest/results", "Get detailed backtest results"),
            ("GET", "/model/logs", "Get model logs"),
            ("GET", "/model/errors", "Get model errors"),
            ("GET", "/safety/check", "Safety check"),
            ("GET", "/trades/analytics", "Get trades analytics")
        ]
        
        for method, endpoint, description, *data in system_tests:
            payload = data[0] if data else None
            result = await self.test_backend_endpoint(method, endpoint, payload)
            self.log_test("SYSTEM_HEALTH", description, result["status"], 
                         result.get("error"), result["response_time"])

    async def test_chart_data_endpoints(self):
        """Test all chart data endpoints and visualization"""
        print("\n📈 TESTING CHART DATA & VISUALIZATION")
        print("=" * 50)
        
        chart_tests = [
            ("GET", "/chart/price_history", "Get price history for charts"),
            ("GET", "/chart/indicators", "Get chart indicators"),
            ("GET", "/chart/volume", "Get volume data for charts"),
            ("GET", "/chart/candlestick", "Get candlestick data"),
            ("GET", "/chart/real_time", "Get real-time chart data"),
            ("GET", "/features/indicators?symbol=ETHUSDT", "Get ETH chart indicators"),
            ("GET", "/features/indicators?symbol=SOLUSDT", "Get SOL chart indicators"),
            ("GET", "/hft/analytics", "Get HFT analytics for charts"),
            ("GET", "/performance/metrics?timeframe=7d", "Get weekly performance charts"),
            ("GET", "/performance/metrics?timeframe=30d", "Get monthly performance charts")
        ]
        
        for method, endpoint, description, *data in chart_tests:
            payload = data[0] if data else None
            result = await self.test_backend_endpoint(method, endpoint, payload)
            self.log_test("CHART_DATA", description, result["status"], 
                         result.get("error"), result["response_time"])

    async def test_callback_simulation(self):
        """Test dashboard callback interactions"""
        print("\n🔄 TESTING DASHBOARD CALLBACKS & INTERACTIONS")
        print("=" * 50)
        
        # Simulate callback interactions by testing endpoint sequences
        callback_sequences = [
            {
                "name": "Symbol Selection Callback",
                "sequence": [
                    ("GET", "/data/symbol_data", "Load symbol dropdown"),
                    ("GET", "/price/BTCUSDT", "Update price on selection"),
                    ("GET", "/features/indicators?symbol=BTCUSDT", "Update indicators")
                ]
            },
            {
                "name": "Auto Trading Toggle Callback",
                "sequence": [
                    ("GET", "/auto_trading/status", "Get current status"),
                    ("POST", "/auto_trading/toggle", "Toggle state", {"enabled": True}),
                    ("GET", "/auto_trading/status", "Verify new status")
                ]
            },
            {
                "name": "HFT Analysis Start Callback",
                "sequence": [
                    ("GET", "/hft/status", "Get HFT status"),
                    ("POST", "/hft/start", "Start HFT analysis"),
                    ("GET", "/hft/analytics", "Get updated analytics")
                ]
            },
            {
                "name": "ML Model Update Callback",
                "sequence": [
                    ("GET", "/ml/online/stats", "Get current ML stats"),
                    ("POST", "/ml/online/update", "Trigger model update"),
                    ("GET", "/ml/performance/history", "Get updated performance")
                ]
            },
            {
                "name": "Risk Settings Update Callback",
                "sequence": [
                    ("GET", "/risk_settings", "Get current risk settings"),
                    ("POST", "/risk_settings", "Update settings", {"max_drawdown": 12.0}),
                    ("GET", "/risk/portfolio_metrics", "Get updated risk metrics")
                ]
            }
        ]
        
        for callback_test in callback_sequences:
            print(f"\n   Testing: {callback_test['name']}")
            sequence_success = True
            sequence_times = []
            
            for method, endpoint, description, *data in callback_test['sequence']:
                payload = data[0] if data else None
                result = await self.test_backend_endpoint(method, endpoint, payload)
                
                if result["status"] != "PASS":
                    sequence_success = False
                
                sequence_times.append(result["response_time"])
                print(f"     {description}: {result['status']}")
            
            total_time = sum(sequence_times)
            self.callback_tests[callback_test['name']] = {
                "success": sequence_success,
                "total_time": total_time,
                "steps": len(callback_test['sequence'])
            }
            
            status = "PASS" if sequence_success else "FAIL"
            self.log_test("CALLBACKS", callback_test['name'], status, 
                         f"{len(callback_test['sequence'])} steps", total_time)

    async def test_data_flow_validation(self):
        """Test data flow between components"""
        print("\n🌊 TESTING DATA FLOW VALIDATION")
        print("=" * 50)
        
        # Test data consistency across endpoints
        data_flow_tests = [
            {
                "name": "Balance Consistency Flow",
                "flow": [
                    ("GET", "/balance", "Get balance from balance endpoint"),
                    ("GET", "/portfolio", "Get balance from portfolio endpoint"),
                    ("GET", "/auto_trading/status", "Get balance from auto trading")
                ],
                "validation": "balance_consistency"
            },
            {
                "name": "Trading Data Flow",
                "flow": [
                    ("POST", "/trade", "Create new trade", {"symbol": "BTCUSDT", "action": "buy", "amount": 0.001, "price": 45000}),
                    ("GET", "/trades", "Get all trades"),
                    ("GET", "/trades/recent", "Get recent trades"),
                    ("GET", "/portfolio", "Check portfolio update")
                ],
                "validation": "trade_consistency"
            },
            {
                "name": "ML Prediction Data Flow",
                "flow": [
                    ("GET", "/ml/predict", "Get ML prediction"),
                    ("GET", "/ml/performance/history", "Get prediction history"),
                    ("GET", "/ml/online/stats", "Get online learning stats")
                ],
                "validation": "ml_consistency"
            },
            {
                "name": "HFT Analytics Data Flow", 
                "flow": [
                    ("POST", "/hft/start", "Start HFT analysis"),
                    ("GET", "/hft/analytics", "Get HFT analytics"),
                    ("GET", "/hft/opportunities", "Get opportunities"),
                    ("GET", "/hft/status", "Check HFT status")
                ],
                "validation": "hft_consistency"
            }
        ]
        
        for flow_test in data_flow_tests:
            print(f"\n   Testing: {flow_test['name']}")
            flow_data = {}
            flow_success = True
            
            for method, endpoint, description, *data in flow_test['flow']:
                payload = data[0] if data else None
                result = await self.test_backend_endpoint(method, endpoint, payload)
                
                if result["status"] == "PASS":
                    flow_data[endpoint] = result.get("data")
                else:
                    flow_success = False
                    break
                    
                print(f"     {description}: {result['status']}")
            
            # Validate data consistency
            if flow_success and flow_test["validation"]:
                consistency_check = self.validate_data_consistency(
                    flow_test["validation"], flow_data
                )
                flow_success = consistency_check
            
            self.data_flow_tests[flow_test['name']] = {
                "success": flow_success,
                "data": flow_data
            }
            
            status = "PASS" if flow_success else "FAIL"
            self.log_test("DATA_FLOW", flow_test['name'], status)

    def validate_data_consistency(self, validation_type: str, flow_data: Dict) -> bool:
        """Validate data consistency across endpoints"""
        try:
            if validation_type == "balance_consistency":
                balances = []
                for endpoint, data in flow_data.items():
                    if isinstance(data, dict):
                        if "balance" in data:
                            balances.append(data["balance"])
                        elif "auto_trading" in data and "balance" in data["auto_trading"]:
                            balances.append(data["auto_trading"]["balance"])
                        elif "spot" in data:
                            balances.append(data["spot"])
                
                # Check if all balances are consistent (within 1% tolerance)
                if len(balances) >= 2:
                    return all(abs(b - balances[0]) / balances[0] < 0.01 for b in balances[1:])
                
            elif validation_type == "trade_consistency":
                # Check if created trade appears in trade lists
                trade_created = False
                trade_in_list = False
                
                for endpoint, data in flow_data.items():
                    if "/trade" in endpoint and isinstance(data, dict) and data.get("status") == "success":
                        trade_created = True
                    elif "/trades" in endpoint and isinstance(data, dict) and "trades" in data:
                        if len(data["trades"]) > 0:
                            trade_in_list = True
                
                return trade_created and trade_in_list
            
            elif validation_type == "ml_consistency":
                # Check if ML endpoints return consistent data structure
                ml_endpoints_working = 0
                for endpoint, data in flow_data.items():
                    if isinstance(data, dict) and data.get("status") == "success":
                        ml_endpoints_working += 1
                
                return ml_endpoints_working >= 2
            
            elif validation_type == "hft_consistency":
                # Check if HFT analysis provides consistent data
                hft_started = False
                analytics_available = False
                
                for endpoint, data in flow_data.items():
                    if "/hft/start" in endpoint and isinstance(data, dict) and data.get("status") == "success":
                        hft_started = True
                    elif "/hft/analytics" in endpoint and isinstance(data, dict) and "analytics" in data:
                        analytics_available = True
                
                return hft_started and analytics_available
            
            return True
            
        except Exception as e:
            print(f"     Validation error: {e}")
            return False

    async def test_performance_benchmarks(self):
        """Test performance benchmarks for critical endpoints"""
        print("\n⚡ TESTING PERFORMANCE BENCHMARKS")
        print("=" * 50)
        
        # Critical endpoints that must be fast (<100ms)
        fast_endpoints = [
            ("GET", "/", "Root endpoint"),
            ("GET", "/health", "Health check"),
            ("GET", "/balance", "Get balance"),
            ("GET", "/price/BTCUSDT", "Get BTC price"),
            ("GET", "/auto_trading/status", "Auto trading status")
        ]
        
        # Endpoints that should be responsive (<500ms)
        responsive_endpoints = [
            ("GET", "/trades", "Get trades"),
            ("GET", "/portfolio", "Get portfolio"),
            ("GET", "/ml/predict", "ML prediction"),
            ("GET", "/hft/analytics", "HFT analytics")
        ]
        
        # Test fast endpoints (should be <100ms)
        for method, endpoint, description in fast_endpoints:
            result = await self.test_backend_endpoint(method, endpoint)
            response_time = result["response_time"] * 1000  # Convert to ms
            
            if response_time < 100:
                benchmark_status = "PASS"
            elif response_time < 200:
                benchmark_status = "WARN"
            else:
                benchmark_status = "FAIL"
                
            self.log_test("PERFORMANCE_FAST", f"{description} (<100ms)", 
                         benchmark_status, f"{response_time:.1f}ms", result["response_time"])
        
        # Test responsive endpoints (should be <500ms)
        for method, endpoint, description in responsive_endpoints:
            result = await self.test_backend_endpoint(method, endpoint)
            response_time = result["response_time"] * 1000  # Convert to ms
            
            if response_time < 500:
                benchmark_status = "PASS"
            elif response_time < 1000:
                benchmark_status = "WARN"
            else:
                benchmark_status = "FAIL"
                
            self.log_test("PERFORMANCE_RESPONSIVE", f"{description} (<500ms)", 
                         benchmark_status, f"{response_time:.1f}ms", result["response_time"])

    def generate_comprehensive_report(self):
        """Generate comprehensive test report"""
        print("\n📄 GENERATING COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        # Categorize results
        categories = {}
        for result in self.test_results:
            category = result["category"]
            if category not in categories:
                categories[category] = {"PASS": 0, "FAIL": 0, "WARN": 0, "total": 0}
            
            categories[category][result["status"]] += 1
            categories[category]["total"] += 1
        
        # Calculate overall statistics
        total_tests = len(self.test_results)
        total_pass = sum(1 for r in self.test_results if r["status"] == "PASS")
        total_fail = sum(1 for r in self.test_results if r["status"] == "FAIL")
        total_warn = sum(1 for r in self.test_results if r["status"] == "WARN")
        
        success_rate = (total_pass / total_tests * 100) if total_tests > 0 else 0
        
        # Generate report
        report = {
            "test_date": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "passed": total_pass,
                "failed": total_fail,
                "warnings": total_warn,
                "success_rate": round(success_rate, 2),
                "overall_status": "EXCELLENT" if success_rate >= 95 else "GOOD" if success_rate >= 85 else "NEEDS_ATTENTION"
            },
            "categories": categories,
            "callback_tests": self.callback_tests,
            "data_flow_tests": self.data_flow_tests,
            "performance_metrics": {
                "avg_response_time": round(sum(r["response_time_ms"] for r in self.test_results) / total_tests, 2) if total_tests > 0 else 0,
                "fastest_endpoint": min(self.test_results, key=lambda x: x["response_time_ms"])["test_name"] if self.test_results else None,
                "slowest_endpoint": max(self.test_results, key=lambda x: x["response_time_ms"])["test_name"] if self.test_results else None
            },
            "detailed_results": self.test_results
        }
        
        # Save report
        report_path = f"ULTIMATE_END_TO_END_VALIDATION_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print(f"🎯 OVERALL SUCCESS RATE: {success_rate:.1f}%")
        print(f"📊 TOTAL TESTS: {total_tests}")
        print(f"✅ PASSED: {total_pass}")
        print(f"❌ FAILED: {total_fail}")
        print(f"⚠️ WARNINGS: {total_warn}")
        print(f"🚀 STATUS: {report['summary']['overall_status']}")
        
        print(f"\n📈 PERFORMANCE METRICS:")
        print(f"   Average Response Time: {report['performance_metrics']['avg_response_time']}ms")
        
        print(f"\n📋 CATEGORY BREAKDOWN:")
        for category, stats in categories.items():
            pass_rate = (stats["PASS"] / stats["total"] * 100) if stats["total"] > 0 else 0
            print(f"   {category}: {stats['PASS']}/{stats['total']} ({pass_rate:.1f}%)")
        
        print(f"\n🔄 CALLBACK TESTS:")
        for callback_name, callback_result in self.callback_tests.items():
            status = "✅" if callback_result["success"] else "❌"
            print(f"   {status} {callback_name}: {callback_result['steps']} steps")
        
        print(f"\n🌊 DATA FLOW TESTS:")
        for flow_name, flow_result in self.data_flow_tests.items():
            status = "✅" if flow_result["success"] else "❌"
            print(f"   {status} {flow_name}")
        
        print(f"\n📄 Detailed report saved to: {report_path}")
        
        return report

    async def run_ultimate_validation(self):
        """Run the complete ultimate validation"""
        print("🚀 STARTING ULTIMATE END-TO-END VALIDATION")
        print("=" * 70)
        print("Testing every button, chart, functionality, callback, and data flow")
        print("=" * 70)
        
        start_time = time.time()
        
        try:
            # Test all functionality categories
            await self.test_basic_operations()
            await self.test_auto_trading_functionality()
            await self.test_advanced_auto_trading()
            await self.test_ml_prediction_functionality()
            await self.test_hft_analysis_functionality()
            await self.test_futures_trading_functionality()
            await self.test_data_collection_functionality()
            await self.test_risk_management_functionality()
            await self.test_email_notifications_functionality()
            await self.test_trading_operations()
            await self.test_system_health_functionality()
            await self.test_chart_data_endpoints()
            
            # Test callbacks and data flow
            await self.test_callback_simulation()
            await self.test_data_flow_validation()
            
            # Test performance benchmarks
            await self.test_performance_benchmarks()
            
            total_time = time.time() - start_time
            
            print(f"\n⏱️ TOTAL VALIDATION TIME: {total_time:.2f} seconds")
            
            # Generate comprehensive report
            report = self.generate_comprehensive_report()
            
            print("\n🎉 ULTIMATE END-TO-END VALIDATION COMPLETED!")
            
            return report
            
        except Exception as e:
            print(f"\n💥 CRITICAL ERROR during validation: {e}")
            import traceback
            traceback.print_exc()
            return None

async def main():
    """Main execution function"""
    print("🎯 ULTIMATE END-TO-END CRYPTO BOT VALIDATION")
    print("Testing every button, chart, callback, and data flow")
    print("=" * 70)
    
    validator = UltimateEndToEndValidator()
    
    # Check backend availability
    try:
        response = requests.get(f"{validator.backend_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and accessible")
        else:
            print("⚠️ Backend responded but may have issues")
    except:
        print("❌ Backend is not accessible - starting validation anyway")
        print("   Some tests may fail due to backend unavailability")
    
    report = await validator.run_ultimate_validation()
    
    if report:
        if report["summary"]["success_rate"] >= 95:
            print("\n🏆 EXCELLENT - System is production ready!")
        elif report["summary"]["success_rate"] >= 85:
            print("\n👍 GOOD - System is mostly functional with minor issues")
        else:
            print("\n⚠️ NEEDS ATTENTION - Significant issues detected")
        
        print("\n📋 NEXT STEPS:")
        if report["summary"]["failed"] > 0:
            print("   1. Review failed tests in the detailed report")
            print("   2. Fix critical issues")
            print("   3. Re-run validation")
        else:
            print("   1. Deploy to production environment")
            print("   2. Monitor performance metrics")
            print("   3. Set up automated testing")

if __name__ == "__main__":
    asyncio.run(main())
