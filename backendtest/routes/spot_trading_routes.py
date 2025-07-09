"""
Spot Trading Routes
Handles spot trading operations: account, positions, buy, sell, cancel orders
"""

from fastapi import APIRouter, HTTPException
import time

router = APIRouter()

@router.get("/account")
async def get_account():
    """Get account information"""
    try:
        return {
            "account_type": "SPOT",
            "total_balance": 10000.0,
            "available_balance": 8500.0,
            "in_order": 1500.0,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/positions")
async def get_positions():
    """Get open positions"""
    try:
        return {
            "positions": [
                {
                    "symbol": "BTCUSDT",
                    "side": "LONG",
                    "size": 0.1,
                    "entry_price": 45000.0,
                    "current_price": 46000.0,
                    "pnl": 100.0,
                    "pnl_percentage": 2.22
                }
            ],
            "total_pnl": 100.0,
            "position_count": 1
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/buy")
async def place_buy_order(request: dict):
    """Place buy order"""
    try:
        return {
            "status": "FILLED",
            "order_id": f"BUY_{int(time.time())}",
            "symbol": request.get("symbol", "BTCUSDT"),
            "side": "BUY",
            "quantity": request.get("quantity", 0.001),
            "price": request.get("price", 45000.0),
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sell")
async def place_sell_order(request: dict):
    """Place sell order"""
    try:
        return {
            "status": "FILLED",
            "order_id": f"SELL_{int(time.time())}",
            "symbol": request.get("symbol", "BTCUSDT"),
            "side": "SELL",
            "quantity": request.get("quantity", 0.001),
            "price": request.get("price", 45000.0),
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cancel_order")
async def cancel_order(request: dict):
    """Cancel order"""
    try:
        return {
            "status": "CANCELLED",
            "order_id": request.get("order_id"),
            "symbol": request.get("symbol", "BTCUSDT"),
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
