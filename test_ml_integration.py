#!/usr/bin/env python3
"""
Test ML Integration with Auto Trading
Verifies that auto trading feeds results back to ML models for continuous learning
"""
import requests
import json
import time

API_URL = "http://localhost:8000"

def test_ml_integration():
    """Test complete ML integration with auto trading"""
    print("🧠 TESTING ML INTEGRATION WITH AUTO TRADING")
    print("=" * 60)
    
    # Step 1: Check ML system status
    print("\n📋 Step 1: Checking ML System Status")
    ml_status = requests.get(f"{API_URL}/ml/hybrid/status")
    if ml_status.status_code == 200:
        print("✅ ML Hybrid System: Available")
        print(f"   Status: {ml_status.json()}")
    else:
        print("❌ ML Hybrid System: Not available")
    
    online_stats = requests.get(f"{API_URL}/ml/online/stats")
    if online_stats.status_code == 200:
        print("✅ Online Learning: Available")
        print(f"   Stats: {online_stats.json()}")
    else:
        print("❌ Online Learning: Not available")
    
    # Step 2: Get initial auto trading status
    print("\n📋 Step 2: Getting Initial Auto Trading Status")
    status_resp = requests.get(f"{API_URL}/auto_trading/status")
    if status_resp.status_code == 200:
        initial_status = status_resp.json()["data"]
        print(f"✅ Auto Trading Status: {initial_status['enabled']}")
        print(f"   Balance: ${initial_status['balance']}")
        print(f"   Total Trades: {initial_status['performance_stats']['total_trades']}")
    else:
        print("❌ Could not get auto trading status")
        return False
    
    # Step 3: Enable auto trading with low confidence threshold for testing
    print("\n📋 Step 3: Configuring Auto Trading for ML Testing")
    
    # Set low confidence threshold to ensure trades execute
    settings_resp = requests.post(f"{API_URL}/auto_trading/settings", json={
        "symbol": "BTCUSDT",
        "risk_per_trade": 2.0,  # Low risk for testing
        "min_confidence": 30.0,  # Low threshold to ensure execution
        "take_profit": 1.0,
        "stop_loss": 0.5
    })
    
    if settings_resp.status_code == 200:
        print("✅ Settings updated for ML testing")
    else:
        print("❌ Failed to update settings")
        return False
    
    # Enable auto trading
    toggle_resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": True})
    if toggle_resp.status_code == 200:
        print("✅ Auto trading enabled")
    else:
        print("❌ Failed to enable auto trading")
        return False
    
    # Step 4: Test signal generation with ML enhancement
    print("\n📋 Step 4: Testing ML-Enhanced Signal Generation")
    
    for i in range(3):
        print(f"\n   Signal Test {i+1}:")
        signal_resp = requests.get(f"{API_URL}/auto_trading/signals")
        
        if signal_resp.status_code == 200:
            signal_data = signal_resp.json()["signal"]
            print(f"   📊 Direction: {signal_data['direction']}")
            print(f"   📊 Confidence: {signal_data['confidence']:.1f}%")
            
            # Check if ML data is included
            if "ml_prediction" in signal_data:
                ml_data = signal_data["ml_prediction"]
                print(f"   🧠 ML Signal: {ml_data['signal']:.3f}")
                print(f"   🧠 ML Confidence: {ml_data['confidence']:.3f}")
                print(f"   🧠 ML Prediction: {ml_data['prediction']:.3f}")
                print("   ✅ ML integration detected in signals")
            else:
                print("   ❌ No ML data in signal response")
            
            # Check signal breakdown
            if "signal_breakdown" in signal_data:
                breakdown = signal_data["signal_breakdown"]
                print(f"   🔍 Technical Signal: {breakdown['technical_signal']:.3f}")
                print(f"   🔍 Final Combined: {breakdown['final_combined']:.3f}")
        else:
            print("   ❌ Failed to get signal")
        
        time.sleep(2)  # Wait between signal tests
    
    # Step 5: Execute trades and monitor ML learning
    print("\n📋 Step 5: Executing Trades and Monitoring ML Learning")
    
    initial_trade_count = initial_status['performance_stats']['total_trades']
    
    # Execute several signals to generate training data
    for i in range(3):
        print(f"\n   Trade Execution {i+1}:")
        execute_resp = requests.post(f"{API_URL}/auto_trading/execute_signal")
        
        if execute_resp.status_code == 200:
            result = execute_resp.json()
            print(f"   📈 Result: {result['status']} - {result['message']}")
            
            if result["status"] == "success" and result.get("action") == "trade_opened":
                print("   ✅ Trade opened successfully")
                
                # Wait a moment then close the trade manually to generate training data
                time.sleep(2)
                
                # Get current trades to find the trade ID
                trades_resp = requests.get(f"{API_URL}/auto_trading/trades")
                if trades_resp.status_code == 200:
                    trades_data = trades_resp.json()["data"]
                    open_trades = trades_data["open_trades"]
                    
                    if open_trades:
                        trade_id = list(open_trades.keys())[0]
                        print(f"   📝 Closing trade {trade_id} to generate ML training data...")
                        
                        close_resp = requests.post(f"{API_URL}/auto_trading/close_trade/{trade_id}")
                        if close_resp.status_code == 200:
                            close_result = close_resp.json()
                            pnl = close_result.get("pnl", 0)
                            print(f"   💰 Trade closed: P&L = ${pnl:.2f}")
                            print("   🧠 Training data should be generated now")
                        else:
                            print("   ❌ Failed to close trade")
            else:
                print(f"   ℹ️  No trade executed: {result['message']}")
        else:
            print("   ❌ Failed to execute signal")
        
        time.sleep(3)  # Wait between executions
    
    # Step 6: Check if ML received training data
    print("\n📋 Step 6: Verifying ML Learning from Trade Results")
    
    # Get updated online learning stats
    final_online_stats = requests.get(f"{API_URL}/ml/online/stats")
    if final_online_stats.status_code == 200:
        final_stats = final_online_stats.json()
        print("✅ Online Learning Final Stats:")
        print(f"   {json.dumps(final_stats, indent=2)}")
    
    # Check auto trading log for ML learning messages
    final_trades_resp = requests.get(f"{API_URL}/auto_trading/trades")
    if final_trades_resp.status_code == 200:
        final_trades_data = final_trades_resp.json()["data"]
        trade_log = final_trades_data["trade_log"]
        
        ml_learning_entries = [entry for entry in trade_log if entry.get("type") == "ml_learning"]
        
        print(f"\n🧠 ML Learning Log Entries Found: {len(ml_learning_entries)}")
        for entry in ml_learning_entries:
            print(f"   📝 {entry['timestamp']}: {entry['message']}")
        
        if ml_learning_entries:
            print("   ✅ ML is receiving training data from trade results!")
        else:
            print("   ❌ No ML learning entries found in trade log")
    
    # Step 7: Disable auto trading
    print("\n📋 Step 7: Cleanup - Disabling Auto Trading")
    disable_resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": False})
    if disable_resp.status_code == 200:
        print("✅ Auto trading disabled")
    
    # Final status
    final_status_resp = requests.get(f"{API_URL}/auto_trading/status")
    if final_status_resp.status_code == 200:
        final_status = final_status_resp.json()["data"]
        final_trade_count = final_status['performance_stats']['total_trades']
        trades_executed = final_trade_count - initial_trade_count
        
        print(f"\n📊 FINAL RESULTS:")
        print(f"   Trades Executed: {trades_executed}")
        print(f"   Final Balance: ${final_status['balance']}")
        print(f"   Total P&L: ${final_status['performance_stats']['total_pnl']}")
        
        if trades_executed > 0 and ml_learning_entries:
            print("   🎉 SUCCESS: ML Integration is working!")
            print("   🔄 Auto trading → ML learning feedback loop confirmed")
        else:
            print("   ⚠️  PARTIAL: Some components may need attention")
    
    return True

if __name__ == "__main__":
    try:
        test_ml_integration()
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
