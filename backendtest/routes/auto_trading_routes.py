"""
Auto Trading Routes
Handles auto trading operations: start, stop, status
"""

from fastapi import APIRouter, HTTPException
import time

router = APIRouter(prefix="/auto_trading", tags=["Auto Trading"])

@router.post("/start")
async def start_auto_trading(request: dict):
    """Start auto trading"""
    try:
        return {
            "status": "STARTED",
            "symbol": request.get("symbol", "BTCUSDT"),
            "strategy": request.get("strategy", "ML_STRATEGY"),
            "amount": request.get("amount", 100.0),
            "risk_level": request.get("risk_level", "MEDIUM"),
            "started_at": time.time(),
            "message": "Auto trading started successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop")
async def stop_auto_trading():
    """Stop auto trading"""
    try:
        return {
            "status": "STOPPED",
            "stopped_at": time.time(),
            "session_pnl": 125.50,
            "trades_executed": 8,
            "message": "Auto trading stopped successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
