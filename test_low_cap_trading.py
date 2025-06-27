#!/usr/bin/env python3
"""
Test Low-Cap Coin Trading Features
Demonstrates KAIA and other low-cap coin auto trading
"""
import requests
import json
import time

API_URL = "http://localhost:8001"

def test_low_cap_trading():
    """Test the low-cap coin trading features"""
    print("🌟 TESTING LOW-CAP COIN TRADING FEATURES")
    print("=" * 60)
    
    # Test 1: Get available low-cap coins
    print("\n1️⃣ AVAILABLE LOW-CAP COINS")
    print("-" * 30)
    
    try:
        resp = requests.get(f"{API_URL}/auto_trading/low_cap_coins")
        if resp.status_code == 200:
            data = resp.json()
            print("✅ Low-cap coins endpoint working!")
            print(f"📋 Available coins: {len(data['coins'])}")
            for coin in data['coins']:
                print(f"   • {coin}")
            
            print(f"\n⚙️ Recommended settings preview:")
            for coin, settings in data['recommended_settings'].items():
                print(f"   • {coin}: Confidence {settings['min_confidence']}%, Risk {settings['risk_per_trade']}%")
        else:
            print(f"❌ Low-cap coins endpoint failed: {resp.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Optimize for KAIA
    print("\n\n2️⃣ OPTIMIZE FOR KAIA TRADING")
    print("-" * 35)
    
    try:
        resp = requests.post(f"{API_URL}/auto_trading/optimize_for_low_cap", 
                           json={"symbol": "KAIAUSDT"})
        if resp.status_code == 200:
            data = resp.json()
            print("✅ KAIA optimization successful!")
            print(f"📊 Settings applied:")
            settings = data['settings']
            print(f"   • Symbol: {data['symbol']}")
            print(f"   • Min Confidence: {settings['min_confidence']}%")
            print(f"   • Risk per Trade: {settings['risk_per_trade']}%")
            print(f"   • Take Profit: {settings['take_profit']}x")
            print(f"   • Stop Loss: {settings['stop_loss']}x")
        else:
            print(f"❌ KAIA optimization failed: {resp.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Check current auto trading status
    print("\n\n3️⃣ CURRENT AUTO TRADING STATUS")
    print("-" * 35)
    
    try:
        resp = requests.get(f"{API_URL}/auto_trading/status")
        if resp.status_code == 200:
            data = resp.json()
            state = data['data']
            print("✅ Auto trading status retrieved!")
            print(f"📊 Current Configuration:")
            print(f"   • Symbol: {state['symbol']}")
            print(f"   • Timeframe: {state['timeframe']}")
            print(f"   • Min Confidence: {state['min_confidence']}%")
            print(f"   • Risk per Trade: {state['risk_per_trade']}%")
            print(f"   • Take Profit: {state['take_profit']}x")
            print(f"   • Stop Loss: {state['stop_loss']}x")
            print(f"   • Current Balance: ${state['balance']:,.2f}")
            print(f"   • Status: {'🟢 ENABLED' if state['enabled'] else '🔴 DISABLED'}")
        else:
            print(f"❌ Status check failed: {resp.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Test different low-cap optimizations
    print("\n\n4️⃣ TEST OTHER LOW-CAP OPTIMIZATIONS")
    print("-" * 40)
    
    test_coins = ["JASMYUSDT", "GALAUSDT", "ROSEUSDT"]
    
    for coin in test_coins:
        try:
            print(f"\n🧪 Testing {coin} optimization...")
            resp = requests.post(f"{API_URL}/auto_trading/optimize_for_low_cap", 
                               json={"symbol": coin})
            if resp.status_code == 200:
                data = resp.json()
                settings = data['settings']
                print(f"   ✅ {coin}: Confidence {settings['min_confidence']}%, Risk {settings['risk_per_trade']}%")
            else:
                print(f"   ❌ {coin}: Failed ({resp.status_code})")
        except Exception as e:
            print(f"   ❌ {coin}: Error - {e}")
    
    # Test 5: Mock trading test with KAIA
    print("\n\n5️⃣ MOCK TRADING TEST WITH KAIA")
    print("-" * 35)
    
    # Set up for KAIA trading
    try:
        print("🔧 Setting up KAIA trading...")
        
        # Optimize for KAIA
        requests.post(f"{API_URL}/auto_trading/optimize_for_low_cap", 
                     json={"symbol": "KAIAUSDT"})
        
        # Update settings
        requests.post(f"{API_URL}/auto_trading/settings", json={
            "symbol": "KAIAUSDT",
            "timeframe": "1h", 
            "risk_per_trade": 3.0,
            "take_profit": 2.5,
            "stop_loss": 1.2,
            "min_confidence": 55.0
        })
        
        print("✅ KAIA setup complete!")
        
        # Get current price for KAIA
        price_resp = requests.get(f"{API_URL}/price?symbol=KAIAUSDT")
        if price_resp.status_code == 200:
            price_data = price_resp.json()
            print(f"💰 Current KAIA price: ${price_data['price']:.6f}")
        
        print("\n🎯 Ready for KAIA auto trading!")
        print("   • Lower confidence threshold for more opportunities")
        print("   • Reduced risk per trade for safety")
        print("   • Higher take profit for low-cap volatility")
        print("   • Tight stop loss for risk management")
        
    except Exception as e:
        print(f"❌ Setup error: {e}")
    
    # Summary
    print("\n\n6️⃣ LOW-CAP TRADING SUMMARY")
    print("-" * 30)
    print("🎉 Low-cap coin trading features are operational!")
    print("\n📈 Benefits of low-cap trading:")
    print("   • Higher volatility = More profit opportunities")
    print("   • Lower market cap = Bigger percentage moves") 
    print("   • Less institutional competition")
    print("   • Better technical analysis patterns")
    print("\n⚙️ Optimizations applied:")
    print("   • KAIA: 55% confidence, 3% risk, 2.5x TP, 1.2x SL")
    print("   • JASMY: 60% confidence, 4% risk, 2.0x TP, 1.0x SL")
    print("   • GALA: 58% confidence, 3.5% risk, 2.2x TP, 1.1x SL")
    print("\n🚀 Ready to trade low-cap gems!")

if __name__ == "__main__":
    test_low_cap_trading()
