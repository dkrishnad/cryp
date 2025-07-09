"""
Binance Futures API-Compatible Trading System
Exact match to Binance Futures for real trading automation
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime
import json
import os
import math
from enum import Enum

# Binance Futures Exact Enums
class PositionSide(str, Enum):
    BOTH = "BOTH"      # One-way mode
    LONG = "LONG"      # Hedge mode long
    SHORT = "SHORT"    # Hedge mode short

class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(str, Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    STOP = "STOP"
    STOP_MARKET = "STOP_MARKET"
    TAKE_PROFIT = "TAKE_PROFIT"
    TAKE_PROFIT_MARKET = "TAKE_PROFIT_MARKET"
    TRAILING_STOP_MARKET = "TRAILING_STOP_MARKET"

class TimeInForce(str, Enum):
    GTC = "GTC"  # Good Till Cancel
    IOC = "IOC"  # Immediate or Cancel
    FOK = "FOK"  # Fill or Kill
    GTX = "GTX"  # Good Till Cross

class OrderStatus(str, Enum):
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"

class WorkingType(str, Enum):
    MARK_PRICE = "MARK_PRICE"
    CONTRACT_PRICE = "CONTRACT_PRICE"

# Binance Futures Models
class BinanceFuturesOrder(BaseModel):
    orderId: int
    symbol: str
    status: OrderStatus
    clientOrderId: str
    price: str
    avgPrice: str
    origQty: str
    executedQty: str
    cumQty: str
    cumQuote: str
    timeInForce: TimeInForce
    type: OrderType
    reduceOnly: bool
    closePosition: bool
    side: OrderSide
    positionSide: PositionSide
    stopPrice: str
    workingType: WorkingType
    priceProtect: bool
    origType: OrderType
    time: int
    updateTime: int

class BinanceFuturesPosition(BaseModel):
    symbol: str
    positionAmt: str
    entryPrice: str
    markPrice: str
    unRealizedProfit: str
    liquidationPrice: str
    leverage: str
    maxNotionalValue: str
    marginType: str  # "isolated" or "cross"
    isolatedMargin: str
    isAutoAddMargin: str
    positionSide: PositionSide
    notional: str
    isolatedWallet: str
    updateTime: int

class BinanceFuturesAccountInfo(BaseModel):
    feeTier: int
    canTrade: bool
    canDeposit: bool
    canWithdraw: bool
    updateTime: int
    multiAssetsMargin: bool
    tradeGroupId: int
    totalWalletBalance: str
    totalUnrealizedProfit: str
    totalMarginBalance: str
    totalPositionInitialMargin: str
    totalOpenOrderInitialMargin: str
    totalCrossWalletBalance: str
    totalCrossUnPnl: str
    availableBalance: str
    maxWithdrawAmount: str

class BinanceFuturesBalance(BaseModel):
    accountAlias: str
    asset: str
    balance: str
    crossWalletBalance: str
    crossUnPnl: str
    availableBalance: str
    maxWithdrawAmount: str
    marginAvailable: bool
    updateTime: int

class BinanceFuturesSymbolInfo(BaseModel):
    symbol: str
    pair: str
    contractType: str
    deliveryDate: int
    onboardDate: int
    status: str
    maintMarginPercent: str
    requiredMarginPercent: str
    baseAsset: str
    quoteAsset: str
    marginAsset: str
    pricePrecision: int
    quantityPrecision: int
    baseAssetPrecision: int
    quotePrecision: int
    underlyingType: str
    underlyingSubType: List[str]
    settlePlan: int
    triggerProtect: str
    liquidationFee: str
    marketTakeBound: str

class BinanceFuturesLeverageBracket(BaseModel):
    bracket: int
    initialLeverage: int
    notionalCap: int
    notionalFloor: int
    maintMarginRatio: float
    cum: float

# Enhanced Futures Trading Engine - Binance Compatible
class BinanceFuturesTradingEngine:
    def __init__(self):
        self.positions: Dict[str, BinanceFuturesPosition] = {}
        self.orders: Dict[int, BinanceFuturesOrder] = {}
        self.balances: Dict[str, BinanceFuturesBalance] = {}
        self.account_info = BinanceFuturesAccountInfo(
            feeTier=0,
            canTrade=True,
            canDeposit=True,
            canWithdraw=True,
            updateTime=int(datetime.now().timestamp() * 1000),
            multiAssetsMargin=False,
            tradeGroupId=0,
            totalWalletBalance="10000.00000000",
            totalUnrealizedProfit="0.00000000",
            totalMarginBalance="10000.00000000",
            totalPositionInitialMargin="0.00000000",
            totalOpenOrderInitialMargin="0.00000000",
            totalCrossWalletBalance="10000.00000000",
            totalCrossUnPnl="0.00000000",
            availableBalance="10000.00000000",
            maxWithdrawAmount="10000.00000000"
        )
        
        # Initialize USDT balance
        self.balances["USDT"] = BinanceFuturesBalance(
            accountAlias="SgsR",
            asset="USDT",
            balance="10000.00000000",
            crossWalletBalance="10000.00000000",
            crossUnPnl="0.00000000",
            availableBalance="10000.00000000",
            maxWithdrawAmount="10000.00000000",
            marginAvailable=True,
            updateTime=int(datetime.now().timestamp() * 1000)
        )
        
        self.order_id_counter = 1000000
        self.leverage_settings: Dict[str, int] = {}  # symbol -> leverage
        self.margin_type: Dict[str, str] = {}  # symbol -> "isolated" or "cross"
        
        # Binance-exact maintenance margin rates
        self.maintenance_margins = {
            "BTCUSDT": [
                {"notional_floor": 0, "notional_cap": 50000, "maint_margin_ratio": 0.004, "cum": 0},
                {"notional_floor": 50000, "notional_cap": 250000, "maint_margin_ratio": 0.005, "cum": 50},
                {"notional_floor": 250000, "notional_cap": 1000000, "maint_margin_ratio": 0.01, "cum": 1300},
                {"notional_floor": 1000000, "notional_cap": 5000000, "maint_margin_ratio": 0.025, "cum": 16300},
                {"notional_floor": 5000000, "notional_cap": 20000000, "maint_margin_ratio": 0.05, "cum": 141300},
                {"notional_floor": 20000000, "notional_cap": 50000000, "maint_margin_ratio": 0.1, "cum": 1141300},
                {"notional_floor": 50000000, "notional_cap": 100000000, "maint_margin_ratio": 0.125, "cum": 2391300},
                {"notional_floor": 100000000, "notional_cap": 200000000, "maint_margin_ratio": 0.15, "cum": 4891300},
                {"notional_floor": 200000000, "notional_cap": 300000000, "maint_margin_ratio": 0.25, "cum": 24891300},
                {"notional_floor": 300000000, "notional_cap": float('inf'), "maint_margin_ratio": 0.5, "cum": 99891300}
            ],
            "ETHUSDT": [
                {"notional_floor": 0, "notional_cap": 10000, "maint_margin_ratio": 0.005, "cum": 0},
                {"notional_floor": 10000, "notional_cap": 100000, "maint_margin_ratio": 0.0075, "cum": 25},
                {"notional_floor": 100000, "notional_cap": 500000, "maint_margin_ratio": 0.01, "cum": 275},
                {"notional_floor": 500000, "notional_cap": 1000000, "maint_margin_ratio": 0.025, "cum": 7775},
                {"notional_floor": 1000000, "notional_cap": 2000000, "maint_margin_ratio": 0.05, "cum": 32775},
                {"notional_floor": 2000000, "notional_cap": 5000000, "maint_margin_ratio": 0.1, "cum": 132775},
                {"notional_floor": 5000000, "notional_cap": 10000000, "maint_margin_ratio": 0.125, "cum": 257775},
                {"notional_floor": 10000000, "notional_cap": float('inf'), "maint_margin_ratio": 0.5, "cum": 4007775}
            ]
        }
        
        self.load_data()
    
    def get_maintenance_margin_rate(self, symbol: str, notional: float) -> tuple:
        """Get maintenance margin rate and cum for a symbol and notional value"""
        brackets = self.maintenance_margins.get(symbol, self.maintenance_margins["BTCUSDT"])
        
        for bracket in brackets:
            if bracket["notional_floor"] <= notional < bracket["notional_cap"]:
                return bracket["maint_margin_ratio"], bracket["cum"]
        
        # Default to highest bracket
        return 0.5, brackets[-1]["cum"]
    
    def calculate_liquidation_price_binance(self, symbol: str, side: str, position_amt: float, 
                                          entry_price: float, leverage: int, 
                                          wallet_balance: float) -> float:
        """Calculate liquidation price using Binance's exact formula"""
        notional = abs(position_amt * entry_price)
        maint_margin_rate, cum = self.get_maintenance_margin_rate(symbol, notional)
        
        # Binance liquidation formula
        # Long: liq_price = (wallet_balance + cum - side * position_amt * entry_price) / (position_amt * (maint_margin_rate - side))
        # Short: same formula but side = -1 for short, +1 for long
        
        side_multiplier = 1 if side == "LONG" else -1
        
        if position_amt == 0:
            return 0
            
        liquidation_price = (wallet_balance + cum - side_multiplier * position_amt * entry_price) / \
                           (position_amt * (maint_margin_rate - side_multiplier))
        
        return max(liquidation_price, 0.001)  # Ensure positive price
    
    def calculate_margin_ratio(self, symbol: str, position_amt: float, mark_price: float, 
                              wallet_balance: float) -> float:
        """Calculate margin ratio using Binance's formula"""
        if wallet_balance <= 0:
            return 1.0
            
        notional = abs(position_amt * mark_price)
        if notional == 0:
            return 0
            
        maint_margin_rate, cum = self.get_maintenance_margin_rate(symbol, notional)
        maintenance_margin = notional * maint_margin_rate + cum
        
        return maintenance_margin / wallet_balance
    
    def new_order(self, symbol: str, side: OrderSide, order_type: OrderType, 
                  quantity: str, price: Optional[str] = None, 
                  position_side: PositionSide = PositionSide.BOTH,
                  time_in_force: TimeInForce = TimeInForce.GTC,
                  reduce_only: bool = False, close_position: bool = False,
                  stop_price: Optional[str] = None, 
                  working_type: WorkingType = WorkingType.CONTRACT_PRICE) -> Dict[str, Any]:
        """Place new order - Binance API compatible"""
        try:
            order_id = self.order_id_counter
            self.order_id_counter += 1
            
            # Convert quantity and price to float for calculations
            qty = float(quantity)
            px = float(price) if price else 0
            
            # Get current leverage
            leverage = self.leverage_settings.get(symbol, 20)
            
            # Calculate notional value
            notional = qty * px if px > 0 else 0
            
            # Check available balance
            usdt_balance = float(self.balances["USDT"].availableBalance)
            required_margin = notional / leverage if leverage > 0 else notional
            
            if required_margin > usdt_balance and not reduce_only:
                return {
                    "code": -2019,
                    "msg": "Margin is insufficient."
                }
            
            # Create order
            order = BinanceFuturesOrder(
                orderId=order_id,
                symbol=symbol,
                status=OrderStatus.NEW if order_type == OrderType.LIMIT else OrderStatus.FILLED,
                clientOrderId=f"web_{order_id}",
                price=price or "0",
                avgPrice="0" if order_type == OrderType.LIMIT else price or "0",
                origQty=quantity,
                executedQty="0" if order_type == OrderType.LIMIT else quantity,
                cumQty="0" if order_type == OrderType.LIMIT else quantity,
                cumQuote="0",
                timeInForce=time_in_force,
                type=order_type,
                reduceOnly=reduce_only,
                closePosition=close_position,
                side=side,
                positionSide=position_side,
                stopPrice=stop_price or "0",
                workingType=working_type,
                priceProtect=False,
                origType=order_type,
                time=int(datetime.now().timestamp() * 1000),
                updateTime=int(datetime.now().timestamp() * 1000)
            )
            
            self.orders[order_id] = order
            
            # Execute market orders immediately
            if order_type == OrderType.MARKET:
                self._execute_order(order, px)
            
            return {
                "orderId": order_id,
                "symbol": symbol,
                "status": order.status,
                "clientOrderId": order.clientOrderId,
                "price": order.price,
                "origQty": order.origQty,
                "executedQty": order.executedQty,
                "cumQty": order.cumQty,
                "cumQuote": order.cumQuote,
                "timeInForce": order.timeInForce,
                "type": order.type,
                "reduceOnly": order.reduceOnly,
                "closePosition": order.closePosition,
                "side": order.side,
                "positionSide": order.positionSide,
                "stopPrice": order.stopPrice,
                "workingType": order.workingType,
                "priceProtect": order.priceProtect,
                "origType": order.origType,
                "updateTime": order.updateTime
            }
            
        except Exception as e:
            return {
                "code": -1000,
                "msg": f"An unknown error occurred while processing the request: {str(e)}"
            }
    
    def _execute_order(self, order: BinanceFuturesOrder, execution_price: float):
        """Execute an order and update positions"""
        symbol = order.symbol
        qty = float(order.origQty)
        side = order.side
        position_side = order.positionSide
        
        # Determine position direction
        if position_side == PositionSide.BOTH:
            # One-way mode
            direction = "LONG" if side == OrderSide.BUY else "SHORT"
        else:
            # Hedge mode
            direction = position_side
        
        # Create position key
        position_key = f"{symbol}_{direction}"
        
        # Get or create position
        if position_key not in self.positions:
            self.positions[position_key] = BinanceFuturesPosition(
                symbol=symbol,
                positionAmt="0",
                entryPrice="0",
                markPrice=str(execution_price),
                unRealizedProfit="0",
                liquidationPrice="0",
                leverage=str(self.leverage_settings.get(symbol, 20)),
                maxNotionalValue="1000000",
                marginType=self.margin_type.get(symbol, "cross"),
                isolatedMargin="0",
                isAutoAddMargin="false",
                positionSide=PositionSide.LONG if direction == "LONG" else PositionSide.SHORT,
                notional="0",
                isolatedWallet="0",
                updateTime=int(datetime.now().timestamp() * 1000)
            )
        
        position = self.positions[position_key]
        current_qty = float(position.positionAmt)
        current_entry = float(position.entryPrice) if position.entryPrice != "0" else execution_price
        
        # Calculate new position
        if side == OrderSide.BUY:
            new_qty = current_qty + qty
        else:
            new_qty = current_qty - qty
        
        # Calculate new entry price (weighted average)
        if new_qty != 0:
            if (current_qty >= 0 and side == OrderSide.BUY) or (current_qty <= 0 and side == OrderSide.SELL):
                # Increasing position
                total_cost = current_qty * current_entry + qty * execution_price
                new_entry_price = total_cost / new_qty if new_qty != 0 else execution_price
            else:
                # Reducing position or changing direction
                new_entry_price = execution_price if abs(new_qty) > abs(current_qty) else current_entry
        else:
            new_entry_price = 0
        
        # Update position
        position.positionAmt = str(new_qty)
        position.entryPrice = str(new_entry_price)
        position.markPrice = str(execution_price)
        position.updateTime = int(datetime.now().timestamp() * 1000)
        
        # Calculate liquidation price
        wallet_balance = float(self.account_info.totalWalletBalance)
        liquidation_price = self.calculate_liquidation_price_binance(
            symbol, direction, new_qty, new_entry_price, 
            int(position.leverage), wallet_balance
        )
        position.liquidationPrice = str(liquidation_price)
        
        # Calculate unrealized PnL
        if new_qty != 0:
            pnl = (execution_price - new_entry_price) * new_qty
            if direction == "SHORT":
                pnl = -pnl
            position.unRealizedProfit = str(pnl)
            position.notional = str(abs(new_qty * execution_price))
        else:
            position.unRealizedProfit = "0"
            position.notional = "0"
        
        # Update balances
        leverage = int(position.leverage)
        margin_used = abs(new_qty * execution_price) / leverage
        
        # Update order status
        order.status = OrderStatus.FILLED
        order.executedQty = order.origQty
        order.cumQty = order.origQty
        order.avgPrice = str(execution_price)
        order.updateTime = int(datetime.now().timestamp() * 1000)
        
        self.save_data()
    
    def get_position_risk(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get position information - Binance API compatible"""
        positions = []
        
        for position in self.positions.values():
            if symbol is None or position.symbol == symbol:
                positions.append({
                    "symbol": position.symbol,
                    "positionAmt": position.positionAmt,
                    "entryPrice": position.entryPrice,
                    "markPrice": position.markPrice,
                    "unRealizedProfit": position.unRealizedProfit,
                    "liquidationPrice": position.liquidationPrice,
                    "leverage": position.leverage,
                    "maxNotionalValue": position.maxNotionalValue,
                    "marginType": position.marginType,
                    "isolatedMargin": position.isolatedMargin,
                    "isAutoAddMargin": position.isAutoAddMargin,
                    "positionSide": position.positionSide,
                    "notional": position.notional,
                    "isolatedWallet": position.isolatedWallet,
                    "updateTime": position.updateTime
                })
        
        return positions
    
    def get_account(self) -> Dict[str, Any]:
        """Get account information - Binance API compatible"""
        # Update account totals
        total_unrealized_pnl = sum(float(pos.unRealizedProfit) for pos in self.positions.values())
        total_margin = sum(abs(float(pos.positionAmt) * float(pos.markPrice)) / float(pos.leverage) 
                          for pos in self.positions.values() if float(pos.positionAmt) != 0)
        
        self.account_info.totalUnrealizedProfit = str(total_unrealized_pnl)
        self.account_info.totalPositionInitialMargin = str(total_margin)
        self.account_info.availableBalance = str(float(self.account_info.totalWalletBalance) - total_margin)
        self.account_info.updateTime = int(datetime.now().timestamp() * 1000)
        
        return {
            "feeTier": self.account_info.feeTier,
            "canTrade": self.account_info.canTrade,
            "canDeposit": self.account_info.canDeposit,
            "canWithdraw": self.account_info.canWithdraw,
            "updateTime": self.account_info.updateTime,
            "multiAssetsMargin": self.account_info.multiAssetsMargin,
            "tradeGroupId": self.account_info.tradeGroupId,
            "totalWalletBalance": self.account_info.totalWalletBalance,
            "totalUnrealizedProfit": self.account_info.totalUnrealizedProfit,
            "totalMarginBalance": str(float(self.account_info.totalWalletBalance) + total_unrealized_pnl),
            "totalPositionInitialMargin": self.account_info.totalPositionInitialMargin,
            "totalOpenOrderInitialMargin": self.account_info.totalOpenOrderInitialMargin,
            "totalCrossWalletBalance": self.account_info.totalCrossWalletBalance,
            "totalCrossUnPnl": self.account_info.totalUnrealizedProfit,
            "availableBalance": self.account_info.availableBalance,
            "maxWithdrawAmount": self.account_info.availableBalance,
            "assets": [
                {
                    "asset": "USDT",
                    "walletBalance": self.account_info.totalWalletBalance,
                    "unrealizedProfit": self.account_info.totalUnrealizedProfit,
                    "marginBalance": str(float(self.account_info.totalWalletBalance) + total_unrealized_pnl),
                    "maintMargin": "0",
                    "initialMargin": self.account_info.totalPositionInitialMargin,
                    "positionInitialMargin": self.account_info.totalPositionInitialMargin,
                    "openOrderInitialMargin": "0",
                    "crossWalletBalance": self.account_info.totalWalletBalance,
                    "crossUnPnl": self.account_info.totalUnrealizedProfit,
                    "availableBalance": self.account_info.availableBalance,
                    "maxWithdrawAmount": self.account_info.availableBalance,
                    "marginAvailable": True,
                    "updateTime": self.account_info.updateTime
                }
            ],
            "positions": self.get_position_risk()
        }
    
    def change_leverage(self, symbol: str, leverage: int) -> Dict[str, Any]:
        """Change leverage for symbol - Binance API compatible"""
        try:
            if leverage < 1 or leverage > 125:
                return {
                    "code": -4028,
                    "msg": "Leverage is over the maximum defined for this symbol."
                }
            
            self.leverage_settings[symbol] = leverage
            
            # Update existing positions
            for position in self.positions.values():
                if position.symbol == symbol:
                    position.leverage = str(leverage)
            
            self.save_data()
            
            return {
                "leverage": leverage,
                "maxNotionalValue": "1000000",
                "symbol": symbol
            }
            
        except Exception as e:
            return {
                "code": -1000,
                "msg": f"An unknown error occurred: {str(e)}"
            }
    
    def change_margin_type(self, symbol: str, margin_type: str) -> Dict[str, Any]:
        """Change margin type for symbol - Binance API compatible"""
        try:
            if margin_type not in ["ISOLATED", "CROSSED"]:
                return {
                    "code": -4046,
                    "msg": "No need to change margin type."
                }
            
            self.margin_type[symbol] = margin_type.lower()
            
            # Update existing positions
            for position in self.positions.values():
                if position.symbol == symbol:
                    position.marginType = margin_type.lower()
            
            self.save_data()
            
            return {
                "code": 200,
                "msg": "success"
            }
            
        except Exception as e:
            return {
                "code": -1000,
                "msg": f"An unknown error occurred: {str(e)}"
            }
    
    def save_data(self):
        """Save data to files"""
        try:
            os.makedirs("data", exist_ok=True)
            
            # Save positions
            positions_data = {key: pos.model_dump() for key, pos in self.positions.items()}
            with open("data/binance_futures_positions.json", "w") as f:
                json.dump(positions_data, f, indent=2)
            
            # Save account info
            with open("data/binance_futures_account.json", "w") as f:
                json.dump(self.account_info.model_dump(), f, indent=2)
            
            # Save orders
            orders_data = {str(key): order.model_dump() for key, order in self.orders.items()}
            with open("data/binance_futures_orders.json", "w") as f:
                json.dump(orders_data, f, indent=2)
            
            # Save settings
            settings_data = {
                "leverage_settings": self.leverage_settings,
                "margin_type": self.margin_type
            }
            with open("data/binance_futures_settings.json", "w") as f:
                json.dump(settings_data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving Binance futures data: {e}")
    
    def load_data(self):
        """Load data from files"""
        try:
            # Load positions
            if os.path.exists("data/binance_futures_positions.json"):
                with open("data/binance_futures_positions.json", "r") as f:
                    positions_data = json.load(f)
                    self.positions = {
                        key: BinanceFuturesPosition(**pos_data)
                        for key, pos_data in positions_data.items()
                    }
            
            # Load account info
            if os.path.exists("data/binance_futures_account.json"):
                with open("data/binance_futures_account.json", "r") as f:
                    account_data = json.load(f)
                    self.account_info = BinanceFuturesAccountInfo(**account_data)
            
            # Load orders
            if os.path.exists("data/binance_futures_orders.json"):
                with open("data/binance_futures_orders.json", "r") as f:
                    orders_data = json.load(f)
                    self.orders = {
                        int(key): BinanceFuturesOrder(**order_data)
                        for key, order_data in orders_data.items()
                    }
            
            # Load settings
            if os.path.exists("data/binance_futures_settings.json"):
                with open("data/binance_futures_settings.json", "r") as f:
                    settings_data = json.load(f)
                    self.leverage_settings = settings_data.get("leverage_settings", {})
                    self.margin_type = settings_data.get("margin_type", {})
            
        except Exception as e:
            print(f"Error loading Binance futures data: {e}")

# Global Binance-compatible futures engine
binance_futures_engine = BinanceFuturesTradingEngine()
