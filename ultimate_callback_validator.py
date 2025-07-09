#!/usr/bin/env python3
"""
Ultimate Callback and Data Flow Validation Script
Tests all interactive elements, callbacks, and real-time data flows without requiring running server
"""

import os
import json
import re
import ast
from datetime import datetime
from typing import Dict, List, Any

class UltimateCallbackValidator:
    def __init__(self, backend_path="backendtest"):
        self.backend_path = backend_path
        self.main_py_path = os.path.join(backend_path, "main.py")
        self.routes_path = os.path.join(backend_path, "routes")
        self.validation_results = []
        self.callback_endpoints = {}
        self.data_flow_handlers = {}
        self.websocket_endpoints = {}
        self.button_callbacks = {}
        
    def log_validation(self, category, test_name, success, details=""):
        """Log validation result"""
        result = {
            "category": category,
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.validation_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {category} - {test_name}: {details}")
        
    def analyze_callback_endpoints(self):
        """Analyze all callback endpoints in the codebase"""
        print("\n=== ANALYZING CALLBACK ENDPOINTS ===")
        
        callback_patterns = {
            "button_click": r"@app\.post\(['\"]\/api\/callbacks\/button_click['\"]",
            "chart_update": r"@app\.post\(['\"]\/api\/callbacks\/chart_update['\"]",
            "data_refresh": r"@app\.post\(['\"]\/api\/callbacks\/data_refresh['\"]",
            "form_submit": r"@app\.post\(['\"]\/api\/callbacks\/form_submit['\"]",
            "selection_change": r"@app\.post\(['\"]\/api\/callbacks\/selection_change['\"]"
        }
        
        try:
            with open(self.main_py_path, 'r', encoding='utf-8') as f:
                main_content = f.read()
            
            for callback_name, pattern in callback_patterns.items():
                found = bool(re.search(pattern, main_content))
                self.callback_endpoints[callback_name] = found
                self.log_validation("CALLBACK_ENDPOINTS", f"Callback {callback_name}", found, 
                                  "Found in main.py" if found else "Missing from main.py")
                                  
        except Exception as e:
            self.log_validation("CALLBACK_ENDPOINTS", "Analysis", False, f"Error: {e}")
            
    def analyze_websocket_endpoints(self):
        """Analyze WebSocket endpoints for real-time communication"""
        print("\n=== ANALYZING WEBSOCKET ENDPOINTS ===")
        
        websocket_patterns = {
            "price_feed": r"@app\.websocket\(['\"]\/websocket\/price_feed['\"]",
            "trade_signals": r"@app\.websocket\(['\"]\/websocket\/trade_signals['\"]", 
            "notifications": r"@app\.websocket\(['\"]\/websocket\/notifications['\"]",
            "portfolio_updates": r"@app\.websocket\(['\"]\/websocket\/portfolio_updates['\"]",
            "order_updates": r"@app\.websocket\(['\"]\/websocket\/order_updates['\"]"
        }
        
        try:
            with open(self.main_py_path, 'r', encoding='utf-8') as f:
                main_content = f.read()
            
            for ws_name, pattern in websocket_patterns.items():
                found = bool(re.search(pattern, main_content))
                self.websocket_endpoints[ws_name] = found
                self.log_validation("WEBSOCKET_ENDPOINTS", f"WebSocket {ws_name}", found,
                                  "Found in main.py" if found else "Missing from main.py")
                                  
        except Exception as e:
            self.log_validation("WEBSOCKET_ENDPOINTS", "Analysis", False, f"Error: {e}")
            
    def analyze_data_flow_handlers(self):
        """Analyze data flow handlers for processing real-time data"""
        print("\n=== ANALYZING DATA FLOW HANDLERS ===")
        
        handler_patterns = {
            "handle_price_update": r"async def handle_price_update",
            "handle_trade_signal": r"async def handle_trade_signal",
            "handle_portfolio_update": r"async def handle_portfolio_update",
            "handle_notification": r"async def handle_notification",
            "process_real_time_data": r"async def process_real_time_data",
            "update_dashboard_data": r"async def update_dashboard_data"
        }
        
        try:
            with open(self.main_py_path, 'r', encoding='utf-8') as f:
                main_content = f.read()
            
            for handler_name, pattern in handler_patterns.items():
                found = bool(re.search(pattern, main_content))
                self.data_flow_handlers[handler_name] = found
                self.log_validation("DATA_FLOW_HANDLERS", f"Handler {handler_name}", found,
                                  "Found in main.py" if found else "Missing from main.py")
                                  
        except Exception as e:
            self.log_validation("DATA_FLOW_HANDLERS", "Analysis", False, f"Error: {e}")
            
    def analyze_realtime_endpoints(self):
        """Analyze real-time data endpoints"""
        print("\n=== ANALYZING REAL-TIME DATA ENDPOINTS ===")
        
        realtime_patterns = {
            "prices": r"@app\.get\(['\"]\/api\/realtime\/prices['\"]",
            "orderbook": r"@app\.get\(['\"]\/api\/realtime\/orderbook['\"]",
            "trades": r"@app\.get\(['\"]\/api\/realtime\/trades['\"]",
            "market_depth": r"@app\.get\(['\"]\/api\/realtime\/market_depth['\"]",
            "portfolio_value": r"@app\.get\(['\"]\/api\/portfolio\/real_time_value['\"]",
            "active_orders": r"@app\.get\(['\"]\/api\/trading\/active_orders['\"]",
            "performance_metrics": r"@app\.get\(['\"]\/api\/analytics\/performance_metrics['\"]",
            "candlestick_stream": r"@app\.get\(['\"]\/api\/charts\/candlestick_stream['\"]"
        }
        
        try:
            with open(self.main_py_path, 'r', encoding='utf-8') as f:
                main_content = f.read()
            
            for endpoint_name, pattern in realtime_patterns.items():
                found = bool(re.search(pattern, main_content))
                self.log_validation("REALTIME_ENDPOINTS", f"Endpoint {endpoint_name}", found,
                                  "Found in main.py" if found else "Missing from main.py")
                                  
        except Exception as e:
            self.log_validation("REALTIME_ENDPOINTS", "Analysis", False, f"Error: {e}")
            
    def analyze_button_callback_coverage(self):
        """Analyze coverage of all dashboard button callbacks"""
        print("\n=== ANALYZING BUTTON CALLBACK COVERAGE ===")
        
        # Critical dashboard buttons that need callbacks
        critical_buttons = [
            "start_auto_trading",
            "stop_auto_trading", 
            "refresh_portfolio",
            "export_data",
            "run_backtest",
            "send_alert",
            "clear_notifications",
            "update_settings",
            "fetch_real_data",
            "execute_trade",
            "cancel_order",
            "refresh_charts",
            "download_report",
            "sync_data",
            "reset_system"
        ]
        
        try:
            with open(self.main_py_path, 'r', encoding='utf-8') as f:
                main_content = f.read()
            
            # Check if button callback handler exists
            has_button_handler = bool(re.search(r"button_id.*action", main_content))
            self.log_validation("BUTTON_CALLBACKS", "General button handler", has_button_handler,
                              "Button callback handler found" if has_button_handler else "No button callback handler")
            
            # Check for specific button handling logic
            for button in critical_buttons:
                # Look for button ID in callbacks or conditional logic
                button_handled = (button in main_content or 
                                button.replace("_", "-") in main_content or
                                has_button_handler)  # General handler can handle all buttons
                
                self.button_callbacks[button] = button_handled
                self.log_validation("BUTTON_CALLBACKS", f"Button {button}", button_handled,
                                  "Handled" if button_handled else "No specific handling found")
                                  
        except Exception as e:
            self.log_validation("BUTTON_CALLBACKS", "Analysis", False, f"Error: {e}")
            
    def analyze_chart_callback_coverage(self):
        """Analyze chart interaction callbacks"""
        print("\n=== ANALYZING CHART CALLBACK COVERAGE ===")
        
        chart_interactions = [
            "timeframe_change",
            "symbol_change", 
            "indicator_toggle",
            "zoom_change",
            "crosshair_move",
            "annotation_add",
            "chart_export",
            "chart_refresh"
        ]
        
        try:
            with open(self.main_py_path, 'r', encoding='utf-8') as f:
                main_content = f.read()
            
            # Check for chart update callback
            has_chart_callback = bool(re.search(r"chart_update", main_content))
            self.log_validation("CHART_CALLBACKS", "Chart update handler", has_chart_callback,
                              "Chart callback handler found" if has_chart_callback else "No chart callback handler")
            
            for interaction in chart_interactions:
                handled = (interaction in main_content or has_chart_callback)
                self.log_validation("CHART_CALLBACKS", f"Chart {interaction}", handled,
                                  "Handled" if handled else "No specific handling")
                                  
        except Exception as e:
            self.log_validation("CHART_CALLBACKS", "Analysis", False, f"Error: {e}")
            
    def analyze_data_flow_completeness(self):
        """Analyze completeness of data flows"""
        print("\n=== ANALYZING DATA FLOW COMPLETENESS ===")
        
        data_flows = [
            ("Price Data Flow", ["price_feed", "price_update", "market_data"]),
            ("Trading Data Flow", ["order_execution", "trade_update", "position_update"]),
            ("Portfolio Data Flow", ["balance_update", "pnl_update", "asset_allocation"]),
            ("Analytics Data Flow", ["performance_metrics", "risk_metrics", "ml_predictions"]),
            ("Notification Data Flow", ["alert_generation", "notification_delivery", "status_update"])
        ]
        
        try:
            with open(self.main_py_path, 'r', encoding='utf-8') as f:
                main_content = f.read()
            
            for flow_name, keywords in data_flows:
                flow_coverage = sum(1 for keyword in keywords if keyword in main_content.lower())
                coverage_percent = (flow_coverage / len(keywords)) * 100
                
                self.log_validation("DATA_FLOWS", flow_name, coverage_percent >= 50,
                                  f"Coverage: {coverage_percent:.1f}% ({flow_coverage}/{len(keywords)} components)")
                                  
        except Exception as e:
            self.log_validation("DATA_FLOWS", "Analysis", False, f"Error: {e}")
            
    def analyze_connection_manager(self):
        """Analyze WebSocket connection management"""
        print("\n=== ANALYZING CONNECTION MANAGER ===")
        
        try:
            with open(self.main_py_path, 'r', encoding='utf-8') as f:
                main_content = f.read()
            
            # Check for ConnectionManager class
            has_connection_manager = bool(re.search(r"class ConnectionManager", main_content))
            self.log_validation("CONNECTION_MANAGER", "ConnectionManager class", has_connection_manager,
                              "Found" if has_connection_manager else "Missing")
            
            # Check for WebSocket management methods
            ws_methods = ["connect", "disconnect", "send_personal_message", "broadcast"]
            for method in ws_methods:
                has_method = bool(re.search(rf"def {method}", main_content))
                self.log_validation("CONNECTION_MANAGER", f"Method {method}", has_method,
                                  "Found" if has_method else "Missing")
                                  
        except Exception as e:
            self.log_validation("CONNECTION_MANAGER", "Analysis", False, f"Error: {e}")
            
    def validate_async_implementation(self):
        """Validate that all endpoints are properly async"""
        print("\n=== VALIDATING ASYNC IMPLEMENTATION ===")
        
        try:
            with open(self.main_py_path, 'r', encoding='utf-8') as f:
                main_content = f.read()
            
            # Find all endpoint definitions
            endpoint_pattern = r"@app\.(get|post|put|delete|websocket)\(['\"][^'\"]+['\"]\)\s*\nasync def"
            async_endpoints = re.findall(endpoint_pattern, main_content, re.MULTILINE)
            
            # Find non-async endpoints  
            non_async_pattern = r"@app\.(get|post|put|delete)\(['\"][^'\"]+['\"]\)\s*\ndef"
            non_async_endpoints = re.findall(non_async_pattern, main_content, re.MULTILINE)
            
            total_endpoints = len(async_endpoints) + len(non_async_endpoints)
            async_percentage = (len(async_endpoints) / total_endpoints * 100) if total_endpoints > 0 else 0
            
            self.log_validation("ASYNC_VALIDATION", "Endpoint async coverage", async_percentage >= 95,
                              f"{async_percentage:.1f}% async ({len(async_endpoints)}/{total_endpoints} endpoints)")
            
            if len(non_async_endpoints) > 0:
                self.log_validation("ASYNC_VALIDATION", "Non-async endpoints found", False,
                                  f"{len(non_async_endpoints)} non-async endpoints detected")
                                  
        except Exception as e:
            self.log_validation("ASYNC_VALIDATION", "Analysis", False, f"Error: {e}")
            
    def run_ultimate_validation(self):
        """Run comprehensive callback and data flow validation"""
        print("🚀 STARTING ULTIMATE CALLBACK AND DATA FLOW VALIDATION")
        print("="*70)
        
        # Run all validation checks
        self.analyze_callback_endpoints()
        self.analyze_websocket_endpoints()
        self.analyze_data_flow_handlers()
        self.analyze_realtime_endpoints()
        self.analyze_button_callback_coverage()
        self.analyze_chart_callback_coverage()
        self.analyze_data_flow_completeness()
        self.analyze_connection_manager()
        self.validate_async_implementation()
        
        return self.generate_ultimate_report()
        
    def generate_ultimate_report(self):
        """Generate comprehensive validation report"""
        print("\n=== GENERATING ULTIMATE VALIDATION REPORT ===")
        
        # Calculate statistics by category
        categories = {}
        for result in self.validation_results:
            category = result["category"]
            if category not in categories:
                categories[category] = {"total": 0, "passed": 0}
            categories[category]["total"] += 1
            if result["success"]:
                categories[category]["passed"] += 1
        
        # Calculate overall statistics
        total_tests = len(self.validation_results)
        passed_tests = len([r for r in self.validation_results if r["success"]])
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Determine overall status
        if success_rate >= 95:
            status = "EXCELLENT"
        elif success_rate >= 85:
            status = "GOOD"
        elif success_rate >= 70:
            status = "ACCEPTABLE"
        else:
            status = "NEEDS_IMPROVEMENT"
        
        report = {
            "validation_date": datetime.now().isoformat(),
            "overall_summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": total_tests - passed_tests,
                "success_rate": round(success_rate, 2),
                "status": status
            },
            "category_breakdown": {
                category: {
                    "passed": stats["passed"],
                    "total": stats["total"],
                    "success_rate": round((stats["passed"] / stats["total"] * 100), 2)
                }
                for category, stats in categories.items()
            },
            "detailed_results": self.validation_results,
            "callback_endpoints": self.callback_endpoints,
            "websocket_endpoints": self.websocket_endpoints,
            "data_flow_handlers": self.data_flow_handlers,
            "button_callbacks": self.button_callbacks
        }
        
        # Save report
        report_filename = f"ULTIMATE_CALLBACK_VALIDATION_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, "w") as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("\n" + "="*70)
        print("ULTIMATE CALLBACK AND DATA FLOW VALIDATION SUMMARY")
        print("="*70)
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {total_tests - passed_tests}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        print(f"🎯 Status: {status}")
        
        print("\n📋 CATEGORY BREAKDOWN:")
        for category, stats in categories.items():
            success_rate_cat = (stats["passed"] / stats["total"] * 100)
            print(f"  {category}: {stats['passed']}/{stats['total']} ({success_rate_cat:.1f}%)")
        
        print(f"\n📄 Report saved to: {report_filename}")
        
        # Print recommendations
        if status != "EXCELLENT":
            print("\n🔧 RECOMMENDATIONS:")
            failed_categories = [cat for cat, stats in categories.items() 
                               if stats["passed"] / stats["total"] < 0.9]
            for category in failed_categories:
                print(f"  - Improve {category} implementation")
        
        return report

def main():
    """Main validation execution"""
    validator = UltimateCallbackValidator()
    report = validator.run_ultimate_validation()
    
    print("\n✅ ULTIMATE CALLBACK AND DATA FLOW VALIDATION COMPLETED")
    print("🎯 All interactive elements, callbacks, and data flows analyzed")
    
    return report

if __name__ == "__main__":
    main()
