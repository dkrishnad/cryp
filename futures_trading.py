"""
Binance Futures-Style Trading System
Complete implementation with leverage, SL, TP, liquidations, and margin management
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime
import json
import os
import math
from enum import Enum

class PositionSide(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"

class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP_MARKET = "STOP_MARKET"
    TAKE_PROFIT_MARKET = "TAKE_PROFIT_MARKET"

class PositionStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    LIQUIDATED = "LIQUIDATED"

class FuturesSignal(BaseModel):
    symbol: str
    side: PositionSide  # LONG or SHORT
    confidence: float
    price: float
    timestamp: str
    leverage: Optional[int] = 10
    stop_loss_percent: Optional[float] = 2.0
    take_profit_percent: Optional[float] = 5.0

class FuturesPosition(BaseModel):
    id: str
    symbol: str
    side: PositionSide
    size: float  # Position size in base currency
    entry_price: float
    current_price: float
    leverage: int
    margin_used: float
    unrealized_pnl: float
    unrealized_pnl_percent: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    liquidation_price: float
    status: PositionStatus
    created_at: str
    closed_at: Optional[str] = None
    closed_pnl: Optional[float] = None

class FuturesAccountInfo(BaseModel):
    total_wallet_balance: float
    available_balance: float
    total_margin_used: float
    total_unrealized_pnl: float
    maintenance_margin: float
    margin_ratio: float  # margin_ratio = maintenance_margin / total_wallet_balance
    can_trade: bool

class FuturesSettings(BaseModel):
    default_leverage: int = 10
    max_leverage: int = 125
    default_margin_per_trade: float = 100.0  # USD
    auto_stop_loss: bool = True
    auto_take_profit: bool = True
    default_stop_loss_percent: float = 2.0
    default_take_profit_percent: float = 5.0
    liquidation_buffer_percent: float = 0.5  # Buffer before liquidation
    risk_per_trade_percent: float = 1.0  # % of total balance to risk per trade

class FuturesTradingEngine:
    def __init__(self):
        self.positions: Dict[str, FuturesPosition] = {}
        self.account_info = FuturesAccountInfo(
            total_wallet_balance=10000.0,  # Starting balance
            available_balance=10000.0,
            total_margin_used=0.0,
            total_unrealized_pnl=0.0,
            maintenance_margin=0.0,
            margin_ratio=0.0,
            can_trade=True
        )
        self.settings = FuturesSettings()
        self.trade_history: List[Dict[str, Any]] = []
        self.load_data()
    
    def calculate_position_size(self, margin: float, leverage: int, price: float) -> float:
        """Calculate position size based on margin, leverage, and current price"""
        return (margin * leverage) / price
    
    def calculate_liquidation_price(self, entry_price: float, leverage: int, side: PositionSide) -> float:
        """Calculate liquidation price for a position"""
        # Simplified liquidation calculation (maintenance margin = 0.5%)
        maintenance_margin_rate = 0.005
        
        if side == PositionSide.LONG:
            # For long: liquidation = entry_price * (1 - (1/leverage - maintenance_margin_rate))
            liquidation_price = entry_price * (1 - (1/leverage - maintenance_margin_rate))
        else:
            # For short: liquidation = entry_price * (1 + (1/leverage - maintenance_margin_rate))
            liquidation_price = entry_price * (1 + (1/leverage - maintenance_margin_rate))
        
        return max(liquidation_price, 0.001)  # Ensure positive price
    
    def calculate_unrealized_pnl(self, position: FuturesPosition, current_price: float) -> tuple:
        """Calculate unrealized PnL for a position"""
        price_diff = current_price - position.entry_price
        
        if position.side == PositionSide.SHORT:
            price_diff = -price_diff  # Inverse for short positions
        
        unrealized_pnl = price_diff * position.size
        unrealized_pnl_percent = (price_diff / position.entry_price) * 100 * position.leverage
        
        return unrealized_pnl, unrealized_pnl_percent
    
    def check_liquidation(self, position: FuturesPosition, current_price: float) -> bool:
        """Check if position should be liquidated"""
        if position.side == PositionSide.LONG:
            return current_price <= position.liquidation_price
        else:
            return current_price >= position.liquidation_price
    
    def check_stop_loss(self, position: FuturesPosition, current_price: float) -> bool:
        """Check if stop loss should be triggered"""
        if not position.stop_loss:
            return False
            
        if position.side == PositionSide.LONG:
            return current_price <= position.stop_loss
        else:
            return current_price >= position.stop_loss
    
    def check_take_profit(self, position: FuturesPosition, current_price: float) -> bool:
        """Check if take profit should be triggered"""
        if not position.take_profit:
            return False
            
        if position.side == PositionSide.LONG:
            return current_price >= position.take_profit
        else:
            return current_price <= position.take_profit
    
    def open_position(self, signal: FuturesSignal) -> Dict[str, Any]:
        """Open a new futures position"""
        try:
            # Calculate margin to use
            margin = self.settings.default_margin_per_trade
            
            # Check if we have enough available balance
            if self.account_info.available_balance < margin:
                return {
                    "status": "error",
                    "message": f"Insufficient balance. Available: ${self.account_info.available_balance:.2f}, Required: ${margin:.2f}"
                }
            
            # Calculate position size
            position_size = self.calculate_position_size(margin, signal.leverage or self.settings.default_leverage, signal.price)
            
            # Calculate liquidation price
            liquidation_price = self.calculate_liquidation_price(
                signal.price, 
                signal.leverage or self.settings.default_leverage, 
                signal.side
            )
            
            # Calculate stop loss and take profit
            stop_loss = None
            take_profit = None
            
            if self.settings.auto_stop_loss and signal.stop_loss_percent:
                if signal.side == PositionSide.LONG:
                    stop_loss = signal.price * (1 - signal.stop_loss_percent / 100)
                else:
                    stop_loss = signal.price * (1 + signal.stop_loss_percent / 100)
            
            if self.settings.auto_take_profit and signal.take_profit_percent:
                if signal.side == PositionSide.LONG:
                    take_profit = signal.price * (1 + signal.take_profit_percent / 100)
                else:
                    take_profit = signal.price * (1 - signal.take_profit_percent / 100)
            
            # Create position
            position_id = f"{signal.symbol}_{signal.side}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            position = FuturesPosition(
                id=position_id,
                symbol=signal.symbol,
                side=signal.side,
                size=position_size,
                entry_price=signal.price,
                current_price=signal.price,
                leverage=signal.leverage or self.settings.default_leverage,
                margin_used=margin,
                unrealized_pnl=0.0,
                unrealized_pnl_percent=0.0,
                stop_loss=stop_loss,
                take_profit=take_profit,
                liquidation_price=liquidation_price,
                status=PositionStatus.OPEN,
                created_at=signal.timestamp
            )
            
            # Update account info
            self.account_info.available_balance -= margin
            self.account_info.total_margin_used += margin
            
            # Store position
            self.positions[position_id] = position
            
            # Save data
            self.save_data()
            
            return {
                "status": "success",
                "message": "Position opened successfully",                "position": position.model_dump(),
                "account_info": self.account_info.model_dump()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to open position: {str(e)}"
            }
    
    def close_position(self, position_id: str, current_price: float, reason: str = "manual") -> Dict[str, Any]:
        """Close a position"""
        try:
            if position_id not in self.positions:
                return {"status": "error", "message": "Position not found"}
            
            position = self.positions[position_id]
            
            # Calculate final PnL
            unrealized_pnl, unrealized_pnl_percent = self.calculate_unrealized_pnl(position, current_price)
            
            # Update position
            position.status = PositionStatus.LIQUIDATED if reason == "liquidation" else PositionStatus.CLOSED
            position.closed_at = datetime.now().isoformat()
            position.closed_pnl = unrealized_pnl
            position.current_price = current_price
            
            # Update account balance
            self.account_info.available_balance += position.margin_used + unrealized_pnl
            self.account_info.total_margin_used -= position.margin_used
            
            # Add to trade history
            trade_record = {
                "position_id": position_id,
                "symbol": position.symbol,
                "side": position.side,
                "entry_price": position.entry_price,
                "exit_price": current_price,
                "size": position.size,
                "leverage": position.leverage,
                "pnl": unrealized_pnl,
                "pnl_percent": unrealized_pnl_percent,
                "margin_used": position.margin_used,
                "reason": reason,
                "created_at": position.created_at,
                "closed_at": position.closed_at
            }
            self.trade_history.append(trade_record)
            
            # Remove from active positions
            del self.positions[position_id]
            
            # Save data
            self.save_data()
            
            return {
                "status": "success",
                "message": f"Position closed ({reason})",
                "pnl": unrealized_pnl,
                "trade_record": trade_record,
                "account_info": self.account_info.model_dump()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to close position: {str(e)}"
            }
    
    def update_positions(self, symbol: str, current_price: float) -> List[Dict[str, Any]]:
        """Update all positions for a symbol and check for triggers"""
        updates = []
        positions_to_close = []
        
        for position_id, position in self.positions.items():
            if position.symbol.upper() != symbol.upper():
                continue
            
            # Update current price and PnL
            unrealized_pnl, unrealized_pnl_percent = self.calculate_unrealized_pnl(position, current_price)
            position.current_price = current_price
            position.unrealized_pnl = unrealized_pnl
            position.unrealized_pnl_percent = unrealized_pnl_percent
            
            # Check for liquidation
            if self.check_liquidation(position, current_price):
                positions_to_close.append((position_id, "liquidation"))
                updates.append({
                    "position_id": position_id,
                    "action": "liquidation",
                    "price": current_price,
                    "pnl": unrealized_pnl
                })
            
            # Check for stop loss
            elif self.check_stop_loss(position, current_price):
                positions_to_close.append((position_id, "stop_loss"))
                updates.append({
                    "position_id": position_id,
                    "action": "stop_loss",
                    "price": current_price,
                    "pnl": unrealized_pnl
                })
            
            # Check for take profit
            elif self.check_take_profit(position, current_price):
                positions_to_close.append((position_id, "take_profit"))
                updates.append({
                    "position_id": position_id,
                    "action": "take_profit",
                    "price": current_price,
                    "pnl": unrealized_pnl
                })
        
        # Close triggered positions
        for position_id, reason in positions_to_close:
            self.close_position(position_id, current_price, reason)
        
        # Update account totals
        self.update_account_totals()
        
        return updates
    
    def update_account_totals(self):
        """Update account totals based on current positions"""
        total_unrealized_pnl = sum(pos.unrealized_pnl for pos in self.positions.values())
        maintenance_margin = sum(pos.margin_used * 0.005 for pos in self.positions.values())  # 0.5% maintenance
        
        self.account_info.total_unrealized_pnl = total_unrealized_pnl
        self.account_info.maintenance_margin = maintenance_margin
        
        # Calculate margin ratio
        total_balance = self.account_info.available_balance + self.account_info.total_margin_used + total_unrealized_pnl
        if total_balance > 0:
            self.account_info.margin_ratio = maintenance_margin / total_balance
        else:
            self.account_info.margin_ratio = 1.0
        
        # Update total wallet balance
        self.account_info.total_wallet_balance = total_balance
        
        # Check if can trade (margin ratio < 80%)
        self.account_info.can_trade = self.account_info.margin_ratio < 0.8
    
    def get_positions(self) -> List[Dict[str, Any]]:
        """Get all open positions"""
        return [pos.model_dump() for pos in self.positions.values()]
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information"""
        self.update_account_totals()
        return self.account_info.model_dump()
    
    def get_trade_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get trade history"""
        return self.trade_history[-limit:]
    
    def save_data(self):
        """Save data to files"""
        try:
            os.makedirs("data", exist_ok=True)
            
            # Save positions
            positions_data = {pos_id: pos.model_dump() for pos_id, pos in self.positions.items()}
            with open("data/futures_positions.json", "w") as f:
                json.dump(positions_data, f, indent=2)
            
            # Save account info
            with open("data/futures_account.json", "w") as f:
                json.dump(self.account_info.model_dump(), f, indent=2)
            
            # Save trade history
            with open("data/futures_trade_history.json", "w") as f:
                json.dump(self.trade_history, f, indent=2)
            
            # Save settings
            with open("data/futures_settings.json", "w") as f:
                json.dump(self.settings.model_dump(), f, indent=2)
                
        except Exception as e:
            print(f"Error saving futures data: {e}")
    
    def load_data(self):
        """Load data from files"""
        try:
            # Load positions
            if os.path.exists("data/futures_positions.json"):
                with open("data/futures_positions.json", "r") as f:
                    positions_data = json.load(f)
                    self.positions = {
                        pos_id: FuturesPosition(**pos_data)
                        for pos_id, pos_data in positions_data.items()
                    }
            
            # Load account info
            if os.path.exists("data/futures_account.json"):
                with open("data/futures_account.json", "r") as f:
                    account_data = json.load(f)
                    self.account_info = FuturesAccountInfo(**account_data)
            
            # Load trade history
            if os.path.exists("data/futures_trade_history.json"):
                with open("data/futures_trade_history.json", "r") as f:
                    self.trade_history = json.load(f)
            
            # Load settings
            if os.path.exists("data/futures_settings.json"):
                with open("data/futures_settings.json", "r") as f:
                    settings_data = json.load(f)
                    self.settings = FuturesSettings(**settings_data)
            
            # Update account totals
            self.update_account_totals()
            
        except Exception as e:
            print(f"Error loading futures data: {e}")

# Global futures trading engine instance
futures_engine = FuturesTradingEngine()
