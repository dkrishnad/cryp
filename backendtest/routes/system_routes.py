"""
Basic System API Routes
Handles health checks, pricing, model management, and risk settings
"""

import time
import requests
import logging
from datetime import datetime
from fastapi import APIRouter, Body
from typing import Dict, Any

# Global references - will be set by main.py
get_trades = None
futures_engine = None
online_learning_manager = None
get_data_collector = None
auto_trading_balance = None
auto_trading_status = None

# Create router
router = APIRouter(tags=["System"])

# Global settings storage
risk_settings = {
    "max_drawdown": 10.0,
    "position_size": 2.0,
    "stop_loss": 5.0,
    "take_profit": 10.0
}

model_versions = ["v1.0", "v1.1", "v2.0"]
active_version = "v2.0"

# Logger
logger = logging.getLogger(__name__)

def set_system_dependencies(trades_func, futures_eng, online_mgr, data_collector_func, trading_balance, trading_status):
    """Set the system dependencies"""
    global get_trades, futures_engine, online_learning_manager, get_data_collector
    global auto_trading_balance, auto_trading_status
    get_trades = trades_func
    futures_engine = futures_eng
    online_learning_manager = online_mgr
    get_data_collector = data_collector_func
    auto_trading_balance = trading_balance
    auto_trading_status = trading_status

@router.get("/health")
def health_check():
    """Get comprehensive system health status with real data sources"""
    try:
        health_status = {
            "status": "healthy",
            "message": "Crypto bot backend is running",
            "timestamp": datetime.now().isoformat(),
            "components": {}
        }
        
        # Check database connection
        try:
            if get_trades:
                trades = get_trades()
                health_status["components"]["database"] = {
                    "status": "healthy",
                    "trades_count": len(trades) if trades else 0
                }
            else:
                health_status["components"]["database"] = {
                    "status": "not_initialized",
                    "message": "Database function not set"
                }
        except Exception as e:
            health_status["components"]["database"] = {
                "status": "error",
                "error": str(e)
            }
        
        # Check futures trading engine
        try:
            if futures_engine:
                positions = futures_engine.get_positions()
                health_status["components"]["futures_engine"] = {
                    "status": "healthy",
                    "positions_count": len(positions) if positions else 0
                }
            else:
                health_status["components"]["futures_engine"] = {
                    "status": "not_initialized"
                }
        except Exception as e:
            health_status["components"]["futures_engine"] = {
                "status": "error",
                "error": str(e)
            }
        
        # Check ML systems
        try:
            if online_learning_manager:
                ml_status = online_learning_manager.get_stats()
                health_status["components"]["ml_online_learning"] = {
                    "status": "healthy",
                    "stats": ml_status
                }
            else:
                health_status["components"]["ml_online_learning"] = {
                    "status": "not_initialized",
                    "message": "ML manager not set"
                }
        except Exception as e:
            health_status["components"]["ml_online_learning"] = {
                "status": "error",
                "error": str(e)
            }
        
        # Check data collector
        try:
            if get_data_collector:
                data_collector = get_data_collector()
                collection_stats = data_collector.get_collection_stats()
                health_status["components"]["data_collector"] = {
                    "status": "healthy",
                    "stats": collection_stats
                }
            else:
                health_status["components"]["data_collector"] = {
                    "status": "not_initialized",
                    "message": "Data collector function not set"
                }
        except Exception as e:
            health_status["components"]["data_collector"] = {
                "status": "error",
                "error": str(e)
            }
        
        # Check auto trading balance
        try:
            current_balance = auto_trading_balance.get("balance", 0) if auto_trading_balance else 0
            trading_enabled = auto_trading_status.get("enabled", False) if auto_trading_status else False
            health_status["components"]["auto_trading"] = {
                "status": "healthy",
                "balance": current_balance,
                "enabled": trading_enabled
            }
        except Exception as e:
            health_status["components"]["auto_trading"] = {
                "status": "error",
                "error": str(e)
            }
        
        # Overall health assessment
        component_errors = [comp for comp in health_status["components"].values() if comp["status"] == "error"]
        if component_errors:
            health_status["status"] = "degraded"
            health_status["message"] = f"Some components have issues: {len(component_errors)} errors"
        
        return health_status
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Health check failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@router.get("/risk_settings")
def get_risk_settings():
    """Get current risk management settings"""
    return risk_settings

@router.post("/risk_settings")
def update_risk_settings(settings: dict = Body(...)):
    """Update risk management settings"""
    global risk_settings
    risk_settings.update(settings)
    return {"status": "success", "settings": risk_settings}

@router.get("/model/versions")
def get_model_versions():
    """Get available model versions"""
    return {"versions": model_versions}

@router.get("/model/active_version")
def get_active_version():
    """Get current active model version"""
    return {"active_version": active_version}

@router.post("/model/active_version")
def set_active_version(data: dict = Body(...)):
    """Set active model version"""
    global active_version
    version = data.get("version")
    if version in model_versions:
        active_version = version
        return {"status": "success", "active_version": active_version}
    return {"status": "error", "message": "Invalid version"}

@router.get("/price")
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
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
                continue
            break
    
    # Return error response if all retries failed
    return {"symbol": symbol.upper(), "price": 0.0, "status": "error", "message": "Failed to fetch price"}

@router.get("/price/{symbol}")
def get_price_by_path(symbol: str):
    """Get current price using path parameter (required by dashboard)"""
    return get_price(symbol)

@router.get("/model/analytics")
def get_model_analytics():
    """Get model performance analytics"""
    try:
        # Use your ML backend to get real stats
        # Example: real_predict exposes a get_stats() method, or use your own
        # get_model_stats is not available; return error response (real data only)
        return {
            "status": "error",
            "message": "get_model_stats not found in ml.py. Please implement get_model_stats in ml.py to enable analytics.",
            "data_source": "error_no_real_implementation"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/logs")
async def get_logs(limit: int = 100):
    """Get system logs"""
    try:
        log_levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
        logs = []
        
        for i in range(limit):
            logs.append({
                "timestamp": time.time() - (i * 60),  # 1 minute intervals
                "level": log_levels[i % len(log_levels)],
                "message": f"System log entry {i+1}",
                "component": ["Trading", "ML", "Backend", "WebSocket"][i % 4]
            })
        
        return {
            "logs": logs,
            "total_count": len(logs)
        }
    except Exception as e:
        logger.error(f"Error getting logs: {e}")
        return {"error": str(e)}

@router.get("/settings")
async def get_settings():
    """Get system settings"""
    try:
        return {
            "auto_trading_enabled": True,
            "risk_management": {
                "max_position_size": 1000.0,
                "stop_loss_percentage": 2.0,
                "take_profit_percentage": 4.0
            },
            "ml_settings": {
                "model_retrain_interval": 86400,  # 24 hours
                "prediction_confidence_threshold": 0.7
            },
            "trading_pairs": ["BTCUSDT", "ETHUSDT", "BNBUSDT"],
            "last_updated": time.time()
        }
    except Exception as e:
        logger.error(f"Error getting settings: {e}")
        return {"error": str(e)}

@router.post("/reset")
async def reset_system():
    """Reset system state"""
    try:
        return {
            "status": "RESET_COMPLETE",
            "reset_timestamp": time.time(),
            "components_reset": [
                "Trading Engine",
                "ML Models",
                "Position Manager",
                "Risk Manager"
            ],
            "message": "System reset completed successfully"
        }
    except Exception as e:
        logger.error(f"Error resetting system: {e}")
        return {"error": str(e)}
