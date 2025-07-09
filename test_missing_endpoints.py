#!/usr/bin/env python3
"""
Quick endpoint test to see which endpoints are registered
"""
import requests
import json

# List of failed endpoints from the simulation
failed_endpoints = [
    "/futures/execute",
    "/futures/open_position", 
    "/futures/close_position",
    "/portfolio/reset",
    "/binance/auto_execute",
    "/binance/manual_trade",
    "/ml/online_learning/enable",
    "/ml/online_learning/disable",
    "/ml/transfer_learning/init",
    "/ml/target_model/train",
    "/ml/learning_rates/optimize",
    "/ml/learning_rates/reset",
    "/ml/model/force_update",
    "/ml/model/retrain",
    "/hft/analysis/start",
    "/hft/analysis/stop",
    "/hft/config",
    "/notifications/send_manual_alert",
    "/notifications/clear_all",
    "/notifications/mark_all_read",
    "/data/collection/start",
    "/data/collection/stop",
    "/backtest/comprehensive",
    "/data/symbol_data"
]

def test_endpoint(endpoint):
    """Test if an endpoint exists"""
    try:
        response = requests.get(f"http://localhost:5000{endpoint}", timeout=2)
        if response.status_code == 404:
            return "❌ NOT FOUND"
        elif response.status_code == 405:
            return "⚠️ METHOD NOT ALLOWED"
        elif response.status_code == 200:
            return "✅ SUCCESS"
        else:
            return f"🔶 {response.status_code}"
    except Exception as e:
        return f"💥 ERROR: {str(e)}"

print("🔍 TESTING FAILED ENDPOINTS:")
print("=" * 50)

for endpoint in failed_endpoints:
    result = test_endpoint(endpoint)
    print(f"{endpoint:35} {result}")

print("=" * 50)
print("🎯 SUMMARY:")
missing = len([ep for ep in failed_endpoints if test_endpoint(ep) == "❌ NOT FOUND"])
print(f"Missing endpoints: {missing}/{len(failed_endpoints)}")
