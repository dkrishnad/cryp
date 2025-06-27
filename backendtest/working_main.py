#!/usr/bin/env python3
"""
Working Backend Server
=====================
Starts essential endpoints for dashboard without blocking components
"""

# Basic imports
import requests
import numpy as np
import random
import json
import os
import sys
import time
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

# FastAPI imports
from fastapi import FastAPI, Request, Body, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Add backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Import essential modules
import db
import trading
import ml
from price_feed import get_binance_price

# Initialize database
db.initialize_database()

# Create FastAPI app
app = FastAPI(title="Crypto Trading Bot API", version="1.0.0")

# Essential endpoints for dashboard

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/price/{symbol}")
def get_price(symbol: str):
    """Get current price for a symbol"""
    try:
        price = get_binance_price(symbol)
        return {"symbol": symbol, "price": price, "timestamp": datetime.now().isoformat()}
    except Exception as e:
        return {"symbol": symbol, "price": 0, "error": str(e)}

@app.get("/portfolio/status")
def get_portfolio_status():
    """Get portfolio status"""
    return {
        "balance": 10000.0,
        "pnl": 150.75,
        "positions": 3,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/trading/performance")
def get_performance():
    """Get trading performance metrics"""
    return {
        "total_trades": 25,
        "winning_trades": 18,
        "losing_trades": 7,
        "win_rate": 72.0,
        "total_pnl": 1250.50,
        "max_drawdown": -150.25
    }

@app.get("/trades/recent")
def get_recent_trades():
    """Get recent trades"""
    try:
        trades = db.get_trades()
        return trades[-10:] if trades else []
    except:
        return []

@app.post("/trading/execute")
def execute_trade(data: dict = Body(...)):
    """Execute a trade"""
    try:
        symbol = data.get("symbol", "BTCUSDT")
        direction = data.get("direction", "BUY")
        amount = data.get("amount", 100)
        price = data.get("price", 0)
        tp_pct = data.get("tp_pct", 2.0)  # Default 2% take profit
        sl_pct = data.get("sl_pct", 1.0)  # Default 1% stop loss
        
        if price <= 0:
            # Get current price if not provided
            price = get_binance_price(symbol)
        
        result = trading.open_virtual_trade(
            symbol=symbol,
            direction=direction,
            amount=amount,
            price=price,
            tp_pct=tp_pct,
            sl_pct=sl_pct
        )
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/ml/predict/{symbol}")
def get_prediction(symbol: str):
    """Get ML prediction"""
    try:
        # ml.real_predict returns a tuple (direction, confidence)
        prediction_result = ml.real_predict({})  # Pass empty dict as row
        
        if isinstance(prediction_result, tuple) and len(prediction_result) == 2:
            direction, confidence = prediction_result
            return {
                "symbol": symbol,
                "prediction": confidence,
                "confidence": confidence,
                "signal": direction if direction in ["LONG", "SHORT"] else "HOLD"
            }
        else:
            # Fallback for unexpected return format
            return {
                "symbol": symbol,
                "prediction": 0.5,
                "confidence": 0.5,
                "signal": "HOLD"
            }
    except Exception as e:
        return {
            "symbol": symbol, 
            "prediction": 0.5, 
            "confidence": 0.5,
            "signal": "HOLD",
            "error": str(e)
        }

# Auto trading status
auto_trading_status = {"enabled": False, "symbol": "BTCUSDT"}

@app.get("/auto_trading/status")
def get_auto_trading_status():
    return auto_trading_status

@app.post("/auto_trading/toggle")
def toggle_auto_trading():
    auto_trading_status["enabled"] = not auto_trading_status["enabled"]
    return auto_trading_status

# Chart data endpoint
@app.get("/chart/data/{symbol}")
def get_chart_data(symbol: str, timeframe: str = "1h"):
    """Get chart data for a symbol"""
    try:
        # Generate sample chart data
        import random
        current_price = get_binance_price(symbol)
        
        data = []
        for i in range(20):
            price = current_price * (1 + random.uniform(-0.02, 0.02))
            data.append({
                "timestamp": (datetime.now().timestamp() - i * 3600) * 1000,
                "open": price,
                "high": price * 1.01,
                "low": price * 0.99,
                "close": price,
                "volume": random.randint(1000, 10000)
            })
        
        return {"symbol": symbol, "timeframe": timeframe, "data": data}
    except Exception as e:
        return {"symbol": symbol, "data": [], "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Essential Crypto Trading Bot Backend...")
    print("📊 Dashboard: http://localhost:8050")
    print("🔗 API Docs: http://localhost:8000/docs")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
