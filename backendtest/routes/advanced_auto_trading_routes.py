"""
Advanced Auto Trading API Routes
Handles all advanced auto trading endpoints
"""

import os
import json
from fastapi import APIRouter, Body
from typing import Dict, Any

# Import the advanced auto trading engine
try:
    from advanced_auto_trading import AdvancedAutoTradingEngine
    ADVANCED_ENGINE_AVAILABLE = True
except ImportError:
    ADVANCED_ENGINE_AVAILABLE = False
    AdvancedAutoTradingEngine = None

# Global engine instance - will be set by main.py
advanced_auto_trading_engine = None

# Create router
router = APIRouter(prefix="/advanced_auto_trading", tags=["Advanced Auto Trading"])

def set_engine_instance(engine):
    """Set the global engine instance"""
    global advanced_auto_trading_engine
    advanced_auto_trading_engine = engine

@router.get("/status")
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

@router.post("/start")
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

@router.post("/stop")
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

@router.get("/positions")
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

@router.get("/market_data")
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

@router.get("/indicators/{symbol}")
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

@router.get("/ai_signals")
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

@router.post("/config")
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
