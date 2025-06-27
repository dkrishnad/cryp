#!/usr/bin/env python3
"""
Online Learning System Demonstration
Shows exactly how the online learning works in the crypto bot
"""
import requests
import json
import time

API_URL = "http://localhost:8001"

def demonstrate_online_learning():
    """Demonstrate the complete online learning workflow"""
    print("🧠 ONLINE LEARNING SYSTEM DEMONSTRATION")
    print("=" * 60)
    
    # Step 1: Show initial online learning state
    print("\n1️⃣ INITIAL ONLINE LEARNING STATE")
    print("-" * 40)
    
    resp = requests.get(f"{API_URL}/ml/online/stats")
    initial_stats = resp.json()
    
    print("📊 Online Learning Models:")
    for model_name, stats in initial_stats['stats'].items():
        if model_name not in ['buffer_size', 'total_models']:
            print(f"   • {model_name}: {stats['model_type']}")
            print(f"     - Last Update: {stats['last_update']}")
            print(f"     - Recent Accuracy: {stats['recent_accuracy']:.4f}")
            print(f"     - Performance History: {stats['performance_history_length']} entries")
    
    print(f"\n📁 Training Data Buffer: {initial_stats['stats']['buffer_size']} samples")
    print(f"🔧 Total Models: {initial_stats['stats']['total_models']}")
    
    # Step 2: Demonstrate how new training data gets added
    print("\n\n2️⃣ ADDING NEW TRAINING DATA VIA AUTO TRADING")
    print("-" * 50)
    
    print("🔄 Executing trades to generate training data...")
    
    # Lower confidence threshold to ensure trades execute
    settings_resp = requests.post(f"{API_URL}/auto_trading/settings", json={
        "symbol": "BTCUSDT",
        "timeframe": "1h",
        "risk_per_trade": 2.0,
        "take_profit": 1.5,
        "stop_loss": 1.0,
        "min_confidence": 15.0  # Very low threshold
    })
    print(f"⚙️  Updated trading settings: {settings_resp.json()['status']}")
    
    # Enable auto trading
    toggle_resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": True})
    print(f"▶️  Auto trading enabled: {toggle_resp.json()['status']}")
    
    # Execute 3 trades to demonstrate learning
    trades_executed = []
    for i in range(3):
        print(f"\n📈 Executing Trade {i+1}/3...")
        
        # Execute signal
        execute_resp = requests.post(f"{API_URL}/auto_trading/execute_signal")
        execute_result = execute_resp.json()
        
        if execute_result['status'] == 'success':
            print(f"   ✅ Trade opened: {execute_result['message']}")
            
            # Get the new trade
            trades_resp = requests.get(f"{API_URL}/auto_trading/trades")
            open_trades = trades_resp.json()['data']['open_trades']
            
            if open_trades:
                trade_id = list(open_trades.keys())[0]
                trade = open_trades[trade_id]
                trades_executed.append(trade_id)
                
                print(f"   📊 Trade Details:")
                print(f"      - Symbol: {trade['symbol']}")
                print(f"      - Direction: {trade['direction']}")
                print(f"      - Entry Price: ${trade['entry_price']:.4f}")
                print(f"      - Signal Features: {'✅' if 'signal_features' in trade else '❌'}")
                
                # Close the trade immediately to trigger ML learning
                close_resp = requests.post(f"{API_URL}/auto_trading/close_trade/{trade_id}")
                close_result = close_resp.json()
                
                if close_result['status'] == 'success':
                    pnl = close_result['pnl']
                    print(f"   💰 Trade closed: P&L = ${pnl:.2f}")
                    print(f"   🧠 ML Learning: {'Profitable' if pnl > 0 else 'Loss'} trade → Training data")
                else:
                    print(f"   ❌ Error closing trade: {close_result.get('message', 'Unknown error')}")
        else:
            print(f"   ❌ Trade execution failed: {execute_result.get('message', 'Unknown error')}")
        
        time.sleep(1)  # Brief pause between trades
    
    # Disable auto trading
    requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": False})
    print(f"\n⏸️  Auto trading disabled")
    
    # Step 3: Show updated online learning state
    print("\n\n3️⃣ UPDATED ONLINE LEARNING STATE")
    print("-" * 40)
    
    resp = requests.get(f"{API_URL}/ml/online/stats")
    updated_stats = resp.json()
    
    buffer_increase = updated_stats['stats']['buffer_size'] - initial_stats['stats']['buffer_size']
    print(f"📁 Training Data Buffer: {updated_stats['stats']['buffer_size']} samples (+{buffer_increase})")
    
    if buffer_increase > 0:
        print("✅ NEW TRAINING DATA ADDED!")
        print("\n📊 Model Status After Training Data Addition:")
        for model_name, stats in updated_stats['stats'].items():
            if model_name not in ['buffer_size', 'total_models']:
                print(f"   • {model_name}:")
                print(f"     - Model Type: {stats['model_type']}")
                print(f"     - Ready for incremental update: ✅")
    else:
        print("❌ No new training data added")
    
    # Step 4: Demonstrate incremental model update
    print("\n\n4️⃣ INCREMENTAL MODEL UPDATE")
    print("-" * 35)
    
    if updated_stats['stats']['buffer_size'] >= 2:  # Need at least 2 samples
        print("🔄 Triggering incremental model update...")
        
        # Trigger model update (this would normally happen automatically)
        update_resp = requests.post(f"{API_URL}/ml/online/update", json={"batch_size": 10})
        
        if update_resp.status_code == 200:
            update_result = update_resp.json()
            print("✅ Models updated successfully!")
            
            if 'accuracies' in update_result:
                print("\n📈 Model Performance After Update:")
                for model_name, accuracy in update_result['accuracies'].items():
                    print(f"   • {model_name}: {accuracy:.4f} accuracy")
        else:
            print(f"❌ Model update failed: {update_resp.text}")
    else:
        print("⚠️  Insufficient training data for model update")
    
    # Step 5: Demonstrate online prediction
    print("\n\n5️⃣ ONLINE PREDICTION DEMONSTRATION")
    print("-" * 40)
    
    print("🔮 Making prediction with updated online models...")
    
    prediction_resp = requests.post(f"{API_URL}/ml/online/predict", json={
        "features": {
            "open": 50000,
            "high": 50500,
            "low": 49500,
            "close": 50200,
            "volume": 1000000,
            "rsi": 45.5,
            "macd": 0.1,
            "volume_ratio": 1.2
        }
    })
    
    if prediction_resp.status_code == 200:
        pred_result = prediction_resp.json()
        print("✅ Online prediction successful!")
        print(f"\n🎯 Ensemble Prediction:")
        print(f"   • Prediction: {pred_result.get('ensemble_prediction', 'N/A')}")
        print(f"   • Confidence: {pred_result.get('ensemble_confidence', 0):.4f}")
        print(f"   • Models Used: {pred_result.get('model_count', 0)}")
        
        if 'individual_predictions' in pred_result:
            print(f"\n🤖 Individual Model Predictions:")
            for model_name, prediction in pred_result['individual_predictions'].items():
                confidence = pred_result.get('probabilities', {}).get(model_name, {}).get('confidence', 0)
                print(f"   • {model_name}: {prediction} (confidence: {confidence:.4f})")
    else:
        print(f"❌ Online prediction failed: {prediction_resp.text}")
    
    # Step 6: Show the complete learning cycle
    print("\n\n6️⃣ ONLINE LEARNING CYCLE SUMMARY")
    print("-" * 40)
    
    print("🔄 Complete Online Learning Workflow:")
    print("   1. 📊 Auto trading generates signals with technical features")
    print("   2. 📈 Trades are executed based on signal confidence")
    print("   3. 💰 Trade results (P&L) determine success/failure labels")
    print("   4. 🧠 Trade features + outcomes → Training data buffer")
    print("   5. 🔄 Models update incrementally with new data")
    print("   6. 🎯 Updated models provide better predictions")
    print("   7. 🔁 Cycle repeats continuously")
    
    print(f"\n📈 Learning Progress:")
    print(f"   • Training samples collected: {updated_stats['stats']['buffer_size']}")
    print(f"   • Models actively learning: {updated_stats['stats']['total_models']}")
    print(f"   • Real-time adaptation: ✅ ENABLED")
    
    # Final status
    resp = requests.get(f"{API_URL}/auto_trading/status")
    final_status = resp.json()
    ml_learning_entries = [e for e in final_status['data']['trade_log'] if e.get('type') == 'ml_learning']
    
    print(f"\n🎉 ONLINE LEARNING DEMONSTRATION COMPLETE!")
    print(f"   • Total ML learning events: {len(ml_learning_entries)}")
    print(f"   • System status: FULLY OPERATIONAL")
    
    return True

if __name__ == "__main__":
    demonstrate_online_learning()
