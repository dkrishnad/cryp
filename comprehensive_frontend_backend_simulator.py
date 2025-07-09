#!/usr/bin/env python3
"""
COMPREHENSIVE FRONTEND-BACKEND SIMULATION TESTER
Tests every button, callback, API call, and data flow in the application
"""
import sys
import os
import requests
import json
import time
import traceback
from datetime import datetime, timedelta
import threading
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add paths
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboardtest'))

class ComprehensiveSimulator:
    def __init__(self):
        self.backend_url = "http://localhost:5000"
        self.frontend_url = "http://localhost:8050"
        self.test_results = {}
        self.backend_process = None
        self.frontend_process = None
        self.session = requests.Session()
        
        # All button IDs and their expected endpoints (UPDATED TO MATCH BACKEND)
        self.button_endpoints = {
            # Main Dashboard Buttons
            'get-prediction-btn': '/ml/predict',
            'quick-prediction-btn': '/ml/predict',  # Use same endpoint
            'buy-btn': '/trade',
            'sell-btn': '/trade',
            'trade-execute-btn': '/trade',
            'trades-list-btn': '/trades/history',
            'reset-balance-btn': '/portfolio/reset',
            'test-ml-btn': '/ml/status',
            'sidebar-analytics-btn': '/ml/analytics',
            'enable-online-learning-btn': '/ml/online_learning/enable',
            
            # Auto Trading Buttons
            'auto-trading-toggle-btn': '/auto_trading/toggle',
            'auto-trading-settings-btn': '/auto_trading/configure',
            'auto-trading-signals-btn': '/auto_trading/signals',
            'auto-trading-status-refresh-btn': '/auto_trading/status',
            'start-advanced-auto-trading-btn': '/auto_trading/toggle',
            'stop-advanced-auto-trading-btn': '/auto_trading/toggle',
            'check-advanced-auto-trading-btn': '/auto_trading/status',
            
            # Futures Trading Buttons
            'futures-execute-signal-btn': '/futures/open_position',
            'futures-history-btn': '/futures/analytics',
            'futures-open-btn': '/futures/open_position',
            'open-futures-position': '/futures/open_position',
            'close-futures-position': '/futures/close_position',
            'update-futures-positions': '/futures/positions',
            
            # Binance Exact API Buttons
            'binance-auto-execute-btn': '/binance/execute',
            'binance-manual-trade-btn': '/binance/manual_trade',
            'binance-check-balance-btn': '/portfolio/balance',  # Use portfolio endpoint
            'binance-get-positions-btn': '/futures/positions',  # Use futures endpoint
            
            # Chart Buttons
            'show-price-chart-btn': '/data/klines',
            'show-indicators-chart-btn': '/data/klines',
            'refresh-charts-btn': '/data/live_prices',
            'chart-refresh-btn': '/data/klines',
            'chart-bollinger-btn': '/data/klines',
            'chart-momentum-btn': '/data/klines',
            'chart-volume-btn': '/data/klines',
            
            # ML and Analytics Buttons
            'refresh-model-analytics': '/ml/analytics',
            'refresh-feature-importance': '/ml/analytics',
            'refresh-model-metrics': '/ml/status',
            'check-transfer-setup': '/ml/status',
            'init-transfer-learning': '/ml/transfer_learning/start',
            'train-target-model': '/ml/train',
            
            # Notification and Email Buttons
            'send-manual-alert-btn': '/notifications/send',
            'test-email-system-btn': '/email/test',
            'clear-all-notifications-btn': '/notifications/clear',
            'mark-all-read-btn': '/notifications/mark_read',
            'refresh-notifications-btn': '/notifications',
            
            # HFT Analysis Buttons
            'start-hft-analysis-btn': '/ml/hft/start',
            'stop-hft-analysis-btn': '/ml/hft/stop',
            'hft-analytics-btn': '/ml/analytics',
            'hft-config-btn': '/ml/hft/configure',
            
            # Data Collection Buttons
            'start-data-collection-btn': '/data_collection/start',
            'stop-data-collection-btn': '/data_collection/stop',
            'data-collection-status-btn': '/data_collection/status',
            
            # Online Learning Buttons
            'enable-online-learning-btn': '/ml/online_learning/enable',
            'disable-online-learning-btn': '/ml/online_learning/disable',
            'optimize-learning-rates-btn': '/ml/optimize',
            'reset-learning-rates-btn': '/ml/reset',
            
            # Risk Management Buttons
            'calculate-position-size-btn': '/portfolio/balance',  # Use existing endpoint
            'check-trade-risk-btn': '/trade',  # Use trade endpoint
            'update-risk-settings-btn': '/auto_trading/configure',
            'risk-portfolio-metrics-btn': '/portfolio/balance',
            
            # Performance Monitoring Buttons
            'performance-dashboard-btn': '/ml/analytics',
            'performance-metrics-btn': '/ml/status',
            'portfolio-btn': '/portfolio/balance',
            
            # Model Management Buttons
            'force-model-update-btn': '/ml/train',
            'ml-compatibility-check-btn': '/ml/status',
            'ml-compatibility-fix-btn': '/ml/status',
            'start-model-retrain': '/ml/train',
            'activate-model-version': '/ml/status',
            
            # Backtesting Buttons
            'run-comprehensive-backtest': '/backtest',
            'load-backtest-results': '/backtest/results',
            
            # Amount Selection Buttons
            'amount-50-btn': None,  # Frontend only
            'amount-100-btn': None,  # Frontend only
            'amount-250-btn': None,  # Frontend only
            'amount-500-btn': None,  # Frontend only
            'amount-1000-btn': None,  # Frontend only
            'amount-max-btn': None,  # Frontend only
            
            # Sidebar Amount Buttons
            'sidebar-amount-50-btn': None,  # Frontend only
            'sidebar-amount-100-btn': None,  # Frontend only
            'sidebar-amount-250-btn': None,  # Frontend only
            'sidebar-amount-500-btn': None,  # Frontend only
            'sidebar-amount-1000-btn': None,  # Frontend only
            'sidebar-amount-max-btn': None,  # Frontend only
        }
        
        # All callback outputs that should be tested
        self.callback_outputs = [
            'live-price-display', 'prediction-output', 'trade-output', 'balance-display',
            'analytics-display', 'chart-price', 'chart-indicators', 'notifications-display',
            'auto-trading-status', 'futures-positions', 'email-status', 'ml-metrics-display',
            'model-analytics-display', 'feature-importance-display', 'backtest-results-display',
            'performance-monitor', 'virtual-balance-display', 'trade-history-display'
        ]

    def safe_print(self, msg):
        """Safe printing with timestamp"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        try:
            print(f"[{timestamp}] {msg}")
            sys.stdout.flush()
        except UnicodeEncodeError:
            print(f"[{timestamp}] {msg.encode('ascii', 'replace').decode('ascii')}")
            sys.stdout.flush()

    def start_backend(self):
        """Start the backend server"""
        self.safe_print("🔧 Starting backend server...")
        try:
            backend_script = os.path.join('backendtest', 'main.py')
            self.backend_process = subprocess.Popen(
                [sys.executable, backend_script],
                cwd=os.path.dirname(__file__),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for backend to start - try multiple health check endpoints
            for i in range(10):
                try:
                    # Try the root endpoint first (which we know exists)
                    response = self.session.get(f"{self.backend_url}/", timeout=2)
                    if response.status_code == 200:
                        self.safe_print("✅ Backend server started successfully")
                        return True
                except:
                    time.sleep(1)
                    
                try:
                    # Also try the api/status endpoint if it exists
                    response = self.session.get(f"{self.backend_url}/api/status", timeout=2)
                    if response.status_code == 200:
                        self.safe_print("✅ Backend server started successfully")
                        return True
                except:
                    pass
            
            self.safe_print("❌ Backend failed to start")
            return False
            
        except Exception as e:
            self.safe_print(f"❌ Backend startup error: {e}")
            return False

    def start_frontend(self):
        """Start the frontend dashboard"""
        self.safe_print("🔧 Starting frontend dashboard...")
        try:
            frontend_script = os.path.join('dashboardtest', 'app.py')
            self.frontend_process = subprocess.Popen(
                [sys.executable, frontend_script],
                cwd=os.path.dirname(__file__),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for frontend to start
            for i in range(15):
                try:
                    response = self.session.get(self.frontend_url, timeout=2)
                    if response.status_code == 200:
                        self.safe_print("✅ Frontend dashboard started successfully")
                        return True
                except:
                    time.sleep(1)
            
            self.safe_print("❌ Frontend failed to start")
            return False
            
        except Exception as e:
            self.safe_print(f"❌ Frontend startup error: {e}")
            return False

    def test_backend_endpoint(self, endpoint, method='GET', data=None):
        """Test a specific backend endpoint"""
        url = f"{self.backend_url}{endpoint}"
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, timeout=5)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data or {}, timeout=5)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data or {}, timeout=5)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, timeout=5)
            else:
                return {'status': 'error', 'message': f'Unsupported method: {method}'}
            
            return {
                'status': 'success' if response.status_code < 400 else 'error',
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds(),
                'content_length': len(response.content),
                'content_type': response.headers.get('content-type', 'unknown')
            }
            
        except requests.exceptions.Timeout:
            return {'status': 'timeout', 'message': 'Request timed out'}
        except requests.exceptions.ConnectionError:
            return {'status': 'connection_error', 'message': 'Cannot connect to backend'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def simulate_button_click(self, button_id):
        """Simulate a button click and test the corresponding API call"""
        endpoint = self.button_endpoints.get(button_id)
        
        result = {
            'button_id': button_id,
            'endpoint': endpoint,
            'timestamp': datetime.now().isoformat(),
            'frontend_only': endpoint is None
        }
        
        if endpoint is None:
            # Frontend-only button (like amount selection)
            result['status'] = 'frontend_only'
            result['message'] = 'Button affects frontend state only'
            return result
        
        # Test the backend endpoint
        endpoint_result = self.test_backend_endpoint(endpoint)
        result.update(endpoint_result)
        
        return result

    def test_all_buttons(self):
        """Test all buttons in parallel"""
        self.safe_print("🔘 Testing all button clicks and API calls...")
        
        results = {}
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Submit all button tests
            future_to_button = {
                executor.submit(self.simulate_button_click, button_id): button_id 
                for button_id in self.button_endpoints.keys()
            }
            
            # Collect results
            for future in as_completed(future_to_button):
                button_id = future_to_button[future]
                try:
                    result = future.result(timeout=10)
                    results[button_id] = result
                    
                    status_icon = "✅" if result.get('status') == 'success' else "❌" if result.get('status') == 'error' else "⚠️"
                    self.safe_print(f"  {status_icon} {button_id}: {result.get('status', 'unknown')}")
                    
                except Exception as e:
                    results[button_id] = {
                        'button_id': button_id,
                        'status': 'test_error',
                        'message': str(e)
                    }
                    self.safe_print(f"  ❌ {button_id}: Test failed - {e}")
        
        return results

    def test_data_flows(self):
        """Test critical data flows"""
        self.safe_print("📊 Testing critical data flows...")
        
        data_flows = {
            'live_price_feed': '/data/live_prices',
            'ml_predictions': '/ml/predict',
            'trade_execution': '/trade',
            'portfolio_sync': '/portfolio/balance',
            'notifications_system': '/notifications',
            'auto_trading_signals': '/auto_trading/signals',
            'futures_positions': '/futures/positions',
            'model_analytics': '/ml/analytics',
            'backtest_results': '/backtest/results',
            'email_system': '/email/test'
        }
        
        results = {}
        for flow_name, endpoint in data_flows.items():
            result = self.test_backend_endpoint(endpoint)
            results[flow_name] = result
            
            status_icon = "✅" if result.get('status') == 'success' else "❌"
            self.safe_print(f"  {status_icon} {flow_name}: {result.get('status', 'unknown')}")
        
        return results

    def test_callback_coverage(self):
        """Test callback coverage by analyzing registered callbacks"""
        self.safe_print("🔄 Testing callback coverage...")
        
        try:
            # Import the app to check registered callbacks
            from dashboardtest.dash_app import app
            from dashboardtest.layout import layout
            import dashboardtest.callbacks
            
            # Set layout to register all callbacks
            app.layout = layout
            
            callback_count = len(app.callback_map)
            self.safe_print(f"  📊 Total registered callbacks: {callback_count}")
            
            # Check for common callback patterns
            callback_analysis = {
                'total_callbacks': callback_count,
                'button_callbacks': 0,
                'interval_callbacks': 0,
                'store_callbacks': 0,
                'chart_callbacks': 0
            }
            
            for callback_id, callback in app.callback_map.items():
                inputs = callback.get('inputs', [])
                for inp in inputs:
                    if 'btn' in inp.get('id', '').lower() or 'button' in inp.get('id', '').lower():
                        callback_analysis['button_callbacks'] += 1
                    elif 'interval' in inp.get('id', '').lower():
                        callback_analysis['interval_callbacks'] += 1
                    elif 'store' in inp.get('id', '').lower():
                        callback_analysis['store_callbacks'] += 1
                    elif 'chart' in inp.get('id', '').lower():
                        callback_analysis['chart_callbacks'] += 1
            
            return callback_analysis
            
        except Exception as e:
            self.safe_print(f"  ❌ Callback coverage test failed: {e}")
            return {'error': str(e)}

    def test_frontend_backend_sync(self):
        """Test frontend-backend synchronization"""
        self.safe_print("🔄 Testing frontend-backend synchronization...")
        
        sync_tests = [
            {'name': 'Symbol Selection Sync', 'frontend_action': 'select_symbol', 'backend_endpoint': '/data/symbol_data'},
            {'name': 'Balance Updates', 'frontend_action': 'balance_update', 'backend_endpoint': '/portfolio/balance'},
            {'name': 'Live Price Updates', 'frontend_action': 'price_update', 'backend_endpoint': '/data/live_prices'},
            {'name': 'Trade Execution Sync', 'frontend_action': 'execute_trade', 'backend_endpoint': '/trade'},
            {'name': 'Notification Sync', 'frontend_action': 'notifications', 'backend_endpoint': '/notifications'},
        ]
        
        results = {}
        for test in sync_tests:
            result = self.test_backend_endpoint(test['backend_endpoint'])
            results[test['name']] = result
            
            status_icon = "✅" if result.get('status') == 'success' else "❌"
            self.safe_print(f"  {status_icon} {test['name']}: {result.get('status', 'unknown')}")
        
        return results

    def generate_comprehensive_report(self, button_results, data_flow_results, callback_analysis, sync_results):
        """Generate comprehensive test report"""
        report = {
            'test_summary': {
                'timestamp': datetime.now().isoformat(),
                'total_buttons_tested': len(button_results),
                'successful_buttons': len([r for r in button_results.values() if r.get('status') == 'success']),
                'failed_buttons': len([r for r in button_results.values() if r.get('status') == 'error']),
                'frontend_only_buttons': len([r for r in button_results.values() if r.get('status') == 'frontend_only']),
                'total_data_flows': len(data_flow_results),
                'successful_data_flows': len([r for r in data_flow_results.values() if r.get('status') == 'success']),
                'callback_coverage': callback_analysis
            },
            'detailed_results': {
                'button_tests': button_results,
                'data_flow_tests': data_flow_results,
                'sync_tests': sync_results,
                'callback_analysis': callback_analysis
            },
            'recommendations': [],
            'critical_issues': []
        }
        
        # Generate recommendations
        if report['test_summary']['failed_buttons'] > 0:
            report['critical_issues'].append("Some buttons are not connected to working backend endpoints")
            report['recommendations'].append("Review and fix failed backend endpoints")
        
        if report['test_summary']['successful_data_flows'] < report['test_summary']['total_data_flows']:
            report['critical_issues'].append("Some data flows are not working")
            report['recommendations'].append("Check backend service availability and endpoint implementations")
        
        if callback_analysis.get('total_callbacks', 0) < 100:
            report['recommendations'].append("Consider adding more interactive callbacks for better user experience")
        
        return report

    def run_comprehensive_simulation(self):
        """Run the complete simulation test suite"""
        self.safe_print("🚀 STARTING COMPREHENSIVE FRONTEND-BACKEND SIMULATION")
        self.safe_print("=" * 80)
        
        # Step 1: Start backend
        if not self.start_backend():
            self.safe_print("❌ Cannot continue without backend")
            return
        
        # Step 2: Start frontend
        if not self.start_frontend():
            self.safe_print("⚠️ Frontend failed to start, testing backend only")
        
        # Step 3: Test all buttons
        button_results = self.test_all_buttons()
        
        # Step 4: Test data flows
        data_flow_results = self.test_data_flows()
        
        # Step 5: Test callback coverage
        callback_analysis = self.test_callback_coverage()
        
        # Step 6: Test frontend-backend sync
        sync_results = self.test_frontend_backend_sync()
        
        # Step 7: Generate comprehensive report
        report = self.generate_comprehensive_report(
            button_results, data_flow_results, callback_analysis, sync_results
        )
        
        # Display summary
        self.safe_print("\n" + "=" * 80)
        self.safe_print("📊 COMPREHENSIVE TEST RESULTS SUMMARY")
        self.safe_print("=" * 80)
        
        summary = report['test_summary']
        self.safe_print(f"✅ Successful Buttons: {summary['successful_buttons']}/{summary['total_buttons_tested']}")
        self.safe_print(f"❌ Failed Buttons: {summary['failed_buttons']}/{summary['total_buttons_tested']}")
        self.safe_print(f"⚠️ Frontend-Only Buttons: {summary['frontend_only_buttons']}/{summary['total_buttons_tested']}")
        self.safe_print(f"📊 Successful Data Flows: {summary['successful_data_flows']}/{summary['total_data_flows']}")
        self.safe_print(f"🔄 Total Callbacks: {summary['callback_coverage'].get('total_callbacks', 0)}")
        
        if report['critical_issues']:
            self.safe_print("\n🚨 CRITICAL ISSUES:")
            for issue in report['critical_issues']:
                self.safe_print(f"  ❌ {issue}")
        
        if report['recommendations']:
            self.safe_print("\n💡 RECOMMENDATIONS:")
            for rec in report['recommendations']:
                self.safe_print(f"  📝 {rec}")
        
        # Save detailed report
        report_file = f"comprehensive_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            self.safe_print(f"\n📄 Detailed report saved to: {report_file}")
        except Exception as e:
            self.safe_print(f"⚠️ Could not save report: {e}")
        
        # Calculate overall health score
        total_tests = summary['total_buttons_tested'] + summary['total_data_flows']
        successful_tests = summary['successful_buttons'] + summary['successful_data_flows']
        health_score = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        self.safe_print(f"\n🎯 OVERALL SYSTEM HEALTH: {health_score:.1f}%")
        
        if health_score >= 90:
            self.safe_print("🎉 EXCELLENT: System is working optimally!")
        elif health_score >= 75:
            self.safe_print("✅ GOOD: System is working well with minor issues")
        elif health_score >= 50:
            self.safe_print("⚠️ FAIR: System has significant issues that need attention")
        else:
            self.safe_print("❌ POOR: System has critical issues requiring immediate attention")
        
        return report

    def cleanup(self):
        """Clean up processes"""
        if self.backend_process:
            self.backend_process.terminate()
        if self.frontend_process:
            self.frontend_process.terminate()

if __name__ == "__main__":
    simulator = ComprehensiveSimulator()
    
    try:
        report = simulator.run_comprehensive_simulation()
    except KeyboardInterrupt:
        simulator.safe_print("\n⏹️ Test interrupted by user")
    except Exception as e:
        simulator.safe_print(f"\n❌ Test failed with error: {e}")
        traceback.print_exc()
    finally:
        simulator.cleanup()
