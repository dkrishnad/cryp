#!/usr/bin/env python3
"""
Backend Endpoint Checker - Check which endpoints exist and which are missing
"""

import requests
import json
from datetime import datetime

def safe_print(message):
    """Safely print messages"""
    try:
        print(message)
    except UnicodeEncodeError:
        fallback_msg = message
        emoji_map = {
            "🔧": "[CONFIG]", "✅": "[OK]", "❌": "[ERROR]", "🚀": "[START]",
            "📊": "[DASHBOARD]", "💎": "[SUCCESS]", "🎉": "[READY]", "🐛": "[DEBUG]",
            "⚡": "[CALLBACK]", "🔍": "[TEST]", "📡": "[API]"
        }
        for emoji, text in emoji_map.items():
            fallback_msg = fallback_msg.replace(emoji, text)
        print(fallback_msg)

def test_endpoint(url, method="GET", data=None):
    """Test a single endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        
        return {
            "status_code": response.status_code,
            "success": response.status_code < 400,
            "content": response.text[:200] if len(response.text) < 200 else response.text[:200] + "..."
        }
    except Exception as e:
        return {
            "status_code": None,
            "success": False,
            "error": str(e)
        }

def check_backend_endpoints():
    """Check all backend endpoints that callbacks might use"""
    safe_print("🚀 Starting Backend Endpoint Check...")
    safe_print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Common endpoints that callbacks use
    endpoints = [
        # Health and status
        {"path": "/health", "method": "GET"},
        {"path": "/", "method": "GET"},
        
        # Account and balance
        {"path": "/account", "method": "GET"},
        {"path": "/balance", "method": "GET"},
        {"path": "/positions", "method": "GET"},
        
        # Trading
        {"path": "/buy", "method": "POST", "data": {"symbol": "BTCUSDT", "amount": 0.001}},
        {"path": "/sell", "method": "POST", "data": {"symbol": "BTCUSDT", "amount": 0.001}},
        {"path": "/cancel_order", "method": "POST", "data": {"order_id": "123"}},
        
        # Futures trading
        {"path": "/futures/account", "method": "GET"},
        {"path": "/futures/positions", "method": "GET"},
        {"path": "/futures/balance", "method": "GET"},
        {"path": "/futures/buy", "method": "POST", "data": {"symbol": "BTCUSDT", "amount": 0.001}},
        {"path": "/futures/sell", "method": "POST", "data": {"symbol": "BTCUSDT", "amount": 0.001}},
        
        # Price and market data
        {"path": "/price", "method": "GET"},
        {"path": "/prices", "method": "GET"},
        {"path": "/market_data", "method": "GET"},
        {"path": "/klines", "method": "GET"},
        
        # ML and predictions
        {"path": "/predict", "method": "POST", "data": {"symbol": "BTCUSDT"}},
        {"path": "/retrain", "method": "POST"},
        {"path": "/model_stats", "method": "GET"},
        {"path": "/analytics", "method": "GET"},
        
        # Auto trading
        {"path": "/auto_trading/start", "method": "POST"},
        {"path": "/auto_trading/stop", "method": "POST"},
        {"path": "/auto_trading/status", "method": "GET"},
        
        # System
        {"path": "/logs", "method": "GET"},
        {"path": "/settings", "method": "GET"},
        {"path": "/reset", "method": "POST"},
    ]
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "base_url": base_url,
        "endpoints": {},
        "summary": {
            "total": len(endpoints),
            "working": 0,
            "missing": 0,
            "errors": 0
        }
    }
    
    safe_print(f"📡 Testing {len(endpoints)} endpoints...\n")
    
    for endpoint in endpoints:
        path = endpoint["path"]
        method = endpoint["method"]
        data = endpoint.get("data")
        
        url = f"{base_url}{path}"
        result = test_endpoint(url, method, data)
        
        results["endpoints"][path] = {
            "method": method,
            "status_code": result["status_code"],
            "success": result["success"],
            "content": result.get("content", ""),
            "error": result.get("error", "")
        }
        
        # Update summary
        if result["success"]:
            status = f"✅ {result['status_code']}"
            results["summary"]["working"] += 1
        elif result["status_code"] == 404:
            status = f"❌ 404 (Missing)"
            results["summary"]["missing"] += 1
        elif result["status_code"]:
            status = f"⚠️ {result['status_code']}"
            results["summary"]["errors"] += 1
        else:
            status = f"❌ ERROR"
            results["summary"]["errors"] += 1
        
        safe_print(f"{method:4} {path:25} {status}")
        if result.get("error"):
            safe_print(f"     Error: {result['error']}")
    
    # Summary
    safe_print("\n" + "=" * 60)
    safe_print("📊 ENDPOINT CHECK SUMMARY")
    safe_print("=" * 60)
    safe_print(f"Total endpoints tested: {results['summary']['total']}")
    safe_print(f"✅ Working: {results['summary']['working']}")
    safe_print(f"❌ Missing (404): {results['summary']['missing']}")
    safe_print(f"⚠️ Errors: {results['summary']['errors']}")
    
    # Missing endpoints
    missing_endpoints = [
        path for path, details in results["endpoints"].items()
        if details["status_code"] == 404
    ]
    
    if missing_endpoints:
        safe_print(f"\n🔧 MISSING ENDPOINTS TO FIX:")
        for endpoint in missing_endpoints:
            safe_print(f"   - {endpoint}")
    
    # Save results
    with open("backend_endpoint_check.json", "w") as f:
        json.dump(results, f, indent=2)
    
    safe_print(f"\n💾 Results saved to: backend_endpoint_check.json")
    safe_print("\n🎉 Endpoint check complete!")
    
    return results

if __name__ == "__main__":
    check_backend_endpoints()
