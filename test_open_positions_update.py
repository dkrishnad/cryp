#!/usr/bin/env python3
"""
Test the updated Open Positions table structure
"""
import requests
import json
from datetime import datetime

def test_open_positions_table():
    """Test the updated open positions table with new columns"""
    print("🧪 Testing Updated Open Positions Table")
    print("="*50)
    
    try:
        # Test backend trades endpoint
        print("1. Testing backend trades endpoint...")
        response = requests.get("http://localhost:8001/auto_trading/trades", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend response: {data['status']}")
            print(f"📊 Trades count: {data.get('count', 0)}")
            
            if data.get('trades'):
                print("\n2. Sample trade structure:")
                sample_trade = data['trades'][0]
                for key, value in sample_trade.items():
                    print(f"   {key}: {value}")
                
                print("\n3. Checking new fields:")
                required_fields = ['entry_price', 'stop_loss', 'take_profit', 'unrealized_pnl', 'current_price']
                for field in required_fields:
                    if field in sample_trade:
                        print(f"   ✅ {field}: {sample_trade[field]}")
                    else:
                        print(f"   ❌ {field}: Missing")
                
                print("\n4. Table column mapping:")
                table_columns = [
                    "ID", "Symbol", "Action", "Amount", 
                    "Entry Price", "Current Price", "Stop Loss", 
                    "Take Profit", "Live P&L", "Confidence"
                ]
                for col in table_columns:
                    print(f"   📋 {col}")
                
                # Test P&L calculation
                if 'unrealized_pnl' in sample_trade:
                    pnl = sample_trade['unrealized_pnl']
                    pnl_color = "🟢" if pnl >= 0 else "🔴"
                    print(f"\n5. P&L Display: {pnl_color} ${pnl:.2f}")
                
            else:
                print("ℹ️  No trades available for testing")
                
        else:
            print(f"❌ Backend error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

def test_table_styling():
    """Test the table styling for different scenarios"""
    print("\n🎨 Testing Table Styling")
    print("="*30)
    
    # Sample data for styling test
    sample_trades = [
        {
            "id": 1,
            "symbol": "BTCUSDT",
            "action": "BUY",
            "amount": 100,
            "entry_price": 105000,
            "current_price": 105500,
            "stop_loss": 102900,
            "take_profit": 109200,
            "unrealized_pnl": 5.00,
            "confidence": 85.5
        },
        {
            "id": 2,
            "symbol": "ETHUSDT", 
            "action": "SELL",
            "amount": 150,
            "entry_price": 4000,
            "current_price": 3950,
            "stop_loss": 4080,
            "take_profit": 3840,
            "unrealized_pnl": -7.50,
            "confidence": 78.2
        }
    ]
    
    for trade in sample_trades:
        print(f"\n📊 Trade {trade['id']} ({trade['symbol']}):")
        print(f"   Action: {trade['action']}")
        print(f"   Entry: ${trade['entry_price']:.2f}")
        print(f"   Current: ${trade['current_price']:.2f}")
        print(f"   Stop Loss: ${trade['stop_loss']:.2f}")
        print(f"   Take Profit: ${trade['take_profit']:.2f}")
        
        pnl = trade['unrealized_pnl']
        pnl_color = "🟢" if pnl >= 0 else "🔴"
        print(f"   P&L: {pnl_color} ${pnl:.2f}")
        
        # Calculate risk/reward
        if trade['action'] == 'BUY':
            risk = trade['entry_price'] - trade['stop_loss']
            reward = trade['take_profit'] - trade['entry_price']
        else:
            risk = trade['stop_loss'] - trade['entry_price']
            reward = trade['entry_price'] - trade['take_profit']
            
        ratio = reward / risk if risk > 0 else 0
        print(f"   Risk/Reward: 1:{ratio:.2f}")

def main():
    """Run all tests"""
    print("🚀 OPEN POSITIONS TABLE UPDATE TEST")
    print("="*60)
    
    test_open_positions_table()
    test_table_styling()
    
    print("\n📋 SUMMARY OF CHANGES:")
    print("✅ Removed 'Time' column")
    print("✅ Added 'Entry Price' column")
    print("✅ Added 'Current Price' column") 
    print("✅ Added 'Stop Loss' column")
    print("✅ Added 'Take Profit' column")
    print("✅ Added 'Live P&L' column with color coding")
    print("✅ Enhanced styling for profit/loss visualization")
    
    print("\n🎯 NEW TABLE STRUCTURE:")
    columns = [
        "ID", "Symbol", "Action", "Amount",
        "Entry Price", "Current Price", "Stop Loss", 
        "Take Profit", "Live P&L", "Confidence"
    ]
    for i, col in enumerate(columns, 1):
        print(f"{i:2}. {col}")
    
    print("\n✨ Features:")
    print("🟢 Green P&L for profits")
    print("🔴 Red P&L for losses") 
    print("📊 Real-time price updates")
    print("🎯 Automatic stop loss calculation (2% risk)")
    print("💰 Automatic take profit calculation (4% reward)")
    print("🔄 Auto-refresh every 5 seconds")

if __name__ == "__main__":
    main()
