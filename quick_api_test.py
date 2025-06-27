#!/usr/bin/env python3
"""
Quick verification script for Binance-exact API
"""

import requests
import json
import sys
import os

def test_binance_api():
    """Test the Binance-exact API endpoints"""
    print("🧪 Testing Binance-Exact API Endpoints")
    print("=" * 50)
    
    base_url = "http://localhost:8001"
    results = []
    
    # Test endpoints
    endpoints = [
        ("GET", "/health", "Backend Health"),
        ("GET", "/fapi/v2/account", "Binance Account"),
        ("GET", "/fapi/v2/balance", "Binance Balance"),
        ("GET", "/fapi/v2/positionRisk", "Position Risk"),
        ("GET", "/fapi/v1/openOrders", "Open Orders"),
        ("GET", "/fapi/v1/ticker/24hr", "24hr Ticker"),
        ("GET", "/fapi/v1/exchangeInfo", "Exchange Info")
    ]
    
    for method, endpoint, name in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                results.append(f"✅ {name}: OK")
                if endpoint == "/fapi/v2/account":
                    data = response.json()
                    balance = data.get("totalWalletBalance", "N/A")
                    results.append(f"   💰 Total Balance: {balance} USDT")
            else:
                results.append(f"❌ {name}: HTTP {response.status_code}")
                
        except Exception as e:
            results.append(f"❌ {name}: {str(e)}")
    
    # Test order placement
    try:
        order_data = {
            "symbol": "BTCUSDT",
            "side": "BUY", 
            "type": "MARKET",
            "quantity": "0.001"
        }
        response = requests.post(f"{base_url}/fapi/v1/order", data=order_data, timeout=5)
        if response.status_code == 200:
            results.append("✅ Order Placement: OK")
            data = response.json()
            order_id = data.get("orderId", "N/A")
            results.append(f"   📋 Order ID: {order_id}")
        else:
            results.append(f"❌ Order Placement: HTTP {response.status_code}")
    except Exception as e:
        results.append(f"❌ Order Placement: {str(e)}")
    
    # Save results
    with open("api_test_results.txt", "w") as f:
        for result in results:
            f.write(result + "\n")
            print(result)
    
    print("\n📁 Results saved to: api_test_results.txt")
    
    # Summary
    success_count = len([r for r in results if r.startswith("✅")])
    total_count = len([r for r in results if r.startswith(("✅", "❌"))])
    
    print(f"\n📊 Summary: {success_count}/{total_count} tests passed")
    
    if success_count == total_count:
        print("🎉 All Binance-exact API endpoints are working!")
        return True
    else:
        print("⚠️  Some endpoints need attention")
        return False

if __name__ == "__main__":
    success = test_binance_api()
    sys.exit(0 if success else 1)
