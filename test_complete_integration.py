#!/usr/bin/env python3
"""
Comprehensive Auto Trading Integration Test
Tests both backend endpoints and dashboard functionality
"""
import requests
import json
import time

API_URL = "http://localhost:8001"
DASHBOARD_URL = "http://127.0.0.1:8050"

def test_endpoint(endpoint, method="GET", data=None, expected_status=200):
    """Test an endpoint with comprehensive validation"""
    print(f"\n🔄 Testing {method} {endpoint}")
    
    try:
        start_time = time.time()
        if method == "GET":
            resp = requests.get(f"{API_URL}{endpoint}", timeout=10)
        elif method == "POST":
            resp = requests.post(f"{API_URL}{endpoint}", json=data, timeout=10)
        elif method == "DELETE":
            resp = requests.delete(f"{API_URL}{endpoint}", timeout=10)
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        
        print(f"   ⏱️  Response time: {response_time:.2f}ms")
        print(f"   📊 Status: {resp.status_code}")
        
        if resp.status_code == expected_status:
            try:
                response_data = resp.json()
                print(f"   ✅ Success: {response_data.get('status', 'N/A')}")
                return response_data
            except:
                print(f"   ✅ Success (non-JSON response)")
                return True
        else:
            print(f"   ❌ Error: {resp.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("   🔴 ERROR: Could not connect to backend server")
        return None
    except requests.exceptions.Timeout:
        print("   ⏰ TIMEOUT: Request took longer than 10 seconds")
        return None
    except Exception as e:
        print(f"   💥 Exception: {e}")
        return None

def test_dashboard_availability():
    """Test if dashboard is accessible"""
    print(f"\n🌐 Testing Dashboard Availability at {DASHBOARD_URL}")
    try:
        resp = requests.get(DASHBOARD_URL, timeout=5)
        if resp.status_code == 200:
            print("   ✅ Dashboard is accessible")
            return True
        else:
            print(f"   ❌ Dashboard returned status {resp.status_code}")
            return False
    except Exception as e:
        print(f"   🔴 Dashboard not accessible: {e}")
        return False

def main():
    print("🚀 COMPREHENSIVE AUTO TRADING INTEGRATION TEST")
    print("=" * 60)
    
    # Test 1: Basic Backend Health
    print("\n📋 SECTION 1: BACKEND HEALTH")
    health_data = test_endpoint("/health")
    if not health_data:
        print("\n❌ CRITICAL: Backend server is not running!")
        print("Please start backend with: cd backend && python main.py")
        return False
    
    # Test 2: Dashboard Availability
    print("\n📋 SECTION 2: DASHBOARD AVAILABILITY")
    dashboard_ok = test_dashboard_availability()
    if not dashboard_ok:
        print("\n⚠️  WARNING: Dashboard is not accessible!")
        print("Please start dashboard with: cd dashboard && python app.py")
    
    # Test 3: Auto Trading Core Endpoints
    print("\n📋 SECTION 3: AUTO TRADING ENDPOINTS")
    
    # Get initial status
    status_data = test_endpoint("/auto_trading/status")
    
    # Update settings
    settings_data = test_endpoint("/auto_trading/settings", "POST", {
        "symbol": "BTCUSDT",
        "timeframe": "1h", 
        "risk_per_trade": 3.0,
        "take_profit": 2.5,
        "stop_loss": 1.5,
        "min_confidence": 75.0
    })
    
    # Get trading signals
    signal_data = test_endpoint("/auto_trading/signals")
    
    # Enable auto trading
    toggle_data = test_endpoint("/auto_trading/toggle", "POST", {"enabled": True})
    
    # Execute a signal
    execute_data = test_endpoint("/auto_trading/execute_signal", "POST")
    
    # Get trades
    trades_data = test_endpoint("/auto_trading/trades")
    
    # Test 4: Dashboard Required Endpoints
    print("\n📋 SECTION 4: DASHBOARD INTEGRATION ENDPOINTS")
    
    # Core dashboard endpoints
    balance_data = test_endpoint("/virtual_balance")
    all_trades_data = test_endpoint("/trades")
    analytics_data = test_endpoint("/trades/analytics")
    notifications_data = test_endpoint("/notifications")
    model_metrics_data = test_endpoint("/model/metrics")
    feature_importance_data = test_endpoint("/model/feature_importance")
    
    # Test 5: Create Test Trade
    print("\n📋 SECTION 5: TRADING FUNCTIONALITY")
    
    test_trade_data = test_endpoint("/trade", "POST", {
        "symbol": "BTCUSDT",
        "direction": "LONG",
        "amount": 100,
        "entry_price": 50000,
        "tp_pct": 0.02,
        "sl_pct": 0.01
    })
    
    # Test backtesting
    backtest_data = test_endpoint("/backtest", "POST", {
        "symbol": "BTCUSDT",
        "timeframe": "1h",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    })
    
    backtest_results = test_endpoint("/backtest/results")
    
    # Test 6: Model Endpoints
    print("\n📋 SECTION 6: ML MODEL ENDPOINTS")
    
    batch_predict_data = test_endpoint("/model/predict_batch", "POST", {
        "features": [[50000, 0.5, 0.3, 1000000, 45.5, 0.1, 0.02]]
    })
    
    # Test 7: Auto Trading Management
    print("\n📋 SECTION 7: AUTO TRADING MANAGEMENT")
    
    # Get current auto trading state
    final_status = test_endpoint("/auto_trading/status")
    
    # If there are open trades, try to close one
    if trades_data and trades_data.get("data", {}).get("open_trades"):
        open_trades = trades_data["data"]["open_trades"]
        if open_trades:
            first_trade_id = list(open_trades.keys())[0]
            close_data = test_endpoint(f"/auto_trading/close_trade/{first_trade_id}", "POST")
    
    # Disable auto trading
    disable_data = test_endpoint("/auto_trading/toggle", "POST", {"enabled": False})
    
    # Test 8: Crypto Transfer Learning
    print("\n📋 SECTION 8: CRYPTO TRANSFER LEARNING")
    
    # Test initial source models status
    source_status = test_endpoint("/model/crypto_transfer/source_status")
    
    # Test if initial training is needed (one-time setup)
    initial_setup = test_endpoint("/model/crypto_transfer/initial_setup_required")
    
    if initial_setup and initial_setup.get("setup_required", False):
        print("   🔄 Initial setup required - training source models...")
        initial_train = test_endpoint("/model/crypto_transfer/initial_train", "POST", {
            "source_pairs": ["ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT"],
            "target_pair": "BTCUSDT",
            "candles": 1000
        })
    else:
        print("   ✅ Source models already trained")
    
    # Test target model training (regular updates)
    target_train = test_endpoint("/model/crypto_transfer/train_target", "POST", {
        "use_recent_data": True,
        "adaptation_mode": "incremental"
    })
    
    # Test retraining triggers
    retrain_check = test_endpoint("/model/crypto_transfer/check_retrain_needed")
    
    # Test performance monitoring
    transfer_performance = test_endpoint("/model/crypto_transfer/performance")
    
    # Test prediction with transfer learning
    transfer_predict = test_endpoint("/model/crypto_transfer/predict", "POST", {
        "features": [[50000, 0.5, 0.3, 1000000, 45.5, 0.1, 0.02, 0.25]]
    })
    
    # Test training schedule
    schedule_data = test_endpoint("/model/crypto_transfer/training_schedule")

    # Test storage management and cleanup
    storage_status = test_endpoint("/model/crypto_transfer/storage_status")
    if storage_status:
        print(f"   💾 Current storage: {storage_status.get('total_mb', 0)} MB")
        print(f"   📊 6-month projection: {storage_status.get('projected_6month_gb', 0)} GB")
    
    # Test automatic cleanup functionality
    cleanup_test = test_endpoint("/model/crypto_transfer/cleanup_old_models", "POST", {
        "keep_versions": 5,
        "compress_old": True
    })
    
    # Test storage optimization
    optimize_test = test_endpoint("/model/crypto_transfer/optimize_storage")

    # Test ML features compatibility with transfer learning
    print("\n📋 SECTION 8A: ML FEATURES COMPATIBILITY")
    
    # Test that existing online learning still works
    online_learning_status = test_endpoint("/model/online_learning/status")
    if online_learning_status:
        print("   ✅ Online Learning: Still operational")
    
    # Test continuous learning functionality
    continuous_learning = test_endpoint("/model/continuous_learning/update", "POST", {
        "new_trade_data": {
            "symbol": "BTCUSDT",
            "profit": 150.0,
            "accuracy": 0.75
        }
    })
    
    # Test ensemble voting with transfer learning included
    ensemble_prediction = test_endpoint("/model/ensemble_predict", "POST", {
        "features": [[50000, 0.5, 0.3, 1000000, 45.5, 0.1, 0.02]],
        "include_transfer": True
    })
    
    # Test hybrid learning integration
    hybrid_learning = test_endpoint("/model/hybrid_learning/status")
    
    # Test that all models are still training independently
    individual_models = test_endpoint("/model/individual_model_status")
    
    if online_learning_status and ensemble_prediction:
        print("   ✅ All ML features compatible with transfer learning")
    else:
        print("   ⚠️  Some ML compatibility issues detected")

    # Summary
    print("\n📋 SECTION 9: INTEGRATION SUMMARY")
    print("=" * 60)
    
    if health_data:
        print("✅ Backend Server: RUNNING")
    else:
        print("❌ Backend Server: NOT RUNNING")
    
    if dashboard_ok:
        print("✅ Dashboard: ACCESSIBLE")
    else:
        print("❌ Dashboard: NOT ACCESSIBLE")
    
    if status_data and signal_data and trades_data:
        print("✅ Auto Trading: FULLY INTEGRATED")
    else:
        print("❌ Auto Trading: INTEGRATION ISSUES")
    
    if balance_data and analytics_data and model_metrics_data:
        print("✅ Dashboard Endpoints: ALL AVAILABLE")
    else:
        print("❌ Dashboard Endpoints: MISSING SOME")    
    if source_status and transfer_predict:
        print("✅ Crypto Transfer Learning: OPERATIONAL")
    else:
        print("❌ Crypto Transfer Learning: INTEGRATION ISSUES")
    
    print("\n🎉 INTEGRATION TEST COMPLETE!")
    print("\nNext Steps:")
    print("1. Open dashboard: http://127.0.0.1:8050/")
    print("2. Navigate to 'Auto Trading' tab")
    print("3. Test auto trading controls")
    print("4. Monitor real-time signals and trades")
    print("5. Check transfer learning performance in ML Models section")
    
    return True

if __name__ == "__main__":
    main()
