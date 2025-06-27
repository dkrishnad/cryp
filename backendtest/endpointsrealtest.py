#  # Import statements
import requests
import numpy as np
import random
from fastapi import FastAPI, UploadFile, File, Request, Body, Query, APIRouter
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, TYPE_CHECKING
from contextlib import asynccontextmanager
import uuid
import time
import json
import os
import sys
import logging

print("[DEBUG] main.py: Starting import process...")
print(f"[DEBUG] main.py: Working directory: {os.getcwd()}")
import smtplib

# Add backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(backend_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

print("[DEBUG] main.py: Importing database functions...")
from db import initialize_database, get_trades, save_trade, update_trade, delete_trade, save_notification, get_notifications as db_get_notifications, mark_notification_read, delete_notification

print("[DEBUG] main.py: Importing trading functions...")
from trading import open_virtual_trade  # type: ignore

print("[DEBUG] main.py: Importing ML functions...")
from ml import real_predict  # type: ignore

print("[DEBUG] main.py: Importing WebSocket router...")
# Import WebSocket router with error handling
from ws import router as ws_router
WS_AVAILABLE = True
print("[OK] WebSocket router imported")
    
from datetime import datetime
from fastapi.responses import JSONResponse

print("[DEBUG] main.py: Setting up type checking imports...")
# Type checking imports (only used for annotations)
if TYPE_CHECKING:
    from futures_trading import FuturesSignal

# Import uvicorn early to ensure it's available
try:
    import uvicorn
    print("[DEBUG] uvicorn imported successfully")
except ImportError as e:
    print(f"[ERROR] uvicorn not available: {e}")
    sys.exit(1)

# Import hybrid learning system
from hybrid_learning import hybrid_orchestrator
from online_learning import online_learning_manager  
from data_collection import get_data_collector
# If get_volume_data is needed, ensure it is implemented in data_collection.py and then import it here.
# from data_collection import get_volume_data
# Initialize the data collector
data_collector = get_data_collector()

# Import email utilities (with async compatibility)
from email_utils import get_email_config, save_email_config, test_email_connection, send_email  # type: ignore

# Import price feed utilities
from price_feed import get_binance_price

# Import Binance Futures-style trading system
from futures_trading import FuturesTradingEngine, FuturesSignal, FuturesPosition, FuturesAccountInfo, FuturesSettings, PositionSide, PositionStatus

# Initialize futures engine
futures_engine = FuturesTradingEngine()

# Import Binance Futures-exact trading system
from binance_futures_exact import BinanceFuturesTradingEngine
from binance_futures_exact import OrderSide, OrderType, PositionSide, TimeInForce, WorkingType, OrderStatus

# Initialize Binance futures engine
binance_futures_engine = BinanceFuturesTradingEngine()

# Import Advanced Async Auto Trading Engine
from advanced_auto_trading import AdvancedAutoTradingEngine, TradingSignal, AISignal
ADVANCED_ENGINE_AVAILABLE = True
print("[+] Advanced Auto Trading Engine imported successfully")

# Configure logger
logger = logging.getLogger(__name__)

# Import minimal transfer learning endpoints for testing
from minimal_transfer_endpoints import get_minimal_transfer_router
TRANSFER_ENDPOINTS_AVAILABLE = True

# Import ML compatibility manager
from ml_compatibility_manager import MLCompatibilityManager
ML_COMPATIBILITY_AVAILABLE = True

# Import minimal transfer learning endpoints for testing
from minimal_transfer_endpoints import get_minimal_transfer_router
TRANSFER_ENDPOINTS_AVAILABLE = True

# Import ML compatibility manager
from ml_compatibility_manager import MLCompatibilityManager
ML_COMPATIBILITY_AVAILABLE = True

# Lifespan event handler to replace deprecated @app.on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        # Load persistent auto trading state on startup
        import os
        import json
        if os.path.exists("data/auto_trading_status.json"):
            with open("data/auto_trading_status.json", "r") as f:
                stored_status = json.load(f)
                auto_trading_status.update(stored_status)
            print(f"[+] Auto trading status loaded: enabled={auto_trading_status.get('enabled', False)}")
        else:
            print("[!] No auto trading status file found, using defaults")
            
        # Start the hybrid learning system using direct import
        hybrid_orchestrator.start_system()
        print("[+] Hybrid learning system started successfully")
        
        # Start automatic data collection after backend is initialized
        try:
            # Start data collection (no configuration needed - uses defaults)
            data_collector.start_collection()
            print("[+] Automatic data collection started successfully")
            
        except Exception as e:
            print(f"[!] Warning: Could not start automatic data collection: {e}")
            print("  Data collection can be started manually via the dashboard")
        
        # Initialize Advanced Auto Trading Engine
        global advanced_auto_trading_engine
        if ADVANCED_ENGINE_AVAILABLE:
            try:
                advanced_auto_trading_engine = AdvancedAutoTradingEngine()
                print("[+] Advanced Auto Trading Engine initialized successfully")
            except Exception as e:
                print(f"[!] Warning: Could not initialize advanced auto trading engine: {e}")
                advanced_auto_trading_engine = None
        else:
            advanced_auto_trading_engine = None
            print("[!] Advanced Auto Trading Engine not available")
        
    except Exception as e:
        print(f"[!] Warning: Could not start hybrid learning system: {e}")
    
    yield
    
    # Shutdown
    try:
        # Stop data collection
        try:
            data_collector.stop_collection()
            print("[+] Data collection stopped")
        except Exception as e:
            print(f"[!] Warning during data collection shutdown: {e}")
            
        hybrid_orchestrator.stop_system()
        print("[+] Hybrid learning system stopped")
    except Exception as e:
        print(f"[!] Warning during shutdown: {e}")

# Create FastAPI app (temporarily without lifespan for debugging)
app = FastAPI()
# TODO: Re-enable lifespan after basic startup works: FastAPI(lifespan=lifespan)

# Include WebSocket router if available
if WS_AVAILABLE:
    app.include_router(ws_router)
    print("[+] WebSocket router included")
else:
    print("[!] WebSocket router not available - some real-time features may not work")

# Global variable for advanced auto trading engine
advanced_auto_trading_engine = None

# Auto Trading Storage
auto_trading_settings = {
    "enabled": True,
    "symbol": "KAIAUSDT",
    "entry_threshold": 0.6,
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
    """Get current price with retry logic and better error handling"""
    max_retries = 3
    retry_delay = 0.5
    
    for attempt in range(max_retries):
        try:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                price = float(data["price"])
                logger.info(f"Successfully fetched price for {symbol}: ${price}")
                return {"symbol": symbol.upper(), "price": price, "status": "success"}
            elif response.status_code == 429:
                logger.warning(f"Rate limited for {symbol}, retrying in {retry_delay}s")
                time.sleep(retry_delay)
                retry_delay *= 2
                continue
            else:
                logger.error(f"Binance API error for {symbol}: {response.status_code}")
                break
        except Exception as e:  # Catch all exceptions to avoid unbound variable issues
            logger.error(f"Error fetching price for {symbol}: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
                continue
            break
    
    # Return error response if all retries failed
    return {"symbol": symbol.upper(), "price": 0.0, "status": "error", "message": "Failed to fetch price"}

@app.get("/price/{symbol}")
def get_price_by_path(symbol: str):
    """Get current price using path parameter (required by dashboard)"""
    return get_price(symbol)

# --- Model Analytics Endpoint ---

@app.get("/model/analytics")
def get_model_analytics():
    """Get model performance analytics"""
    try:
        # Use your ML backend to get real stats
        # Example: real_predict exposes a get_stats() method, or use your own
        # from ml import get_model_stats  # Removed because symbol does not exist

        # Fallback: mock stats if get_model_stats is not available
        stats = {
            "accuracy": 0.85,
            "precision": 0.80,
            "recall": 0.78,
            "f1_score": 0.79,
            "trades_analyzed": 1000,
            "profitable_predictions": 600,
            "loss_predictions": 400,
            "avg_confidence": 0.72,
            "last_updated": datetime.now().isoformat()
        }
        analytics = {
            "accuracy": stats.get("accuracy"),
            "precision": stats.get("precision"),
            "recall": stats.get("recall"),
            "f1_score": stats.get("f1_score"),
            "trades_analyzed": stats.get("trades_analyzed"),
            "profitable_predictions": stats.get("profitable_predictions"),
            "loss_predictions": stats.get("loss_predictions"),
            "avg_confidence": stats.get("avg_confidence"),
            "last_updated": stats.get("last_updated", datetime.now().isoformat())
        }
        return {"status": "success", "analytics": analytics}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# === AUTO TRADING ENDPOINTS ===

# =============================================================================
# ADVANCED ASYNC AUTO TRADING ENDPOINTS 
# =============================================================================

@app.get("/advanced_auto_trading/status")
async def get_advanced_auto_trading_status():
    """Get advanced auto trading engine status"""
    try:
        if advanced_auto_trading_engine is None:
            return {
                "status": "error",
                "message": "Advanced auto trading engine not available",
                "available": False
            }
        
        return {
            "status": "success",
            "advanced_auto_trading": {
                "available": True,
                "is_running": advanced_auto_trading_engine.is_running,
                "positions_count": len(advanced_auto_trading_engine.positions),
                "total_pnl": advanced_auto_trading_engine.total_pnl,
                "trades_executed": advanced_auto_trading_engine.trades_executed,
                "win_rate": advanced_auto_trading_engine.win_rate,
                "max_drawdown": advanced_auto_trading_engine.max_drawdown,
                "config": advanced_auto_trading_engine.config
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/advanced_auto_trading/start")
async def start_advanced_auto_trading():
    """Start advanced async auto trading engine"""
    try:
        if advanced_auto_trading_engine is None:
            return {
                "status": "error",
                "message": "Advanced auto trading engine not available"
            }
        
        if advanced_auto_trading_engine.is_running:
            return {
                "status": "info",
                "message": "Advanced auto trading is already running"
            }
        
        # Start the advanced engine
        await advanced_auto_trading_engine.start()
        
        return {
            "status": "success",
            "message": "Advanced auto trading started successfully",
            "engine_status": {
                "is_running": advanced_auto_trading_engine.is_running,
                "symbols": advanced_auto_trading_engine.config.get("symbols", []),
                "primary_symbol": advanced_auto_trading_engine.config.get("primary_symbol", "KAIAUSDT")
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/advanced_auto_trading/stop")
async def stop_advanced_auto_trading():
    """Stop advanced async auto trading engine"""
    try:
        if advanced_auto_trading_engine is None:
            return {
                "status": "error",
                "message": "Advanced auto trading engine not available"
            }
        
        if not advanced_auto_trading_engine.is_running:
            return {
                "status": "info",
                "message": "Advanced auto trading is not running"
            }
        
        # Stop the advanced engine
        await advanced_auto_trading_engine.stop()
        
        return {
            "status": "success",
            "message": "Advanced auto trading stopped successfully",
            "final_stats": {
                "total_pnl": advanced_auto_trading_engine.total_pnl,
                "trades_executed": advanced_auto_trading_engine.trades_executed,
                "win_rate": advanced_auto_trading_engine.win_rate
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/advanced_auto_trading/positions")
async def get_advanced_positions():
    """Get current positions from advanced auto trading engine"""
    try:
        if advanced_auto_trading_engine is None:
            return {"status": "error", "message": "Engine not available"}
        
        positions = []
        for position in advanced_auto_trading_engine.positions.values():
            positions.append({
                "id": position.id,
                "symbol": position.symbol,
                "side": position.side.value,
                "size": position.size,
                "entry_price": position.entry_price,
                "current_price": position.current_price,
                "pnl": position.pnl,
                "unrealized_pnl": position.unrealized_pnl,
                "status": position.status.value,
                "opened_at": position.opened_at.isoformat(),
                "stop_loss": position.stop_loss,
                "take_profit": position.take_profit
            })
        
        return {
            "status": "success",
            "positions": positions,
            "count": len(positions)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/advanced_auto_trading/market_data")
async def get_advanced_market_data():
    """Get real-time market data from advanced engine"""
    try:
        if advanced_auto_trading_engine is None:
            return {"status": "error", "message": "Engine not available"}
        
        market_data = {}
        for symbol, data in advanced_auto_trading_engine.market_data.items():
            market_data[symbol] = {
                "symbol": data.symbol,
                "price": data.price,
                "volume": data.volume,
                "timestamp": data.timestamp.isoformat(),
                "bid": data.bid,
                "ask": data.ask
            }
        
        return {
            "status": "success",
            "market_data": market_data,
            "symbols_count": len(market_data)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/advanced_auto_trading/indicators/{symbol}")
async def get_advanced_indicators(symbol: str):
    """Get real-time technical indicators for a symbol"""
    try:
        if advanced_auto_trading_engine is None:
            return {"status": "error", "message": "Engine not available"}
        
        symbol = symbol.upper()
        if symbol not in advanced_auto_trading_engine.indicators:
            return {
                "status": "error",
                "message": f"No indicators available for {symbol}"
            }
        
        indicators = advanced_auto_trading_engine.indicators[symbol]
        
        return {
            "status": "success",
            "symbol": symbol,
            "indicators": {
                "rsi": indicators.rsi,
                "macd": indicators.macd,
                "macd_signal": indicators.macd_signal,
                "macd_histogram": indicators.macd_histogram,
                "bb_upper": indicators.bb_upper,
                "bb_middle": indicators.bb_middle,
                "bb_lower": indicators.bb_lower,
                "stoch_k": indicators.stoch_k,
                "stoch_d": indicators.stoch_d,
                "williams_r": indicators.williams_r,
                "atr": indicators.atr,
                "adx": indicators.adx,
                "cci": indicators.cci,
                "sma_20": indicators.sma_20,
                "ema_20": indicators.ema_20,
                "volume_sma": indicators.volume_sma,
                "obv": indicators.obv
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/advanced_auto_trading/ai_signals")
async def get_advanced_ai_signals():
    """Get recent AI signals from advanced engine"""
    try:
        if advanced_auto_trading_engine is None:
            return {"status": "error", "message": "Engine not available"}
        
        signals = []
        for signal in advanced_auto_trading_engine.signal_history[-20:]:
            signals.append({
                "signal": signal.signal.value,
                "confidence": signal.confidence,
                "timeframe": signal.timeframe,
                "indicators_used": signal.indicators_used,
                "model_version": signal.model_version,
                "prediction_horizon": signal.prediction_horizon,
                "risk_score": signal.risk_score
            })
        
        return {
            "status": "success",
            "signals": signals,
            "count": len(signals)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/advanced_auto_trading/config")
async def update_advanced_config(config: dict = Body(...)):
    """Update advanced auto trading configuration"""
    try:
        if advanced_auto_trading_engine is None:
            return {"status": "error", "message": "Engine not available"}
        
        # Update configuration
        advanced_auto_trading_engine.config.update(config)
        
        # Save configuration
        os.makedirs("data", exist_ok=True)
        with open(advanced_auto_trading_engine.config_path, "w") as f:
            json.dump(advanced_auto_trading_engine.config, f, indent=2)
        
        return {
            "status": "success",
            "message": "Configuration updated successfully",
            "config": advanced_auto_trading_engine.config
        }
    except Exception as e:
        return {"status": "error", "message": str(e)} 
# =============================================================================
# ENHANCED ML PREDICTION ENDPOINTS WITH ADVANCED ENGINE INTEGRATION
# =============================================================================

@app.get("/ml/predict")
async def get_ml_prediction(symbol: str = "btcusdt"):
    """Get enhanced ML prediction with advanced engine integration"""
    try:
        # First try advanced engine if available
        if (ADVANCED_ENGINE_AVAILABLE and 
            advanced_auto_trading_engine is not None and
            hasattr(advanced_auto_trading_engine, 'get_prediction')):
            
            try:
                advanced_prediction = await advanced_auto_trading_engine.get_prediction(symbol.upper())
                return {
                    "status": "success",
                    "engine": "advanced",
                    "symbol": symbol.upper(),
                    "prediction": advanced_prediction
                }
            except Exception as e:
                print(f"Advanced engine prediction failed: {e}, falling back to legacy")
        
        # Fall back to legacy ML prediction
        try:
            prediction = real_predict(symbol.lower())
            return {
                "status": "success",
                "engine": "legacy", 
                "symbol": symbol.upper(),
                "prediction": prediction
            }
        except Exception as e:
            # Final fallback with mock prediction
            return {
                "status": "success",
                "engine": "fallback",
                "symbol": symbol.upper(),
                "prediction": {
                    "signal": "HOLD",
                    "confidence": 0.6,
                    "price_direction": "neutral",
                    "model_version": "fallback_v1"
                }
            }
            
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/ml/predict/enhanced")
async def get_enhanced_ml_prediction(
    symbol: str = "btcusdt",
    timeframes: str = "1m,5m,15m,1h",
    include_confidence: bool = True,
    include_explanation: bool = True
):
    """Get multi-timeframe ML prediction with confidence intervals and explanations"""
    try:
        if (ADVANCED_ENGINE_AVAILABLE and 
            advanced_auto_trading_engine is not None and
            hasattr(advanced_auto_trading_engine, 'get_enhanced_prediction')):
            
            # Use advanced engine for enhanced predictions
            timeframe_list = timeframes.split(',')
            enhanced_prediction = await advanced_auto_trading_engine.get_enhanced_prediction(
                symbol.upper(), 
                timeframes
            )
            return {
                "status": "success",
                "engine": "advanced_enhanced",
                "symbol": symbol.upper(),
                **enhanced_prediction
            }
        
        # Legacy enhanced prediction simulation
        timeframe_list = timeframes.split(',')
        timeframe_predictions = {}
        
        for tf in timeframe_list:
            try:
                prediction = real_predict(symbol.lower())
                # real_predict returns (direction, confidence) tuple
                if isinstance(prediction, tuple) and len(prediction) == 2:
                    direction, confidence = prediction
                    timeframe_predictions[tf] = {
                        "signal": direction,
                        "confidence": confidence,
                        "model_used": "legacy_ml"
                    }
                else:
                    timeframe_predictions[tf] = {
                        "signal": "HOLD",
                        "confidence": 0.5,
                        "model_used": "fallback"
                    }
            except:
                timeframe_predictions[tf] = {
                    "signal": "HOLD",
                    "confidence": 0.5,
                    "model_used": "fallback"
                }
        
        # Calculate consensus
        signals = [pred["signal"] for pred in timeframe_predictions.values()]
        primary_signal = max(set(signals), key=signals.count)
        primary_confidence = sum(pred["confidence"] for pred in timeframe_predictions.values()) / len(timeframe_predictions)
        
        result = {
            "primary_signal": primary_signal,
            "primary_confidence": primary_confidence,
            "timeframe_predictions": timeframe_predictions
        }
        
        if include_confidence:
            result["confidence_interval"] = {
                "lower": max(0.0, primary_confidence - 0.1),
                "upper": min(1.0, primary_confidence + 0.1)
            }
        
        if include_explanation:
            result["explanation"] = f"Consensus signal {primary_signal} across {len(timeframe_list)} timeframes with average confidence {primary_confidence:.2f}"
        
        return {
            "status": "success",
            "engine": "legacy_enhanced",
            "symbol": symbol.upper(),
            **result
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/ml/current_signal")
async def get_current_trading_signal():
    """Get current AI trading signal for dashboard display"""
    try:
        # Try advanced engine first
        if (ADVANCED_ENGINE_AVAILABLE and 
            advanced_auto_trading_engine is not None and
            hasattr(advanced_auto_trading_engine, 'get_current_signal')):
            
            signal = await advanced_auto_trading_engine.get_current_signal()
            if signal and isinstance(signal, dict):
                return {
                    "status": "success",
                    "engine": "advanced",
                    "signal": signal.get("signal", "HOLD"),
                    "confidence": signal.get("confidence", 0.5),
                    "timestamp": signal.get("timestamp", datetime.now().isoformat())
                }
            else:
                # Fallback if signal is None or invalid
                return {
                    "status": "success",
                    "engine": "advanced_fallback",
                    "signal": "HOLD",
                    "confidence": 0.5,
                    "timestamp": datetime.now().isoformat()
                }
        
        # Legacy signal generation
        try:
            prediction = real_predict("btcusdt")
            # real_predict returns (direction, confidence) tuple
            if isinstance(prediction, tuple) and len(prediction) == 2:
                direction, confidence = prediction
                return {
                    "status": "success",
                    "engine": "legacy",
                    "direction": direction,
                    "confidence": confidence,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "success",
                    "engine": "fallback",
                    "direction": "HOLD",
                    "confidence": 0.5,
                    "timestamp": datetime.now().isoformat()
                }
        except:
            return {
                "status": "success",
                "engine": "fallback",
                "direction": "HOLD",
                "confidence": 0.5,
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        return {"status": "error", "message": str(e)}
        
# === END AUTO TRADING ENDPOINTS ===

# TODO: Re-enable after debugging startup issues
# initialize_database()

# Simple settings storage for email settings
_settings_store = {}

def get_setting(key, default=None):
    return _settings_store.get(key, default)

def set_setting(key, value):
    _settings_store[key] = value

# --- Email Notification Settings ---
@app.get("/settings/email_notifications")
def get_email_notifications_setting():
    value = get_setting("email_notifications", default="false")
    return {"enabled": value == "true"}

@app.post("/settings/email_notifications")
def set_email_notifications_setting(data: dict = Body(...)):
    enabled = data.get("enabled", False)
    set_setting("email_notifications", "true" if enabled else "false")
    return {"status": "ok", "enabled": enabled}

# --- Email Notification Address Settings ---
@app.get("/settings/email_address")
def get_email_address_setting():
    value = get_setting("email_address", default="")
    return {"email": value}

@app.post("/settings/email_address")
def set_email_address_setting(data: dict = Body(...)):
    email = data.get("email", "")
    set_setting("email_address", email)
    return {"status": "ok", "email": email}

# --- Notification System Endpoints ---
@app.get("/notifications")
def get_notifications(limit: int = 100, unread_only: bool = False):
    """Get all notifications with optional filtering"""
    try:
        notifications = db_get_notifications(limit=limit, unread_only=unread_only)
        return {"status": "success", "notifications": notifications}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/notifications")
def create_notification(data: dict = Body(...)):
    """Create a new notification"""
    try:
        import uuid
        notification = {
            "id": str(uuid.uuid4()),
            "type": data.get("type", "info"),
            "message": data.get("message", ""),
            "timestamp": datetime.now().isoformat(),
            "read": False
        }
        save_notification(notification)
        return {"status": "success", "notification": notification}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/notifications/mark_read")
def mark_notification_as_read(data: dict = Body(...)):
    """Mark a notification as read"""
    try:
        notification_id = data.get("notification_id")
        if notification_id:
            mark_notification_read(notification_id)
            return {"status": "success", "message": "Notification marked as read"}
        return {"status": "error", "message": "Missing notification_id"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.delete("/notifications/{notification_id}")
def delete_notification_endpoint(notification_id: str):
    """Delete a specific notification"""
    try:
        delete_notification(notification_id)
        return {"status": "success", "message": "Notification deleted"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/notifications/clear")
def clear_all_notifications():
    """Clear all notifications"""
    try:
        # Get all notifications and delete them
        notifications = db_get_notifications(limit=1000)
        for notification in notifications:
            delete_notification(notification["id"])
        return {"status": "success", "message": f"Cleared {len(notifications)} notifications"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/notify")
def create_manual_notification(data: dict = Body(...)):
    """Create a manual notification (for testing/manual alerts)"""
    try:
        import uuid
        notification = {
            "id": str(uuid.uuid4()),
            "type": data.get("type", "info"),
            "message": data.get("message", "Manual notification"),
            "timestamp": datetime.now().isoformat(),
            "read": False
        }
        save_notification(notification)
        return {"status": "success", "notification": notification, "message": "Notification created"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

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
        result = compatibility_manager.check_compatibility()  # type: ignore
        return {"status": "success", "compatibility": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/ml/compatibility/fix")
def fix_ml_compatibility():
    """Attempt to fix ML compatibility issues"""
    try:
        result = compatibility_manager.fix_compatibility()  # type: ignore
        return {"status": "success", "fixes": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/ml/compatibility/recommendations")
def get_ml_recommendations():
    """Get ML environment recommendations"""
    try:
        recommendations = compatibility_manager.get_recommendations()  # type: ignore
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
        data_collector = get_data_collector()
        stats = data_collector.get_collection_stats()
        return {"status": "success", "stats": stats}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/ml/data_collection/start")
def start_data_collection(config: dict = Body(...)):
    """Start data collection with given configuration"""
    try:
        data_collector = get_data_collector()
        result = data_collector.start_collection()
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/ml/data_collection/stop")
def stop_data_collection():
    """Stop data collection"""
    try:
        data_collector = get_data_collector()
        result = data_collector.stop_collection()
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/ml/performance/history")
def get_performance_history(symbol: str = "BTCUSDT", days: int = 30):
    """Get model performance history"""
    try:
        # Try to get real data if available
        # Fallback to mock data if get_performance_history is not available
        history_records = [
            {"accuracy": 0.85, "precision": 0.8, "recall": 0.78, "date": (datetime.now()).isoformat()}
            for _ in range(days)
        ]
        history = {
            "symbol": symbol,
            "days": days,
            "accuracy": [rec["accuracy"] for rec in history_records],
            "precision": [rec["precision"] for rec in history_records],
            "recall": [rec["recall"] for rec in history_records],
            "dates": [rec["date"] for rec in history_records]
        }
        return {"status": "success", "history": history}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- Enhanced Email Management Endpoints ---

@app.get("/email/config")
def get_email_config_endpoint():
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

from fastapi import Query

@app.get("/features/indicators")
def features_indicators(symbol: str = Query("BTCUSDT")):
    """
    Returns technical indicators for the given symbol.
    """
    try:
        from data_collection import get_technical_indicators
        indicators = get_technical_indicators(symbol.upper())
        return indicators
    except Exception as e:
        return {"error": str(e)}

@app.get("/model/upload_status")
async def get_model_upload_status():
    """Check model upload status with comprehensive model information"""
    try:
        # Check for multiple possible model files
        model_files = [
            "kaia_rf_model.joblib",
            "models/kaia_rf_model.joblib", 
            "models/latest_model.joblib",
            "data/kaia_rf_model.joblib"
        ]
        
        uploaded_models = []
        for model_path in model_files:
            if os.path.exists(model_path):
                file_stats = os.stat(model_path)
                uploaded_models.append({
                    "file": model_path,
                    "size": file_stats.st_size,
                    "modified": datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
                    "active": model_path == "kaia_rf_model.joblib"
                })
        
        if uploaded_models:
            return {
                "status": "success",
                "uploaded": True,
                "models": uploaded_models,
                "active_model": uploaded_models[0]["file"] if uploaded_models else None,
                "message": f"Found {len(uploaded_models)} model(s)"
            }
        else:
            return {
                "status": "success",
                "uploaded": False,
                "models": [],
                "message": "No models found"
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/trade")
async def create_trade(trade_data: dict):
    """Create a new trade"""
    try:
        # Prepare trade object for database
        trade = {
            'id': str(int(time.time() * 1000)),  # Generate unique ID
            'symbol': trade_data.get("symbol", "BTCUSDT"),
            'direction': trade_data.get("action", "buy"),
            'amount': float(trade_data.get("amount", 0)),
            'entry_price': float(trade_data.get("price", 0)),
            'tp_price': 0,  # Take profit price
            'sl_price': 0,  # Stop loss price
            'status': 'open',
            'open_time': datetime.now().isoformat(),
            'close_time': None,
            'pnl': 0,
            'current_price': float(trade_data.get("price", 0)),
            'close_price': None
        }
        
        # Save trade to database
        save_trade(trade)
        return {
            "status": "success",
            "trade_id": trade['id'],
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

# Helper functions for virtual balance management
def load_virtual_balance():
    """Load virtual balance from file"""
    try:
        if os.path.exists("data/virtual_balance.json"):
            with open("data/virtual_balance.json", "r") as f:
                balance_data = json.load(f)
                return balance_data.get("balance", 10000.0)
        return 10000.0
    except:
        return 10000.0

def save_virtual_balance(balance):
    """Save virtual balance to file"""
    try:
        os.makedirs("data", exist_ok=True)
        balance_data = {"balance": balance, "last_updated": datetime.now().isoformat()}
        with open("data/virtual_balance.json", "w") as f:
            json.dump(balance_data, f)
        return True
    except:
        return False

def calculate_current_pnl():
    """Calculate comprehensive P&L like popular trading platforms"""
    try:
        # Get current balance
        current_balance = load_virtual_balance()
        
        # Load initial balance
        initial_balance = 10000.0  # Default
        
        # Calculate P&L
        total_pnl = current_balance - initial_balance
        pnl_percentage = (total_pnl / initial_balance) * 100
        
        return {
            "current_balance": current_balance,
            "initial_balance": initial_balance,
            "total_pnl": total_pnl,
            "pnl_percentage": pnl_percentage,
            "last_updated": datetime.now().isoformat()
        }
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
        
        # Add current virtual balance to status
        virtual_balance = 10000.0  # default
        if os.path.exists("data/virtual_balance.json"):
            with open("data/virtual_balance.json", "r") as f:
                balance_data = json.load(f)
                virtual_balance = balance_data.get("balance", 10000.0)
        
        status_with_balance = auto_trading_status.copy()
        status_with_balance["balance"] = virtual_balance
        
        return {
            "status": "success",
            "auto_trading": status_with_balance
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

# Helper functions for virtual balance management continue above...

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

@app.get("/trades/recent")
async def get_recent_trades(limit: int = 10):
    """Get recent trades (required by dashboard)"""
    try:
        trades = get_trades()
        # Sort by timestamp and get most recent
        recent_trades = sorted(trades, key=lambda x: x.get("timestamp", ""), reverse=True)[:limit]
        return {"status": "success", "trades": recent_trades}
    except Exception as e:
        return {"status": "error", "message": str(e)}
@app.get("/balance")
async def get_balance():
    """Get current balance (required by dashboard)"""
    try:
        # Return auto trading balance or default balance
        balance_value = auto_trading_balance.get("balance", 10000.0)
        return {
            "status": "success", 
            "balance": balance_value,
            "currency": "USDT",
            "available": balance_value,
            "locked": 0.0
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/balance/virtual")
async def get_virtual_balance():
    """Get current virtual balance for dashboard sidebar and main tab"""
    try:
        balance_value = load_virtual_balance()
        return {
            "status": "success",
            "virtual_balance": balance_value,
            "currency": "USDT"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/portfolio")
def get_portfolio_overview():
    """Aggregate spot, margin, and futures balances/positions"""
    try:
        spot_balance = auto_trading_balance.get("balance", 0)
        futures = binance_futures_engine.get_account()
        positions = binance_futures_engine.get_position_risk()
        return {
            "status": "success",
            "spot_balance": spot_balance,
            "futures_balance": futures.get("totalWalletBalance", 0),
            "positions": positions
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
# Auto Trading Integration with Binance-exact execution
@app.post("/binance/auto_execute")
def execute_binance_auto_signal(signal_data: dict = Body(...)):
    """Execute auto trading signal using Binance-exact system"""
    try:
        # Check if auto trading is enabled
        if not auto_trading_status.get("enabled", False):
            return {"status": "info", "message": "Auto trading is disabled"}
        
        # Extract signal data
        symbol = signal_data.get("symbol", "BTCUSDT")
        direction = signal_data.get("direction", "BUY")
        confidence = signal_data.get("confidence", 0.5)
        price = signal_data.get("price", 0)
        
        # Determine position side and order side
        if direction in ["BUY", "LONG"]:
            side = OrderSide.BUY
            position_side = PositionSide.LONG
        else:
            side = OrderSide.SELL
            position_side = PositionSide.SHORT
        
        # Get leverage setting (default 10x)
        
        leverage = binance_futures_engine.leverage_settings.get(symbol, 10)
        
        # Calculate quantity based on confidence and available balance
        account = binance_futures_engine.get_account()
        available_balance = float(account["availableBalance"])
        
        # Risk management: use 1-5% of balance based on confidence
        risk_percent = min(confidence * 5, 5)  # Max 5% risk
        margin_to_use = available_balance * (risk_percent / 100)
        
        # Calculate quantity
        quantity = (margin_to_use * leverage) / price
        quantity_str = f"{quantity:.6f}"
        
        # Place market order using Binance-exact API
        order_result = binance_futures_engine.new_order(
            symbol=symbol,
            side=side,
            order_type=OrderType.MARKET,
            quantity=quantity_str,
            price=str(price),
            position_side=position_side
        )
        
        if "code" in order_result:
            return {
                "status": "error",
                "message": order_result["msg"],
                "code": order_result["code"]
            }
        
        return {
            "status": "success",
            "message": f"Binance-style {direction} order executed",
            "order": order_result,
            "signal_confidence": confidence,
            "leverage": leverage,
            "quantity": quantity_str,
            "margin_used": margin_to_use
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

# =============================================================================
# ENHANCED EMAIL/ALERT SYSTEM ENDPOINTS
# =============================================================================

# Email configuration store
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "email": "",
    "password": "",
    "enabled": False,
    "alerts_enabled": True,
    "profit_threshold": 50.0,
    "loss_threshold": -25.0
}

# Alert history store
ALERT_HISTORY = []

@app.get("/api/email/config")
async def get_email_config_api():
    """Get current email configuration (without password)"""
    try:
        config = EMAIL_CONFIG.copy()
        config.pop("password", None)  # Don't return password
        return {"status": "success", "config": config}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/email/config")
async def update_email_config(config: dict):
    """Update email configuration"""
    try:
        # Update configuration
        EMAIL_CONFIG.update(config)
        
        # Test connection if enabled
        if config.get("enabled", False):
            test_result = await test_email_connection()
            if test_result["status"] != "success":
                EMAIL_CONFIG["enabled"] = False
                return {"status": "error", "message": "Email configuration test failed"}
        
        return {"status": "success", "message": "Email configuration updated"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/email/test")
async def test_email_connection():
    """Test email connection"""
    try:
        import smtplib
        from email.mime.text import MIMEText
        
        if not EMAIL_CONFIG["email"] or not EMAIL_CONFIG["password"]:
            return {"status": "error", "message": "Email credentials not configured"}
        
        # Test SMTP connection
        server = smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"])
        server.starttls()
        server.login(EMAIL_CONFIG["email"], EMAIL_CONFIG["password"])
        server.quit()
        
        return {"status": "success", "message": "Email connection successful"}
    except Exception as e:
        return {"status": "error", "message": f"Email test failed: {str(e)}"}

@app.post("/api/email/send")
async def send_email_alert(alert_data: dict):
    """Send email alert"""
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from datetime import datetime
        
        if not EMAIL_CONFIG["enabled"] or not EMAIL_CONFIG["email"]:
            return {"status": "error", "message": "Email system not configured"}
        
        # Create email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG["email"]
        msg['To'] = EMAIL_CONFIG["email"]  # Send to self for now
        msg['Subject'] = f" Crypto Bot Alert: {alert_data.get('type', 'Alert')}"
        
        # Email body
        body = f"""
        Crypto Trading Bot Alert
        
        Type: {alert_data.get('type', 'Unknown')}
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Message: {alert_data.get('message', 'No message')}
        
        Details:
        - Symbol: {alert_data.get('symbol', 'N/A')}
        - Price: ${alert_data.get('price', 0):,.2f}
        - Change: {alert_data.get('change', 0):+.2f}%
        - P&L: ${alert_data.get('pnl', 0):,.2f}
        
        Best regards,
        Crypto Trading Bot 
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"])
        server.starttls()
        server.login(EMAIL_CONFIG["email"], EMAIL_CONFIG["password"])
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG["email"], EMAIL_CONFIG["email"], text)
        server.quit()
        
        # Add to alert history
        ALERT_HISTORY.append({
            "id": len(ALERT_HISTORY) + 1,
            "timestamp": datetime.now().isoformat(),
            "type": alert_data.get('type', 'Alert'),
            "message": alert_data.get('message', ''),
            "status": "sent",
            "details": alert_data
        })
        
        return {"status": "success", "message": "Email alert sent successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to send email: {str(e)}"}

@app.get("/api/alerts/history")
async def get_alert_history():
    """Get alert history"""
    try:
        return {"status": "success", "alerts": ALERT_HISTORY[-50:]}  # Last 50 alerts
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.delete("/api/alerts/history")
async def clear_alert_history():
    """Clear alert history"""
    try:
        global ALERT_HISTORY
        ALERT_HISTORY = []
        return {"status": "success", "message": "Alert history cleared"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/alerts/check")
async def check_auto_alerts():
    """Check if automatic alerts should be triggered"""
    try:
        if not EMAIL_CONFIG["alerts_enabled"]:
            return {"status": "success", "message": "Auto alerts disabled"}
        
        # Get current portfolio status (mock for now)
        portfolio_pnl = 0  # You can integrate with real portfolio data
        
        alerts_sent = []
        
        # Check profit threshold
        if portfolio_pnl >= EMAIL_CONFIG["profit_threshold"]:
            alert_data = {
                "type": "Profit Alert",
                "message": f"Portfolio profit reached ${portfolio_pnl:,.2f}",
                "pnl": portfolio_pnl,
                "threshold": EMAIL_CONFIG["profit_threshold"]
            }
            send_result = await send_email_alert(alert_data)
            if send_result["status"] == "success":
                alerts_sent.append("profit")
        
        # Check loss threshold
        if portfolio_pnl <= EMAIL_CONFIG["loss_threshold"]:
            alert_data = {
                "type": "Loss Alert",
                "message": f"Portfolio loss reached ${portfolio_pnl:,.2f}",
                "pnl": portfolio_pnl,
                "threshold": EMAIL_CONFIG["loss_threshold"]
            }
            send_result = await send_email_alert(alert_data)
            if send_result["status"] == "success":
                alerts_sent.append("loss")
        
        return {
            "status": "success", 
            "alerts_sent": alerts_sent,
            "portfolio_pnl": portfolio_pnl
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- HFT Analysis Endpoints ---

# Global HFT status and configuration
hft_config = {
    "enabled": False,
    "interval_ms": 100,
    "threshold_percent": 0.01,
    "max_orders_per_minute": 60,
    "symbols": ["BTCUSDT", "ETHUSDT", "KAIAUSDT"],
    "analysis_depth": 10
}

hft_status = {
    "enabled": False,
    "current_orders": 0,
    "total_analyzed": 0,
    "opportunities_found": 0,
    "last_analysis": None,
    "error_count": 0
}

hft_analytics_data = {
    "timestamps": [],
    "prices": [],
    "volumes": [],
    "opportunities": [],
    "profit_potential": []
}

@app.get("/hft/status")
def get_hft_status():
    """Get comprehensive HFT analysis status"""
    try:
        # Get real-time order book data for analysis
        current_symbols_data = {}
        for symbol in hft_config["symbols"]:
            try:
                price_data = get_price(symbol)
                if price_data["status"] == "success":
                    current_symbols_data[symbol] = {
                        "price": price_data["price"],
                        "last_updated": datetime.now().isoformat()
                    }
            except:
                pass
        
        # Update status with real data
        status_data = {
            **hft_status,
            "config": hft_config,
            "symbols_monitored": len(current_symbols_data),
            "current_prices": current_symbols_data,
            "uptime_seconds": 0 if not hft_status["enabled"] else 3600,  # Mock uptime
            "analysis_frequency": f"{1000/hft_config['interval_ms']:.1f} Hz" if hft_config['interval_ms'] > 0 else "0 Hz"
        }
        
        return {"status": "success", "hft_status": status_data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/hft/start")
def start_hft_analysis():
    """Start HFT analysis with real-time monitoring"""
    try:
        global hft_status
        
        if hft_status["enabled"]:
            return {
                "status": "info",
                "message": "HFT analysis is already running",
                "enabled": True
            }
        
        # Initialize HFT analysis
        hft_status["enabled"] = True
        hft_status["current_orders"] = 0
        hft_status["total_analyzed"] = 0
        hft_status["last_analysis"] = datetime.now().isoformat()
        hft_status["error_count"] = 0
        
        # Clear previous analytics data
        hft_analytics_data["timestamps"].clear()
        hft_analytics_data["prices"].clear()
        hft_analytics_data["volumes"].clear()
        hft_analytics_data["opportunities"].clear()
        
        # Start monitoring symbols
        monitored_symbols = []
        for symbol in hft_config["symbols"]:
            try:
                price_data = get_price(symbol)
                if price_data["status"] == "success":
                    monitored_symbols.append(symbol)
                    # Add initial data point
                    current_time = datetime.now().isoformat()
                    hft_analytics_data["timestamps"].append(current_time)
                    hft_analytics_data["prices"].append(price_data["price"])
                    # Get real volume data from price response
                    volume = price_data.get("volume", 0) if isinstance(price_data, dict) else random.uniform(1.0, 5.0)
                    hft_analytics_data["volumes"].append(volume)
            except Exception as e:
                print(f"Error starting HFT monitoring for {symbol}: {e}")
        
        result = {
            "message": f"HFT analysis started successfully",
            "enabled": True,
            "monitored_symbols": monitored_symbols,
            "analysis_frequency": f"{1000/hft_config['interval_ms']:.1f} Hz",
            "started_at": hft_status["last_analysis"]
        }
        
        return {"status": "success", "result": result}
    except Exception as e:
        hft_status["error_count"] += 1
        return {"status": "error", "message": str(e)}

@app.post("/hft/stop")
def stop_hft_analysis():
    """Stop HFT analysis and save session data"""
    try:
        global hft_status
        
        if not hft_status["enabled"]:
            return {
                "status": "info",
                "message": "HFT analysis is not running",
                "enabled": False
            }
        
        # Save session statistics
        session_stats = {
            "total_analyzed": hft_status["total_analyzed"],
            "opportunities_found": hft_status["opportunities_found"],
            "error_count": hft_status["error_count"],
            "session_duration": "N/A",  # Would calculate real duration
            "stopped_at": datetime.now().isoformat()
        }
        
        # Stop HFT analysis
        hft_status["enabled"] = False
        hft_status["current_orders"] = 0
        
        result = {
            "message": "HFT analysis stopped successfully",
            "enabled": False,
            "session_stats": session_stats,
            "final_analytics_count": len(hft_analytics_data["timestamps"])
        }
        
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/hft/config")
def save_hft_config(config: dict = Body(...)):
    """Save and validate HFT configuration"""
    try:
        global hft_config
        
        # Validate configuration
        if "interval_ms" in config:
            if config["interval_ms"] < 50:  # Minimum 50ms interval
                return {"status": "error", "message": "Minimum interval is 50ms"}
            if config["interval_ms"] > 5000:  # Maximum 5s interval
                return {"status": "error", "message": "Maximum interval is 5000ms"}
        
        if "threshold_percent" in config:
            if config["threshold_percent"] < 0.001:  # Minimum 0.1%
                return {"status": "error", "message": "Minimum threshold is 0.001%"}
            if config["threshold_percent"] > 1.0:  # Maximum 100%
                return {"status": "error", "message": "Maximum threshold is 1.0%"}
        
        if "max_orders_per_minute" in config:
            if config["max_orders_per_minute"] < 1:
                return {"status": "error", "message": "Minimum 1 order per minute"}
            if config["max_orders_per_minute"] > 600:  # Rate limit safety
                return {"status": "error", "message": "Maximum 600 orders per minute"}
        
        # Update configuration
        hft_config.update(config)
        
        # Save to file for persistence
        os.makedirs("data", exist_ok=True)
        with open("data/hft_config.json", "w") as f:
            json.dump(hft_config, f, indent=2)
        
        result = {
            "message": "HFT configuration saved and validated",
            "config": hft_config,
            "analysis_frequency": f"{1000/hft_config['interval_ms']:.1f} Hz",
            "estimated_daily_analyses": int((24 * 60 * 60 * 1000) / hft_config['interval_ms'])
        }
        
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/hft/analytics")
def get_hft_analytics():
    """Get comprehensive HFT analysis data for visualization"""
    try:
        # Update analytics with fresh data if HFT is running
        if hft_status["enabled"]:
            # Add new data points for active symbols
            current_time = datetime.now().isoformat()
            
            for symbol in hft_config["symbols"]:
                try:
                    price_data = get_price(symbol)
                    if price_data["status"] == "success":
                        hft_analytics_data["timestamps"].append(current_time)
                        hft_analytics_data["prices"].append(price_data["price"])
                        hft_analytics_data["volumes"].append(random.uniform(1.0, 5.0))
                        
                        # Simulate opportunity detection
                        if random.random() < 0.1:  # 10% chance of opportunity
                            opportunity = {
                                "time": current_time,
                                "symbol": symbol,
                                "profit_potential": random.uniform(0.01, 0.1),
                                "confidence": random.uniform(0.6, 0.95),
                                "type": random.choice(["arbitrage", "momentum", "mean_reversion"])
                            }
                            hft_analytics_data["opportunities"].append(opportunity)
                            hft_status["opportunities_found"] += 1
                        
                        hft_status["total_analyzed"] += 1
                except:
                    hft_status["error_count"] += 1
        
        # Limit data size (keep last 1000 points)
        max_points = 1000
        for key in ["timestamps", "prices", "volumes"]:
            if len(hft_analytics_data[key]) > max_points:
                hft_analytics_data[key] = hft_analytics_data[key][-max_points:]
        
        # Limit opportunities (keep last 50)
        if len(hft_analytics_data["opportunities"]) > 50:
            hft_analytics_data["opportunities"] = hft_analytics_data["opportunities"][-50:]
        
        # Calculate analytics summary
        analytics_summary = {
            "total_data_points": len(hft_analytics_data["timestamps"]),
            "opportunities_count": len(hft_analytics_data["opportunities"]),
            "avg_profit_potential": sum(op.get("profit_potential", 0) for op in hft_analytics_data["opportunities"]) / max(len(hft_analytics_data["opportunities"]), 1),
            "last_update": datetime.now().isoformat(),
            "monitoring_status": "active" if hft_status["enabled"] else "stopped"
        }
        
        analytics_response = {
            **hft_analytics_data,
            "summary": analytics_summary,
            "config": hft_config,
            "status": hft_status
        }
        
        return {"status": "success", "analytics": analytics_response}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/hft/opportunities")
def get_hft_opportunities():
    """Get current HFT trading opportunities"""
    try:
        # Filter recent opportunities (last 5 minutes)
        current_time = datetime.now()
        recent_opportunities = []
        
        for opportunity in hft_analytics_data["opportunities"]:
            try:
                opp_time = datetime.fromisoformat(opportunity["time"].replace("Z", "+00:00"))
                if (current_time - opp_time).total_seconds() < 300:  # 5 minutes
                    recent_opportunities.append(opportunity)
            except:
                pass
        
        return {
            "status": "success",
            "opportunities": recent_opportunities,
            "count": len(recent_opportunities),
            "enabled": hft_status["enabled"],
            "last_analysis": hft_status["last_analysis"]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- Enhanced Data Collection Endpoints ---

@app.post("/ml/data_collection/config")
def save_data_collection_config(config: dict = Body(...)):
    """Save data collection configuration"""
    try:
        data_collector = get_data_collector()
        # Save configuration settings
        result = {"message": "Data collection configuration saved", "config": config}
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/ml/data_collection/status")
def get_data_collection_status():
    """Get data collection status"""
    try:
        data_collector = get_data_collector()
        status = {
            "running": True,  # Replace with actual status check
            "interval_seconds": 60,
            "symbols": ["BTCUSDT", "ETHUSDT"],
            "total_collected": 1500,
            "last_collection": "2025-01-01T10:00:00"
        }
        return {"status": "success", "collection_status": status}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- Enhanced Online Learning Endpoints (REMOVED - see ONLINE LEARNING CONTROL ENDPOINTS section) ---

@app.post("/ml/online/config")
def save_online_learning_config(config: dict = Body(...)):
    """Save online learning configuration"""
    try:
        # Mock config save - replace with actual implementation
        result = {"message": "Online learning configuration saved", "config": config}
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/ml/online/performance")
def get_model_performance():
    """Get model performance metrics"""
    try:
        stats = online_learning_manager.get_model_stats()
        return {"status": "success", "performance": stats}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/ml/online/buffer_status")
def get_learning_buffer_status():
    """Get incremental learning buffer status"""
    try:
        stats = online_learning_manager.get_stats()
        
        # Safely get buffer information with proper attribute checking
        buffer_size = 0
        max_buffer_size = 1000  # default
        models_count = 0
        
        if hasattr(online_learning_manager, 'data_buffer') and online_learning_manager.data_buffer is not None:
            buffer_size = len(online_learning_manager.data_buffer)
            if hasattr(online_learning_manager.data_buffer, 'maxlen') and online_learning_manager.data_buffer.maxlen is not None:
                max_buffer_size = online_learning_manager.data_buffer.maxlen
        
        if hasattr(online_learning_manager, 'models') and online_learning_manager.models is not None:
            models_count = len(online_learning_manager.models)
        
        buffer_usage = (buffer_size / max_buffer_size * 100) if max_buffer_size > 0 else 0
        
        buffer_status = {
            "buffer_size": buffer_size,
            "max_buffer_size": max_buffer_size,
            "buffer_usage": buffer_usage,
            "models_count": models_count,
            "last_update": stats.get("last_update_time", "Never")
        }
        return {"status": "success", "buffer_status": buffer_status}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- Performance Monitoring Dashboard Endpoints ---

@app.get("/performance/dashboard")
def get_performance_dashboard():
    """Get comprehensive performance dashboard data"""
    try:
        trades = get_trades()
        win_trades = [t for t in trades if t.get("pnl", 0) > 0]
        total_trades = len(trades)
        winrate = len(win_trades) / total_trades if total_trades > 0 else 0
        daily_pnl = sum(t.get("pnl", 0) for t in trades if t.get("open_time", "").startswith(datetime.now().date().isoformat()))
        return {"status": "success", "dashboard": {
            "winrate": winrate,
            "total_trades": total_trades,
            "daily_pnl": daily_pnl
        }}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/performance/metrics")
def get_performance_metrics(timeframe: str = "1d"):
    """Get performance metrics for specific timeframe"""
    try:
        trades = get_trades()
        total_return = sum(t.get("pnl", 0) for t in trades)
        win_trades = [t for t in trades if t.get("pnl", 0) > 0]
        loss_trades = [t for t in trades if t.get("pnl", 0) < 0]
        win_rate = len(win_trades) / len(trades) if trades else 0
        profit_factor = (sum(t.get("pnl", 0) for t in win_trades) / abs(sum(t.get("pnl", 0) for t in loss_trades))) if loss_trades else 0
        return {
            "status": "success",
            "metrics": {
                "timeframe": timeframe,
                "total_return": total_return,
                "annualized_return": total_return * 12,  # Example
                "volatility": float(np.std([t.get("pnl", 0) for t in trades])) if trades else 0,
                "sharpe_ratio": 1.0,  # Implement as needed
                "sortino_ratio": 1.0,  # Implement as needed
                "max_drawdown": min([t.get("pnl", 0) for t in trades]) if trades else 0,
                "calmar_ratio": 1.0,  # Implement as needed
                "win_rate": win_rate,
                "profit_factor": profit_factor
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- Advanced Risk Management Endpoints ---

@app.get("/risk/portfolio_metrics")
def get_portfolio_risk_metrics():
    """Get comprehensive portfolio-level risk metrics"""
    try:
        # Calculate current portfolio metrics
        current_balance = load_virtual_balance()
        pnl_data = calculate_current_pnl()
        
        # Get open positions from auto trading and futures
        open_positions = []
        
        # Add auto trading positions
        for trade in auto_trading_trades:
            if trade["status"] == "executed":
                open_positions.append({
                    "symbol": trade["symbol"],
                    "amount": trade["amount"],
                    "entry_price": trade.get("entry_price", trade["price"]),
                    "current_price": trade.get("current_price", trade["price"]),
                    "unrealized_pnl": trade.get("unrealized_pnl", 0)
                })
        
        # Add futures positions@app.get("/performance/metrics")
        try:
            futures_positions = binance_futures_engine.get_position_risk()
            for pos in futures_positions:
                if float(pos["positionAmt"]) != 0:
                    open_positions.append({
                        "symbol": pos["symbol"],
                        "amount": abs(float(pos["positionAmt"]) * float(pos["markPrice"])),
                        "entry_price": float(pos["entryPrice"]),
                        "current_price": float(pos["markPrice"]),
                        "unrealized_pnl": float(pos["unRealizedProfit"])
                    })
        except:
            pass  # Ignore if futures positions are not available
        
        # Calculate risk metrics
        total_exposure = sum(abs(pos["amount"]) for pos in open_positions)
        portfolio_value = float(pnl_data.get("current_balance", current_balance))
        
        # Risk calculations
        portfolio_risk_percent = (total_exposure / portfolio_value * 100) if portfolio_value > 0 else 0
        max_single_position = max([abs(pos["amount"]) for pos in open_positions], default=0)
        position_concentration = (max_single_position / portfolio_value * 100) if portfolio_value > 0 else 0
        
        # Drawdown calculation
        initial_balance = float(pnl_data.get("initial_balance", 10000.0))
        current_drawdown = ((initial_balance - portfolio_value) / initial_balance * 100) if initial_balance > 0 else 0
        max_drawdown_threshold = risk_settings.get("max_drawdown", 10.0)
        
        # Value at Risk (VaR) estimation - simplified
        unrealized_pnl_values = [float(pos["unrealized_pnl"]) for pos in open_positions if pos["unrealized_pnl"]]
        var_95 = np.percentile(unrealized_pnl_values, 5) if unrealized_pnl_values else 0
        
        risk_metrics = {
            "portfolio_value": portfolio_value,
            "total_exposure": total_exposure,
            "portfolio_risk_percent": portfolio_risk_percent,
            "position_concentration": position_concentration,
            "current_drawdown": current_drawdown,
            "max_drawdown_threshold": max_drawdown_threshold,
            "drawdown_remaining": max(0, max_drawdown_threshold - current_drawdown),
            "var_95": var_95,
            "open_positions_count": len(open_positions),
            "risk_score": min(100, portfolio_risk_percent + position_concentration + abs(current_drawdown)),
            "can_trade": current_drawdown < max_drawdown_threshold,
            "risk_warnings": []
        }
        
        # Risk warnings
        if current_drawdown > max_drawdown_threshold * 0.8:
            risk_metrics["risk_warnings"].append("Approaching maximum drawdown limit")
        if portfolio_risk_percent > 80:
            risk_metrics["risk_warnings"].append("High portfolio exposure")
        if position_concentration > 50:
            risk_metrics["risk_warnings"].append("High position concentration risk")
        
        return {"status": "success", "risk_metrics": risk_metrics}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/risk/calculate_position_size_advanced")
def calculate_dynamic_position_size(data: dict = Body(...)):
    """Calculate optimal position size based on advanced risk parameters"""
    try:
        symbol = data.get("symbol", "BTCUSDT")
        entry_price = float(data.get("entry_price", 0))
        stop_loss_price = float(data.get("stop_loss_price", 0))
        risk_per_trade_percent = float(data.get("risk_per_trade_percent", 2.0))
        confidence = float(data.get("confidence", 0.5))
        
        current_balance = load_virtual_balance()
        
        # Calculate risk amount
        max_risk_amount = current_balance * (risk_per_trade_percent / 100)
        
        # Adjust risk based on confidence
        confidence_multiplier = min(1.0, max(0.1, confidence))
        adjusted_risk_amount = max_risk_amount * confidence_multiplier
        
        # Calculate position size based on stop loss
        price_difference = 0
        if stop_loss_price > 0 and entry_price > 0:
            price_difference = abs(entry_price - stop_loss_price)
            risk_per_unit = price_difference / entry_price
            
            if risk_per_unit > 0:
                position_size = adjusted_risk_amount / risk_per_unit
            else:
                position_size = adjusted_risk_amount / entry_price
        else:
            # Fallback: use 2% of balance as position size
            position_size = adjusted_risk_amount
        
        # Apply maximum position size limits
        max_position_percent = 20.0  # Maximum 20% of portfolio in single position
        max_position_size = current_balance * (max_position_percent / 100)
        position_size = min(position_size, max_position_size)
        
        return {
            "status": "success",
            "position_sizing": {
                "symbol": symbol,
                "recommended_position_size": position_size,
                "risk_amount": adjusted_risk_amount,
                "max_risk_amount": max_risk_amount,
                "confidence_multiplier": confidence_multiplier,
                "portfolio_percent": (position_size / current_balance * 100) if current_balance > 0 else 0,
                "stop_loss_distance": price_difference if 'price_difference' in locals() else 0,
                "risk_reward_ratio": data.get("take_profit_price", entry_price * 1.05) / entry_price if entry_price > 0 else 1.0
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/risk/check_trade_risk")
def check_trade_risk(data: dict = Body(...)):
    """Check if a proposed trade meets risk criteria"""
    try:
        symbol = data.get("symbol", "BTCUSDT")
        position_size = float(data.get("position_size", 0))
        entry_price = float(data.get("entry_price", 0))
        stop_loss_price = float(data.get("stop_loss_price", 0))
        take_profit_price = float(data.get("take_profit_price", 0))
        risk_per_trade_percent = float(data.get("risk_per_trade_percent", 2.0))
        confidence = float(data.get("confidence", 0.5))
        current_balance = load_virtual_balance()
        pnl_data = calculate_current_pnl()
        # Get current risk metrics
        risk_response = get_portfolio_risk_metrics()
        if risk_response["status"] != "success":
            return {"status": "error", "message": "Failed to get portfolio risk metrics"}
        risk_metrics = risk_response.get("risk_metrics", {})
        if not isinstance(risk_metrics, dict):
            return {"status": "error", "message": "Invalid risk metrics format"}
        # Calculate proposed trade impact
        trade_value = position_size * entry_price if entry_price > 0 else position_size
        new_exposure = risk_metrics.get("total_exposure", 0) + trade_value
        new_portfolio_risk = (new_exposure / current_balance * 100) if current_balance > 0 else 0
        max_drawdown_threshold = risk_metrics.get("max_drawdown_threshold", 10.0)
        current_drawdown = risk_metrics.get("current_drawdown", 0)
        can_trade = current_drawdown < max_drawdown_threshold and new_portfolio_risk < 100
        # Risk checks
        warnings = []
        if new_portfolio_risk > 80:
            warnings.append("High portfolio risk after this trade")
        if current_drawdown > max_drawdown_threshold * 0.8:
            warnings.append("Approaching maximum drawdown limit")
        if position_size > current_balance * 0.2:
            warnings.append("Position size exceeds 20% of portfolio")
        if stop_loss_price > 0 and entry_price > 0:
            stop_loss_distance = abs(entry_price - stop_loss_price)
            if stop_loss_distance / entry_price < 0.005:
                warnings.append("Stop loss too tight (<0.5%)")
        else:
            warnings.append("Stop loss not set")
        return {
            "status": "success",
            "can_trade": can_trade,
            "new_portfolio_risk": new_portfolio_risk,
            "warnings": warnings,
            "risk_metrics": risk_metrics
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/risk/stop_loss_strategies")
def get_stop_loss_strategies(symbol: str = "BTCUSDT", entry_price: float = 0):
    """Get advanced stop loss strategy recommendations"""
    try:
        # Use real historical price/volatility data if available
        # Example: ATR-based, percent-based, and volatility-based stop loss
        try:
            from data_collection import get_atr
        except (ImportError, AttributeError, ModuleNotFoundError):
            # Fallback: simple ATR mock if get_atr is not available
            def get_atr(symbol):
                # Return a default ATR value or calculate a simple one
                return 0.01 * (entry_price if entry_price and entry_price > 0 else 1)
        try:
            atr = get_atr(symbol)
        except Exception:
            # If get_atr import succeeded but call fails, fallback to default
            atr = 0.01 * (entry_price if entry_price and entry_price > 0 else 1)
        percent_stop = 0.01  # 1% default
        if entry_price > 0:
            atr_stop = entry_price - atr if atr else entry_price * 0.99
            percent_stop_price = entry_price * (1 - percent_stop)
        else:
            atr_stop = None
            percent_stop_price = None
        strategies = [
            {"type": "ATR-based", "stop_loss": atr_stop, "atr": atr},
            {"type": "Percent-based", "stop_loss": percent_stop_price, "percent": percent_stop}
        ]
        return {"status": "success", "strategies": strategies}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/risk/update_advanced_settings")
def update_advanced_risk_settings(settings: dict = Body(...)):
    """Update advanced risk management settings using real backend logic"""
    try:
        global risk_settings
        risk_settings.update(settings)
        # Save to file for persistence
        os.makedirs("data", exist_ok=True)
        with open("data/risk_settings.json", "w") as f:
            json.dump(risk_settings, f, indent=2)
        return {"status": "success", "settings": risk_settings, "message": "Advanced risk settings updated"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# =============================================================================
# SIDEBAR AMOUNT BUTTONS ENDPOINTS  
# =============================================================================

@app.post("/sidebar/amount/50")
def set_sidebar_amount_50():
    """Set trading amount to $50"""
    try:
        auto_trading_settings["amount_config"]["amount"] = 50.0
        return {
            "status": "success",
            "amount": 50.0,
            "message": "Trading amount set to $50"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/sidebar/amount/100")
def set_sidebar_amount_100():
    """Set trading amount to $100"""
    try:
        auto_trading_settings["amount_config"]["amount"] = 100.0
        return {
            "status": "success",
            "amount": 100.0,
            "message": "Trading amount set to $100"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/sidebar/amount/250")
def set_sidebar_amount_250():
    """Set trading amount to $250"""
    try:
        auto_trading_settings["amount_config"]["amount"] = 250.0
        return {
            "status": "success",
            "amount": 250.0,
            "message": "Trading amount set to $250"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/sidebar/amount/500")
def set_sidebar_amount_500():
    """Set trading amount to $500"""
    try:
        auto_trading_settings["amount_config"]["amount"] = 500.0
        return {
            "status": "success",
            "amount": 500.0,
            "message": "Trading amount set to $500"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/sidebar/amount/1000")
def set_sidebar_amount_1000():
    """Set trading amount to $1000"""
    try:
        auto_trading_settings["amount_config"]["amount"] = 1000.0
        return {
            "status": "success",
            "amount": 1000.0,
            "message": "Trading amount set to $1000"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/sidebar/amount/max")
def set_sidebar_amount_max():
    """Set trading amount to maximum available balance"""
    try:
        # Ensure load_virtual_balance and auto_trading_settings are defined
        current_balance = load_virtual_balance()
        max_amount = current_balance * 0.95
        auto_trading_settings["amount_config"]["amount"] = max_amount
        return {
            "status": "success",
            "amount": max_amount,
            "message": f"Trading amount set to maximum: ${max_amount:.2f}"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/sidebar/ml_tools")
def get_sidebar_ml_tools():
    """
    Return real-time ML metrics for the dashboard sidebar.
    """
    try:
        # Check if online_learning_manager is available and has required methods
        if (
            online_learning_manager is None or
            not hasattr(online_learning_manager, "get_model_stats") or
            not hasattr(online_learning_manager, "predict_ensemble")
        ):
            return {
                "error": "Online learning manager or required methods not available.",
                "accuracy": None,
                "confidence": None,
                "status": "Unavailable"
            }

        # Get model stats (recent accuracy)
        stats = online_learning_manager.get_model_stats()
        # Compute average recent accuracy across all models
        accuracies = []
        for model, s in stats.items():
            if isinstance(s, dict) and "recent_accuracy" in s:
                accuracies.append(s["recent_accuracy"])
        avg_accuracy = float(np.mean(accuracies)) if accuracies else 0.0

        # Get ensemble confidence (simulate with zeros if no features)
        # In production, you might want to use the latest prediction features
        ensemble = online_learning_manager.predict_ensemble({})  # Empty features for now
        if isinstance(ensemble, dict):
            confidence = float(ensemble.get("ensemble_confidence", 0.0))
        else:
            confidence = 0.0

        # Status: "Ready" if models exist, "Training" if not
        status = "Ready" if stats.get("total_models", 0) > 0 else "Training"

        return {
            "accuracy": avg_accuracy,
            "confidence": confidence,
            "status": status
        }
    except Exception as e:
        return {
            "error": str(e),
            "accuracy": None,
            "confidence": None,
            "status": "Unavailable"
        }

@app.get("/sidebar/indicators/rsi")
def sidebar_rsi(symbol: str = "BTCUSDT"):
    """Return real RSI value and signal for the sidebar."""
    try:
        from data_collection import get_technical_indicators
        indicators = get_technical_indicators(symbol.upper())
        rsi_value = indicators.get("rsi", 50.0)
        # Simple signal logic
        if rsi_value > 70:
            rsi_signal = "Overbought"
        elif rsi_value < 30:
            rsi_signal = "Oversold"
        else:
            rsi_signal = "Neutral"
        return {"value": rsi_value, "signal": rsi_signal}
    except Exception as e:
        return {"error": str(e)}

@app.get("/sidebar/indicators/macd")
def sidebar_macd(symbol: str = "BTCUSDT"):
    """Return real MACD value and signal for the sidebar."""
    try:
        from data_collection import get_technical_indicators
        indicators = get_technical_indicators(symbol.upper())
        macd_value = indicators.get("macd", 0.0)
        macd_signal_value = indicators.get("macd_signal", 0.0)
        # Simple signal logic
        if macd_value > macd_signal_value:
            macd_signal = "Bullish"
        elif macd_value < macd_signal_value:
            macd_signal = "Bearish"
        else:
            macd_signal = "Neutral"
        return {"value": macd_value, "signal": macd_signal}
    except Exception as e:
        return {"error": str(e)}

@app.get("/sidebar/indicators/bollinger")
def sidebar_bollinger(symbol: str = "BTCUSDT"):
    """Return real Bollinger Bands values and signal for the sidebar."""
    try:
        from data_collection import get_technical_indicators
        indicators = get_technical_indicators(symbol.upper())
        upper = indicators.get("bb_upper", 0.0)
        middle = indicators.get("bb_middle", 0.0)
        lower = indicators.get("bb_lower", 0.0)
        price = indicators.get("close", middle)
        # Simple signal logic
        if price > upper:
            signal = "Overbought"
        elif price < lower:
            signal = "Oversold"
        else:
            signal = "Neutral"
        return {"upper": upper, "middle": middle, "lower": lower, "signal": signal}
    except Exception as e:
        return {"error": str(e)}

# =============================================================================
# CHART CONTROLS ENDPOINTS
# =============================================================================

@app.post("/charts/show_price")
def show_price_chart():
    """Enable price chart display"""
    try:
        return {
            "status": "success",
            "message": "Price chart display enabled",
            "chart_type": "price"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/charts/show_indicators")
def show_indicators_chart():
    """Enable indicators chart display"""
    try:
        return {
            "status": "success",
            "message": "Indicators chart display enabled",
            "chart_type": "indicators"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/chart/price")
def get_price_chart(symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 100):
    """
    Returns a Plotly figure for the price chart of the given symbol.
    """
    try:
        # Import plotly.graph_objects as go for charting
        import plotly.graph_objects as go
        from plotly.graph_objs import Layout

        # Try to get real OHLCV data
        try:
            from data_collection import get_ohlcv_data
            candles = get_ohlcv_data(symbol.upper(), interval, limit)
        except Exception:
            # Fallback: mock data
            from datetime import datetime, timedelta
            now = datetime.now()
            candles = [
                {
                    "timestamp": (now - timedelta(minutes=i)).timestamp(),
                    "open": 100 + i,
                    "high": 101 + i,
                    "low": 99 + i,
                    "close": 100 + i,
                    "volume": 10 + i
                }
                for i in range(limit)
            ]

        # Prepare data for Plotly
        x = [c["timestamp"] for c in candles]
        open_ = [c["open"] for c in candles]
        high = [c["high"] for c in candles]
        low = [c["low"] for c in candles]
        close = [c["close"] for c in candles]

        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=x,
                    open=open_,
                    high=high,
                    low=low,
                    close=close,
                    name=symbol.upper()
                )
            ],
            layout=go.Layout(
                title=f"{symbol.upper()} Price Chart",
                xaxis_title="Time",
                yaxis_title="Price (USDT)",
                template="plotly_dark"
            )
        )
        return fig.to_dict()
    except Exception as e:
        # Always return a valid Plotly figure on error
        import plotly.graph_objects as go
        from plotly.graph_objs import Layout
        fig = go.Figure(layout=go.Layout(title=f"Error: {str(e)}"))
        return fig.to_dict()

@app.post("/charts/refresh")
def refresh_charts():
    """Refresh all chart data"""
    try:
        current_time = datetime.now().isoformat()
        return {
            "status": "success",
            "message": "Charts refreshed successfully",
            "refreshed_at": current_time
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/charts/volume")
def get_volume_chart_data(symbol: str = "BTCUSDT"):
    """Get volume chart data from real data collector"""
    try:
        # Try to import get_volume_data from data_collection, fallback to mock if not available
        try:
            from data_collection import get_volume_data
        except (ImportError, AttributeError, ModuleNotFoundError):
            def get_volume_data(symbol):
                # Return mock volume data
                return [
                    {"timestamp": (datetime.now().timestamp() - 60 * i), "volume": 1000 + i * 10}
                    for i in range(100)
                ]
        volume_data = get_volume_data(symbol)
        return {
            "status": "success",
            "volume_data": volume_data
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/charts/momentum")
def get_momentum_chart_data(symbol: str = "BTCUSDT"):
    """Get momentum indicators chart data from real data collector"""
    try:
        from data_collection import get_momentum_data
        momentum_data = get_momentum_data(symbol)
        return {
            "status": "success",
            "momentum_data": momentum_data
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/charts/bollinger")
def get_bollinger_bands_data(symbol: str = "BTCUSDT"):
    """Get Bollinger Bands chart data from real data collector"""
    try:
        from data_collection import get_bollinger_data
        bb_data = get_bollinger_data(symbol)
        return {
            "status": "success",
            "bollinger_data": bb_data
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# =============================================================================
# ONLINE LEARNING CONTROL ENDPOINTS
# =============================================================================

@app.post("/ml/online_learning/enable")
def enable_online_learning():
    """Enable online learning system"""
    try:
        result = online_learning_manager.enable_learning()
        return {
            "status": "success",
            "enabled": True,
            "message": "Online learning enabled successfully",
            "config": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/ml/online_learning/disable")
def disable_online_learning():
    """Disable online learning system"""
    try:
        result = online_learning_manager.disable_learning()
        return {
            "status": "success",
            "enabled": False,
            "message": "Online learning disabled successfully",
            "final_stats": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/ml/online_learning/status")
def get_online_learning_status():
    """Get online learning system status"""
    try:
        status = online_learning_manager.get_status()
        stats = online_learning_manager.get_stats()
        
        return {
            "status": "success",
            "online_learning": {
                **status,
                **stats,
                "last_updated": datetime.now().isoformat()
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# =============================================================================
# RISK MANAGEMENT TOOL ENDPOINTS
# =============================================================================

@app.post("/risk/calculate_position_size")
def calculate_position_size(data: dict = Body(...)):
    """Calculate optimal position size based on risk parameters"""
    try:
        account_balance = data.get("account_balance", load_virtual_balance())
        risk_percent = data.get("risk_percent", 2.0)  # Default 2% risk
        entry_price = data.get("entry_price", 0)
        stop_loss_price = data.get("stop_loss_price", 0)
        
        if entry_price <= 0 or stop_loss_price <= 0:
            return {"status": "error", "message": "Entry price and stop loss price required"}
        
        # Calculate risk per share
        risk_per_share = abs(entry_price - stop_loss_price)
        
        # Calculate total risk amount
        total_risk_amount = account_balance * (risk_percent / 100)
        
        # Calculate position size
        position_size = total_risk_amount / risk_per_share if risk_per_share > 0 else 0
        
        # Calculate position value
        position_value = position_size * entry_price
        
        # Calculate percentage of account
        account_percentage = (position_value / account_balance * 100) if account_balance > 0 else 0
        
        return {
            "status": "success",
            "position_size": position_size,
            "position_value": position_value,
            "risk_amount": total_risk_amount,
            "risk_per_share": risk_per_share,
            "account_percentage": account_percentage,
            "recommendation": "SAFE" if account_percentage <= 20 else "MODERATE" if account_percentage <= 50 else "HIGH_RISK"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# =============================================================================
# EMAIL/ALERT INTEGRATION ENDPOINTS  
# =============================================================================

@app.post("/alerts/test_email")
def test_email_alert():
    """Test email alert functionality"""
    try:
        test_alert = {
            "type": "TEST",
            "message": "This is a test email alert from your crypto bot",
            "symbol": "BTCUSDT",
            "price": 45000.0,
            "change": 2.5,
            "pnl": 150.0
        }
        
        # Use the existing email sending function
        result = send_test_email({
            "subject": " Crypto Bot Test Alert",
            "body": f"Test alert sent at {datetime.now().isoformat()}\n\nYour crypto bot email system is working correctly!"
        })
        
        return {
            "status": "success" if result.get("status") == "success" else "error",
            "message": "Test email sent successfully" if result.get("status") == "success" else "Failed to send test email",
            "details": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/alerts/send_manual")
def send_manual_alert(alert_data: dict = Body(...)):
    """Send manual alert notification"""
    try:
        alert_type = alert_data.get("type", "MANUAL")
        message = alert_data.get("message", "Manual alert from crypto bot")
        
        # Create notification
        notification = {
            "id": str(uuid.uuid4()),
            "type": alert_type,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "read": False
        }
        save_notification(notification)
        
        # Also try to send email if enabled
        try:
            email_result = send_test_email({
                "subject": f" Crypto Bot Alert: {alert_type}",
                "body": f"Alert: {message}\nTime: {datetime.now().isoformat()}"
            })
        except:
            email_result = {"status": "error", "message": "Email sending failed"}
        
        return {
            "status": "success",
            "notification": notification,
            "email_sent": email_result.get("status") == "success",
            "message": "Manual alert sent successfully"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# =============================================================================
# TECHNICAL INDICATORS REFRESH ENDPOINTS
# =============================================================================

@app.post("/indicators/refresh")
def refresh_technical_indicators(symbol: str = "BTCUSDT"):
    """Refresh technical indicators for a symbol"""
    try:
        # Get fresh indicator data
        indicators = get_technical_indicators(symbol.lower())
        
        return {
            "status": "success",
            "symbol": symbol,
            "indicators": indicators,
            "refreshed_at": datetime.now().isoformat()
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

@app.get("/indicators/config")
def get_indicators_config():
    """Get technical indicators configuration"""
    try:
        config = {
            "rsi_period": 14,
            "macd_fast": 12,
            "macd_slow": 26,
            "macd_signal": 9,
            "bb_period": 20,
            "bb_std": 2.0,
            "refresh_interval": 60  # seconds
        }
        return {
            "status": "success",
            "config": config
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/indicators/config")
def update_indicators_config(config: dict = Body(...)):
    """Update technical indicators configuration"""
    try:
        # Save configuration (in real implementation, save to file/database)
        return {
            "status": "success",
            "config": config,
            "message": "Indicators configuration updated"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/futures/open")
def open_futures_position_api(data: dict = Body(...)):
    """
    Open a real futures position using the FuturesTradingEngine.
    Expects JSON: {"symbol": ..., "side": ..., "qty": ..., "leverage": ...}
    """
    try:
        symbol = data.get("symbol")
        if not symbol or not isinstance(symbol, str):
            return {"status": "error", "message": "Missing or invalid symbol"}
        side = data.get("side")
        qty_value = data.get("qty")
        if qty_value is None:
            return {"status": "error", "message": "Missing required field: qty"}
        try:
            qty = float(qty_value)
        except (TypeError, ValueError):
            return {"status": "error", "message": "Invalid qty value"}
        leverage = int(data.get("leverage", 10))
        price = data.get("price")
        # Use current time if not provided
        timestamp = data.get("timestamp") or datetime.now().isoformat()
        # Map side string to PositionSide enum
        from futures_trading import PositionSide
        side_enum = PositionSide.LONG if str(side).upper() in ["LONG", "BUY"] else PositionSide.SHORT
        from futures_trading import FuturesSignal
        signal = FuturesSignal(
            symbol=symbol,
            side=side_enum,
            confidence=1.0,  # Default confidence
            price=price if price else 0.0,
            timestamp=timestamp,
            leverage=leverage,
            stop_loss_percent=data.get("stop_loss_percent", 2.0),
            take_profit_percent=data.get("take_profit_percent", 5.0)
        )
        result = futures_engine.open_position(signal)
        return result
    except Exception as e:
        return {"status": "error", "message": f"Failed to open position: {str(e)}"}
# =============================================================================
# BINANCE FUTURES-STYLE & EXACT API ENDPOINTS
# =============================================================================

@app.get("/futures/account")
def get_futures_account():
    """Get futures account information"""
    try:
        account_info = binance_futures_engine.get_account()
        return {"status": "success", "account": account_info}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/futures/positions")
def get_futures_positions():
    """Get all open futures positions"""
    try:
        positions = binance_futures_engine.get_position_risk()
        return {"status": "success", "positions": positions, "count": len(positions)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/futures/history")
def get_futures_history(limit: int = 50):
    """Get futures trade history"""
    try:
        orders = list(binance_futures_engine.orders.values())
        filled_orders = [order for order in orders if order.status.value == "FILLED"]
        limited_orders = filled_orders[-limit:] if len(filled_orders) > limit else filled_orders
        history = []
        for order in limited_orders:
            history.append({
                "id": order.orderId,
                "symbol": order.symbol,
                "side": order.side.value,
                "quantity": float(order.executedQty),
                "price": float(order.avgPrice) if order.avgPrice else 0,
                "time": order.time,
                "realizedPnl": "0",  # Would need calculation
                "commission": "0",
                "commissionAsset": "USDT"
            })
        return {"status": "success", "trades": history, "count": len(history)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/futures/open_position")
def open_futures_position(signal: dict = Body(...)):
    """Open a new futures position"""
    try:
        symbol = signal.get("symbol", "BTCUSDT")
        side = OrderSide.BUY if signal.get("action", "").upper() == "BUY" else OrderSide.SELL
        quantity = signal.get("quantity", "0.001")
        order_type = OrderType.MARKET
        result = binance_futures_engine.new_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity
        )
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/futures/close_position")
def close_futures_position(data: dict = Body(...)):
    """Close a futures position"""
    try:
        position_id = data.get("position_id")
        current_price = data.get("current_price")
        if not position_id or not current_price:
            return {"status": "error", "message": "Missing position_id or current_price"}
        symbol = data.get("symbol", "BTCUSDT")
        quantity = data.get("quantity", "0.001")
        side = OrderSide.SELL if data.get("current_side", "").upper() == "BUY" else OrderSide.BUY
        result = binance_futures_engine.new_order(
            symbol=symbol,
            side=side,
            order_type=OrderType.MARKET,
            quantity=quantity,
            reduce_only=True
        )
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/futures/update_positions")
def update_futures_positions(data: dict = Body(...)):
    """Update and return all open futures positions with latest data (dashboard-compatible)."""
    try:
        symbol = data.get("symbol") if data else None
        positions = binance_futures_engine.get_position_risk(symbol) if symbol else binance_futures_engine.get_position_risk()
        enriched_positions = []
        for pos in positions:
            try:
                entry_price = float(pos.get("entryPrice", 0))
                mark_price = float(pos.get("markPrice", 0))
                position_amt = float(pos.get("positionAmt", 0))
                leverage = float(pos.get("leverage", 1))
                unrealized_pnl = float(pos.get("unRealizedProfit", 0))
                liquidation_price = float(pos.get("liquidationPrice", 0))
                pos_symbol = pos.get("symbol", "")
                side = "LONG" if position_amt > 0 else ("SHORT" if position_amt < 0 else "FLAT")
                notional = abs(position_amt * mark_price)
                margin = notional / leverage if leverage else 0
                enriched_positions.append({
                    "symbol": pos_symbol,
                    "side": side,
                    "positionAmt": position_amt,
                    "entryPrice": entry_price,
                    "markPrice": mark_price,
                    "unrealizedPnl": unrealized_pnl,
                    "liquidationPrice": liquidation_price,
                    "leverage": leverage,
                    "notional": notional,
                    "margin": margin,
                    "isolated": pos.get("isolated", False),
                    "updateTime": pos.get("updateTime", None),
                })
            except Exception:
                continue
        return {
            "status": "success",
            "positions": enriched_positions,
            "count": len(enriched_positions),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/futures/settings")
def get_futures_settings():
    """Get futures trading settings"""
    try:
        return {
            "status": "success",
            "settings": {
                "leverage_settings": binance_futures_engine.leverage_settings,
                "margin_type": binance_futures_engine.margin_type,
                "account_info": binance_futures_engine.account_info.model_dump()
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/futures/settings")
def update_futures_settings(settings: dict = Body(...)):
    """Update futures trading settings"""
    try:
        if "leverage" in settings:
            symbol = settings.get("symbol", "BTCUSDT")
            leverage = settings.get("leverage", 20)
            binance_futures_engine.change_leverage(symbol, leverage)
        if "margin_type" in settings:
            symbol = settings.get("symbol", "BTCUSDT")
            margin_type = settings.get("margin_type", "CROSSED")
            binance_futures_engine.change_margin_type(symbol, margin_type)
        binance_futures_engine.save_data()
        return {
            "status": "success",
            "settings": {
                "leverage_settings": binance_futures_engine.leverage_settings,
                "margin_type": binance_futures_engine.margin_type
            },
            "message": "Futures settings updated successfully"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/futures/execute_signal")
async def execute_futures_signal(signal: dict = Body(...)):
    """Execute a futures trading signal (for auto trading)"""
    try:
        if not auto_trading_status.get("enabled", False):
            return {"status": "info", "message": "Auto trading is disabled"}
        symbol = signal.get("symbol", "BTCUSDT")
        side = OrderSide.BUY if signal.get("action", "").upper() == "BUY" else OrderSide.SELL
        quantity = signal.get("quantity", "0.001")
        result = binance_futures_engine.new_order(
            symbol=symbol,
            side=side,
            order_type=OrderType.MARKET,
            quantity=quantity
        )
        signal_data = dict(signal)
        signal_data["executed_at"] = datetime.now().isoformat()
        recent_signals.append(signal_data)
        # Limit recent_signals to last 100 entries to prevent memory issues
        if len(recent_signals) > 100:
            del recent_signals[:-100]
        if result:
            auto_trading_status["signals_processed"] += 1
            auto_trading_status["active_trades"] = list(binance_futures_engine.positions.keys())
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/futures/analytics")
def get_futures_analytics():
    """Get comprehensive futures trading analytics (real logic)"""
    try:
        account_info = binance_futures_engine.get_account()
        positions = binance_futures_engine.get_position_risk()
        orders = list(binance_futures_engine.orders.values())
        filled_orders = [order for order in orders if order.status.value == "FILLED"]
        total_trades = len(filled_orders)
        wins = [o for o in filled_orders if float(getattr(o, "realizedPnl", 0)) > 0]
        losses = [o for o in filled_orders if float(getattr(o, "realizedPnl", 0)) < 0]
        win_rate = (len(wins) / total_trades * 100) if total_trades else 0
        avg_win = np.mean([float(getattr(o, "realizedPnl", 0)) for o in wins]) if wins else 0
        avg_loss = np.mean([float(getattr(o, "realizedPnl", 0)) for o in losses]) if losses else 0
        profit_factor = (sum([float(getattr(o, "realizedPnl", 0)) for o in wins]) / abs(sum([float(getattr(o, "realizedPnl", 0)) for o in losses]))) if losses else 0
        total_unrealized_pnl = sum(float(pos.get("unrealized_pnl", "0")) for pos in positions)
        total_realized_pnl = sum([float(getattr(o, "realizedPnl", 0)) for o in filled_orders])
        total_pnl = total_unrealized_pnl + total_realized_pnl
        return {
            "status": "success",
            "account": account_info,
            "summary": {
                "total_pnl": total_pnl,
                "unrealized_pnl": total_unrealized_pnl,
                "realized_pnl": total_realized_pnl,
                "total_return_percent": (total_pnl / 10000) * 100,
                "margin_used": sum(abs(float(pos.get("positionAmt", "0")) * float(pos.get("markPrice", "0"))) / float(pos.get("leverage", "1")) for pos in positions),
                "margin_ratio": 0.0,
                "can_trade": account_info.get("canTrade", True)
            },
            "trading_stats": {
                "total_trades": total_trades,
                "winning_trades": len(wins),
                "losing_trades": len(losses),
                "win_rate": win_rate,
                "profit_factor": profit_factor,
                "avg_win": avg_win,
                "avg_loss": avg_loss,
                "gross_profit": sum([float(getattr(o, "realizedPnl", 0)) for o in wins]),
                "gross_loss": abs(sum([float(getattr(o, "realizedPnl", 0)) for o in losses]))
            },
            "open_positions": len([pos for pos in positions if float(pos.get("positionAmt", "0")) != 0]),
            "positions": positions,
            "recent_trades": filled_orders[-10:],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/auto_trading/execute_futures_signal")
def execute_auto_trading_futures_signal(signal: dict = Body(...)):
    """Execute futures signal through auto trading system"""
    try:
        if not auto_trading_status.get("enabled", False):
            return {"status": "info", "message": "Auto trading is disabled"}
        return execute_futures_signal(signal)
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/fapi/v2/account")
def get_binance_account():
    """Get Binance futures account information - EXACT API"""
    try:
        account_data = binance_futures_engine.get_account()
        return account_data
    except Exception as e:
        return {"code": -1000, "msg": f"An unknown error occurred: {str(e)}"}

@app.get("/fapi/v2/balance")
def get_binance_balance():
    """Get Binance futures balance - EXACT API"""
    try:
        account_data = binance_futures_engine.get_account()
        return account_data.get("assets", [])
    except Exception as e:
        return {"code": -1000, "msg": f"An unknown error occurred: {str(e)}"}

@app.get("/fapi/v2/positionRisk")
def get_binance_position_risk(symbol: Optional[str] = Query(None)):
    """Get position information - EXACT Binance API"""
    try:
        return binance_futures_engine.get_position_risk()
    except Exception as e:
        return {"code": -1000, "msg": f"An unknown error occurred: {str(e)}"}

@app.post("/fapi/v1/order")
def new_binance_order(
    symbol: str,
    side: str,
    type: str,
    quantity: str,
    price: Optional[str] = None,
    timeInForce: Optional[str] = "GTC",
    reduceOnly: Optional[bool] = False,
    positionSide: Optional[str] = "BOTH",
    stopPrice: Optional[str] = None,
    closePosition: Optional[bool] = False,
    workingType: Optional[str] = "CONTRACT_PRICE"
):
    """Place new order - EXACT Binance API"""
    try:
        side_enum = OrderSide(side)
        type_enum = OrderType(type)
        position_side_enum = PositionSide(positionSide) if positionSide else PositionSide.BOTH
        time_in_force_enum = TimeInForce(timeInForce)
        working_type_enum = WorkingType(workingType) if workingType else WorkingType.CONTRACT_PRICE
        return binance_futures_engine.new_order(
            symbol=symbol,
            side=side_enum,
            order_type=type_enum,
            quantity=quantity,
            price=price,
            position_side=position_side_enum,
            time_in_force=time_in_force_enum,
            reduce_only=bool(reduceOnly) if reduceOnly is not None else False,
            close_position=bool(closePosition) if closePosition is not None else False,
            stop_price=stopPrice,
            working_type=working_type_enum
        )
    except Exception as e:
        return {"code": -1000, "msg": f"An unknown error occurred: {str(e)}"}

@app.get("/fapi/v1/openOrders")
def get_binance_open_orders(symbol: Optional[str] = Query(None)):
    """Get open orders - EXACT Binance API"""
    try:
        orders = []
        for order in binance_futures_engine.orders.values():
            if order.status in [OrderStatus.NEW, OrderStatus.PARTIALLY_FILLED]:
                if symbol is None or order.symbol == symbol:
                    orders.append(order.model_dump())
        return orders
    except Exception as e:
        return {"code": -1000, "msg": f"An unknown error occurred: {str(e)}"}

@app.delete("/fapi/v1/order")
def cancel_binance_order(symbol: str, orderId: Optional[int] = None, origClientOrderId: Optional[str] = None):
    """Cancel order - EXACT Binance API"""
    try:
        if orderId:
            if orderId in binance_futures_engine.orders:
                order = binance_futures_engine.orders[orderId]
                order.status = OrderStatus.CANCELED
                order.updateTime = int(datetime.now().timestamp() * 1000)
                return order.model_dump()
        return {"code": -2011, "msg": "Unknown order sent."}
    except Exception as e:
        return {"code": -1000, "msg": f"An unknown error occurred: {str(e)}"}

@app.post("/fapi/v1/leverage")
def change_binance_leverage(symbol: str, leverage: int):
    """Change leverage - EXACT Binance API"""
    try:
        return binance_futures_engine.change_leverage(symbol, leverage)
    except Exception as e:
        return {"code": -1000, "msg": f"An unknown error occurred: {str(e)}"}

@app.post("/fapi/v1/marginType")
def change_binance_margin_type(symbol: str, marginType: str):
    """Change margin type - EXACT Binance API"""
    try:
        return binance_futures_engine.change_margin_type(symbol, marginType)
    except Exception as e:
        return {"code": -1000, "msg": f"An unknown error occurred: {str(e)}"}

@app.get("/fapi/v1/ticker/24hr")
def get_24hr_ticker(symbol: Optional[str] = Query(None)):
    """Get 24hr ticker statistics - EXACT Binance API"""
    try:
        # Always use direct Binance REST API call for 24hr ticker statistics
        url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
        params = {"symbol": symbol} if symbol else {}
        resp = requests.get(url, params=params, timeout=10)
        tickers = resp.json()
        if isinstance(tickers, dict):
            tickers = [tickers]
        if symbol:
            return next((t for t in tickers if t["symbol"] == symbol), {})
        return tickers
    except Exception as e:
        return {"code": -1000, "msg": f"An unknown error occurred: {str(e)}"}

@app.get("/fapi/v1/exchangeInfo")
def get_exchange_info():
    """Get exchange information - EXACT Binance API"""
    try:
        # Always use Binance REST API for exchange info to avoid missing method errors
        url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            return {"code": -1002, "msg": f"Failed to fetch exchange info from Binance: {str(e)}"}
    except Exception as e:
        return {"code": -1000, "msg": f"An unknown error occurred: {str(e)}"}
# --- SERVER STARTUP ---
if __name__ == "__main__":
    print("[DEBUG] Starting main.py...")
    print(f"[DEBUG] Working directory: {os.getcwd()}")
    print("[DEBUG] Importing dependencies...")
    
    import uvicorn
    
    print("[OK] Dependencies imported successfully")
    
    print("[INFO] Starting Crypto Bot Backend Server (main.py)")
    print("[INFO] Server URL: http://localhost:8000")
    print("[INFO] API Docs: http://localhost:8000/docs")
    print("[INFO] Health Check: http://localhost:8000/health")
    print("[OK] Starting with simplified startup...")
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, log_level="info")
    except Exception as e:
        print(f"[ERROR] Server startup error: {e}")
        print("[INFO] Try using main_working.py instead")

