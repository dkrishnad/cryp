#!/usr/bin/env python3
"""
Comprehensive test script for the Hybrid Learning System
Tests all components: data collection, online learning, batch training integration
"""
import requests
import json
import time
import numpy as np
from datetime import datetime

API_URL = "http://localhost:8000"

def test_api_endpoint(endpoint, method="GET", data=None, timeout=10):
    """Test an API endpoint with error handling"""
    try:
        start_time = time.time()
        
        if method == "GET":
            resp = requests.get(f"{API_URL}{endpoint}", timeout=timeout)
        elif method == "POST":
            resp = requests.post(f"{API_URL}{endpoint}", json=data, timeout=timeout)
        else:
            print(f"❌ Unsupported method: {method}")
            return None
            
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        
        print(f"📡 {method} {endpoint}")
        print(f"   ⏱️  Response time: {response_time:.2f}ms")
        print(f"   📊 Status: {resp.status_code}")
        
        if resp.status_code == 200:
            result = resp.json()
            print(f"   ✅ Success")
            return result
        else:
            print(f"   ❌ Error: {resp.text}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"   ⏰ TIMEOUT: {endpoint} took longer than {timeout} seconds")
        return None
    except Exception as e:
        print(f"   💥 Exception: {e}")
        return None

def test_hybrid_learning_system():
    """Test the complete hybrid learning system"""
    
    print("🚀 Testing Hybrid Learning System")
    print("=" * 60)
    
    # 1. Test system health
    print("\n1️⃣  Testing System Health")
    print("-" * 30)
    health = test_api_endpoint("/health")
    
    if not health:
        print("❌ Backend not available. Please start the backend first.")
        return
        
    # 2. Test hybrid learning status
    print("\n2️⃣  Testing Hybrid Learning Status")
    print("-" * 30)
    status = test_api_endpoint("/ml/hybrid/status")
    
    if status:
        print(f"   📈 System running: {status.get('data', {}).get('system_running', False)}")
        print(f"   🤖 Online models: {status.get('data', {}).get('online_learning', {}).get('total_models', 0)}")
        print(f"   💾 Data collection: {status.get('data', {}).get('data_collection', {}).get('is_running', False)}")
    
    # 3. Test online learning statistics
    print("\n3️⃣  Testing Online Learning Statistics")
    print("-" * 30)
    online_stats = test_api_endpoint("/ml/online/stats")
    
    if online_stats:
        stats = online_stats.get('stats', {})
        print(f"   🧠 Buffer size: {stats.get('buffer_size', 0)}")
        print(f"   🔢 Total models: {stats.get('total_models', 0)}")
        
        for model_name, model_stats in stats.items():
            if isinstance(model_stats, dict) and 'model_type' in model_stats:
                print(f"   📊 {model_name}: {model_stats.get('model_type', 'Unknown')} - Accuracy: {model_stats.get('recent_accuracy', 0):.4f}")
    
    # 4. Test data collection statistics
    print("\n4️⃣  Testing Data Collection Statistics")
    print("-" * 30)
    data_stats = test_api_endpoint("/ml/data_collection/stats")
    
    if data_stats:
        stats = data_stats.get('stats', {})
        print(f"   📡 Collection running: {stats.get('is_running', False)}")
        print(f"   ⏱️  Interval: {stats.get('collection_interval', 0)} seconds")
        print(f"   🎯 Symbols: {len(stats.get('symbols', []))}")
        
        symbol_stats = stats.get('symbol_stats', {})
        for symbol, symbol_data in symbol_stats.items():
            print(f"   📈 {symbol}: {symbol_data.get('total_records', 0)} records, last: {symbol_data.get('last_update', 'Never')}")
    
    # 5. Test adding training data
    print("\n5️⃣  Testing Online Training Data Addition")
    print("-" * 30)
    
    # Generate sample training data
    sample_features = {
        'open': 45000.0, 'high': 46000.0, 'low': 44500.0, 'close': 45500.0,
        'volume': 1000000.0, 'rsi': 65.2, 'stoch_k': 78.5, 'stoch_d': 72.1,
        'williams_r': -21.8, 'roc': 2.34, 'ao': 150.2, 'macd': 1.23,
        'macd_signal': 1.15, 'macd_diff': 0.08, 'adx': 28.7, 'cci': 112.5,
        'sma_20': 45200.0, 'ema_20': 45300.0, 'bb_high': 46000.0, 'bb_low': 44500.0,
        'atr': 800.0, 'obv': 5000000.0, 'cmf': 0.15
    }
    
    training_data = {
        'features': sample_features,
        'target': np.random.randint(0, 2),
        'symbol': 'BTCUSDT'
    }
    
    add_result = test_api_endpoint("/ml/online/add_training_data", method="POST", data=training_data)
    
    if add_result:
        print(f"   ✅ Training data added. Buffer size: {add_result.get('buffer_size', 0)}")
    
    # 6. Test hybrid predictions
    print("\n6️⃣  Testing Hybrid Predictions")
    print("-" * 30)
    
    test_symbols = ['btcusdt', 'kaiausdt', 'ethusdt']
    
    for symbol in test_symbols:
        print(f"\n   Testing {symbol.upper()}")
        prediction = test_api_endpoint(f"/ml/hybrid/predict?symbol={symbol}")
        
        if prediction:
            pred_data = prediction.get('prediction', {})
            print(f"   🎯 Ensemble: {pred_data.get('ensemble_prediction', 'N/A')}")
            print(f"   🎲 Confidence: {pred_data.get('ensemble_confidence', 0):.4f}")
            print(f"   🤖 Models used: {pred_data.get('model_count', 0)}")
            
            if pred_data.get('batch_prediction') is not None:
                print(f"   📊 Batch model: {pred_data.get('batch_prediction')}")
            
            online_preds = pred_data.get('individual_predictions', {})
            if online_preds:
                print(f"   🧠 Online models: {online_preds}")
    
    # 7. Test online model update
    print("\n7️⃣  Testing Online Model Update")
    print("-" * 30)
    
    # First add more training data
    for i in range(10):
        random_features = {k: v + np.random.normal(0, v * 0.1) for k, v in sample_features.items()}
        random_training = {
            'features': random_features,
            'target': np.random.randint(0, 2),
            'symbol': f'TEST_{i%3}'
        }
        test_api_endpoint("/ml/online/add_training_data", method="POST", data=random_training)
    
    # Now trigger update
    update_result = test_api_endpoint("/ml/online/update?batch_size=10", method="POST")
    
    if update_result:
        results = update_result.get('update_results', {})
        print(f"   ✅ Models updated: {len(results)}")
        for model_name, accuracy in results.items():
            print(f"   📊 {model_name}: {accuracy:.4f}")
    
    # 8. Test performance history
    print("\n8️⃣  Testing Performance History")
    print("-" * 30)
    
    history = test_api_endpoint("/ml/performance/history")
    
    if history:
        hist_data = history.get('performance_history', [])
        print(f"   📈 History entries: {len(hist_data)}")
        
        if hist_data:
            latest = hist_data[-1]
            print(f"   ⏰ Latest: {latest.get('timestamp', 'Unknown')}")
            perf = latest.get('performance', {})
            print(f"   🎯 Latest accuracy: {perf.get('accuracy', 0):.4f}")
    
    # 9. Test configuration update
    print("\n9️⃣  Testing Configuration Update")
    print("-" * 30)
    
    new_config = {
        'online_update_interval_minutes': 45,
        'ensemble_weight_batch': 0.8,
        'ensemble_weight_online': 0.2
    }
    
    config_result = test_api_endpoint("/ml/hybrid/config", method="POST", data=new_config)
    
    if config_result:
        print(f"   ✅ Configuration updated successfully")
    
    # 10. Final status check
    print("\n🔟 Final System Status Check")
    print("-" * 30)
    
    final_status = test_api_endpoint("/ml/hybrid/status")
    
    if final_status:
        print("   ✅ System operational")
        data = final_status.get('data', {})
        config = data.get('configuration', {})
        print(f"   ⚙️  Batch weight: {config.get('ensemble_weight_batch', 'N/A')}")
        print(f"   ⚙️  Online weight: {config.get('ensemble_weight_online', 'N/A')}")
        print(f"   ⚙️  Update interval: {config.get('online_update_interval_minutes', 'N/A')} minutes")
    
    print("\n" + "=" * 60)
    print("🎉 Hybrid Learning System Test Complete!")
    print("=" * 60)

def test_quick_predictions():
    """Quick test of prediction endpoints"""
    print("\n🎯 Quick Prediction Test")
    print("-" * 30)
    
    # Test original indicators endpoint
    print("📊 Original indicators:")
    indicators = test_api_endpoint("/features/indicators?symbol=btcusdt")
    
    # Test new hybrid prediction
    print("\n🤖 Hybrid prediction:")
    hybrid_pred = test_api_endpoint("/ml/hybrid/predict?symbol=btcusdt")
    
    if indicators and hybrid_pred:
        print("\n📋 Comparison:")
        print(f"   Original regime: {indicators.get('regime', 'N/A')}")
        print(f"   Hybrid ensemble: {hybrid_pred.get('prediction', {}).get('ensemble_prediction', 'N/A')}")
        print(f"   Hybrid confidence: {hybrid_pred.get('prediction', {}).get('ensemble_confidence', 0):.4f}")

if __name__ == "__main__":
    print("🧪 Hybrid Learning System Test Suite")
    print("🔧 Make sure the backend is running on http://localhost:8000")
    print()
    
    # Wait a moment for user to see the message
    time.sleep(2)
    
    # Run comprehensive test
    test_hybrid_learning_system()
    
    # Run quick prediction comparison
    test_quick_predictions()
    
    print("\n✨ Testing complete! Check the results above.")
