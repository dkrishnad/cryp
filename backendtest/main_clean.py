from fastapi import FastAPI, UploadFile, File, Request, Body, Query, APIRouter
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager
import os
import json
import logging
from db import initialize_database, get_trades, save_trade, update_trade, delete_trade, save_notification, get_notifications as db_get_notifications, mark_notification_read, delete_notification
from trading import open_virtual_trade
from ml import real_predict
from ws import router as ws_router
from datetime import datetime
from fastapi.responses import JSONResponse

# Import hybrid learning system
from hybrid_learning import hybrid_orchestrator
from online_learning import online_learning_manager
from data_collection import get_data_collector

# Import email utilities
from email_utils import get_email_config, save_email_config, test_email_connection, send_email

# Configure logger
logger = logging.getLogger(__name__)

# Import minimal transfer learning endpoints for testing
from minimal_transfer_endpoints import get_minimal_transfer_router
from ml_compatibility_manager import MLCompatibilityManager

# Lifespan event handler to replace deprecated @app.on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        # Start the hybrid learning system
        hybrid_orchestrator.start_system()
        print("✓ Hybrid learning system started successfully")
    except Exception as e:
        print(f"⚠ Warning: Could not start hybrid learning system: {e}")
    
    yield
    
    # Shutdown
    try:
        hybrid_orchestrator.stop_system()
        print("✓ Hybrid learning system stopped")
    except Exception as e:
        print(f"⚠ Warning during shutdown: {e}")

app = FastAPI(lifespan=lifespan)

# Include WebSocket router
app.include_router(ws_router)

# Auto Trading Storage
auto_trading_settings = {
    "enabled": False,
    "symbol": "BTCUSDT",
    "entry_threshold": 0.7,
    "exit_threshold": 0.3,
    "max_positions": 3,
    "risk_per_trade": 2.0,
    "amount_config": {
        "type": "fixed",  # "fixed" or "percentage"
        "amount": 100.0,  # Fixed amount in USDT
        "percentage": 10.0  # Percentage of balance
    }
}

# Auto Trading Balance Storage
auto_trading_balance = {"balance": 5000.0}

# Auto Trading Status Storage
auto_trading_status = {
    "enabled": False,
    "active_trades": [],
    "total_profit": 0.0,
    "signals_processed": 0
}

# Auto Trading Signals Storage
recent_signals = []

# Store for auto trading trades
auto_trading_trades = []

class AutoTradingSettings(BaseModel):
    enabled: bool
    symbol: str
    entry_threshold: float
    exit_threshold: float
    max_positions: int
    risk_per_trade: float
    amount_config: dict

class SignalData(BaseModel):
    symbol: str
    signal: str
    confidence: float
    price: float
    timestamp: str

# --- Health Endpoint ---

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Crypto bot backend is running"}

# --- Risk Management Settings ---

risk_settings = {
    "max_drawdown": 10.0,
    "position_size": 2.0,
    "stop_loss": 5.0,
    "take_profit": 10.0
}

@app.get("/risk_settings")
def get_risk_settings():
    return risk_settings

@app.post("/risk_settings")
def update_risk_settings(settings: dict = Body(...)):
    global risk_settings
    risk_settings.update(settings)
    return {"status": "success", "settings": risk_settings}

# --- Model Version Management ---

model_versions = ["v1.0", "v1.1", "v2.0"]
active_version = "v2.0"

@app.get("/model/versions")
def get_model_versions():
    return {"versions": model_versions}

@app.get("/model/active_version")
def get_active_version():
    return {"active_version": active_version}

@app.post("/model/active_version")
def set_active_version(data: dict = Body(...)):
    global active_version
    version = data.get("version")
    if version in model_versions:
        active_version = version
        return {"status": "success", "active_version": active_version}
    return {"status": "error", "message": "Invalid version"}

# --- Real-Time Price Endpoint ---

@app.get("/price")
def get_price(symbol: str = "BTCUSDT"):
    try:
        import requests
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {"symbol": symbol.upper(), "price": float(data["price"])}
        else:
            return {"symbol": symbol.upper(), "price": 50000.0, "note": "fallback price"}
    except Exception as e:
        return {"symbol": symbol.upper(), "price": 50000.0, "error": str(e)}

# --- Model Analytics Endpoint ---

@app.get("/model/analytics")
def get_model_analytics():
    """Get model performance analytics"""
    try:
        # Mock analytics data - replace with actual model analytics
        analytics = {
            "accuracy": 0.78,
            "precision": 0.75,
            "recall": 0.82,
            "f1_score": 0.78,
            "trades_analyzed": 1500,
            "profitable_predictions": 1170,
            "loss_predictions": 330,
            "avg_confidence": 0.73,
            "last_updated": datetime.now().isoformat()
        }
        return {"status": "success", "analytics": analytics}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- Model Retrain on CSV Upload ---

@app.post("/retrain")
async def retrain_model(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        filename = f"uploads/{file.filename}"
        
        # Save uploaded file
        os.makedirs("uploads", exist_ok=True)
        with open(filename, "wb") as f:
            f.write(contents)
        
        # Mock retrain process
        return {
            "status": "success",
            "message": f"Model retrained with {file.filename}",
            "new_accuracy": 0.85,
            "training_samples": 1000
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# === AUTO TRADING ENDPOINTS ===

@app.get("/auto_trading/status")
def get_auto_trading_status():
    """Get current auto trading status"""
    try:
        # Load from persistent storage if exists
        if os.path.exists("data/auto_trading_status.json"):
            with open("data/auto_trading_status.json", "r") as f:
                stored_status = json.load(f)
                auto_trading_status.update(stored_status)
        
        return {
            "status": "success",
            "auto_trading": auto_trading_status
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/auto_trading/toggle")
def toggle_auto_trading(data: dict = Body(...)):
    """Toggle auto trading on/off"""
    try:
        enabled = data.get("enabled", False)
        auto_trading_status["enabled"] = enabled
        auto_trading_settings["enabled"] = enabled
        
        # Save to persistent storage
        os.makedirs("data", exist_ok=True)
        with open("data/auto_trading_status.json", "w") as f:
            json.dump(auto_trading_status, f)
        with open("data/auto_trading_settings.json", "w") as f:
            json.dump(auto_trading_settings, f)
        
        return {
            "status": "success",
            "enabled": enabled,
            "message": f"Auto trading {'enabled' if enabled else 'disabled'}"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/auto_trading/settings")
def update_auto_trading_settings(settings: AutoTradingSettings):
    """Update auto trading settings"""
    try:
        # Update settings
        auto_trading_settings.update(settings.model_dump())
        
        # Save to persistent storage
        os.makedirs("data", exist_ok=True)
        with open("data/auto_trading_settings.json", "w") as f:
            json.dump(auto_trading_settings, f)
        
        return {
            "status": "success",
            "settings": auto_trading_settings,
            "message": "Auto trading settings updated"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/auto_trading/signals")
def get_auto_trading_signals():
    """Get recent auto trading signals"""
    try:
        return {
            "status": "success",
            "signals": recent_signals[-10:],  # Last 10 signals
            "count": len(recent_signals)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/auto_trading/execute_signal")
def execute_auto_trading_signal(signal: SignalData):
    """Execute an auto trading signal"""
    try:
        # Add signal to recent signals
        signal_data = signal.model_dump()
        signal_data["executed_at"] = datetime.now().isoformat()
        recent_signals.append(signal_data)
        
        # Process signal if auto trading is enabled
        if auto_trading_status["enabled"]:
            # Create a mock trade
            trade_data = {
                "id": len(auto_trading_trades) + 1,
                "symbol": signal.symbol,
                "action": signal.signal,
                "amount": auto_trading_settings["amount_config"]["amount"],
                "price": signal.price,
                "confidence": signal.confidence,
                "status": "executed",
                "timestamp": signal.timestamp
            }
            auto_trading_trades.append(trade_data)
            
            # Update status
            auto_trading_status["signals_processed"] += 1
            auto_trading_status["active_trades"].append(trade_data["id"])
            
            return {
                "status": "success",
                "trade": trade_data,
                "message": f"Signal executed: {signal.signal} {signal.symbol}"
            }
        else:
            return {
                "status": "skipped",
                "message": "Auto trading is disabled"
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/auto_trading/trades")
def get_auto_trading_trades():
    """Get auto trading trades"""
    try:
        return {
            "status": "success", 
            "trades": auto_trading_trades,
            "count": len(auto_trading_trades)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/auto_trading/close_trade/{trade_id}")
def close_auto_trading_trade(trade_id: int):
    """Close an auto trading trade"""
    try:
        # Find and close the trade
        for trade in auto_trading_trades:
            if trade["id"] == trade_id:
                trade["status"] = "closed"
                trade["closed_at"] = datetime.now().isoformat()
                
                # Remove from active trades
                if trade_id in auto_trading_status["active_trades"]:
                    auto_trading_status["active_trades"].remove(trade_id)
                
                return {
                    "status": "success",
                    "trade": trade,
                    "message": f"Trade {trade_id} closed"
                }
        
        return {"status": "error", "message": "Trade not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/auto_trading/reset")
def reset_auto_trading():
    """Reset auto trading data"""
    try:
        global auto_trading_trades, recent_signals
        auto_trading_trades = []
        recent_signals = []
        auto_trading_status["active_trades"] = []
        auto_trading_status["total_profit"] = 0.0
        auto_trading_status["signals_processed"] = 0
        
        # Clear persistent storage
        for file_path in ["data/auto_trading_status.json", "data/auto_trading_settings.json"]:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        return {
            "status": "success",
            "message": "Auto trading data reset"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
        
# === END AUTO TRADING ENDPOINTS ===

initialize_database()

# --- Email Notification Settings ---
import db
@app.get("/settings/email_notifications")
def get_email_notifications_setting():
    value = db.get_setting("email_notifications", default="false")
    return {"enabled": value == "true"}

@app.post("/settings/email_notifications")
def set_email_notifications_setting(data: dict = Body(...)):
    enabled = data.get("enabled", False)
    db.set_setting("email_notifications", "true" if enabled else "false")
    return {"status": "ok", "enabled": enabled}

# --- Email Notification Address Settings ---
@app.get("/settings/email_address")
def get_email_address_setting():
    value = db.get_setting("email_address", default="")
    return {"email": value}

@app.post("/settings/email_address")
def set_email_address_setting(data: dict = Body(...)):
    email = data.get("email", "")
    db.set_setting("email_address", email)
    return {"status": "ok", "email": email}

# --- Hybrid Learning System Endpoints ---

@app.get("/ml/hybrid/status")
def get_hybrid_learning_status():
    """Get comprehensive status of the hybrid learning system"""
    try:
        status = hybrid_orchestrator.get_system_status()
        return {"status": "success", "data": status}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/ml/hybrid/config")
def update_hybrid_learning_config(config: dict = Body(...)):
    """Update hybrid learning configuration"""
    try:
        result = hybrid_orchestrator.update_config(config)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/ml/hybrid/predict")
def get_hybrid_prediction(symbol: str = "BTCUSDT"):
    """Get hybrid prediction for a symbol"""
    try:
        prediction = hybrid_orchestrator.get_prediction(symbol)
        return {
            "status": "success",
            "symbol": symbol,
            "prediction": prediction
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Transfer Learning Endpoints (Minimal Test Versions)
app.include_router(get_minimal_transfer_router(), prefix="/ml/transfer", tags=["ML Transfer"])

# ML Compatibility Management Endpoints
compatibility_manager = MLCompatibilityManager()

@app.get("/ml/compatibility/check")
def check_ml_compatibility():
    """Check ML environment compatibility"""
    try:
        result = compatibility_manager.check_compatibility()
        return {"status": "success", "compatibility": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/ml/compatibility/fix")
def fix_ml_compatibility():
    """Attempt to fix ML compatibility issues"""
    try:
        result = compatibility_manager.fix_compatibility()
        return {"status": "success", "fixes": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/ml/compatibility/recommendations")
def get_ml_recommendations():
    """Get ML environment recommendations"""
    try:
        recommendations = compatibility_manager.get_recommendations()
        return {"status": "success", "recommendations": recommendations}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Online Learning Management Endpoints

@app.post("/ml/online/add_training_data")
def add_online_training_data(data: dict = Body(...)):
    """Add new training data for online learning"""
    try:
        symbol = data.get("symbol", "BTCUSDT")
        features = data.get("features", {})
        target = data.get("target", 0.0)
        
        result = online_learning_manager.add_training_data(symbol, features, target)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/ml/online/update")
def trigger_online_learning_update():
    """Trigger online learning model update"""
    try:
        result = online_learning_manager.update_models()
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/ml/online/stats")
def get_online_learning_stats():
    """Get online learning statistics"""
    try:
        stats = online_learning_manager.get_stats()
        return {"status": "success", "stats": stats}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/ml/data_collection/stats")
def get_data_collection_stats():
    """Get data collection statistics"""
    try:
        collector = get_data_collector()
        stats = collector.get_collection_stats()
        return {"status": "success", "stats": stats}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/ml/data_collection/start")
def start_data_collection(config: dict = Body(...)):
    """Start data collection with given configuration"""
    try:
        collector = get_data_collector()
        collector.start_collection()
        return {"status": "success", "result": "started"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/ml/data_collection/stop")
def stop_data_collection():
    """Stop data collection"""
    try:
        collector = get_data_collector()
        collector.stop_collection()
        return {"status": "success", "result": "stopped"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/ml/performance/history")
def get_performance_history(symbol: str = "BTCUSDT", days: int = 30):
    """Get model performance history"""
    try:
        # Mock performance data - replace with actual implementation
        history = {
            "symbol": symbol,
            "days": days,
            "accuracy": [0.75, 0.78, 0.72, 0.81, 0.76],
            "precision": [0.73, 0.76, 0.70, 0.79, 0.74],
            "recall": [0.71, 0.74, 0.68, 0.77, 0.72]
        }
        return {"status": "success", "history": history}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- Enhanced Email Management Endpoints ---

@app.get("/email/config")
def get_email_config():
    """Get current email configuration"""
    try:
        config = get_email_config()
        return {"status": "success", "config": config}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/email/config")
def save_email_config_endpoint(config: dict = Body(...)):
    """Save email configuration"""
    try:
        result = save_email_config(config)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/email/test")
def test_email_config_endpoint():
    """Test email configuration"""
    try:
        result = test_email_connection()
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/email/send_test")
def send_test_email(data: dict = Body(...)):
    """Send a test email"""
    try:
        subject = data.get('subject', 'Test Email from Crypto Bot')
        body = data.get('body', 'This is a test email to verify your configuration is working correctly.')
        to_email = data.get('to_email', None)
        
        result = send_email(subject, body, to_email)
        return {"status": "success" if result['success'] else "error", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- Missing Endpoints for Dashboard Integration ---

@app.get("/features/indicators")
async def get_technical_indicators(symbol: str = "btcusdt"):
    """Get technical indicators for a symbol"""
    try:
        from data_collection import get_technical_indicators
        indicators = get_technical_indicators(symbol.upper())
        return {
            "status": "success",
            "symbol": symbol.upper(),
            "indicators": indicators
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": str(e),
            "indicators": {
                "rsi": 50.0,
                "macd": 0.0,
                "signal": 0.0,
                "bb_upper": 0.0,
                "bb_middle": 0.0,
                "bb_lower": 0.0
            }
        }

@app.get("/model/upload_status")
async def get_model_upload_status():
    """Check model upload status"""
    try:
        # Check if model file exists
        model_path = "kaia_rf_model.joblib"
        if os.path.exists(model_path):
            return {
                "status": "success",
                "uploaded": True,
                "model_file": model_path,
                "message": "Model is available"
            }
        else:
            return {
                "status": "success",
                "uploaded": False,
                "message": "No model uploaded"
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/trade")
async def create_trade(trade_data: dict):
    """Create a new trade"""
    try:
        # Save trade to database
        trade_id = save_trade(
            symbol=trade_data.get("symbol", "BTCUSDT"),
            action=trade_data.get("action", "buy"),
            amount=float(trade_data.get("amount", 0)),
            price=float(trade_data.get("price", 0)),
            trade_type=trade_data.get("type", "virtual")
        )
        return {
            "status": "success",
            "trade_id": trade_id,
            "message": "Trade created successfully"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/trades/{trade_id}/close")
async def close_trade(trade_id: int):
    """Close a specific trade"""
    try:
        # Update trade status to closed
        update_trade(trade_id, {"status": "closed", "closed_at": datetime.now().isoformat()})
        return {
            "status": "success",
            "message": f"Trade {trade_id} closed successfully"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/trades/{trade_id}/cancel")
async def cancel_trade(trade_id: int):
    """Cancel a specific trade"""
    try:
        # Update trade status to cancelled
        update_trade(trade_id, {"status": "cancelled", "cancelled_at": datetime.now().isoformat()})
        return {
            "status": "success", 
            "message": f"Trade {trade_id} cancelled successfully"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/trades/{trade_id}/activate")
async def activate_trade(trade_id: int):
    """Activate a specific trade"""
    try:
        # Update trade status to active
        update_trade(trade_id, {"status": "active", "activated_at": datetime.now().isoformat()})
        return {
            "status": "success",
            "message": f"Trade {trade_id} activated successfully"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/virtual_balance")
async def get_virtual_balance():
    """Get current virtual balance"""
    try:
        # Load balance from file
        if os.path.exists("data/virtual_balance.json"):
            with open("data/virtual_balance.json", "r") as f:
                balance_data = json.load(f)
        else:
            balance_data = {"balance": 10000.0}
        
        return {
            "status": "success",
            "balance": balance_data.get("balance", 10000.0)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/virtual_balance")  
async def update_virtual_balance(data: dict):
    """Update virtual balance"""
    try:
        balance = float(data.get("balance", 10000.0))
        balance_data = {"balance": balance, "last_updated": datetime.now().isoformat()}
        
        # Save to file
        os.makedirs("data", exist_ok=True)
        with open("data/virtual_balance.json", "w") as f:
            json.dump(balance_data, f)
            
        return {"status": "success", "balance": balance}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/virtual_balance/reset")
async def reset_virtual_balance():
    """Reset virtual balance to default"""
    try:
        # Reset virtual balance
        balance_data = {"balance": 10000.0, "last_updated": datetime.now().isoformat()}
        
        # Save to file
        os.makedirs("data", exist_ok=True)
        with open("data/virtual_balance.json", "w") as f:
            json.dump(balance_data, f)
            
        return {
            "status": "success", 
            "balance": 10000.0,
            "message": "Virtual balance reset to $10,000"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/trades")
async def get_all_trades():
    """Get all trades"""
    try:
        trades = get_trades()
        return {"status": "success", "trades": trades}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/trades/analytics")
async def get_trades_analytics():
    """Get trade analytics"""
    try:
        trades = get_trades()
        total_trades = len(trades)
        profitable_trades = len([t for t in trades if t.get("profit", 0) > 0])
        
        analytics = {
            "total_trades": total_trades,
            "profitable_trades": profitable_trades,
            "win_rate": (profitable_trades / total_trades * 100) if total_trades > 0 else 0,
            "total_profit": sum(t.get("profit", 0) for t in trades)
        }
        
        return {"status": "success", "analytics": analytics}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/auto_trading/optimize_for_low_cap")
async def optimize_for_low_cap(data: dict):
    """Optimize settings for low cap trading"""
    try:
        symbol = data.get("symbol", "KAIAUSDT")
        
        # Apply low cap optimizations
        optimizations = {
            "risk_per_trade": 2.0,  # Lower risk
            "max_positions": 3,     # Fewer positions  
            "stop_loss": 5.0,       # Tighter stop loss
            "take_profit": 10.0,    # Conservative take profit
            "enabled": True
        }
        
        # Save optimization settings
        os.makedirs("data", exist_ok=True)
        with open(f"data/low_cap_settings_{symbol.lower()}.json", "w") as f:
            json.dump(optimizations, f)
            
        return {
            "status": "success",
            "symbol": symbol,
            "optimizations": optimizations,
            "message": f"Low cap optimizations applied for {symbol}"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/notifications")
async def get_notifications():
    """Get all notifications"""
    try:
        notifications = db_get_notifications()
        return {"status": "success", "notifications": notifications}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Backtesting endpoints
@app.post("/backtest")
async def start_backtest(config: dict):
    """Start a backtest with the given configuration"""
    try:
        # Mock backtest implementation
        results = {
            "total_return": 15.2,
            "max_drawdown": -8.5,
            "win_rate": 65.4,
            "total_trades": 156,
            "profitable_trades": 102,
            "avg_trade_return": 2.1
        }
        
        return {"status": "success", "results": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/backtest/results")
async def get_backtest_results():
    """Get the latest backtest results"""
    try:
        # Mock results
        results = {
            "total_return": 15.2,
            "max_drawdown": -8.5,
            "win_rate": 65.4,
            "total_trades": 156,
            "profitable_trades": 102,
            "avg_trade_return": 2.1,
            "timestamp": datetime.now().isoformat()
        }
        
        return {"status": "success", "results": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Model prediction endpoints
@app.post("/model/predict_batch")
async def predict_batch(data: dict):
    """Make batch predictions"""
    try:
        symbols = data.get("symbols", ["BTCUSDT"])
        predictions = {}
        
        for symbol in symbols:
            # Mock prediction - replace with actual model
            predictions[symbol] = {
                "prediction": 0.75,
                "confidence": 0.82,
                "signal": "buy" if 0.75 > 0.6 else "sell"
            }
        
        return {"status": "success", "predictions": predictions}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/model/metrics")
async def get_model_metrics():
    """Get model performance metrics"""
    try:
        metrics = {
            "accuracy": 0.78,
            "precision": 0.75,
            "recall": 0.82,
            "f1_score": 0.78,
            "last_updated": datetime.now().isoformat()
        }
        
        return {"status": "success", "metrics": metrics}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/model/feature_importance")
async def get_feature_importance():
    """Get model feature importance"""
    try:
        features = {
            "rsi": 0.25,
            "macd": 0.20,
            "volume": 0.18,
            "price_change": 0.15,
            "bollinger_bands": 0.12,
            "sma": 0.10
        }
        
        return {"status": "success", "features": features}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
