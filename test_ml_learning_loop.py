#!/usr/bin/env python3
"""
Test ML Learning Feedback Loop
Specifically tests that trade results feed back to ML system for learning
"""
import requests
import json
import time

API_URL = "http://localhost:8001"

def test_ml_learning_loop():
    """Test the complete ML learning feedback loop"""
    print("🧠 TESTING ML LEARNING FEEDBACK LOOP")
    print("=" * 50)
    
    # Step 1: Check initial state
    print("\n1️⃣ Checking initial state...")
    
    # Get auto trading status
    resp = requests.get(f"{API_URL}/auto_trading/status")
    status_data = resp.json()
    print(f"   Auto Trading Enabled: {status_data['data']['enabled']}")
    print(f"   Balance: ${status_data['data']['balance']:.2f}")
    print(f"   Open Trades: {len(status_data['data']['open_trades'])}")
    
    # Get initial trade log count
    initial_log_count = len(status_data['data']['trade_log'])
    print(f"   Trade Log Entries: {initial_log_count}")
    
    # Step 2: Enable auto trading
    print("\n2️⃣ Enabling auto trading...")
    resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": True})
    print(f"   ✅ Auto trading enabled: {resp.json()['status']}")
    
    # Step 3: Execute a signal to create a trade
    print("\n3️⃣ Executing trading signal...")
    resp = requests.post(f"{API_URL}/auto_trading/execute_signal")
    execute_result = resp.json()
    print(f"   Signal execution: {execute_result['status']}")
    print(f"   Message: {execute_result['message']}")
    
    # Step 4: Check if trade was created
    print("\n4️⃣ Checking for new trade...")
    resp = requests.get(f"{API_URL}/auto_trading/trades")
    trades_data = resp.json()
    open_trades = trades_data['data']['open_trades']
    
    if open_trades:
        trade_id = list(open_trades.keys())[0]
        trade = open_trades[trade_id]
        print(f"   ✅ Trade created: {trade_id}")
        print(f"   Symbol: {trade['symbol']}")
        print(f"   Direction: {trade['direction']}")
        print(f"   Entry Price: ${trade['entry_price']:.4f}")
        print(f"   Signal Features Stored: {'signal_features' in trade}")
        
        # Step 5: Close the trade to trigger ML learning
        print("\n5️⃣ Closing trade to trigger ML learning...")
        resp = requests.post(f"{API_URL}/auto_trading/close_trade/{trade_id}")
        close_result = resp.json()
        print(f"   Trade closure: {close_result['status']}")
        print(f"   P&L: ${close_result.get('pnl', 0):.2f}")
        
        # Step 6: Check for ML learning log entry
        print("\n6️⃣ Checking for ML learning activity...")
        resp = requests.get(f"{API_URL}/auto_trading/status")
        updated_status = resp.json()
        trade_log = updated_status['data']['trade_log']
        
        # Look for ML learning entries
        ml_learning_entries = [entry for entry in trade_log if entry.get('type') == 'ml_learning']
        
        print(f"   Total trade log entries: {len(trade_log)}")
        print(f"   ML learning entries: {len(ml_learning_entries)}")
        
        if ml_learning_entries:
            latest_ml_entry = ml_learning_entries[-1]
            print(f"   ✅ ML Learning Detected!")
            print(f"   Timestamp: {latest_ml_entry['timestamp']}")
            print(f"   Message: {latest_ml_entry['message']}")
            print(f"   Trade ID: {latest_ml_entry.get('trade_id', 'N/A')}")
        else:
            print("   ❌ No ML learning entries found")        
        # Step 7: Check online learning buffer
        print("\n7️⃣ Checking online learning buffer...")
        resp = requests.get(f"{API_URL}/ml/online/stats")
        ml_stats = resp.json()
        
        if ml_stats['status'] == 'success':
            buffer_size = ml_stats.get('data', {}).get('buffer_size', 0)
            if buffer_size == 0 and 'buffer_size' in ml_stats:
                buffer_size = ml_stats['buffer_size']
            print(f"   Online learning buffer size: {buffer_size}")
            
            if buffer_size > 0:
                print("   ✅ Training data added to online learning buffer!")
            else:
                print("   ❌ No training data in online learning buffer")
        else:
            print(f"   ❌ Error getting ML stats: {ml_stats.get('message', 'Unknown error')}")
        
        # Step 8: Test ML prediction with the learned data
        print("\n8️⃣ Testing ML prediction...")
        resp = requests.post(f"{API_URL}/ml/hybrid/predict", json={
            "symbol": trade['symbol'],
            "features": {
                "rsi": 45.5,
                "macd": 0.1,
                "volume_ratio": 1.2,
                "current_price": 50000
            }
        })
        
        if resp.status_code == 200:
            prediction_result = resp.json()
            print(f"   ✅ ML Prediction successful")
            print(f"   Prediction: {prediction_result.get('data', {}).get('prediction', 'N/A')}")
            print(f"   Confidence: {prediction_result.get('data', {}).get('confidence', 'N/A')}")
        else:
            print(f"   ❌ ML Prediction failed: {resp.text}")
    
    else:
        print("   ❌ No trade was created")
    
    # Step 9: Disable auto trading
    print("\n9️⃣ Disabling auto trading...")
    resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": False})
    print(f"   ✅ Auto trading disabled: {resp.json()['status']}")
    
    # Final Summary
    print("\n📊 ML LEARNING LOOP TEST SUMMARY")
    print("=" * 50)
    
    # Check final state
    resp = requests.get(f"{API_URL}/auto_trading/status")
    final_status = resp.json()
    final_log = final_status['data']['trade_log']
    
    ml_entries = [entry for entry in final_log if entry.get('type') == 'ml_learning']
    
    if ml_entries:
        print("✅ ML LEARNING FEEDBACK LOOP: WORKING")
        print(f"   - {len(ml_entries)} ML learning events detected")
        print("   - Trade results are being fed to ML system")
        print("   - Online learning is receiving training data")
    else:
        print("❌ ML LEARNING FEEDBACK LOOP: NOT WORKING")
        print("   - No ML learning events detected")
        print("   - Need to debug ML integration")
    
    return len(ml_entries) > 0

if __name__ == "__main__":
    success = test_ml_learning_loop()
    if success:
        print("\n🎉 SUCCESS: ML Learning feedback loop is operational!")
    else:
        print("\n⚠️  NEEDS ATTENTION: ML Learning feedback loop needs debugging")
