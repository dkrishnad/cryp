"""
Minimal working FastAPI server for the crypto bot
This ensures the server starts and basic endpoints work
"""

from fastapi import FastAPI, Body, Query
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
import json
import os
import sys
import time
from datetime import datetime
import random
import uvicorn

print("[INFO] Starting minimal crypto bot backend...")

# Create FastAPI app
app = FastAPI(
    title="Crypto Bot Backend",
    description="Minimal working backend for crypto trading bot",
    version="1.0.0"
)

# Global state
virtual_balance = 10000.0
auto_trading_enabled = False
trades = []

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "service": "crypto-bot-backend"
    }

# Basic trading endpoints
@app.get("/balance")
def get_balance():
    """Get current virtual balance"""
    return {
        "status": "success",
        "balance": virtual_balance,
        "currency": "USD"
    }

@app.get("/trades")
def get_trades():
    """Get all trades"""
    return {
        "status": "success",
        "trades": trades,
        "count": len(trades)
    }

@app.get("/trades/recent")
def get_recent_trades(limit: int = 10):
    """Get recent trades"""
    recent = trades[-limit:] if trades else []
    return {
        "status": "success",
        "trades": recent,
        "count": len(recent)
    }

# Price endpoints
@app.get("/price/{symbol}")
def get_price(symbol: str):
    """Get current price for a symbol"""
    # Mock price data
    base_prices = {
        "BTCUSDT": 45000,
        "ETHUSDT": 3000,
        "BNBUSDT": 300
    }
    base_price = base_prices.get(symbol.upper(), 100)
    current_price = base_price + random.uniform(-1000, 1000)
    
    return {
        "status": "success",
        "symbol": symbol.upper(),
        "price": round(current_price, 2),
        "timestamp": datetime.now().isoformat()
    }

# Auto trading endpoints
@app.get("/auto_trading/status")
def get_auto_trading_status():
    """Get auto trading status"""
    return {
        "status": "success",
        "enabled": auto_trading_enabled,
        "balance": virtual_balance,
        "active_trades": len(trades)
    }

@app.post("/auto_trading/enable")
def enable_auto_trading():
    """Enable auto trading"""
    global auto_trading_enabled
    auto_trading_enabled = True
    return {
        "status": "success",
        "enabled": True,
        "message": "Auto trading enabled"
    }

@app.post("/auto_trading/disable")
def disable_auto_trading():
    """Disable auto trading"""
    global auto_trading_enabled
    auto_trading_enabled = False
    return {
        "status": "success",
        "enabled": False,
        "message": "Auto trading disabled"
    }

# ML prediction endpoints
@app.get("/ml/predict")
def ml_predict(symbol: str = "BTCUSDT"):
    """Get ML prediction"""
    prediction = random.choice(["BUY", "SELL", "HOLD"])
    confidence = random.uniform(0.5, 0.9)
    
    return {
        "status": "success",
        "symbol": symbol,
        "prediction": prediction,
        "confidence": confidence,
        "timestamp": datetime.now().isoformat()
    }

# Settings endpoints
@app.get("/settings")
def get_settings():
    """Get bot settings"""
    return {
        "status": "success",
        "settings": {
            "auto_trading_enabled": auto_trading_enabled,
            "max_trade_amount": 1000,
            "risk_percent": 2.0,
            "stop_loss_percent": 5.0,
            "take_profit_percent": 10.0
        }
    }

@app.post("/settings")
def update_settings(settings: dict = Body(...)):
    """Update bot settings"""
    return {
        "status": "success",
        "settings": settings,
        "message": "Settings updated successfully"
    }

# Sidebar amount buttons
@app.post("/sidebar/amount/50")
def set_amount_50():
    return {"status": "success", "amount": 50, "message": "Amount set to $50"}

@app.post("/sidebar/amount/100")
def set_amount_100():
    return {"status": "success", "amount": 100, "message": "Amount set to $100"}

@app.post("/sidebar/amount/250")
def set_amount_250():
    return {"status": "success", "amount": 250, "message": "Amount set to $250"}

@app.post("/sidebar/amount/500")
def set_amount_500():
    return {"status": "success", "amount": 500, "message": "Amount set to $500"}

@app.post("/sidebar/amount/1000")
def set_amount_1000():
    return {"status": "success", "amount": 1000, "message": "Amount set to $1000"}

@app.post("/sidebar/amount/max")
def set_amount_max():
    return {"status": "success", "amount": virtual_balance * 0.95, "message": f"Amount set to max: ${virtual_balance * 0.95:.2f}"}

# Chart endpoints
@app.get("/charts/volume")
def get_volume_data():
    return {
        "status": "success",
        "data": [random.uniform(1000, 5000) for _ in range(24)]
    }

@app.get("/charts/momentum")
def get_momentum_data():
    return {
        "status": "success",
        "rsi": random.uniform(30, 70),
        "macd": random.uniform(-0.1, 0.1)
    }

# Performance dashboard
@app.get("/performance/dashboard")
def get_performance_dashboard():
    return {
        "status": "success",
        "dashboard": {
            "total_trades": len(trades),
            "win_rate": 0.65,
            "daily_pnl": random.uniform(-100, 200),
            "balance": virtual_balance
        }
    }

# Notifications
@app.get("/notifications")
def get_notifications():
    return {
        "status": "success",
        "notifications": [],
        "count": 0
    }

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Crypto Bot Backend API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    print("[INFO] Starting Crypto Bot Backend Server (minimal)")
    print("[INFO] Server URL: http://localhost:8000")
    print("[INFO] API Docs: http://localhost:8000/docs")
    print("[INFO] Health Check: http://localhost:8000/health")
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, log_level="info")
    except Exception as e:
        print(f"[ERROR] Server startup error: {e}")
