#!/usr/bin/env python3
"""
Advanced Async Auto Trading Engine with Full AI/ML Integration
Fully asynchronous trading system with real-time indicators and AI signals
"""
import asyncio
import aiohttp
import json
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import threading
import time
from dataclasses import dataclass, asdict
from enum import Enum
# Import ta library (better alternative to talib for Windows)
try:
    import ta
    TA_AVAILABLE = True
    print("[+] TA library imported successfully - professional technical analysis available")
except ImportError:
    TA_AVAILABLE = False
    print("[!] Warning: 'ta' library not available. Please install with: pip install ta")
    # Create a minimal fallback
    class MockTA:
        @staticmethod
        def momentum_rsi(close, window=14):
            return [50.0] * len(close)
        @staticmethod  
        def trend_macd(close):
            return [0.0] * len(close)
        @staticmethod
        def volatility_bollinger_hband(close, window=20):
            return close
        @staticmethod
        def volatility_bollinger_lband(close, window=20):
            return close
        @staticmethod
        def trend_sma_fast(close, window=20):
            return close
        @staticmethod
        def trend_ema_fast(close, window=20):
            return close
    ta = MockTA()
import websockets
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradingSignal(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

class PositionStatus(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    PENDING = "PENDING"

@dataclass
class MarketData:
    symbol: str
    price: float
    volume: float
    timestamp: datetime
    bid: float = 0.0
    ask: float = 0.0
    
@dataclass
class TechnicalIndicators:
    rsi: float
    macd: float
    macd_signal: float
    macd_histogram: float
    bb_upper: float
    bb_middle: float
    bb_lower: float
    stoch_k: float
    stoch_d: float
    williams_r: float
    atr: float
    adx: float
    cci: float
    sma_20: float
    ema_20: float
    volume_sma: float
    obv: float
    
@dataclass
class AISignal:
    signal: TradingSignal
    confidence: float
    timeframe: str
    indicators_used: List[str]
    model_version: str
    prediction_horizon: str
    risk_score: float
    
@dataclass
class Position:
    id: str
    symbol: str
    side: TradingSignal
    size: float
    entry_price: float
    current_price: float
    stop_loss: float
    take_profit: float
    pnl: float
    unrealized_pnl: float
    status: PositionStatus
    opened_at: datetime
    closed_at: Optional[datetime] = None

class AdvancedAutoTradingEngine:
    """
    Advanced Auto Trading Engine with:
    - Fully asynchronous operation
    - Real-time AI/ML signal generation
    - Multi-timeframe analysis
    - Advanced risk management
    - Dynamic position sizing
    - Real-time technical indicators
    """
    
    def __init__(self, config_path: str = "data/auto_trading_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        
        # Core components
        self.is_running = False
        self.positions: Dict[str, Position] = {}
        self.market_data: Dict[str, MarketData] = {}
        self.indicators: Dict[str, TechnicalIndicators] = {}
        
        # AI/ML components
        self.ml_models = {}
        self.signal_history: List[AISignal] = []
        
        # Performance tracking
        self.total_pnl = 0.0
        self.trades_executed = 0
        self.win_rate = 0.0
        self.max_drawdown = 0.0
        
        # Async components
        self.trading_loop_task = None
        self.data_feed_task = None
        self.ai_signal_task = None
        self.risk_monitor_task = None
        
        # Event system
        self.events = asyncio.Queue()
        
    def _load_config(self) -> Dict:
        """Load configuration from file"""
        default_config = {
            "enabled": False,
            "symbols": ["KAIAUSDT", "BTCUSDT", "ETHUSDT"],
            "primary_symbol": "KAIAUSDT",
            "timeframes": ["1m", "5m", "15m", "1h"],
            "primary_timeframe": "5m",
            "balance": 10000.0,
            "risk_per_trade": 2.0,
            "max_positions": 3,
            "min_confidence": 0.70,
            "stop_loss_pct": 2.0,
            "take_profit_pct": 4.0,
            "position_sizing": {
                "method": "fixed_risk",  # fixed_risk, kelly, martingale
                "base_amount": 100.0,
                "max_position_size": 1000.0
            },
            "ai_models": {
                "enabled": True,
                "ensemble_weight": 0.8,
                "confidence_threshold": 0.65,
                "model_refresh_interval": 3600  # 1 hour
            },
            "technical_indicators": {
                "rsi_period": 14,
                "macd_fast": 12,
                "macd_slow": 26,
                "macd_signal": 9,
                "bb_period": 20,
                "bb_std": 2.0,
                "stoch_k": 14,
                "stoch_d": 3,
                "atr_period": 14,
                "adx_period": 14
            },
            "websocket": {
                "binance_url": "wss://stream.binance.com:9443/ws/",
                "reconnect_interval": 5
            },
            "api": {
                "base_url": "http://localhost:8001",
                "timeout": 10
            }
        }
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            
        return default_config
    
    def _save_config(self):
        """Save configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    async def start(self):
        """Start the advanced auto trading engine"""
        if self.is_running:
            logger.warning("Auto trading engine already running")
            return
            
        logger.info("🚀 Starting Advanced Auto Trading Engine...")
        
        self.is_running = True
        
        try:
            # Start all async tasks
            self.data_feed_task = asyncio.create_task(self._data_feed_loop())
            await asyncio.sleep(2)  # Allow data feed to initialize
            
            self.ai_signal_task = asyncio.create_task(self._ai_signal_loop())
            await asyncio.sleep(1)
            
            self.risk_monitor_task = asyncio.create_task(self._risk_monitor_loop())
            await asyncio.sleep(1)
            
            self.trading_loop_task = asyncio.create_task(self._main_trading_loop())
            
            logger.info("✅ Advanced Auto Trading Engine fully operational")
            
        except Exception as e:
            logger.error(f"Error starting auto trading engine: {e}")
            await self.stop()
            raise
    
    async def stop(self):
        """Stop the advanced auto trading engine"""
        logger.info("🛑 Stopping Advanced Auto Trading Engine...")
        
        self.is_running = False
        
        # Cancel all tasks
        tasks = [self.trading_loop_task, self.data_feed_task, 
                self.ai_signal_task, self.risk_monitor_task]
        
        for task in tasks:
            if task and not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        
        # Close all positions if enabled
        if self.config.get("close_positions_on_stop", True):
            await self._close_all_positions()
        
        logger.info("✅ Advanced Auto Trading Engine stopped")
    
    async def _data_feed_loop(self):
        """Real-time data feed loop with WebSocket integration"""
        logger.info("📡 Starting real-time data feed...")
        
        while self.is_running:
            try:
                # Get real-time price data
                for symbol in self.config["symbols"]:
                    market_data = await self._fetch_market_data(symbol)
                    if market_data:
                        self.market_data[symbol] = market_data
                        
                        # Calculate technical indicators
                        indicators = await self._calculate_indicators(symbol)
                        if indicators:
                            self.indicators[symbol] = indicators
                
                await asyncio.sleep(1)  # Update every second
                
            except Exception as e:
                logger.error(f"Error in data feed loop: {e}")
                await asyncio.sleep(5)
    
    async def _ai_signal_loop(self):
        """AI/ML signal generation loop"""
        logger.info("🧠 Starting AI signal generation...")
        
        while self.is_running:
            try:
                if self.config["ai_models"]["enabled"]:
                    for symbol in self.config["symbols"]:
                        if symbol in self.market_data and symbol in self.indicators:
                            signal = await self._generate_ai_signal(symbol)
                            if signal and signal.confidence >= self.config["min_confidence"]:
                                await self.events.put(("AI_SIGNAL", signal))
                
                await asyncio.sleep(30)  # Generate signals every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in AI signal loop: {e}")
                await asyncio.sleep(60)
    
    async def _risk_monitor_loop(self):
        """Risk monitoring and management loop"""
        logger.info("⚠️ Starting risk monitor...")
        
        while self.is_running:
            try:
                # Update position P&L
                await self._update_position_pnl()
                
                # Check stop losses and take profits
                await self._check_exit_conditions()
                
                # Monitor portfolio risk
                await self._monitor_portfolio_risk()
                
                await asyncio.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                logger.error(f"Error in risk monitor: {e}")
                await asyncio.sleep(10)
    
    async def _main_trading_loop(self):
        """Main trading decision and execution loop"""
        logger.info("💹 Starting main trading loop...")
        
        while self.is_running:
            try:
                # Process events
                while not self.events.empty():
                    event_type, data = await self.events.get()
                    
                    if event_type == "AI_SIGNAL":
                        await self._process_ai_signal(data)
                    elif event_type == "MARKET_UPDATE":
                        await self._process_market_update(data)
                    elif event_type == "RISK_ALERT":
                        await self._process_risk_alert(data)
                
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error in main trading loop: {e}")
                await asyncio.sleep(5)
    
    async def _fetch_market_data(self, symbol: str) -> Optional[MarketData]:
        """Fetch real-time market data"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.config['api']['base_url']}/price/{symbol.lower()}"
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return MarketData(
                            symbol=symbol,
                            price=float(data.get("price", 0)),
                            volume=float(data.get("volume", 0)),
                            timestamp=datetime.now(),
                            bid=float(data.get("bid", 0)),
                            ask=float(data.get("ask", 0))
                        )
        except Exception as e:
            logger.error(f"Error fetching market data for {symbol}: {e}")
        return None
    
    async def _calculate_indicators(self, symbol: str) -> Optional[TechnicalIndicators]:
        """Calculate technical indicators for symbol"""
        try:
            # Get historical data for indicator calculation
            async with aiohttp.ClientSession() as session:
                url = f"{self.config['api']['base_url']}/features/indicators"
                params = {"symbol": symbol.lower(), "limit": 100}
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Extract indicator values
                        return TechnicalIndicators(
                            rsi=float(data.get("rsi", 50)),
                            macd=float(data.get("macd", 0)),
                            macd_signal=float(data.get("macd_signal", 0)),
                            macd_histogram=float(data.get("macd_histogram", 0)),
                            bb_upper=float(data.get("bb_upper", 0)),
                            bb_middle=float(data.get("bb_middle", 0)),
                            bb_lower=float(data.get("bb_lower", 0)),
                            stoch_k=float(data.get("stoch_k", 50)),
                            stoch_d=float(data.get("stoch_d", 50)),
                            williams_r=float(data.get("williams_r", -50)),
                            atr=float(data.get("atr", 0)),
                            adx=float(data.get("adx", 25)),
                            cci=float(data.get("cci", 0)),
                            sma_20=float(data.get("sma_20", 0)),
                            ema_20=float(data.get("ema_20", 0)),
                            volume_sma=float(data.get("volume_sma", 0)),
                            obv=float(data.get("obv", 0))
                        )
        except Exception as e:
            logger.error(f"Error calculating indicators for {symbol}: {e}")
        return None
    
    async def _generate_ai_signal(self, symbol: str) -> Optional[AISignal]:
        """Generate AI/ML trading signal"""
        try:
            market_data = self.market_data[symbol]
            indicators = self.indicators[symbol]
            
            # Prepare feature vector
            features = {
                "price": market_data.price,
                "volume": market_data.volume,
                "rsi": indicators.rsi,
                "macd": indicators.macd,
                "macd_signal": indicators.macd_signal,
                "bb_position": (market_data.price - indicators.bb_lower) / (indicators.bb_upper - indicators.bb_lower),
                "stoch_k": indicators.stoch_k,
                "stoch_d": indicators.stoch_d,
                "williams_r": indicators.williams_r,
                "atr": indicators.atr,
                "adx": indicators.adx,
                "cci": indicators.cci
            }
            
            # Get ML prediction
            async with aiohttp.ClientSession() as session:
                url = f"{self.config['api']['base_url']}/ml/predict/enhanced"
                params = {
                    "symbol": symbol.lower(),
                    "features": json.dumps(features),
                    "timeframes": ",".join(self.config["timeframes"]),
                    "include_confidence": True
                }
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=15)) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        signal_str = result.get("primary_signal", "HOLD")
                        confidence = float(result.get("primary_confidence", 0))
                        
                        # Convert string to enum
                        signal = TradingSignal.HOLD
                        if signal_str == "BUY":
                            signal = TradingSignal.BUY
                        elif signal_str == "SELL":
                            signal = TradingSignal.SELL
                        
                        # Calculate risk score based on indicators
                        risk_score = self._calculate_risk_score(indicators, market_data)
                        
                        ai_signal = AISignal(
                            signal=signal,
                            confidence=confidence,
                            timeframe=self.config["primary_timeframe"],
                            indicators_used=list(features.keys()),
                            model_version=result.get("model_version", "unknown"),
                            prediction_horizon=result.get("prediction_horizon", "short"),
                            risk_score=risk_score
                        )
                        
                        self.signal_history.append(ai_signal)
                        if len(self.signal_history) > 100:
                            self.signal_history = self.signal_history[-100:]
                        
                        return ai_signal
                        
        except Exception as e:
            logger.error(f"Error generating AI signal for {symbol}: {e}")
        return None
    
    def _calculate_risk_score(self, indicators: TechnicalIndicators, market_data: MarketData) -> float:
        """Calculate risk score based on market conditions"""
        try:
            risk_factors = []
            
            # Volatility risk (ATR-based)
            if indicators.atr > 0:
                volatility_risk = indicators.atr / market_data.price
                risk_factors.append(min(volatility_risk * 10, 1.0))
            
            # Trend strength risk (ADX-based)
            trend_risk = max(0, (50 - indicators.adx) / 50)  # Higher risk when trend is weak
            risk_factors.append(trend_risk)
            
            # Momentum risk (RSI-based)
            rsi_extreme = abs(indicators.rsi - 50) / 50
            momentum_risk = max(0, rsi_extreme - 0.6)  # Risk when RSI is extreme
            risk_factors.append(momentum_risk)
            
            # Calculate average risk score (0-1, where 1 = highest risk)
            avg_risk = np.mean(risk_factors) if risk_factors else 0.5
            return float(np.clip(avg_risk, 0.0, 1.0))
            
        except Exception as e:
            logger.error(f"Error calculating risk score: {e}")
            return 0.5
    
    async def _process_ai_signal(self, signal: AISignal):
        """Process AI signal and make trading decision"""
        try:
            symbol = self.config["primary_symbol"]
            
            # Check if we can open new position
            if len(self.positions) >= self.config["max_positions"]:
                logger.info(f"Max positions reached ({self.config['max_positions']}), skipping signal")
                return
            
            # Check signal confidence
            if signal.confidence < self.config["min_confidence"]:
                logger.info(f"Signal confidence {signal.confidence:.2%} below threshold {self.config['min_confidence']:.2%}")
                return
            
            # Check risk score
            if signal.risk_score > 0.8:
                logger.info(f"Risk score too high: {signal.risk_score:.2f}")
                return
            
            # Calculate position size
            position_size = self._calculate_position_size(signal)
            
            if position_size > 0:
                await self._open_position(symbol, signal, position_size)
                
        except Exception as e:
            logger.error(f"Error processing AI signal: {e}")
    
    def _calculate_position_size(self, signal: AISignal) -> float:
        """Calculate optimal position size based on risk management"""
        try:
            method = self.config["position_sizing"]["method"]
            balance = self.config["balance"]
            risk_per_trade = self.config["risk_per_trade"] / 100
            
            if method == "fixed_risk":
                # Fixed risk per trade
                risk_amount = balance * risk_per_trade
                
                # Adjust based on confidence and risk score
                confidence_multiplier = signal.confidence
                risk_multiplier = 1.0 - (signal.risk_score * 0.5)
                
                position_size = risk_amount * confidence_multiplier * risk_multiplier
                
            elif method == "kelly":
                # Kelly criterion (simplified)
                win_rate = self.win_rate if self.trades_executed > 10 else 0.6
                avg_win = 1.04  # Assuming 4% average win
                avg_loss = 0.98  # Assuming 2% average loss
                
                kelly_fraction = (win_rate * avg_win - (1 - win_rate) * avg_loss) / avg_win
                kelly_fraction = max(0, min(kelly_fraction, 0.25))  # Cap at 25%
                
                position_size = balance * kelly_fraction * signal.confidence
                
            else:
                # Default fixed amount
                position_size = self.config["position_sizing"]["base_amount"]
            
            # Apply limits
            max_size = self.config["position_sizing"]["max_position_size"]
            position_size = min(position_size, max_size)
            
            # Minimum viable position
            min_size = 10.0
            return position_size if position_size >= min_size else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating position size: {e}")
            return 0.0
    
    async def _open_position(self, symbol: str, signal: AISignal, size: float):
        """Open a new trading position"""
        try:
            market_data = self.market_data[symbol]
            
            # Calculate stop loss and take profit
            if signal.signal == TradingSignal.BUY:
                entry_price = market_data.price
                stop_loss = entry_price * (1 - self.config["stop_loss_pct"] / 100)
                take_profit = entry_price * (1 + self.config["take_profit_pct"] / 100)
            else:
                entry_price = market_data.price
                stop_loss = entry_price * (1 + self.config["stop_loss_pct"] / 100)
                take_profit = entry_price * (1 - self.config["take_profit_pct"] / 100)
            
            # Create position
            position_id = f"{symbol}_{signal.signal.value}_{int(time.time())}"
            position = Position(
                id=position_id,
                symbol=symbol,
                side=signal.signal,
                size=size,
                entry_price=entry_price,
                current_price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                pnl=0.0,
                unrealized_pnl=0.0,
                status=PositionStatus.OPEN,
                opened_at=datetime.now()
            )
            
            self.positions[position_id] = position
            self.trades_executed += 1
            
            logger.info(f"🎯 Opened {signal.signal.value} position: {symbol} @ ${entry_price:.4f}, Size: ${size:.2f}, Confidence: {signal.confidence:.2%}")
            
            # Save to backend
            await self._save_position_to_backend(position)
            
        except Exception as e:
            logger.error(f"Error opening position: {e}")
    
    async def _process_market_update(self, market_data: Dict):
        """Process market update and monitor positions"""
        try:
            symbol = market_data.get("symbol")
            price = float(market_data.get("price", 0))
            
            if not symbol or not price:
                return
            
            # Update market data
            if symbol in self.market_data:
                self.market_data[symbol].price = price
                self.market_data[symbol].timestamp = datetime.now()
            
            # Check for stop loss / take profit triggers
            for position_id, position in list(self.positions.items()):
                if position.symbol == symbol and position.status == PositionStatus.OPEN:
                    position.current_price = price
                    
                    # Check stop loss
                    if position.side == TradingSignal.BUY and price <= position.stop_loss:
                        await self._close_position(position.id, "Stop Loss Hit")
                    elif position.side == TradingSignal.SELL and price >= position.stop_loss:
                        await self._close_position(position.id, "Stop Loss Hit")
                    
                    # Check take profit
                    elif position.side == TradingSignal.BUY and price >= position.take_profit:
                        await self._close_position(position.id, "Take Profit Hit")
                    elif position.side == TradingSignal.SELL and price <= position.take_profit:
                        await self._close_position(position.id, "Take Profit Hit")
            
        except Exception as e:
            logger.error(f"Error processing market update: {e}")
    
    async def _update_position_pnl(self):
        """Update P&L for all open positions"""
        try:
            total_unrealized = 0.0
            
            for position in self.positions.values():
                if position.status == PositionStatus.OPEN:
                    market_data = self.market_data.get(position.symbol)
                    if market_data:
                        position.current_price = market_data.price
                        
                        # Calculate unrealized P&L
                        if position.side == TradingSignal.BUY:
                            position.unrealized_pnl = (position.current_price - position.entry_price) * position.size / position.entry_price
                        else:
                            position.unrealized_pnl = (position.entry_price - position.current_price) * position.size / position.entry_price
                        
                        total_unrealized += position.unrealized_pnl
            
            # Update total P&L
            realized_pnl = sum(p.pnl for p in self.positions.values() if p.status == PositionStatus.CLOSED)
            self.total_pnl = realized_pnl + total_unrealized
            
        except Exception as e:
            logger.error(f"Error updating position P&L: {e}")
    
    async def _check_exit_conditions(self):
        """Check stop loss and take profit conditions"""
        try:
            for position in list(self.positions.values()):
                if position.status == PositionStatus.OPEN:
                    should_close = False
                    close_reason = ""
                    
                    if position.side == TradingSignal.BUY:
                        if position.current_price <= position.stop_loss:
                            should_close = True
                            close_reason = "Stop Loss"
                        elif position.current_price >= position.take_profit:
                            should_close = True
                            close_reason = "Take Profit"
                    else:
                        if position.current_price >= position.stop_loss:
                            should_close = True
                            close_reason = "Stop Loss"
                        elif position.current_price <= position.take_profit:
                            should_close = True
                            close_reason = "Take Profit"
                    
                    if should_close:
                        await self._close_position(position.id, close_reason)
                        
        except Exception as e:
            logger.error(f"Error checking exit conditions: {e}")
    
    async def _close_position(self, position_id: str, reason: str = "Manual"):
        """Close a trading position"""
        try:
            position = self.positions.get(position_id)
            if not position or position.status != PositionStatus.OPEN:
                return
            
            # Calculate final P&L
            if position.side == TradingSignal.BUY:
                position.pnl = (position.current_price - position.entry_price) * position.size / position.entry_price
            else:
                position.pnl = (position.entry_price - position.current_price) * position.size / position.entry_price
            
            position.status = PositionStatus.CLOSED
            position.closed_at = datetime.now()
            position.unrealized_pnl = 0.0
            
            # Update statistics
            if position.pnl > 0:
                winning_trades = sum(1 for p in self.positions.values() if p.status == PositionStatus.CLOSED and p.pnl > 0)
            else:
                winning_trades = sum(1 for p in self.positions.values() if p.status == PositionStatus.CLOSED and p.pnl > 0)
            
            closed_trades = sum(1 for p in self.positions.values() if p.status == PositionStatus.CLOSED)
            self.win_rate = winning_trades / closed_trades if closed_trades > 0 else 0.0
            
            logger.info(f"🏁 Closed {position.side.value} position: {position.symbol} @ ${position.current_price:.4f}, P&L: ${position.pnl:.2f} ({reason})")
            
            # Save to backend
            await self._save_position_to_backend(position)
            
        except Exception as e:
            logger.error(f"Error closing position: {e}")
    
    async def _monitor_portfolio_risk(self):
        """Monitor overall portfolio risk"""
        try:
            # Calculate total exposure
            total_exposure = sum(p.size for p in self.positions.values() if p.status == PositionStatus.OPEN)
            max_exposure = self.config["balance"] * 0.5  # 50% max exposure
            
            if total_exposure > max_exposure:
                await self.events.put(("RISK_ALERT", {"type": "HIGH_EXPOSURE", "exposure": total_exposure}))
            
            # Check drawdown
            if self.total_pnl < 0:
                drawdown_pct = abs(self.total_pnl) / self.config["balance"] * 100
                if drawdown_pct > 10:  # 10% drawdown alert
                    await self.events.put(("RISK_ALERT", {"type": "HIGH_DRAWDOWN", "drawdown": drawdown_pct}))
                    
        except Exception as e:
            logger.error(f"Error monitoring portfolio risk: {e}")
    
    async def _process_risk_alert(self, alert_data: Dict):
        """Process risk management alerts"""
        try:
            alert_type = alert_data.get("type")
            
            if alert_type == "HIGH_EXPOSURE":
                # Close least profitable position
                open_positions = [p for p in self.positions.values() if p.status == PositionStatus.OPEN]
                if open_positions:
                    worst_position = min(open_positions, key=lambda p: p.unrealized_pnl)
                    await self._close_position(worst_position.id, "Risk Management - High Exposure")
            
            elif alert_type == "HIGH_DRAWDOWN":
                # Close all positions
                await self._close_all_positions()
                # Temporarily disable trading
                self.config["enabled"] = False
                logger.warning("⚠️ Auto trading disabled due to high drawdown")
                
        except Exception as e:
            logger.error(f"Error processing risk alert: {e}")
    
    async def _close_all_positions(self):
        """Close all open positions"""
        try:
            open_positions = [p for p in self.positions.values() if p.status == PositionStatus.OPEN]
            for position in open_positions:
                await self._close_position(position.id, "System Stop")
                
        except Exception as e:
            logger.error(f"Error closing all positions: {e}")
    
    async def _save_position_to_backend(self, position: Position):
        """Save position to backend for dashboard display"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.config['api']['base_url']}/auto_trading/positions"
                data = asdict(position)
                # Convert datetime objects to strings
                data["opened_at"] = position.opened_at.isoformat()
                if position.closed_at:
                    data["closed_at"] = position.closed_at.isoformat()
                
                async with session.post(url, json=data, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        logger.debug(f"Position saved to backend: {position.id}")
                        
        except Exception as e:
            logger.debug(f"Error saving position to backend: {e}")
    
    # API methods for dashboard integration
    async def get_status(self) -> Dict:
        """Get current auto trading status"""
        open_positions = [p for p in self.positions.values() if p.status == PositionStatus.OPEN]
        closed_positions = [p for p in self.positions.values() if p.status == PositionStatus.CLOSED]
        
        return {
            "enabled": self.config["enabled"],
            "is_running": self.is_running,
            "balance": self.config["balance"],
            "total_pnl": self.total_pnl,
            "open_positions": len(open_positions),
            "total_trades": self.trades_executed,
            "win_rate": self.win_rate * 100,
            "max_drawdown": self.max_drawdown,
            "current_signals": len(self.signal_history),
            "primary_symbol": self.config["primary_symbol"],
            "risk_per_trade": self.config["risk_per_trade"]
        }
    
    async def get_positions(self) -> List[Dict]:
        """Get all positions"""
        positions_data = []
        for position in self.positions.values():
            pos_data = asdict(position)
            pos_data["opened_at"] = position.opened_at.isoformat()
            if position.closed_at:
                pos_data["closed_at"] = position.closed_at.isoformat()
            positions_data.append(pos_data)
        return positions_data
    
    async def get_recent_signals(self) -> List[Dict]:
        """Get recent AI signals"""
        return [asdict(signal) for signal in self.signal_history[-20:]]
    
    async def get_prediction(self, symbol: str) -> Dict:
        """Get AI prediction for a specific symbol"""
        try:
            # Ensure we have market data and indicators
            if symbol not in self.market_data or symbol not in self.indicators:
                return {"direction": "NO_MODEL", "confidence": 0.0}
            
            # Generate AI signal for the symbol
            signal = await self._generate_ai_signal(symbol)
            if signal:
                return {
                    "direction": signal.signal.value,
                    "confidence": signal.confidence,
                    "timeframe": signal.timeframe,
                    "model_version": signal.model_version,
                    "risk_score": signal.risk_score
                }
            
            return {"direction": "HOLD", "confidence": 0.5}
            
        except Exception as e:
            logger.error(f"Error getting prediction for {symbol}: {e}")
            return {"direction": "ERROR", "confidence": 0.0}
    
    async def get_enhanced_prediction(self, symbol: str, timeframe: str = "5m") -> Dict:
        """Get enhanced AI prediction with multi-timeframe analysis"""
        try:
            predictions = {}
            
            # Get predictions for different timeframes
            timeframes = ["1m", "5m", "15m", "1h"]
            for tf in timeframes:
                pred = await self.get_prediction(symbol)
                predictions[tf] = pred
            
            # Calculate ensemble prediction
            total_confidence = sum(p["confidence"] for p in predictions.values())
            if total_confidence > 0:
                weighted_signal = max(predictions.values(), key=lambda x: x["confidence"])
                
                return {
                    "symbol": symbol,
                    "primary_signal": weighted_signal["direction"],
                    "confidence": weighted_signal["confidence"],
                    "timeframe_analysis": predictions,
                    "ensemble_confidence": total_confidence / len(timeframes),
                    "recommendation": "STRONG_" + weighted_signal["direction"] if weighted_signal["confidence"] > 0.8 else weighted_signal["direction"]
                }
            
            return {
                "symbol": symbol,
                "primary_signal": "HOLD",
                "confidence": 0.5,
                "timeframe_analysis": predictions,
                "ensemble_confidence": 0.5,
                "recommendation": "HOLD"
            }
            
        except Exception as e:
            logger.error(f"Error getting enhanced prediction for {symbol}: {e}")
            return {
                "symbol": symbol,
                "primary_signal": "ERROR",
                "confidence": 0.0,
                "error": str(e)
            }
    
    async def get_current_signal(self) -> Optional[Dict]:
        """Get the most recent AI signal"""
        try:
            if not self.signal_history:
                return None
            
            latest_signal = self.signal_history[-1]
            return {
                "signal": latest_signal.signal.value,
                "confidence": latest_signal.confidence,
                "timeframe": latest_signal.timeframe,
                "timestamp": datetime.now().isoformat(),
                "model_version": latest_signal.model_version,
                "risk_score": latest_signal.risk_score
            }
            
        except Exception as e:
            logger.error(f"Error getting current signal: {e}")
            return None
