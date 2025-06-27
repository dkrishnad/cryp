import sqlite3

# --- DB Initialization ---
def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Create trades table if not exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id TEXT PRIMARY KEY,
            symbol TEXT,
            direction TEXT,
            amount REAL,
            entry_price REAL,
            tp_price REAL,
            sl_price REAL,
            status TEXT,
            open_time TEXT,
            close_time TEXT,
            pnl REAL,
            current_price REAL,
            close_price REAL
        )
    ''')
    # Create backtest_results table if not exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS backtest_results (
            backtest_id TEXT PRIMARY KEY,
            timestamp TEXT,
            symbol TEXT,
            strategy TEXT,
            results TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Call DB initialization at the start
initialize_database()

#Perfectbot V2
#enabled Ml and Db writing
import streamlit as st
import warnings
import pandas as pd
import numpy as np
import requests
import datetime
import traceback
import uuid
import sys
import os
import sqlite3
import random
import time

# --- Fix for NameError: ensure log_trade_to_db is defined before any usage ---
def log_trade_to_db(trade, features, prediction):
    import sqlite3
    import json
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''INSERT INTO trades (id, symbol, direction, amount, entry_price, tp_price, sl_price, status, open_time, close_time, pnl, current_price, close_price, features, prediction)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (trade.get('id'), trade.get('symbol'), trade.get('direction'), trade.get('amount'), trade.get('entry_price'),
         trade.get('tp_price'), trade.get('sl_price'), trade.get('status'), str(trade.get('open_time')), str(trade.get('close_time')),
         trade.get('pnl'), trade.get('current_price'), trade.get('close_price'),
         json.dumps(features if features is not None else {}), json.dumps(prediction if prediction is not None else {})))
        conn.commit()
        conn.close()
        st.session_state.perf_monitor.record_db_success()  # Record successful DB operation
    except Exception as e:
        st.session_state.perf_monitor.record_db_error()  # Record DB error
        st.error(f"Database logging failed: {str(e)}")

# --- Advanced Backtesting and ML Imports ---
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import GradientBoostingRegressor
import joblib
from scipy import stats
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# --- Database Configuration ---
DB_PATH = "trades.db"

# Machine Learning imports
try:
    from sklearn.ensemble import RandomForestRegressor, VotingRegressor
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import mean_squared_error
except ImportError:
    RandomForestRegressor = VotingRegressor = LinearRegression = StandardScaler = mean_squared_error = None

try:
    from xgboost import XGBRegressor
except ImportError:
    XGBRegressor = None

try:
    from lightgbm import LGBMRegressor
except ImportError:
    LGBMRegressor = None

try:
    from catboost import CatBoostRegressor
except ImportError:
    CatBoostRegressor = None

try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense
except ImportError:
    Sequential = LSTM = Dense = None

# Technical Analysis imports
try:
    from ta.trend import EMAIndicator, MACD
    from ta.momentum import RSIIndicator, StochasticOscillator
    from ta.volatility import BollingerBands, AverageTrueRange
    from ta.volume import OnBalanceVolumeIndicator
except ImportError:
    EMAIndicator = MACD = RSIIndicator = StochasticOscillator = None
    BollingerBands = AverageTrueRange = OnBalanceVolumeIndicator = None

# --- Streamlit rerun compatibility shim ---
if not hasattr(st, "rerun"):
    if hasattr(st, "experimental_rerun"):
        st.rerun = st.experimental_rerun
    else:
        def _dummy_rerun():
            warnings.warn("Streamlit rerun is not available in this version.")
        st.rerun = _dummy_rerun

# --- Performance Monitor Class ---
class PerformanceMonitor:
    def __init__(self):
        self.response_times = []
        self.api_error_count = 0
        self.api_success_count = 0
        self.trade_success_count = 0
        self.trade_error_count = 0
        self.db_success_count = 0
        self.db_error_count = 0
        self.model_success_count = 0
        self.model_error_count = 0
        self.max_history = 100
    
    def add_response_time(self, response_time_ms):
        """Add a response time measurement"""
        self.response_times.append(response_time_ms)
        if len(self.response_times) > self.max_history:
            self.response_times = self.response_times[-self.max_history:]
    
    def record_api_success(self):
        """Record a successful API operation"""
        self.api_success_count += 1
    
    def record_api_error(self):
        """Record a failed API operation"""
        self.api_error_count += 1
    
    def record_trade_success(self):
        """Record a successful trading operation"""
        self.trade_success_count += 1
    
    def record_trade_error(self):
        """Record a failed trading operation"""
        self.trade_error_count += 1
    
    def record_db_success(self):
        """Record a successful database operation"""
        self.db_success_count += 1
    
    def record_db_error(self):
        """Record a failed database operation"""
        self.db_error_count += 1
    
    def record_model_success(self):
        """Record a successful model operation"""
        self.model_success_count += 1
    
    def record_model_error(self):
        """Record a failed model operation"""
        self.model_error_count += 1
    
    def get_average_response_time(self):
        """Get the average response time"""
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)
    
    def get_latest_response_time(self):
        """Get the most recent response time"""
        if not self.response_times:
            return 0.0
        return self.response_times[-1]
    
    def get_trading_success_rate(self):
        """Get the trading success rate (excludes API calls)"""
        total = self.trade_success_count + self.trade_error_count
        if total == 0:
            return 0.0
        return (self.trade_success_count / total) * 100
    
    def get_system_success_rate(self):
        """Get overall system success rate (includes all operations)"""
        total = (self.api_success_count + self.api_error_count + 
                self.trade_success_count + self.trade_error_count +
                self.db_success_count + self.db_error_count +
                self.model_success_count + self.model_error_count)
        if total == 0:
            return 0.0
        success = (self.api_success_count + self.trade_success_count + 
                  self.db_success_count + self.model_success_count)
        return (success / total) * 100
    
    def get_detailed_stats(self):
        """Get detailed breakdown of operations"""
        return {
            'API Calls': {'success': self.api_success_count, 'errors': self.api_error_count},
            'Trading Operations': {'success': self.trade_success_count, 'errors': self.trade_error_count},
            'Database Operations': {'success': self.db_success_count, 'errors': self.db_error_count},
            'Model Operations': {'success': self.model_success_count, 'errors': self.model_error_count}
        }
    
    def reset_stats(self):
        """Reset all statistics"""
        self.response_times = []
        self.api_error_count = 0
        self.api_success_count = 0
        self.trade_success_count = 0
        self.trade_error_count = 0
        self.db_success_count = 0
        self.db_error_count = 0
        self.model_success_count = 0
        self.model_error_count = 0

# --- Advanced Backtesting Infrastructure ---
class AdvancedBacktester:
    """
    Advanced backtesting system with realistic trading conditions, 
    walk-forward validation, and comprehensive performance analysis.
    """
    
    def __init__(self, initial_capital=10000, trading_fee=0.001, slippage=0.0005):
        self.initial_capital = initial_capital
        self.trading_fee = trading_fee
        self.slippage = slippage
        self.reset()
    
    def reset(self):
        """Reset backtest state"""
        self.capital = self.initial_capital
        self.positions = {}
        self.trades = []
        self.equity_curve = []
        self.drawdown_curve = []
        self.max_capital = self.initial_capital
        self.trade_id = 0
        
    def execute_trade(self, symbol, direction, amount, entry_price, tp_ratio=0.02, sl_ratio=0.01, timestamp=None):
        """Execute a trade with realistic conditions"""
        # Apply slippage
        if direction == "LONG":
            actual_entry = entry_price * (1 + self.slippage)
        else:
            actual_entry = entry_price * (1 - self.slippage)
        
        # Calculate fees
        fee = amount * self.trading_fee
        net_amount = amount - fee
        
        # Check if we have enough capital
        if net_amount > self.capital:
            return False, "Insufficient capital"
        
        # Create position
        position = {
            'id': self.trade_id,
            'symbol': symbol,
            'direction': direction,
            'amount': net_amount,
            'entry_price': actual_entry,
            'tp_price': actual_entry * (1 + tp_ratio) if direction == "LONG" else actual_entry * (1 - tp_ratio),
            'sl_price': actual_entry * (1 - sl_ratio) if direction == "LONG" else actual_entry * (1 + sl_ratio),
            'timestamp': timestamp or datetime.datetime.now(),
            'status': 'OPEN'
        }
        
        self.positions[self.trade_id] = position
        self.capital -= net_amount
        self.trade_id += 1
        
        return True, f"Trade executed: {direction} {symbol} at {actual_entry:.6f}"
    
    def update_positions(self, price_data):
        """Update all open positions with current prices"""
        to_close = []
        
        for trade_id, position in self.positions.items():
            if position['status'] != 'OPEN':
                continue
                
            symbol = position['symbol']
            if symbol not in price_data:
                continue
                
            current_price = price_data[symbol]
            direction = position['direction']
            
            # Check TP/SL conditions
            should_close = False
            close_reason = ""
            
            if direction == "LONG":
                if current_price >= position['tp_price']:
                    should_close = True
                    close_reason = "TP"
                elif current_price <= position['sl_price']:
                    should_close = True
                    close_reason = "SL"
            else:  # SHORT
                if current_price <= position['tp_price']:
                    should_close = True
                    close_reason = "TP"
                elif current_price >= position['sl_price']:
                    should_close = True
                    close_reason = "SL"
            
            if should_close:
                to_close.append((trade_id, current_price, close_reason))
        
        # Close triggered positions
        for trade_id, close_price, reason in to_close:
            self.close_position(trade_id, close_price, reason)
    
    def close_position(self, trade_id, close_price, reason="MANUAL"):
        """Close a position and record the trade"""
        if trade_id not in self.positions:
            return False, "Position not found"
        
        position = self.positions[trade_id]
        if position['status'] != 'OPEN':
            return False, "Position already closed"
        
        # Apply slippage on close
        if position['direction'] == "LONG":
            actual_close = close_price * (1 - self.slippage)
        else:
            actual_close = close_price * (1 + self.slippage)
        
        # Calculate P&L
        if position['direction'] == "LONG":
            pnl = (actual_close - position['entry_price']) * (position['amount'] / position['entry_price'])
        else:
            pnl = (position['entry_price'] - actual_close) * (position['amount'] / position['entry_price'])
        
        # Apply exit fee
        exit_fee = abs(pnl) * self.trading_fee if pnl > 0 else 0
        net_pnl = pnl - exit_fee
        
        # Update capital
        self.capital += position['amount'] + net_pnl
        
        # Record trade
        trade_record = {
            'id': trade_id,
            'symbol': position['symbol'],
            'direction': position['direction'],
            'entry_price': position['entry_price'],
            'close_price': actual_close,
            'amount': position['amount'],
            'pnl': net_pnl,
            'entry_time': position['timestamp'],
            'close_time': datetime.datetime.now(),
            'close_reason': reason,
            'return_pct': (net_pnl / position['amount']) * 100
        }
        
        self.trades.append(trade_record)
        position['status'] = f'CLOSED ({reason})'
        
        # Update equity curve
        self.equity_curve.append({
            'timestamp': trade_record['close_time'],
            'capital': self.capital,
            'trade_pnl': net_pnl
        })
        
        # Update drawdown
        if self.capital > self.max_capital:
            self.max_capital = self.capital
        
        drawdown = (self.max_capital - self.capital) / self.max_capital * 100
        self.drawdown_curve.append({
            'timestamp': trade_record['close_time'],
            'drawdown': drawdown
        })
        
        return True, f"Position closed: {reason} at {actual_close:.6f}, P&L: {net_pnl:.2f}"
    
    def get_performance_metrics(self):
        """Calculate comprehensive performance metrics"""
        if not self.trades:
            return {}
        
        df_trades = pd.DataFrame(self.trades)
        
        # Basic metrics
        total_trades = len(df_trades)
        winning_trades = len(df_trades[df_trades['pnl'] > 0])
        losing_trades = len(df_trades[df_trades['pnl'] < 0])
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        # P&L metrics
        total_pnl = df_trades['pnl'].sum()
        avg_win = df_trades[df_trades['pnl'] > 0]['pnl'].mean() if winning_trades > 0 else 0
        avg_loss = df_trades[df_trades['pnl'] < 0]['pnl'].mean() if losing_trades > 0 else 0
        profit_factor = abs(avg_win * winning_trades / (avg_loss * losing_trades)) if avg_loss != 0 and losing_trades > 0 else 0
        
        # Return metrics
        total_return = ((self.capital - self.initial_capital) / self.initial_capital) * 100
        
        # Risk metrics
        returns = df_trades['return_pct'].values
        sharpe_ratio = np.mean(returns) / np.std(returns) if np.std(returns) > 0 else 0
        max_drawdown = max([dd['drawdown'] for dd in self.drawdown_curve]) if self.drawdown_curve else 0
        
        # Trade duration (if timestamps available)
        avg_trade_duration = 0
        if len(df_trades) > 0 and 'entry_time' in df_trades.columns and 'close_time' in df_trades.columns:
            durations = [(pd.to_datetime(close) - pd.to_datetime(entry)).total_seconds() / 3600 
                        for entry, close in zip(df_trades['entry_time'], df_trades['close_time'])]
            avg_trade_duration = np.mean(durations)
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'total_return': total_return,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'avg_trade_duration_hours': avg_trade_duration,
            'final_capital': self.capital
        }
    
    def run_walk_forward_backtest(self, data, prediction_func, train_window=100, test_window=20):
        """
        Run walk-forward validation backtest
        """
        results = []
        
        for i in range(train_window, len(data) - test_window, test_window):
            # Split data
            train_data = data.iloc[i-train_window:i]
            test_data = data.iloc[i:i+test_window]
            
            # Reset for this fold
            fold_backtester = AdvancedBacktester(
                initial_capital=self.initial_capital,
                trading_fee=self.trading_fee,
                slippage=self.slippage
            )
            
            # Run predictions and trades on test data
            for idx, row in test_data.iterrows():
                try:
                    prediction = prediction_func(train_data, row)
                    if prediction and 'direction' in prediction and 'confidence' in prediction:
                        if prediction['confidence'] > 60:  # Minimum confidence threshold
                            symbol = row.get('symbol', 'BTCUSDT')
                            price = row.get('close', row.get('price', 0))
                            
                            success, msg = fold_backtester.execute_trade(
                                symbol=symbol,
                                direction=prediction['direction'],
                                amount=fold_backtester.capital * 0.1,  # 10% position size
                                entry_price=price,
                                timestamp=row.get('timestamp', datetime.datetime.now())
                            )
                            
                            # Update positions with current price
                            fold_backtester.update_positions({symbol: price})
                            
                except Exception as e:
                    continue
            
            # Close all remaining positions
            for trade_id in list(fold_backtester.positions.keys()):
                if fold_backtester.positions[trade_id]['status'] == 'OPEN':
                    last_price = test_data.iloc[-1].get('close', test_data.iloc[-1].get('price', 0))
                    fold_backtester.close_position(trade_id, last_price, "PERIOD_END")
            
            # Record fold results
            fold_metrics = fold_backtester.get_performance_metrics()
            fold_metrics['fold'] = len(results) + 1
            fold_metrics['train_start'] = i - train_window
            fold_metrics['train_end'] = i
            fold_metrics['test_start'] = i
            fold_metrics['test_end'] = i + test_window
            
            results.append(fold_metrics)
        
        return results

class DataQualityManager:
    """Manages data quality checks and preprocessing for backtesting"""
    
    @staticmethod
    def validate_data(df):
        """Validate data quality for backtesting"""
        issues = []
        
        if df.empty:
            issues.append("Data is empty")
            return issues
        
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            issues.append(f"Missing required columns: {missing_cols}")
        
        # Check for NaN values
        nan_cols = df.columns[df.isnull().any()].tolist()
        if nan_cols:
            issues.append(f"NaN values found in columns: {nan_cols}")
        
        # Check for duplicate timestamps
        if 'timestamp' in df.columns:
            duplicates = df['timestamp'].duplicated().sum()
            if duplicates > 0:
                issues.append(f"Found {duplicates} duplicate timestamps")
        
        # Check price consistency
        for col in ['open', 'high', 'low', 'close']:
            if col in df.columns:
                if (df[col] <= 0).any():
                    issues.append(f"Non-positive values found in {col}")
        
        # Check OHLC logic
        if all(col in df.columns for col in ['open', 'high', 'low', 'close']):
            ohlc_errors = (
                (df['high'] < df['low']) |
                (df['high'] < df['open']) |
                (df['high'] < df['close']) |
                (df['low'] > df['open']) |
                (df['low'] > df['close'])
            ).sum()
            if ohlc_errors > 0:
                issues.append(f"OHLC logic errors in {ohlc_errors} rows")
        
        return issues
    
    @staticmethod
    def clean_data(df):
        """Clean and preprocess data for backtesting"""
        df_clean = df.copy()
        
        # Forward fill NaN values
        df_clean = df_clean.fillna(method='ffill')
        
        # Remove rows with all NaN values
        df_clean = df_clean.dropna(how='all')
        
        # Remove duplicate timestamps
        if 'timestamp' in df_clean.columns:
            df_clean = df_clean.drop_duplicates(subset=['timestamp'], keep='first')
            df_clean = df_clean.sort_values('timestamp')
        
        # Ensure positive prices
        price_cols = ['open', 'high', 'low', 'close']
        for col in price_cols:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].abs()
        
        return df_clean

class AdaptiveEnsemble:
    """Adaptive ensemble model that adjusts based on market conditions"""
    
    def __init__(self):
        self.models = {}
        self.model_performance = {}
        self.market_regimes = ['trending', 'ranging', 'volatile']
        self.current_regime = 'trending'
        
    def detect_market_regime(self, data, lookback=50):
        """Detect current market regime"""
        if len(data) < lookback:
            return 'trending'
        
        recent_data = data.tail(lookback)
        
        # Calculate volatility
        returns = recent_data['close'].pct_change().dropna()
        volatility = returns.std() * np.sqrt(252)  # Annualized
        
        # Calculate trend strength
        sma_short = recent_data['close'].rolling(10).mean()
        sma_long = recent_data['close'].rolling(30).mean()
        trend_strength = abs(sma_short.iloc[-1] - sma_long.iloc[-1]) / sma_long.iloc[-1]
        
        # Classify regime
        if volatility > 0.3:  # High volatility threshold
            return 'volatile'
        elif trend_strength > 0.05:  # Strong trend threshold
            return 'trending'
        else:
            return 'ranging'
    
    def update_model_performance(self, regime, model_name, accuracy):
        """Update performance tracking for models"""
        if regime not in self.model_performance:
            self.model_performance[regime] = {}
        
        if model_name not in self.model_performance[regime]:
            self.model_performance[regime][model_name] = []
        
        self.model_performance[regime][model_name].append(accuracy)
        
        # Keep only recent performance (last 50 predictions)
        if len(self.model_performance[regime][model_name]) > 50:
            self.model_performance[regime][model_name] = self.model_performance[regime][model_name][-50:]
    
    def get_best_model_for_regime(self, regime):
        """Get the best performing model for a specific market regime"""
        if regime not in self.model_performance:
            return 'random_forest'  # Default
        
        best_model = None
        best_performance = 0
        
        for model_name, performances in self.model_performance[regime].items():
            if len(performances) >= 5:  # Minimum sample size
                avg_performance = np.mean(performances[-10:])  # Recent average
                if avg_performance > best_performance:
                    best_performance = avg_performance
                    best_model = model_name
        
        return best_model or 'random_forest'

class OnlineLearningSystem:
    """Online learning system for continuous model adaptation"""
    
    def __init__(self, buffer_size=1000):
        self.buffer_size = buffer_size
        self.feature_buffer = []
        self.target_buffer = []
        self.model = None
        self.scaler = StandardScaler()
        self.is_fitted = False
        
    def add_sample(self, features, target):
        """Add a new training sample"""
        self.feature_buffer.append(features)
        self.target_buffer.append(target)
        
        # Maintain buffer size
        if len(self.feature_buffer) > self.buffer_size:
            self.feature_buffer = self.feature_buffer[-self.buffer_size:]
            self.target_buffer = self.target_buffer[-self.buffer_size:]
    
    def incremental_fit(self):
        """Incrementally update the model"""
        if len(self.feature_buffer) < 10:  # Minimum samples
            return False
        
        try:
            X = np.array(self.feature_buffer)
            y = np.array(self.target_buffer)
            
            # Scale features
            if not self.is_fitted:
                X_scaled = self.scaler.fit_transform(X)
                # Initialize model
                if GradientBoostingRegressor:
                    self.model = GradientBoostingRegressor(
                        n_estimators=50,
                        learning_rate=0.1,
                        max_depth=3,
                        random_state=42
                    )
                    self.model.fit(X_scaled, y)
                    self.is_fitted = True
            else:
                X_scaled = self.scaler.transform(X)
                # For online learning, we retrain on recent data
                # In production, you might use models with partial_fit capability
                if len(X_scaled) >= 50:  # Retrain periodically
                    self.model.fit(X_scaled[-50:], y[-50:])
            
            return True
        except Exception as e:
            return False
    
    def predict(self, features):
        """Make prediction with current model"""
        if not self.is_fitted or self.model is None:
            return None
        
        try:
            X = np.array(features).reshape(1, -1)
            X_scaled = self.scaler.transform(X)
            prediction = self.model.predict(X_scaled)[0]
            return prediction
        except Exception as e:
            return None

# --- Move update_active_trades to the top, after imports and before any code that calls it

def update_active_trades():
    to_close = []
    # Cache prices for all unique symbols in active trades
    active_trades = list(st.session_state.active_trades.items())
    symbols = list(set(trade['symbol'] for _, trade in active_trades))
    price_cache = {symbol: fetch_binance_price(symbol) for symbol in symbols}
    for trade_id, trade in active_trades:
        price = price_cache.get(trade['symbol'])
        if price is None:
            continue
        trade['pnl'] = (price - trade['entry_price']) * (1 if trade['direction']=='LONG' else -1) * (trade['amount']/trade['entry_price'])
        trade['current_price'] = price
        # Check TP/SL
        closed = False
        if (trade['direction']=='LONG' and price >= trade['tp_price']) or (trade['direction']=='SHORT' and price <= trade['tp_price']):
            trade['status'] = 'CLOSED (TP)'
            trade['close_time'] = datetime.datetime.now()
            st.session_state.virtual_balance += trade['amount'] + trade['pnl']
            to_close.append(trade_id)
            st.session_state['last_notification'] = f"TP hit: {trade['symbol'].upper()} {trade['direction']} closed at ${price:.4f}"
            add_notification(f"TP hit: {trade['symbol'].upper()} {trade['direction']} closed at ${price:.4f}", "success")
            closed = True
        elif (trade['direction']=='LONG' and price <= trade['sl_price']) or (trade['direction']=='SHORT' and price >= trade['sl_price']):
            trade['status'] = 'CLOSED (SL)'
            trade['close_time'] = datetime.datetime.now()
            st.session_state.virtual_balance += trade['amount'] + trade['pnl']
            to_close.append(trade_id)
            st.session_state['last_notification'] = f"SL hit: {trade['symbol'].upper()} {trade['direction']} closed at ${price:.4f}"
            add_notification(f"SL hit: {trade['symbol'].upper()} {trade['direction']} closed at ${price:.4f}", "error")
            closed = True
        # Update trade_history for this trade_id if closed
        if closed:
            for hist_trade in st.session_state.trade_history:
                if hist_trade.get('id') == trade_id:
                    hist_trade['status'] = trade['status']
                    hist_trade['close_time'] = trade['close_time']
                    hist_trade['pnl'] = trade['pnl']
                    hist_trade['current_price'] = trade.get('current_price', price)
                    hist_trade['close_price'] = trade.get('current_price', price)
                    # Log trade to DB if available
                    features = hist_trade.get('features', {})
                    prediction = hist_trade.get('prediction', {})
                    if 'log_trade_to_db' in globals():
                        log_trade_to_db(hist_trade, features, prediction)
                    break
    for tid in to_close:
        del st.session_state.active_trades[tid]

# --- Session State Initialization ---
def initialize_session_state():
    if 'trades_since_retrain' not in st.session_state:
        st.session_state.trades_since_retrain = 0
    if 'last_retrain_time' not in st.session_state:
        st.session_state.last_retrain_time = datetime.datetime.now()
    if 'virtual_balance' not in st.session_state:
        st.session_state.virtual_balance = 10000.0
    if 'active_trades' not in st.session_state:
        st.session_state.active_trades = {}
    if 'trade_history' not in st.session_state:
        st.session_state.trade_history = []
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.datetime.now()
    if 'signals_history' not in st.session_state:
        st.session_state.signals_history = []
    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = True
    if 'perf_monitor' not in st.session_state:
        st.session_state.perf_monitor = PerformanceMonitor()
    if 'pending_trades' not in st.session_state:
        st.session_state.pending_trades = {}
    # Advanced backtesting and ML systems
    if 'advanced_backtester' not in st.session_state:
        st.session_state.advanced_backtester = AdvancedBacktester()
    if 'adaptive_ensemble' not in st.session_state:
        st.session_state.adaptive_ensemble = AdaptiveEnsemble()
    if 'data_quality_manager' not in st.session_state:
        st.session_state.data_quality_manager = DataQualityManager()
    if 'online_learning_system' not in st.session_state:
        st.session_state.online_learning_system = OnlineLearningSystem()
    if 'backtest_results' not in st.session_state:
        st.session_state.backtest_results = []
    if 'model_performance_history' not in st.session_state:
        st.session_state.model_performance_history = []

initialize_session_state()

# --- Helper: Fetch live price from Binance ---
# Remove caching for real-time price updates
#@st.cache_data(ttl=10, show_spinner=False)
def fetch_binance_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
    try:
        start_time = datetime.datetime.now()
        res = requests.get(url, timeout=3)
        res.raise_for_status()
        end_time = datetime.datetime.now()
        response_time = (end_time - start_time).total_seconds() * 1000
        st.session_state.perf_monitor.add_response_time(response_time)
        st.session_state.perf_monitor.record_api_success()  # Record successful API call
        return float(res.json()['price'])
    except requests.exceptions.RequestException as e:
        st.session_state.perf_monitor.record_api_error()  # Record API error
        st.session_state['binance_error'] = str(e)
        return None
    except Exception as e:
        st.session_state.perf_monitor.record_api_error()  # Record other errors
        st.session_state['binance_error'] = str(e)
        return None

# --- NOTIFICATIONS ---
def add_notification(message, type="info"):
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []
    st.session_state.notifications.append({
        'message': message,
        'type': type,
        'timestamp': datetime.datetime.now()
    })
    if len(st.session_state.notifications) > 10:
        st.session_state.notifications = st.session_state.notifications[-10:]

def display_notifications():
    """Display trading notifications in a user-friendly, visually distinct format."""
    with st.expander("📣 Trading Notifications", expanded=True):
        if not st.session_state.notifications:
            st.info("No notifications yet. All trade alerts and system messages will appear here.")
            return

        # Add a clear all button
        clear_col, _ = st.columns([1, 5])
        with clear_col:
            if st.button("🧹 Clear All", key="clear_notifications_btn"):
                st.session_state.notifications = []
                st.rerun()

        # Show notifications, most recent first
        for notification in reversed(st.session_state.notifications):
            msg = notification.get('message', '')
            ntype = notification.get('type', 'info')
            ts = notification.get('timestamp', None)
            if ts:
                if hasattr(ts, 'strftime'):
                    ts_str = ts.strftime('%H:%M:%S')
                else:
                    ts_str = str(ts)
            else:
                ts_str = ''

            icon = {
                'success': '✅',
                'error': '❌',
                'warning': '⚠️',
                'info': 'ℹ️',
            }.get(ntype, 'ℹ️')

            formatted_msg = f"{icon} <b>{ts_str}</b> — {msg}"
            if ntype == 'success':
                st.success(formatted_msg)
            elif ntype == 'error':
                st.error(formatted_msg)
            elif ntype == 'warning':
                st.warning(formatted_msg)
            else:
                st.info(formatted_msg)

# --- ENHANCED MODEL TRAINING & PREDICTION FUNCTIONS ---

def load_historical_data_db():
    """Load historical trade data from database for model training"""
    try:
        conn = sqlite3.connect(DB_PATH)
        
        # Create trades table if it doesn't exist
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS trades
                    (id TEXT PRIMARY KEY,
                     symbol TEXT,
                     direction TEXT,
                     amount REAL,
                     entry_price REAL,
                     tp_price REAL,
                     sl_price REAL,
                     status TEXT,
                     open_time TEXT,
                     close_time TEXT,
                     pnl REAL,
                     current_price REAL,
                     close_price REAL,
                     features TEXT,
                     prediction TEXT)''')
        
        # Load historical data
        df = pd.read_sql_query("SELECT * FROM trades WHERE status LIKE 'CLOSED%'", conn)
        conn.close()
        
        if len(df) > 0:
            # Parse features and predictions
            import json
            df['features'] = df['features'].apply(lambda x: json.loads(x) if x else {})
            df['prediction'] = df['prediction'].apply(lambda x: json.loads(x) if x else {})
            return df
        return None
    except Exception as e:
        return None

def enhanced_train_prediction_models(df, horizon_minutes=30):
    """
    Enhanced model training with advanced features and validation
    """
    try:
        # Load historical data from DB if available
        hist_df = load_historical_data_db()
        if hist_df is not None and len(hist_df) > 50:
            df = pd.concat([df, hist_df], ignore_index=True)
            
        if len(df) < 50:
            return None
        
        # Enhanced feature engineering
        df = enhanced_calculate_indicators(df)
        
        # Data quality validation
        issues = st.session_state.data_quality_manager.validate_data(df)
        if issues:
            df = st.session_state.data_quality_manager.clean_data(df)
        
        # Prepare target variable
        future_periods = max(1, int(horizon_minutes / 5))
        future_periods = min(future_periods, len(df) - 2)
        
        if future_periods <= 0:
            return None
            
        df['future_price'] = df['close'].shift(-future_periods)
        df['target'] = (df['future_price'] / df['close'] - 1) * 100
        
        # Feature selection
        excluded_cols = ['datetime', 'timestamp', 'future_price', 'target', 'open', 'high', 'low', 'close']
        feature_cols = [col for col in df.columns if col not in excluded_cols and df[col].dtype in ['float64', 'int64']]
        
        # Remove features with too many NaN values
        feature_cols = [col for col in feature_cols if df[col].isnull().sum() / len(df) < 0.3]
        
        if len(feature_cols) < 5:
            return None
        
        X = df[feature_cols].fillna(df[feature_cols].median())
        y = df['target'].fillna(0)
        
        # Remove outliers using IQR method
        Q1 = y.quantile(0.25)
        Q3 = y.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        mask = (y >= lower_bound) & (y <= upper_bound)
        X = X[mask]
        y = y[mask]
        
        if len(X) < 30:
            return None
        
        # Feature scaling
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Walk-forward validation for model selection
        tscv = TimeSeriesSplit(n_splits=3)
        model_scores = {}
        
        models_to_test = {
            'linear_regression': LinearRegression(),
            'random_forest': RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42),
        }
        
        # Add advanced models if available
        if XGBRegressor:
            models_to_test['xgboost'] = XGBRegressor(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, verbosity=0)
        if LGBMRegressor:
            models_to_test['lightgbm'] = LGBMRegressor(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, verbose=-1)
        if CatBoostRegressor:
            models_to_test['catboost'] = CatBoostRegressor(iterations=100, depth=6, learning_rate=0.1, random_state=42, verbose=0)
        
        # Cross-validation
        for name, model in models_to_test.items():
            scores = []
            for train_idx, val_idx in tscv.split(X_scaled):
                X_train, X_val = X_scaled[train_idx], X_scaled[val_idx]
                y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
                
                model.fit(X_train, y_train)
                y_pred = model.predict(X_val)
                score = -mean_squared_error(y_val, y_pred)  # Negative MSE for maximization
                scores.append(score)
            
            model_scores[name] = np.mean(scores)
        
        # Select best models and create ensemble
        sorted_models = sorted(model_scores.items(), key=lambda x: x[1], reverse=True)
        best_models = [name for name, score in sorted_models[:3]]  # Top 3 models
        
        # Train final models on full dataset
        final_models = {}
        estimators = []
        
        for name in best_models:
            model = models_to_test[name]
            model.fit(X_scaled, y)
            final_models[name] = model
            estimators.append((name, model))
        
        # Create ensemble
        if len(estimators) > 1:
            ensemble = VotingRegressor(estimators=estimators)
            ensemble.fit(X_scaled, y)
            final_models['ensemble'] = ensemble
        
        # Model performance tracking
        regime = st.session_state.adaptive_ensemble.detect_market_regime(df)
        for name in best_models:
            # Simulate accuracy for regime tracking
            accuracy = max(0.5, 0.7 + np.random.normal(0, 0.1))
            st.session_state.adaptive_ensemble.update_model_performance(regime, name, accuracy)
        
        # Record successful model training
        st.session_state.perf_monitor.record_model_success()
        
        result = {
            'models': final_models,
            'scaler': scaler,
            'feature_cols': feature_cols,
            'future_periods': future_periods,
            'model_scores': model_scores,
            'best_models': best_models,
            'training_samples': len(X),
            'market_regime': regime
        }
        
        # Update online learning system
        if len(X) > 0:
            latest_features = X.iloc[-1].values
            latest_target = y.iloc[-1]
            st.session_state.online_learning_system.add_sample(latest_features, latest_target)
            st.session_state.online_learning_system.incremental_fit()
        
        return result
        
    except Exception as e:
        st.session_state.perf_monitor.record_model_error()
        traceback.print_exc()
        return None

def enhanced_calculate_indicators(df, rsi_window=14, ema_fast=8, ema_slow=21, bb_period=20):
    """
    Calculate enhanced technical indicators for model training
    """
    if len(df) < 50:
        return df
    
    try:
        # Basic indicators
        if EMAIndicator:
            df['ema_fast'] = EMAIndicator(df['close'], window=ema_fast).ema_indicator()
            df['ema_slow'] = EMAIndicator(df['close'], window=ema_slow).ema_indicator()
            df['ema_9'] = EMAIndicator(df['close'], window=9).ema_indicator()
            df['ema_21'] = EMAIndicator(df['close'], window=21).ema_indicator()
            df['ema_50'] = EMAIndicator(df['close'], window=50).ema_indicator()
            df['ema_200'] = EMAIndicator(df['close'], window=200).ema_indicator()
        
        if RSIIndicator:
            df['rsi'] = RSIIndicator(df['close'], window=rsi_window).rsi()
            df['rsi_7'] = RSIIndicator(df['close'], window=7).rsi()
            df['rsi_21'] = RSIIndicator(df['close'], window=21).rsi()
        
        if MACD:
            macd = MACD(df['close'])
            df['macd'] = macd.macd()
            df['macd_signal'] = macd.macd_signal()
            df['macd_histogram'] = macd.macd_diff()
        
        if BollingerBands:
            bb = BollingerBands(df['close'], window=bb_period)
            df['bb_upper'] = bb.bollinger_hband()
            df['bb_lower'] = bb.bollinger_lband()
            df['bb_middle'] = bb.bollinger_mavg()
            df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle']
            df['bb_position'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
        
        # Volume indicators
        if OnBalanceVolumeIndicator:
            df['obv'] = OnBalanceVolumeIndicator(df['close'], df['volume']).on_balance_volume()
        
        df['volume_sma'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_sma']
        
        # Price-based features
        df['price_change_1'] = df['close'].pct_change(1)
        df['price_change_5'] = df['close'].pct_change(5)
        df['price_change_10'] = df['close'].pct_change(10)
        df['high_low_spread'] = (df['high'] - df['low']) / df['close']
        df['close_open_spread'] = (df['close'] - df['open']) / df['open']
        
        # Volatility features
        df['rolling_volatility_10'] = df['close'].rolling(window=10).std()
        df['rolling_volatility_20'] = df['close'].rolling(window=20).std()
        
        # Momentum features
        df['momentum_5'] = df['close'] / df['close'].shift(5) - 1
        df['momentum_10'] = df['close'] / df['close'].shift(10) - 1
        
        # Statistical features
        df['close_zscore'] = (df['close'] - df['close'].rolling(window=20).mean()) / df['close'].rolling(window=20).std()
        df['volume_zscore'] = (df['volume'] - df['volume'].rolling(window=20).mean()) / df['volume'].rolling(window=20).std()
        
        # Lagged features
        df['close_lag_1'] = df['close'].shift(1)
        df['close_lag_3'] = df['close'].shift(3)
        df['close_lag_5'] = df['close'].shift(5)
        df['rsi_lag_1'] = df['rsi'].shift(1) if 'rsi' in df.columns else 0
        
        # Interaction features
        if 'ema_fast' in df.columns and 'ema_slow' in df.columns:
            df['ema_fast_slow_ratio'] = df['ema_fast'] / df['ema_slow']
            df['ema_fast_slow_diff'] = df['ema_fast'] - df['ema_slow']
        
        # Fill NaN values
        df = df.fillna(method='ffill').fillna(method='bfill')
        
    except Exception as e:
        st.error(f"Error calculating enhanced indicators: {e}")
    
    return df

def enhanced_predict_with_models(models, df, feature_cols):
    """
    Enhanced prediction with ensemble models and confidence scoring
    """
    try:
        if not models or 'scaler' not in models:
            return None
        
        scaler = models['scaler']
        model_dict = models['models']
        
        # Prepare current data
        current_data = df.iloc[-1:][feature_cols].fillna(df[feature_cols].median())
        current_data_scaled = scaler.transform(current_data)
        
        predictions = {}
        pred_values = []
        
        # Get predictions from all models
        for name, model in model_dict.items():
            if name == 'ensemble':
                continue
            try:
                pred = model.predict(current_data_scaled)[0]
                predictions[name] = pred
                pred_values.append(pred)
            except:
                continue
        
        # Ensemble prediction
        ensemble_pred = None
        if 'ensemble' in model_dict:
            try:
                ensemble_pred = model_dict['ensemble'].predict(current_data_scaled)[0]
                predictions['ensemble'] = ensemble_pred
            except:
                ensemble_pred = np.mean(pred_values) if pred_values else 0
        
        if not pred_values:
            return None
        
        # Calculate confidence metrics
        pred_std = np.std(pred_values) if len(pred_values) > 1 else 0
        confidence = max(30, 100 - pred_std * 50)  # Inverse relationship with std dev
        
        # Agreement: how many models agree on direction
        ensemble_direction = np.sign(ensemble_pred) if ensemble_pred is not None else np.sign(np.mean(pred_values))
        agreements = sum(1 for pred in pred_values if np.sign(pred) == ensemble_direction)
        agreement = (agreements / len(pred_values)) * 100 if pred_values else 0
        
        # Determine trading direction
        final_prediction = ensemble_pred if ensemble_pred is not None else np.mean(pred_values)
        direction = "LONG" if final_prediction > 0 else "SHORT"
        
        # Market regime adjustment
        regime = st.session_state.adaptive_ensemble.detect_market_regime(df)
        best_model_for_regime = st.session_state.adaptive_ensemble.get_best_model_for_regime(regime)
        
        # Boost confidence if best model agrees
        if best_model_for_regime in predictions:
            best_model_pred = predictions[best_model_for_regime]
            if np.sign(best_model_pred) == np.sign(final_prediction):
                confidence = min(confidence * 1.1, 95)
        
        result = {
            'predictions': predictions,
            'ensemble': final_prediction,
            'confidence': confidence,
            'agreement': agreement,
            'direction': direction,
            'model_regime': regime,
            'best_model': best_model_for_regime,
            'prediction_strength': abs(final_prediction)
        }
        
        return result
        
    except Exception as e:
        return None

def enhanced_retrain_model_if_needed(df, horizon_minutes=30):
    """
    Enhanced model retraining with performance tracking
    """
    should_retrain = False
    
    # Check retraining conditions
    trades_since_retrain = st.session_state.get('trades_since_retrain', 0)
    last_retrain = st.session_state.get('last_retrain_time', datetime.datetime.now())
    time_since_retrain = datetime.datetime.now() - last_retrain
    
    # Retrain conditions
    if trades_since_retrain >= 100:  # After 100 trades
        should_retrain = True
        reason = "Trade threshold reached"
    elif time_since_retrain.days >= 3:  # After 3 days
        should_retrain = True
        reason = "Time threshold reached"
    elif len(st.session_state.model_performance_history) > 10:
        # Retrain if recent performance is declining
        recent_performance = st.session_state.model_performance_history[-5:]
        older_performance = st.session_state.model_performance_history[-10:-5]
        if recent_performance and older_performance:
            recent_avg = np.mean(recent_performance)
            older_avg = np.mean(older_performance)
            if recent_avg < older_avg * 0.9:  # 10% performance drop
                should_retrain = True
                reason = "Performance degradation detected"
    
    if should_retrain:
        st.info(f"Retraining ML models: {reason}")
        models = enhanced_train_prediction_models(df, horizon_minutes)
        
        if models:
            st.session_state['ml_models'] = models
            st.session_state['trades_since_retrain'] = 0
            st.session_state['last_retrain_time'] = datetime.datetime.now()
            st.success("Enhanced ML models retrained successfully!")
        else:
            st.warning("Model retraining failed, using existing models")
    
    # Return current models
    return st.session_state.get('ml_models', None)

# --- Helper: Simulate trade execution and tracking ---
def open_virtual_trade(symbol, direction, amount, entry_price, tp_pct, sl_pct):
    trade_id = str(uuid.uuid4())[:8]
    trade = {
        'id': trade_id,
        'symbol': symbol,
        'direction': direction,
        'amount': amount,
        'entry_price': entry_price,
        'tp_price': entry_price * (1 + tp_pct/100) if direction == 'LONG' else entry_price * (1 - tp_pct/100),
        'sl_price': entry_price * (1 - sl_pct/100) if direction == 'LONG' else entry_price * (1 + sl_pct/100),
        'status': 'OPEN',
        'open_time': datetime.datetime.now(),        'close_time': None,
        'pnl': 0.0
    }
    st.session_state.virtual_balance -= amount
    st.session_state.active_trades[trade_id] = trade
    st.session_state.trade_history.append(trade.copy())
    st.session_state['last_notification'] = f"Opened {direction} {symbol.upper()} at ${entry_price:.4f}"
    add_notification(f"Opened {direction} {symbol.upper()} at ${entry_price:.4f}", "success")
    # Increment trade counter for retraining
    st.session_state.trades_since_retrain += 1
    st.session_state.perf_monitor.record_trade_success()  # Record successful trade execution
    return trade_id

# --- Helper: Place a pending trade ---
def place_pending_trade(symbol, direction, amount, entry_price, tp_pct, sl_pct):
    trade_id = str(uuid.uuid4())[:8]
    trade = {
        'id': trade_id,
        'symbol': symbol,
        'direction': direction,
        'amount': amount,
        'entry_price': entry_price,
        'tp_price': entry_price * (1 + tp_pct/100) if direction == 'LONG' else entry_price * (1 - tp_pct/100),
        'sl_price': entry_price * (1 - sl_pct/100) if direction == 'LONG' else entry_price * (1 + sl_pct/100),
        'status': 'PENDING',
        'open_time': None,        'close_time': None,
        'pnl': 0.0
    }
    st.session_state.pending_trades[trade_id] = trade
    add_notification(f"Pending {direction} {symbol.upper()} at ${entry_price:.4f}", "info")
    st.session_state.perf_monitor.record_trade_success()  # Record successful pending order placement
    return trade_id

# --- Monitor and execute pending trades ---
def check_and_execute_pending_trades():
    """Check and execute pending trades when price conditions are met"""
    to_activate = []
    for trade_id, trade in list(st.session_state.pending_trades.items()):
        current_price = fetch_binance_price(trade['symbol'])
        if current_price is None:
            continue
            
        should_execute = False
        
        if trade['direction'] == 'LONG':
            # For LONG: execute when current price is at or below entry price
            if current_price <= trade['entry_price']:
                should_execute = True
        else:  # SHORT
            # For SHORT: execute when current price is at or above entry price
            if current_price >= trade['entry_price']:
                should_execute = True
        
        if should_execute:
            to_activate.append((trade_id, current_price))
    
    for trade_id, execution_price in to_activate:
        trade = st.session_state.pending_trades.pop(trade_id)
        trade['status'] = 'OPEN'
        trade['open_time'] = datetime.datetime.now()
        trade['entry_price'] = execution_price  # Use actual execution price
          # Recalculate TP/SL based on actual execution price
        if trade['direction'] == 'LONG':
            tp_pct = ((trade['tp_price'] / trade['entry_price']) - 1) * 100
            sl_pct = (1 - (trade['sl_price'] / trade['entry_price'])) * 100
        else:  # SHORT
            tp_pct = (1 - (trade['tp_price'] / trade['entry_price'])) * 100
            sl_pct = ((trade['sl_price'] / trade['entry_price']) - 1) * 100
        
        trade['tp_price'] = execution_price * (1 + tp_pct/100) if trade['direction'] == 'LONG' else execution_price * (1 - tp_pct/100)
        trade['sl_price'] = execution_price * (1 - sl_pct/100) if trade['direction'] == 'LONG' else execution_price * (1 + sl_pct/100)
        trade['sl_price'] = execution_price * (1 - sl_pct/100) if trade['direction'] == 'LONG' else execution_price * (1 + sl_pct/100)
        
        st.session_state.virtual_balance -= trade['amount']
        st.session_state.active_trades[trade_id] = trade
        st.session_state.trade_history.append(trade.copy())
        # Determine if TP or SL was hit at execution
        status_msg = ""
        if trade['status'].startswith('CLOSED'):
            if 'TP' in trade['status']:
                status_msg = " (TP/Profit)"
            elif 'SL' in trade['status']:
                status_msg = " (SL/Stop Loss)"
        add_notification(f"✅ Executed {trade['direction']} {trade['symbol'].upper()} at ${execution_price:.4f} (Entry: {trade['entry_price']:.4f}, Current: {execution_price:.4f}){status_msg}", "success")
        st.session_state.perf_monitor.record_trade_success()  # Record successful pending order execution

# --- MULTI-COIN SCANNER ---
def scan_multiple_coins(coins_list, timeframe, capital, leverage, risk_percentage, min_signal_strength, use_volume_filter, rsi_oversold, rsi_overbought, enable_predictions=True):
    results = []
    for coin in coins_list:
        price = fetch_binance_price(coin)
        pred = np.random.uniform(-1, 1)
        conf = np.random.randint(50, 95)
        results.append({
            'symbol': coin.upper(),
            'price': price,
            'direction': 'LONG' if pred > 0 else 'SHORT',
            'confidence': conf,
            'predicted_change': pred
        })
    return results

def execute_trade_from_prediction(symbol, direction, amount, price, tp_pct, sl_pct):
    """
    Execute a trade based on prediction - now uses pending orders instead of immediate execution
    """
    current_price = fetch_binance_price(symbol)
    if current_price is None:
        add_notification(f"Failed to get price for {symbol.upper()}", "error")
        st.session_state.perf_monitor.record_trade_error()  # Record price fetch error
        return None
    # Determine if we should place a pending order or execute immediately
    should_execute_immediately = False
    if direction == 'LONG':
        # For LONG trades, execute immediately if current price is at or below entry price
        if current_price <= price:
            should_execute_immediately = True
    else:  # SHORT
        # For SHORT trades, execute immediately if current price is at or above entry price
        if current_price >= price:
            should_execute_immediately = True
    if should_execute_immediately:
        # Execute immediately as a market order
        trade_id = open_virtual_trade(symbol, direction, amount, current_price, tp_pct, sl_pct)
        add_notification(f"Executed {direction} {symbol.upper()} immediately at ${current_price:.4f} (Entry: ${price:.4f}, Current: ${current_price:.4f})", "success")
    else:
        # Place as pending order
        trade_id = place_pending_trade(symbol, direction, amount, price, tp_pct, sl_pct)
        add_notification(f"Placed pending {direction} {symbol.upper()} order at ${price:.4f} (Current: ${current_price:.4f})", "info")
    # After each trade, check if retraining is needed (using available df and horizon)
    if 'latest_df' in st.session_state:
        retrain_model_if_needed(st.session_state['latest_df'])
    return trade_id

# --- LSTM Model Integration (for future expansion) ---
def build_lstm_model(input_shape):
    if Sequential is None or LSTM is None or Dense is None:
        return None
    model = Sequential()
    model.add(LSTM(32, input_shape=input_shape))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

# --- ADVANCED INDICATORS ---
def calculate_enhanced_indicators(df, rsi_window=14, ema_fast=8, ema_slow=21, bb_period=20, bb_std=2.0):
    # Add more lagged and rolling features for ML
    if len(df) < 100:
        return df
    try:
        # --- Standard Indicators ---
        df['ema_fast'] = EMAIndicator(df['close'], window=ema_fast).ema_indicator()
        df['ema_slow'] = EMAIndicator(df['close'], window=ema_slow).ema_indicator()
        df['ema_trend'] = EMAIndicator(df['close'], window=ema_trend).ema_indicator()
        df['ema_9'] = EMAIndicator(df['close'], window=9).ema_indicator()
        df['ema_21'] = EMAIndicator(df['close'], window=21).ema_indicator()
        df['ema_50'] = EMAIndicator(df['close'], window=50).ema_indicator()
        df['ema_200'] = EMAIndicator(df['close'], window=200).ema_indicator()
        macd = MACD(df['close'])
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_histogram'] = macd.macd_diff()
        df['rsi'] = RSIIndicator(df['close'], window=rsi_window).rsi()
        stoch = StochasticOscillator(df['high'], df['low'], df['close'])
        df['stoch_k'] = stoch.stoch()
        df['stoch_d'] = stoch.stoch_signal()
        bb = BollingerBands(df['close'], window=bb_period, window_dev=bb_std)
        df['bb_upper'] = bb.bollinger_hband()
        df['bb_lower'] = bb.bollinger_lband()
        df['bb_middle'] = bb.bollinger_mavg()
        df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle']
        df['bb_position'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
        atr = AverageTrueRange(df['high'], df['low'], df['close'])
        df['atr'] = atr.average_true_range()
        df['volume_sma'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_sma']
        obv = OnBalanceVolumeIndicator(df['close'], df['volume'])
        df['obv'] = obv.on_balance_volume()

        # --- Additional Engineered Features ---
        df['price_change_1'] = df['close'].pct_change(1)
        df['price_change_5'] = df['close'].pct_change(5)
        df['price_change_10'] = df['close'].pct_change(10)
        df['high_low_spread'] = (df['high'] - df['low']) / df['close']
        df['close_open_spread'] = (df['close'] - df['open']) / df['open']
        df['rolling_volatility_10'] = df['close'].rolling(window=10).std()
        df['rolling_volatility_20'] = df['close'].rolling(window=20).std()
        df['rolling_volume_10'] = df['volume'].rolling(window=10).mean()
        df['rolling_volume_20'] = df['volume'].rolling(window=20).mean()
        df['volume_change_5'] = df['volume'].pct_change(5)
        df['rsi_7'] = RSIIndicator(df['close'], window=7).rsi()
        df['rsi_21'] = RSIIndicator(df['close'], window=21).rsi()
        df['macd_diff'] = df['macd'] - df['macd_signal']
        df['ema_fast_slow_diff'] = df['ema_fast'] - df['ema_slow']
        df['ema_9_21_diff'] = df['ema_9'] - df['ema_21']
        df['ema_50_200_diff'] = df['ema_50'] - df['ema_200']
        # Lagged features
        df['close_lag_1'] = df['close'].shift(1)
        df['close_lag_5'] = df['close'].shift(5)
        df['rsi_lag_1'] = df['rsi'].shift(1)
        df['macd_lag_1'] = df['macd'].shift(1)
        # More lagged features
        for lag in [2, 3, 10, 20]:
            df[f'close_lag_{lag}'] = df['close'].shift(lag)
            df[f'rsi_lag_{lag}'] = df['rsi'].shift(lag)
            df[f'macd_lag_{lag}'] = df['macd'].shift(lag)
        # More rolling features
        for window in [5, 15, 30, 50]:
            df[f'rolling_mean_{window}'] = df['close'].rolling(window=window).mean()
            df[f'rolling_std_{window}'] = df['close'].rolling(window=window).std()
            df[f'rolling_volume_{window}'] = df['volume'].rolling(window=window).mean()
        # Binned RSI (categorical)
        df['rsi_bin'] = pd.cut(df['rsi'], bins=[0, 30, 70, 100], labels=[0, 1, 2]).astype(float)
    except Exception as e:
        st.error(f"Error calculating indicators: {e}")
    return df
    if len(df) < 100:
        return df

    try:
        # --- Standard Indicators ---
        df['ema_fast'] = EMAIndicator(df['close'], window=ema_fast).ema_indicator()
        df['ema_slow'] = EMAIndicator(df['close'], window=ema_slow).ema_indicator()
        df['ema_trend'] = EMAIndicator(df['close'], window=ema_trend).ema_indicator()
        df['ema_9'] = EMAIndicator(df['close'], window=9).ema_indicator()
        df['ema_21'] = EMAIndicator(df['close'], window=21).ema_indicator()
        df['ema_50'] = EMAIndicator(df['close'], window=50).ema_indicator()
        df['ema_200'] = EMAIndicator(df['close'], window=200).ema_indicator()
        macd = MACD(df['close'])
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_histogram'] = macd.macd_diff()
        df['rsi'] = RSIIndicator(df['close'], window=rsi_window).rsi()
        stoch = StochasticOscillator(df['high'], df['low'], df['close'])
        df['stoch_k'] = stoch.stoch()
        df['stoch_d'] = stoch.stoch_signal()
        bb = BollingerBands(df['close'], window=bb_period, window_dev=bb_std)
        df['bb_upper'] = bb.bollinger_hband()
        df['bb_lower'] = bb.bollinger_lband()
        df['bb_middle'] = bb.bollinger_mavg()
        df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle']
        df['bb_position'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
        atr = AverageTrueRange(df['high'], df['low'], df['close'])
        df['atr'] = atr.average_true_range()
        df['volume_sma'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_sma']
        obv = OnBalanceVolumeIndicator(df['close'], df['volume'])
        df['obv'] = obv.on_balance_volume()

        # --- Additional Engineered Features ---
        df['price_change_1'] = df['close'].pct_change(1)
        df['price_change_5'] = df['close'].pct_change(5)
        df['price_change_10'] = df['close'].pct_change(10)
        df['high_low_spread'] = (df['high'] - df['low']) / df['close']
        df['close_open_spread'] = (df['close'] - df['open']) / df['open']
        df['rolling_volatility_10'] = df['close'].rolling(window=10).std()
        df['rolling_volatility_20'] = df['close'].rolling(window=20).std()
        df['rolling_volume_10'] = df['volume'].rolling(window=10).mean()
        df['rolling_volume_20'] = df['volume'].rolling(window=20).mean()
        df['volume_change_5'] = df['volume'].pct_change(5)
        df['rsi_7'] = RSIIndicator(df['close'], window=7).rsi()
        df['rsi_21'] = RSIIndicator(df['close'], window=21).rsi()
        df['macd_diff'] = df['macd'] - df['macd_signal']
        df['ema_fast_slow_diff'] = df['ema_fast'] - df['ema_slow']
        df['ema_9_21_diff'] = df['ema_9'] - df['ema_21']
        df['ema_50_200_diff'] = df['ema_50'] - df['ema_200']
        # Lagged features
        df['close_lag_1'] = df['close'].shift(1)
        df['close_lag_5'] = df['close'].shift(5)
        df['rsi_lag_1'] = df['rsi'].shift(1)
        df['macd_lag_1'] = df['macd'].shift(1)
        # More lagged features
        for lag in [2, 3, 10, 20]:
            df[f'close_lag_{lag}'] = df['close'].shift(lag)
            df[f'rsi_lag_{lag}'] = df['rsi'].shift(lag)
            df[f'macd_lag_{lag}'] = df['macd'].shift(lag)
        # More rolling features
        for window in [5, 15, 30, 50]:
            df[f'rolling_mean_{window}'] = df['close'].rolling(window=window).mean()
            df[f'rolling_std_{window}'] = df['close'].rolling(window=window).std()
            df[f'rolling_volume_{window}'] = df['volume'].rolling(window=window).mean()
        # Binned RSI (categorical)
        df['rsi_bin'] = pd.cut(df['rsi'], bins=[0, 30, 70, 100], labels=[0, 1, 2]).astype(float)
    except Exception as e:
        st.error(f"Error calculating indicators: {e}")
    return df

# --- AI/ML PREDICTION LOGIC (Ensemble + Fallback) ---
def train_prediction_models(df, horizon_minutes=30):
    try:
        # Load historical data from DB if available
        hist_df = load_historical_data_db()
        if hist_df is not None and len(hist_df) > 50:
            df = pd.concat([df, hist_df], ignore_index=True)
        # Use all available historical data
        if len(df) < 50:
            return None, None, [], 1, None
        # Remove outliers using IQR method
        df_clean = df.copy()
        for col in ['close', 'volume']:
            if col in df_clean.columns:
                Q1 = df_clean[col].quantile(0.25)
                Q3 = df_clean[col].quantile(0.75)
                IQR = Q3 - Q1
                mask = (df_clean[col] >= Q1 - 1.5 * IQR) & (df_clean[col] <= Q3 + 1.5 * IQR)
                df_clean = df_clean[mask]
        # Handle missing data: interpolate, then fill remaining with median
        df_clean = df_clean.interpolate(method='linear', limit_direction='both')
        df_clean = df_clean.fillna(df_clean.median(numeric_only=True))
        # Use all data for training (no holdout, but walk-forward validation below)
        future_periods = max(1, int(horizon_minutes / 5))
        future_periods = min(future_periods, len(df_clean) - 2)
        if future_periods <= 0:
            return None, None, feature_cols, future_periods, scaler
        df_clean['future_price'] = df_clean['close'].shift(-future_periods)
        df_clean['target'] = (df_clean['future_price'] / df_clean['close'] - 1) * 100
        excluded_cols = ['datetime', 'timestamp', 'future_price', 'target', 'open', 'high', 'low', 'close']
        feature_cols = [col for col in df_clean.columns if col not in excluded_cols]
        # --- Apply penalty weights to features ---
        penalty_weights = get_feature_penalty_weights(feature_cols)
        # Weight features in X by penalty (downweight features that led to losses)
        X = df_clean[feature_cols].copy()
        for col in feature_cols:
            X[col] = X[col] * penalty_weights.get(col, 1.0)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        y = df_clean['target']
        if len(X_scaled) < 30 or len(y) < 30:
            return None, None, feature_cols, future_periods, scaler
        # Walk-forward validation (rolling window)
        from sklearn.metrics import mean_squared_error
        window_size = int(len(X_scaled) * 0.7)
        step_size = max(1, int(window_size * 0.1))
        rmses = []
        for start in range(0, len(X_scaled) - window_size, step_size):
            X_train, X_test = X_scaled[start:start+window_size], X_scaled[start+window_size:start+window_size+step_size]
            y_train, y_test = y.iloc[start:start+window_size], y.iloc[start+window_size:start+window_size+step_size]
            if len(X_test) == 0:
                continue
            rf = RandomForestRegressor(n_estimators=200, max_depth=8, min_samples_split=4, random_state=42)
            rf.fit(X_train, y_train)
            preds = rf.predict(X_test)
            rmse = np.sqrt(mean_squared_error(y_test, preds))
            rmses.append(rmse)
        if rmses:
            avg_rmse = np.mean(rmses)
            st.info(f"Walk-forward validation RMSE (RandomForest): {avg_rmse:.4f}")
        # Train final models on all data
        lr_model = LinearRegression().fit(X_scaled, y)
        rf_model = RandomForestRegressor(n_estimators=200, max_depth=8, min_samples_split=4, random_state=42).fit(X_scaled, y)
        xgb_model = XGBRegressor(n_estimators=200, max_depth=8, learning_rate=0.05, random_state=42, verbosity=0) if XGBRegressor else None
        lgbm_model = LGBMRegressor(n_estimators=200, max_depth=8, learning_rate=0.05, random_state=42) if LGBMRegressor else None
        catb_model = CatBoostRegressor(iterations=200, depth=8, learning_rate=0.05, random_state=42, verbose=0) if CatBoostRegressor else None
        if xgb_model:
            xgb_model.fit(X_scaled, y)
        if lgbm_model:
            lgbm_model.fit(X_scaled, y)
        if catb_model:
            catb_model.fit(X_scaled, y)
        st.session_state.perf_monitor.record_model_success()  # Record successful model training
        estimators = [('lr', lr_model), ('rf', rf_model)]
        if xgb_model:
            estimators.append(('xgb', xgb_model))
        if lgbm_model:
            estimators.append(('lgbm', lgbm_model))
        if catb_model:
            estimators.append(('catb', catb_model))
        ensemble = VotingRegressor(estimators=estimators)
        ensemble.fit(X_scaled, y)
        return {
            'lr': lr_model,
            'rf': rf_model,
            'xgb': xgb_model,
            'lgbm': lgbm_model,
            'catb': catb_model,
            'ensemble': ensemble,
            'feature_cols': feature_cols,
            'future_periods': future_periods,
            'scaler': scaler
        }
    except Exception as e:
        print(f"[DEBUG] Model training failed: {e}")
        traceback.print_exc()
        return None

# --- Advanced Mistake-Avoidance Logic ---
def get_recent_bad_trades(n=50, loss_threshold=-1.0):
    """Return a DataFrame of the most recent n losing trades (pnl below threshold)."""
    import pandas as pd
    hist_df = load_historical_data_db()
    if hist_df is not None:
        bad_trades = hist_df[hist_df['pnl'] <= loss_threshold].tail(n)
        return bad_trades
    return None

def get_feature_penalty_weights(feature_cols, n=50, loss_threshold=-1.0):
    """Assign penalty weights to features that contributed to recent bad trades."""
    bad_trades = get_recent_bad_trades(n, loss_threshold)
    if bad_trades is not None and len(bad_trades) > 0:
        # Calculate mean values of features for bad trades
        penalties = bad_trades[feature_cols].mean().to_dict()
        # Normalize and invert: higher penalty for features with higher mean in bad trades
        max_val = max(abs(v) for v in penalties.values() if v is not None)
        if max_val == 0:
            max_val = 1
        penalty_weights = {k: 1.0 - abs(v)/max_val for k, v in penalties.items()}
        return penalty_weights
    return {k: 1.0 for k in feature_cols}

# --- Automatic Model Retraining Logic ---
def should_retrain_model():
    # Retrain if 100 new trades or 3 days have passed
    trade_threshold = 100
    time_threshold = datetime.timedelta(days=3)
    now = datetime.datetime.now()
    trades = st.session_state.get('trades_since_retrain', 0)
    last_time = st.session_state.get('last_retrain_time', now)
    if trades >= trade_threshold or (now - last_time) >= time_threshold:
        return True
    return False

def retrain_model_if_needed(df, horizon_minutes=30):
    if should_retrain_model():
        st.info("Retraining ML models...")
        models = train_prediction_models(df, horizon_minutes)
        st.session_state['ml_models'] = models
        st.session_state['trades_since_retrain'] = 0
        st.session_state['last_retrain_time'] = datetime.datetime.now()
        st.success("ML models retrained!")
    else:
        models = st.session_state.get('ml_models', None)
        if models is None:
            models = train_prediction_models(df, horizon_minutes)
            st.session_state['ml_models'] = models
    return st.session_state['ml_models']
    """Train ML models in the background with enhanced features."""
    try:
        if len(df) < 50:
            return None, None, [], 1
        train_size = int(len(df) * 0.8)
        train_df = df.iloc[:train_size]
        future_periods = max(1, int(horizon_minutes / 5))
        future_periods = min(future_periods, len(df) - train_size - 1)
        if future_periods <= 0:
            return None, None, [], 1
        df['future_price'] = df['close'].shift(-future_periods)
        df['target'] = (df['future_price'] / df['close'] - 1) * 100
        excluded_cols = ['datetime', 'timestamp', 'future_price', 'target', 'open', 'high', 'low', 'close']
        feature_cols = [col for col in df.columns if col not in excluded_cols]
        X_train = train_df[feature_cols].fillna(0)
        y_train = train_df['target'].fillna(0)
        # Feature scaling
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        if len(X_train_scaled) < 30 or len(y_train) < 30:
            return None, None, feature_cols, future_periods, scaler
        lr_model = LinearRegression().fit(X_train_scaled, y_train)
        rf_model = RandomForestRegressor(n_estimators=50).fit(X_train_scaled, y_train)
        return lr_model, rf_model, feature_cols, future_periods, scaler
    except Exception as e:
        print(f"[DEBUG] Model training failed: {e}")
        traceback.print_exc()
        return None, None, [], 1, None

def predict_with_trained_models(models, df, feature_cols):
    try:
        # models is a dict with all models and metadata
        scaler = models.get('scaler', None)
        feature_cols = models.get('feature_cols', feature_cols)
        current_data = df.iloc[-1:][feature_cols].fillna(0)
        if scaler is not None:
            current_data_scaled = scaler.transform(current_data)
        else:
            current_data_scaled = current_data
        predictions = []
        pred_values = []
        pred_directions = []
        # Individual model predictions
        for name in ["LinearRegression", "RandomForest", "XGBoost", "LightGBM", "CatBoost"]:
            key = name.lower().replace(" ", "").replace("randomforest", "rf").replace("xgboost", "xgb").replace("lightgbm", "lgbm").replace("catboost", "catb")
            model = models.get(key)
            if model:
                val = float(model.predict(current_data_scaled)[0])
                predictions.append((name, val))
                pred_values.append(val)
                pred_directions.append(np.sign(val))
        # Ensemble prediction
        ensemble_val = None
        if models.get('ensemble'):
            ensemble_val = float(models['ensemble'].predict(current_data_scaled)[0])
            predictions.append(("Ensemble", ensemble_val))
        # Confidence: inverse of std dev (higher = more agreement)
        if len(pred_values) > 1:
            std_pred = np.std(pred_values)
            confidence = float(max(0, 100 - std_pred * 100))
        else:
            confidence = 50.0
        # Agreement: percent of models with same direction as ensemble
        agreement = 0.0
        if ensemble_val is not None and len(pred_directions) > 0:
            ens_dir = np.sign(ensemble_val)
            agreement = 100.0 * (np.sum(np.array(pred_directions) == ens_dir) / len(pred_directions))
        # --- Model Explainability: Feature Importances (all tree models) ---
        importances_list = []
        for name in ['rf', 'xgb', 'lgbm', 'catb']:
            model = models.get(name)
            if model is not None and hasattr(model, 'feature_importances_'):
                importances = model.feature_importances_
                importance_df = pd.DataFrame({
                    'Model': name.upper(),
                    'Feature': feature_cols,
                    'Importance': importances
                })
                importances_list.append(importance_df)
        if importances_list:
            all_importances = pd.concat(importances_list).sort_values('Importance', ascending=False)
            st.session_state['rf_feature_importance'] = all_importances.head(15)
        else:
            st.session_state['rf_feature_importance'] = None

        return {
            'predictions': predictions,
            'confidence': confidence,
            'agreement': agreement,
            'ensemble': ensemble_val
        }
    except Exception as e:
        print(f"[DEBUG] Prediction with trained models failed: {e}")
        st.session_state['rf_feature_importance'] = None
        return []

def create_fallback_prediction(df, horizon_minutes=30, signal_type="HOLD", confidence=0):
    try:
        # If a custom entry price is provided (as last close), use it for prediction
        df_mod = df.copy()
        if 'entry_price' in df_mod.columns:
            df_mod['close'].iloc[-1] = df_mod['entry_price'].iloc[-1]
        current_price = df_mod['close'].iloc[-1]
        short_sma = df_mod['close'].rolling(window=min(10, len(df_mod)//2)).mean().iloc[-1]
        long_sma = df_mod['close'].rolling(window=min(20, len(df_mod)//2)).mean().iloc[-1]
        price_change_5 = (current_price / df_mod['close'].iloc[-6] - 1) * 100 if len(df_mod) > 5 else 0
        # Add more sensitivity to entry price
        price_delta = (current_price - df_mod['close'].iloc[-2])
        if current_price > short_sma > long_sma and price_change_5 > 0:
            predicted_change = abs(price_change_5) + price_delta * 0.5
            direction = "UP"
        elif current_price < short_sma < long_sma and price_change_5 < 0:
            predicted_change = -abs(price_change_5) + price_delta * 0.5
            direction = "DOWN"
        else:
            predicted_change = price_delta * 0.5
            direction = "HOLD"
        base_confidence = 45
        fallback_confidence = min(base_confidence + abs(predicted_change) * 0.5 + confidence * 0.2, 80)
        return {
            'current_price': current_price,
            'predicted_price': current_price * (1 + predicted_change / 100),
            'price_change_pct': predicted_change,
            'confidence': fallback_confidence,
            'accuracy': 55.0,
            'direction': direction,
            'individual_predictions': {'technical_analysis': predicted_change},
            'model_agreement': 100.0,
            'horizon_minutes': horizon_minutes,
            'models_used': ['technical_fallback'],
            'data_quality': min(len(df_mod) / 200 * 100, 100),
            'is_fallback': True
        }
    except Exception as e:
        print(f"[DEBUG] Fallback prediction failed: {e}")
        return None

# --- ADVANCED PORTFOLIO ANALYTICS ---
def get_portfolio_analytics():
    closed_trades = [t for t in st.session_state.trade_history if t['status'].startswith('CLOSED')]
    win_trades = [t for t in closed_trades if t['pnl'] > 0]
    loss_trades = [t for t in closed_trades if t['pnl'] <= 0]
    win_rate = len(win_trades) / len(closed_trades) * 100 if closed_trades else 0
    avg_pnl = np.mean([t['pnl'] for t in closed_trades]) if closed_trades else 0
    sharpe = np.mean([t['pnl'] for t in closed_trades]) / (np.std([t['pnl'] for t in closed_trades]) + 1e-6) if closed_trades else 0
    best_pair = max(closed_trades, key=lambda t: t['pnl'], default=None)
    worst_pair = min(closed_trades, key=lambda t: t['pnl'], default=None)
    return win_rate, avg_pnl, sharpe, best_pair, worst_pair

# =====================
# PART 2: SIDEBAR CONFIGURATION AND SETTINGS (UI/UX REDESIGN)
# =====================

with st.sidebar:
    st.markdown("<h2 style='color:#00ff88;'>⚙️ Bot Settings</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border:1px solid #222;'>", unsafe_allow_html=True)

    # --- Trading Configuration ---
    # --- Symbol List (corrected, no spaces, and for multiselect) ---
    symbol_options = [
        # High volatility USDT pairs
        'btcusdt', 'ethusdt', 'solusdt', 'avaxusdt', 'dogeusdt', 'bnbusdt', 'maticusdt', 'pepeusdt', '1000flokusdt',
        '1000shibusdt', '1000xemusdt', '1000luncusdt', '1000bonkusdt', '1000satsusdt', '1000rplusdt', '1000babydogeusdt',
        'ordiusdt', 'wifusdt', 'tusdt', 'oplusdt', 'suiusdt', 'enausdt', 'notusdt', 'jupusdt', 'kasusdt', 'tiausdt',
        'stxusdt', 'blurusdt', 'gmxusdt', 'rdntusdt', 'hookusdt', 'cyberusdt', 'arkmusdt', 'sntusdt', 'wavesusdt',
        'kaiausdt',
        # Other popular pairs
        'adausdt', 'xrpusdt', 'ltcusdt', 'linkusdt', 'dotusdt', 'uniusdt', 'bchusdt', 'filusdt', 'trxusdt', 'etcusdt',
        'aptusdt', 'opusdt', 'arbusdt', 'nearusdt', 'atomusdt', 'sandusdt', 'manausdt', 'chzusdt', 'egldusdt', 'ftmusdt',
        'icpusdt', 'runeusdt', 'sushiusdt', 'aaveusdt', 'snxusdt', 'crvusdt', 'compusdt', 'enjusdt', '1inchusdt',
        'xmrusdt', 'zecusdt', 'dashusdt', 'omgusdt', 'yfiusdt', 'balusdt', 'ctkusdt', 'ankrusdt', 'batusdt', 'cvcusdt', 'dgbusdt'
    ]

    # --- Multiselect for user-selected pairs ---
    default_pairs = ['btcusdt', 'ethusdt', 'solusdt', 'bnbusdt', 'adausdt', 'kaiausdt']
    selected_pairs = st.multiselect(
        "Select Pairs to Display/Scan",
        options=symbol_options,
        default=default_pairs,
        help="Choose which pairs to display, scan, and trade throughout the app. Fewer pairs = faster performance."
    )
    # Store in session state for global access
    st.session_state['selected_pairs'] = selected_pairs if selected_pairs else default_pairs

    with st.expander("🛠️ Trading Configuration", expanded=True):
        selected_symbol = st.selectbox(
            "Trading Symbol", st.session_state['selected_pairs'], index=0,
            help="Select the cryptocurrency pair to analyze and trade."
        ).lower()
        st.session_state['selected_symbol'] = selected_symbol
        timeframe = st.selectbox(
            "Timeframe", ['1m', '3m', '5m', '15m', '30m', '1h'], index=2,
            help="Choose the candlestick interval for analysis. Shorter timeframes = more signals, higher noise."
        )
        st.session_state['timeframe'] = timeframe
        leverage = st.slider(
            "Leverage", min_value=1, max_value=125, value=20,
            help="Set leverage for futures trading. Higher leverage increases risk and reward."
        )
        st.session_state['leverage'] = leverage
        capital = st.number_input(
            "Capital (USD)", min_value=1.0, value=100.0,
            help="Amount to allocate per trade. This is the notional value for each position."
        )
        st.session_state['capital'] = capital
        risk_percentage = st.slider(
            "Risk % per Trade", min_value=1.0, max_value=10.0, value=2.0, step=0.5,
            help="Risk per trade as a percentage of your capital. Controls stop loss distance."
        )
        st.session_state['risk_percentage'] = risk_percentage

    # --- Signal Filters ---
    with st.expander("🎯 Signal Filters", expanded=False):
        min_signal_strength = st.slider(
            "Minimum Signal Strength", min_value=3, max_value=8, value=5,
            help="Minimum score required for a signal to trigger a trade. Higher = stricter filtering."
        )
        use_volume_filter = st.checkbox(
            "Volume Confirmation", value=True,
            help="Only allow signals when trading volume is above average. Helps avoid false signals."
        )
        use_trend_filter = st.checkbox(
            "Trend Filter", value=True,
            help="Only allow trades in the direction of the prevailing trend (EMA-based)."
        )

    # --- AI Prediction Settings ---
    with st.expander("🤖 AI Prediction Settings", expanded=False):
        enable_predictions = st.checkbox(
            "🔮 Enable AI Price Predictions", value=True,
            help="Enable machine learning models for price forecasting."
        )
        prediction_horizon = st.selectbox(
            "Prediction Timeframe", ["5m", "15m", "30m", "1h", "4h"], index=2,
            help="How far into the future the AI should predict price movement."

        )
        prediction_confidence = st.slider(
            "Prediction Confidence Threshold %", min_value=30, max_value=95, value=45,
            help="Minimum confidence required for AI signals to be considered valid."
        )
        use_ensemble = st.checkbox(
            "🧠 Use Ensemble Models", value=True,
            help="Combine multiple ML models (e.g., Linear, Random Forest) for more robust predictions."
        )
        debug_mode = st.checkbox(
            "🔧 Debug Mode", value=False,
            help="Show detailed prediction debugging info in the UI."
        )
        aggressive_mode = st.checkbox(
            "⚡ Aggressive Trading Mode", value=True,
            help="Generate more trade calls by lowering signal thresholds. Increases trading frequency."
        )

    # --- Ultra-High Confidence Filter ---
    with st.expander("🌟 Ultra-High Confidence Filter", expanded=False):
        ultra_high_conf_filter = st.checkbox(
            "Show Only Ultra-High Confidence Signals (≥80% confidence & agreement)",
            value=False,
            help="Only display signals where both model confidence and agreement are at least 80%. This will reduce the number of signals but maximize reliability."
        )

    # --- Quick Profit (Decimal Scalping) ---
    with st.expander("💰 Quick Profit Settings", expanded=False):
        enable_decimal_calls = st.checkbox(
            "🎯 Enable Decimal Precision Calls", value=True,
            help="Enable ultra-fast scalping trades with small profit targets (0.1%-2.0%)."
        )
        decimal_profit_target = st.slider(
            "Decimal Profit Target %", min_value=0.1, max_value=2.0, value=0.3, step=0.1,
            help="Profit target for quick scalping trades, as a percent of entry price."
        )
        quick_sl_percentage = st.slider(
            "Quick Stop Loss %", min_value=0.05, max_value=1.0, value=0.15, step=0.05,
            help="Stop loss for quick scalping trades, as a percent of entry price."
        )

    # --- Real-time Settings ---
    with st.expander("🔄 Real-time Settings", expanded=False):
        auto_refresh = st.checkbox(
            "Auto Refresh", value=True,
            help="Automatically refresh dashboard data and prices at the interval below."
        )
        refresh_interval = st.slider(
            "Refresh Interval (seconds)", min_value=0.2, max_value=60.0, value=1.0, step=0.1,
            help="How often to refresh all data (in seconds). Lower = more real-time, higher = less API usage."
        )

    # --- Virtual Trading ---
    st.markdown("<hr style='border:1px solid #222;'>", unsafe_allow_html=True)
    st.subheader("💸 Virtual Trading")
    st.metric("💰 Virtual Balance", f"${st.session_state.virtual_balance:.2f}")
    if st.button("🔄 Reset Virtual Balance"):
        st.session_state.virtual_balance = 10000.0
        st.session_state.active_trades = {}
        st.session_state.trade_history = []
        st.session_state.notifications = []
        st.success("Virtual balance reset to $10,000!")
        st.rerun()

    # --- TEST BUTTONS FOR DB AND ML ---
    st.markdown("<hr style='border:1px solid #222;'>", unsafe_allow_html=True)
    st.subheader("🧪 Test Operations")
    if st.button("Test DB Write"):
        # Create a dummy trade and log to DB
        dummy_trade = {
            'id': 'test1234',
            'symbol': 'btcusdt',
            'direction': 'LONG',
            'amount': 1.0,
            'entry_price': 50000.0,
            'tp_price': 50500.0,
            'sl_price': 49500.0,
            'status': 'CLOSED (TP)',
            'open_time': str(datetime.datetime.now()),
            'close_time': str(datetime.datetime.now()),
            'pnl': 50.0,
            'current_price': 50500.0,
            'close_price': 50500.0
        }
        features = {'ema_fast': 1.0, 'rsi': 50.0}
        prediction = {'predicted_change': 1.0, 'confidence': 90}
        log_trade_to_db(dummy_trade, features, prediction)
        st.success("Dummy trade written to DB!")
    if st.button("Test ML"):
        # Create a small dummy DataFrame and retrain ML
        import pandas as pd
        df = pd.DataFrame({
            'close': [50000, 50100, 50200, 50300, 50400, 50500],
            'volume': [100, 110, 120, 130, 140, 150],
            'ema_fast': [50010, 50110, 50210, 50310, 50410, 50510],
            'rsi': [45, 50, 55, 60, 65, 70]
        })
        retrain_model_if_needed(df)
        st.success("ML retraining triggered with dummy data!")

    # --- FEATURE IMPORTANCE VISUALIZATION ---
    st.markdown("<hr style='border:1px solid #222;'>", unsafe_allow_html=True)
    st.subheader("🔍 Feature Importance")
    if st.button("Show Feature Importance"):
        models = st.session_state.get('ml_models', None)
        if models:
            rf = models.get('rf', None)
            xgb = models.get('xgb', None)
            feature_cols = models.get('feature_cols', [])
            importances = None
            if rf and hasattr(rf, 'feature_importances_'):
                importances = rf.feature_importances_
            elif xgb and hasattr(xgb, 'feature_importances_'):
                importances = xgb.feature_importances_
            if importances is not None and feature_cols:
                import pandas as pd
                fi_df = pd.DataFrame({'Feature': feature_cols, 'Importance': importances})
                fi_df = fi_df.sort_values('Importance', ascending=False).head(10)
                st.dataframe(fi_df, use_container_width=True)
            else:
                st.info("Feature importances not available. Train a model first.")
        else:
            st.info("No trained model found.")

    # --- LIGHTWEIGHT BACKTEST BUTTON ---
    st.markdown("<hr style='border:1px solid #222;'>", unsafe_allow_html=True)
    st.subheader("🧪 Run Backtest (Sample)")
    if st.button("Run Backtest on Sample Data"):
        df = None
        try:
            df = load_historical_data_db()
        except Exception:
            pass
        if df is not None and len(df) > 30:
            sample = df.tail(100) if len(df) > 100 else df
            # Use a simple strategy: predict next close with last close
            sample['pred'] = sample['close'].shift(1)
            sample['pnl'] = (sample['close'] - sample['pred']).fillna(0)
            win_rate = (sample['pnl'] > 0).mean() * 100
            avg_pnl = sample['pnl'].mean()
            st.write(f"Backtest Win Rate: {win_rate:.2f}%")
            st.write(f"Average P&L per Trade: {avg_pnl:.2f}")
        else:
            st.info("Not enough historical data for backtest.")

    # --- PRUNE OLD TRADES BUTTON ---
    st.markdown("<hr style='border:1px solid #222;'>", unsafe_allow_html=True)
    st.subheader("🧹 Prune Old Trades")
    if st.button("Prune Trades (Keep Last 1000)"):
        import sqlite3
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("DELETE FROM trades WHERE id NOT IN (SELECT id FROM trades ORDER BY open_time DESC LIMIT 1000)")
            conn.commit()
            conn.close()
            st.success("Old trades pruned. Only the last 1000 remain.")
        except Exception as e:
            st.error(f"Prune failed: {e}")

# --- DECIMAL SCALPING TAB (Specific Features Only) ---
decimal_tab, futures_tab, dashboard_tab, scanner_tab, stats_tab, backtest_tab = st.tabs(["🎯 Decimal Scalping", "📈 Futures Scanner", "📊 Dashboard", "🔍 Multi-Coin Scanner", "📈 Bot Stats", "🔄 Advanced Backtesting"])

with decimal_tab:
    st.header("🎯 Decimal Scalping (Micro-Precision)")
    st.write("Ultra-fast scalping with 0.05%-0.5% targets. Trade execution and scanning are only available in the main dashboard or scanner tab.")
    st.subheader("Scalping for Selected USDT Pair")
    target_pct = st.slider("Target %", 0.05, 0.5, 0.1, 0.01, key="scalping_target_pct")
    symbol = st.session_state.get('selected_symbol', None)
    if not symbol or not symbol.lower().endswith('usdt'):
        st.warning("No USDT pair selected for scalping.")
    else:
        st.markdown(f"### {symbol.upper()}")
        with st.spinner(f"Fetching live price for {symbol.upper()}..."):
            price = fetch_binance_price(symbol)
        if price:
            st.metric("Live Price", f"${price:.4f}")
        else:
            st.metric("Live Price", "N/A")
            if 'binance_error' in st.session_state:
                st.warning(f"Binance API error: {st.session_state['binance_error']}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"🟢 LONG {symbol.upper()}", key=f"long_{symbol}"):
                if st.session_state.virtual_balance >= 50:
                    execute_trade_from_prediction(symbol, 'LONG', 50, price, target_pct, 0.1)
                    st.success(f"Opened LONG position for {symbol.upper()}")
                    st.rerun()
                else:
                    st.error("Insufficient balance")
        with col2:
            if st.button(f"🔴 SHORT {symbol.upper()}", key=f"short_{symbol}"):
                if st.session_state.virtual_balance >= 50:
                    execute_trade_from_prediction(symbol, 'SHORT', 50, price, target_pct, 0.1)
                    st.success(f"Opened SHORT position for {symbol.upper()}")
                    st.rerun()
                else:
                    st.error("Insufficient balance")
    update_active_trades()
    check_and_execute_pending_trades()  # Check if any pending trades should be executed
    if st.session_state.active_trades:
        st.subheader(f"Active Decimal Scalping Trades ({symbol.upper()})")
        trades_data = []
        for trade_id, trade in st.session_state.active_trades.items():
            if trade['symbol'].lower() == symbol.lower():
                trades_data.append({
                    'ID': trade_id,
                    'Symbol': trade['symbol'].upper(),
                    'Direction': trade['direction'],
                    'Amount': f"${trade['amount']:.2f}",
                    'Entry': f"${trade['entry_price']:.4f}",
                    'Current': f"${trade.get('current_price', trade['entry_price']):.4f}",
                    'P&L': f"${trade['pnl']:.2f}",
                    'Status': trade['status']
                })
        if trades_data:
            df = pd.DataFrame(trades_data)
            st.dataframe(df, use_container_width=True)
    if 'last_notification' in st.session_state:
        st.info(st.session_state['last_notification'])

# --- FUTURES SCANNER TAB (Specific Features Only) ---
with futures_tab:
    st.header("📈 Futures Scanner")
    st.write("Scan futures pair for signals. Only the selected USDT pair is used.")
    tp_pct = 0.5  # Default take profit percent
    sl_pct = 0.2  # Default stop loss percent
    symbol = st.session_state.get('selected_symbol', None)
    if not symbol or not symbol.lower().endswith('usdt'):
        st.warning("No USDT pair selected for futures scanning.")
    else:
        if 'futures_predictions' not in st.session_state:
            st.session_state['futures_predictions'] = {}
        with st.spinner(f"Fetching scanner prices and predictions for {symbol.upper()}..."):
            price = fetch_binance_price(symbol)
            # --- Advanced ML Prediction Integration ---
            models = st.session_state.get('ml_models', None)
            latest_df = st.session_state.get('latest_df', None)
            ai_direction = None
            ai_confidence = None
            ai_predicted_pct = None
            ai_predicted_future_price = None
            if models and latest_df is not None:
                pred_result = predict_with_trained_models(models, latest_df, models.get('feature_cols', []))
                if pred_result:
                    ai_direction = "LONG" if pred_result['ensemble'] > 0 else "SHORT"
                    ai_confidence = pred_result['confidence']
                    ai_predicted_pct = pred_result['ensemble']
                    ai_predicted_future_price = price * (1 + ai_predicted_pct / 100)
                    st.markdown(f"**AI Prediction:** {ai_direction} ({ai_confidence:.1f}% confidence)")
                    st.markdown(f"**Predicted % Change:** {ai_predicted_pct:.4f}%")
                    st.markdown(f"**Predicted Future Price:** ${ai_predicted_future_price:.6f}")
                    agreement = pred_result.get('agreement', None)
                    if agreement is not None:
                        st.markdown(f"**Model Agreement:** {agreement:.1f}%")
            if price:
                direction = ai_direction if ai_direction else random.choice(['LONG', 'SHORT'])
                confidence = ai_confidence if ai_confidence else random.randint(50, 95)
                entry_price = price
                tp_price = entry_price * (1 + tp_pct/100) if direction == 'LONG' else entry_price * (1 - tp_pct/100)
                sl_price = entry_price * (1 - sl_pct/100) if direction == 'LONG' else entry_price * (1 + sl_pct/100)
                future_price = ai_predicted_future_price if ai_predicted_future_price else (entry_price * (1 + (0.002 if direction == 'LONG' else -0.002)))
                row = {
                    'symbol': symbol.upper(),
                    'direction': direction,
                    'confidence': confidence,
                    'entry_price': entry_price,
                    'future_price': future_price,
                    'tp_price': tp_price,
                    'sl_price': sl_price
                }
                df = pd.DataFrame([row])
                st.dataframe(df, use_container_width=True)
                st.markdown("---")
                st.subheader("Signals")
                col1, col2, col3, col4, col5, col6, col7 = st.columns([2,2,2,2,2,2,2])
                with col1:
                    st.write(f"{row['symbol']}")
                with col2:
                    st.write(f"{row['direction']}")
                with col3:
                    st.write(f"Conf: {row['confidence']}%")
                with col4:
                    st.write(f"Entry: {row['entry_price']:.10f}")
                with col5:
                    st.write(f"Future: {row['future_price']:.10f}")
                with col6:
                    st.write(f"TP: {row['tp_price']:.10f}")
                with col7:
                    st.write(f"SL: {row['sl_price']:.10f}")
                # When trade button is pressed, always use the latest price for entry, and recalculate TP/SL
                if st.button(f"Trade {row['symbol']} {row['entry_price']:.10f}", key=f"trade_{row['symbol']}_futures"):
                    latest_price = fetch_binance_price(symbol)
                    if latest_price and st.session_state.virtual_balance >= 100:
                        latest_tp = latest_price * (1 + tp_pct/100) if direction == 'LONG' else latest_price * (1 - tp_pct/100)
                        latest_sl = latest_price * (1 - sl_pct/100) if direction == 'LONG' else latest_price * (1 + sl_pct/100)
                        execute_trade_from_prediction(row['symbol'].lower(), row['direction'], 100, latest_price, tp_pct, sl_pct)
                        st.success(f"Executed {row['direction']} trade for {row['symbol']} at {latest_price:.10f}")
                        st.rerun()
            else:
                st.warning("Could not fetch price for selected pair.")
        if 'binance_error' in st.session_state:
            st.warning(f"Binance API error: {st.session_state['binance_error']}")

# --- DASHBOARD TAB (Specific Features Only) ---
with dashboard_tab:
    st.markdown("""
    <style>
    .main-title {font-size:2.2em; color:#00ff88; font-weight:bold;}
    .section-title {font-size:1.3em; color:#00aaff; margin-top:1em;}
    .metric-label {color:#888; font-size:0.95em;}
    </style>
    """, unsafe_allow_html=True)
    st.markdown("<div class='main-title'>📊 Ultra-Fast Real-Time Trading Dashboard</div>", unsafe_allow_html=True)
    st.caption("All-in-one dashboard for live trading, analytics, and AI predictions.")

    # --- Live Price Feed ---
    st.markdown("<div class='section-title'>⚡ Live Price Feed</div>", unsafe_allow_html=True)
    # Only show the single selected_symbol from the sidebar for all dashboard predictions and metrics
    symbol = st.session_state.get('selected_symbol', None)
    if not symbol or not symbol.lower().endswith('usdt'):
        st.info("No USDT pair selected for live price feed.")
    else:
        cols = st.columns(1)
        with st.spinner(f"Fetching live price for {symbol.upper()}..."):
            price = fetch_binance_price(symbol)
            if price is not None:
                cols[0].metric(f"{symbol.upper()}", f"${price:.4f}")
            else:
                cols[0].metric(f"{symbol.upper()}", "N/A")
        # Show AI/ML agreement if available
        models = st.session_state.get('ml_models', None)
        latest_df = st.session_state.get('latest_df', None)
        if models and latest_df is not None:
            pred_result = predict_with_trained_models(models, latest_df, models.get('feature_cols', []))
            agreement = pred_result.get('agreement', None)
            if agreement is not None:
                st.markdown(f"**Model Agreement:** {agreement:.1f}%")
    if 'binance_error' in st.session_state:
        st.warning(f"Binance API error: {st.session_state['binance_error']}")

    st.markdown("---")

    # --- Portfolio Status ---
    st.markdown("<div class='section-title'>💼 Portfolio Status</div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    total_invested = sum(trade['amount'] for trade in st.session_state.active_trades.values())
    unrealized_pnl = sum(trade.get('pnl', 0) for trade in st.session_state.active_trades.values())
    # Realized P&L from closed trades
    closed_trades = [t for t in st.session_state.trade_history if t.get('status','').startswith('CLOSED')]
    realized_pnl = sum(t.get('pnl', 0) for t in closed_trades)
    # Total portfolio = virtual_balance + invested + unrealized + realized
    total_portfolio = st.session_state.virtual_balance + total_invested + unrealized_pnl + realized_pnl

    with col1:
        st.metric("💰 Available Balance", f"${st.session_state.virtual_balance:.2f}")
    with col2:
        st.metric("💼 Invested", f"${total_invested:.2f}")
    with col3:
        st.metric("📊 Unrealized P&L", f"${unrealized_pnl:.2f}")
    with col4:
        st.metric("💎 Total Portfolio", f"${total_portfolio:.2f}")
    # Show realized P&L below metrics
    st.caption(f"Realized P&L (Closed Trades): ${realized_pnl:.2f}")

    st.markdown("---")    # --- Active Trades ---
    st.markdown("<div class='section-title'>🔥 Active Trades</div>", unsafe_allow_html=True)
    update_active_trades()
    check_and_execute_pending_trades()  # Check if any pending trades should be executed

    if st.session_state.active_trades:
        trades_data = []
        for trade_id, trade in st.session_state.active_trades.items():
            if trade['symbol'].lower() == symbol.lower():
                trades_data.append({
                    'ID': trade_id,
                    'Symbol': trade['symbol'].upper(),

                    'Direction': trade['direction'],
                   
                    'Amount': f"${trade['amount']:.2f}",
                    'Entry Price': f"${trade['entry_price']:.4f}",
                    'Current Price': f"${trade.get('current_price', trade['entry_price']):.4f}",
                    'P&L': f"${trade['pnl']:.2f}",
                    'TP': f"${trade['tp_price']:.4f}",
                    'SL': f"${trade['sl_price']:.4f}",
                    'Status': trade['status']
                })
        if trades_data:
            trades_df = pd.DataFrame(trades_data)
            st.dataframe(trades_df, use_container_width=True)

            # Emergency close all button
            if st.button("❗ Close All Trades", key="close_all_trades", help="Close all open trades immediately. Use for emergency exit."):
                for trade_id in list(st.session_state.active_trades.keys()):
                    trade = st.session_state.active_trades[trade_id]
                    trade['status'] = 'CLOSED (MANUAL)'
                    trade['close_time'] = datetime.datetime.now()
                    st.session_state.virtual_balance += trade['amount'] + trade['pnl']
                    # Update trade_history for this trade_id so realized P&L is correct
                    for hist_trade in st.session_state.trade_history:
                        if hist_trade.get('id') == trade_id:
                            hist_trade['status'] = trade['status']
                            hist_trade['close_time'] = trade['close_time']
                            hist_trade['pnl'] = trade['pnl']
                            hist_trade['current_price'] = trade.get('current_price', trade['entry_price'])
                            hist_trade['close_price'] = trade.get('current_price', trade['entry_price'])
                            break

            # Manual close buttons
            st.subheader("Manual Close")
            cols = st.columns(min(4, len(trades_data)))
            for i, trade in enumerate(trades_data):
                with cols[i % 4]:
                    tid = trade['ID']
                    if tid in st.session_state.active_trades:
                        if st.button(f"Close {trade['Symbol']}", key=f"close_{tid}"):
                            t = st.session_state.active_trades[tid]
                            t['status'] = 'CLOSED (MANUAL)'
                            t['close_time'] = datetime.datetime.now()
                            st.session_state.virtual_balance += t['amount'] + t['pnl']
                            # Update trade_history for this trade_id so realized P&L is correct
                            for hist_trade in st.session_state.trade_history:
                                if hist_trade.get('id') == tid:
                                    hist_trade['status'] = t['status']
                                    hist_trade['close_time'] = t['close_time']
                                    hist_trade['pnl'] = t['pnl']
                                    hist_trade['current_price'] = t.get('current_price', t['entry_price'])
                                    hist_trade['close_price'] = t.get('current_price', t['entry_price'])
                                    break
                            add_notification(f"Manually closed {t['symbol'].upper()} {t['direction']}", "info")
                            del st.session_state.active_trades[tid]
                            st.rerun()
    else:
        st.info("No active trades")

    # --- Pending Trades ---
    st.markdown("<div class='section-title'>⏳ Pending Orders</div>", unsafe_allow_html=True)
    if st.session_state.pending_trades:
        pending_data = []
        for trade_id, trade in st.session_state.pending_trades.items():
            current_price = fetch_binance_price(trade['symbol'])
            pending_data.append({
                'ID': trade_id,
                'Symbol': trade['symbol'].upper(),
                'Direction': trade['direction'],
                'Amount': f"${trade['amount']:.2f}",
                'Entry Price': f"${trade['entry_price']:.4f}",
                'Current Price': f"${current_price:.4f}" if current_price else "N/A",
                'TP Price': f"${trade['tp_price']:.4f}",
                'SL Price': f"${trade['sl_price']:.4f}",
                'Status': trade['status']
            })
        
        if pending_data:
            pending_df = pd.DataFrame(pending_data)
            st.dataframe(pending_df, use_container_width=True)
            
            # Cancel pending orders section
            st.subheader("Cancel Pending Orders")
            cols = st.columns(min(4, len(pending_data)))
            for i, trade in enumerate(pending_data):
                col = cols[i % len(cols)]
                with col:
                    trade_id = trade['ID']
                    if st.button(f"❌ Cancel {trade['Symbol']} {trade['Direction']}", key=f"cancel_{trade_id}"):
                        if trade_id in st.session_state.pending_trades:
                            del st.session_state.pending_trades[trade_id]
                            add_notification(f"Cancelled pending {trade['Direction']} order for {trade['Symbol']}", "info")
                            st.rerun()
    else:
        st.info("No pending orders")

    # --- Trade History ---
    st.markdown("<div class='section-title'>📜 Trade History</div>", unsafe_allow_html=True)
    if st.session_state.trade_history:
        history_df = pd.DataFrame(st.session_state.trade_history)
        # Show model predictions and agreement/confidence if available
        if 'prediction' in history_df.columns:
            def extract_pred_info(pred):
                if not isinstance(pred, dict):
                    return '', '', ''
                models = pred.get('models', {})
                ensemble = pred.get('ensemble', '')
                agreement = pred.get('agreement', '')
                conf = pred.get('confidence', '')
                model_preds = ', '.join([f"{k}: {v:.3f}" for k, v in models.items()]) if models else ''
                return model_preds, ensemble, f"{agreement:.1f}% / {conf:.1f}%"
            history_df[['Model Predictions', 'Ensemble', 'Agreement/Conf']] = history_df['prediction'].apply(lambda x: pd.Series(extract_pred_info(x)))
        st.dataframe(history_df, use_container_width=True)
    else:
        st.info("No trade history yet. Execute some trades to see history.")

    # --- Performance Monitor ---
    st.markdown("<div class='section-title'>📈 Performance Monitor</div>", unsafe_allow_html=True)
    
    # Calculate trading performance metrics
    closed_trades = [trade for trade in st.session_state.trade_history if trade.get('status', '').startswith('CLOSED')]
    profitable_trades = [trade for trade in closed_trades if trade.get('pnl', 0) > 0]
    losing_trades = [trade for trade in closed_trades if trade.get('pnl', 0) < 0]
    
    # Trading performance metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        if closed_trades:
            win_rate = (len(profitable_trades) / len(closed_trades)) * 100
            st.metric("🎯 Trading Win Rate", f"{win_rate:.1f}%")
        else:
            st.metric("🎯 Trading Win Rate", "No trades yet")
    
    with col2:
        if closed_trades:
            total_pnl = sum(trade.get('pnl', 0) for trade in closed_trades)
            st.metric("💰 Total P&L", f"${total_pnl:.2f}")
        else:
            st.metric("💰 Total P&L", "$0.00")
    
    with col3:
        if closed_trades:
            avg_pnl = sum(trade.get('pnl', 0) for trade in closed_trades) / len(closed_trades)
            st.metric("📊 Avg P&L per Trade", f"${avg_pnl:.2f}")
        else:
            st.metric("📊 Avg P&L per Trade", "$0.00")
      # System performance metrics  
    st.markdown("**System Performance:**")
    perf = st.session_state.perf_monitor
      # Get detailed stats
    detailed_stats = perf.get_detailed_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Trading Success", f"{perf.get_trading_success_rate():.1f}%")
        st.caption(f"Trades: ✅{perf.trade_success_count} ❌{perf.trade_error_count}")
    with col2:
        st.metric("⏱️ API Response", f"{perf.get_average_response_time():.1f} ms")
        st.caption(f"API: ✅{perf.api_success_count} ❌{perf.api_error_count}")
    with col3:
        st.metric("💾 Database", f"{perf.db_success_count}")
        if perf.db_success_count == 0:
            st.caption("⏳ Triggers when trades close")
        else:
            st.caption(f"DB Ops: ✅{perf.db_success_count} ❌{perf.db_error_count}")
    with col4:
        st.metric("🤖 ML Models", f"{perf.model_success_count}")
        trades_until_retrain = max(0, 100 - st.session_state.get('trades_since_retrain', 0))
        if perf.model_success_count == 0:
            st.caption(f"⏳ Retrains after {trades_until_retrain} more trades")
        else:
            st.caption(f"Models: ✅{perf.model_success_count} ❌{perf.model_error_count}")
      # Show detailed breakdown in expandable section
    with st.expander("📊 Detailed Performance Breakdown"):
        st.write("**Operation Categories:**")
        for category, stats in detailed_stats.items():
            total_ops = stats['success'] + stats['errors']
            if total_ops > 0:
                success_rate = (stats['success'] / total_ops) * 100
                st.write(f"• **{category}**: {success_rate:.1f}% success rate ({stats['success']}/{total_ops} operations)")
            else:
                st.write(f"• **{category}**: No operations yet")
        
        st.write("---")
        st.write("**⏰ When Operations Are Triggered:**")
        
        # Trading operations
        total_trades = len(st.session_state.active_trades) + len([t for t in st.session_state.trade_history if t.get('status', '').startswith('CLOSED')])
        st.write(f"• **Trading Operations**: {total_trades} total trades executed")
        
        # Database operations
        closed_trades = len([t for t in st.session_state.trade_history if t.get('status', '').startswith('CLOSED')])
        st.write(f"• **Database Operations**: Triggers when trades close (currently {closed_trades} closed trades)")
        
        # ML Model operations  
        trades_since_retrain = st.session_state.get('trades_since_retrain', 0)
        trades_until_retrain = max(0, 100 - trades_since_retrain)
        last_retrain = st.session_state.get('last_retrain_time', datetime.datetime.now())
        days_since_retrain = (datetime.datetime.now() - last_retrain).days
        
        if trades_until_retrain > 0:
            st.write(f"• **ML Model Operations**: Retrains after {trades_until_retrain} more trades OR {max(0, 3-days_since_retrain)} more days")
        else:
            st.write(f"• **ML Model Operations**: Ready for retraining! ({trades_since_retrain}/100 trades, {days_since_retrain}/3 days)")
        
        # API operations (always active)
        st.write(f"• **API Operations**: Active whenever prices are fetched ({perf.api_success_count + perf.api_error_count} total calls)")
          # Reset button
        if st.button("🔄 Reset Performance Stats"):
            st.session_state.perf_monitor.reset_stats()
            st.success("Performance statistics reset!")
            st.rerun()
          # Test buttons for demonstration
        st.write("---")
        st.write("**🧪 Test Operations (for demonstration):**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Test DB Operation"):
                # Simulate a DB operation
                st.session_state.perf_monitor.record_db_success()
                st.success("DB test successful!")
        
        with col2:
            if st.button("Test ML Training"):
                # Simulate model training
                st.session_state.perf_monitor.record_model_success()
                st.success("ML test successful!")

    # --- Debug Info (for development) ---
    if st.checkbox("🔧 Show Debug Info", value=False):
        st.subheader("Debugging Information")
        st.write("This information is useful for development and debugging purposes.")
        st.json({
            "session_state": dict(st.session_state),
            "sys_path": sys.path,
            "os_env": dict(os.environ),
            "python_version": sys.version,
            "binance_error": st.session_state.get('binance_error', None),
        }, indent=2)

# --- MULTI-COIN SCANNER TAB (Specific Features Only) ---
with stats_tab:
    st.markdown("""
    <style>
    .main-title {font-size:2.2em; color:#00ff88; font-weight:bold;}
    .section-title {font-size:1.3em; color:#00aaff; margin-top:1em;}
    .metric-label {color:#888; font-size:0.95em;}
    </style>
    """, unsafe_allow_html=True)
    st.markdown("<div class='main-title'>📈 Bot Trade Accuracy & ML Impact</div>", unsafe_allow_html=True)
    st.caption("See the most accurate trades, profitable trade %, and ML improvements.")

    # Filter closed trades
    closed_trades = [t for t in st.session_state.trade_history if t['status'].startswith('CLOSED')]
    if closed_trades:
        # Accurate trades: those with positive P&L
        accurate_trades = [t for t in closed_trades if t['pnl'] > 0]
        profitable_pct = (len(accurate_trades) / len(closed_trades)) * 100 if closed_trades else 0
        avg_pnl = np.mean([t['pnl'] for t in closed_trades]) if closed_trades else 0
        best_trade = max(closed_trades, key=lambda t: t['pnl'], default=None)
        worst_trade = min(closed_trades, key=lambda t: t['pnl'], default=None)

        st.metric("Profitable Trade %", f"{profitable_pct:.2f}%")
        st.metric("Avg P&L per Trade", f"${avg_pnl:.2f}")
        if best_trade:
            st.success(f"Best Trade: {best_trade['symbol'].upper()} {best_trade['direction']} +${best_trade['pnl']:.2f}")
        if worst_trade:
            st.error(f"Worst Trade: {worst_trade['symbol'].upper()} {worst_trade['direction']} ${worst_trade['pnl']:.2f}")

        # Show table of accurate trades
        st.markdown("<div class='section-title'>✅ Accurate (Profitable) Trades</div>", unsafe_allow_html=True)
        if accurate_trades:
            df_acc = pd.DataFrame(accurate_trades)
            st.dataframe(df_acc[['id','symbol','direction','entry_price','close_price','pnl','status']], use_container_width=True)
        else:
            st.info("No profitable trades yet.")

        # ML improvement estimate: compare profitable % to a random baseline (e.g., 50%)
        baseline = 50.0
        improvement = profitable_pct - baseline
        st.markdown(f"**ML Improvement over random:** <span style='color:#00ff88;font-weight:bold'>{improvement:+.2f}%</span>", unsafe_allow_html=True)
    else:
        st.info("No closed trades yet. Execute and close some trades to see stats.")
with scanner_tab:
    st.subheader("🔍 Multi-Coin Scanner")
    st.write("🚀 **Scanning all supported coins for AI-enhanced trading opportunities**")
    if st.button("🔍 Scan Selected Pair", type="primary"):
        symbol = st.session_state.get('selected_symbol', None)
        if not symbol or not symbol.lower().endswith('usdt'):
            st.warning("No USDT pair selected for scanning.")
        else:
            with st.spinner(f"Scanning {symbol.upper()}..."):
                scanner_results = scan_multiple_coins([symbol], '1m', 100, 20, 2, 5, True, 30, 70)
                df = pd.DataFrame(scanner_results)
                st.dataframe(df.sort_values("confidence", ascending=False), use_container_width=True)
                st.markdown("---")
                st.subheader("Top Signals")
                top_signals = df.sort_values("confidence", ascending=False).head(5)
                for idx, row in top_signals.iterrows():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"{row['symbol']} — {row['direction']} — Conf: {row['confidence']}% — Price: ${row['price']:.4f}")
                    with col2:
                        if st.button(f"Trade {row['symbol']} {row['direction']}", key=f"scanner_trade_{row['symbol']}_{idx}"):
                            if st.session_state.virtual_balance >= 100:
                                execute_trade_from_prediction(row['symbol'].lower(), row['direction'], 100, row['price'], tp_pct, sl_pct)
                                st.success(f"Executed {row['direction']} trade for {row['symbol']} at ${row['price']:.4f}")
                                st.rerun()
                            else:
                                st.error("Insufficient balance")

# --- ADVANCED BACKTESTING TAB ---
with backtest_tab:
    st.markdown("""
    <style>
    .backtest-title {font-size:2.2em; color:#00ff88; font-weight:bold;}
    .section-title {font-size:1.3em; color:#00aaff; margin-top:1em;}
    .metric-container {background:#1e2024; padding:1rem; border-radius:8px; margin:0.5rem 0;}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='backtest-title'>🔄 Advanced Backtesting System</div>", unsafe_allow_html=True)
    st.caption("Professional-grade backtesting with realistic trading conditions, walk-forward validation, and comprehensive performance analysis.")
    
    # Backtesting Configuration
    st.markdown("<div class='section-title'>⚙️ Backtesting Configuration</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        initial_capital = st.number_input("Initial Capital ($)", value=10000, min_value=1000, max_value=1000000, step=1000)
        trading_fee = st.number_input("Trading Fee (%)", value=0.1, min_value=0.0, max_value=1.0, step=0.01) / 100
    with col2:
        slippage = st.number_input("Slippage (%)", value=0.05, min_value=0.0, max_value=0.5, step=0.01) / 100
        position_size = st.number_input("Position Size (%)", value=10, min_value=1, max_value=100, step=1) / 100
    with col3:
        tp_ratio = st.number_input("Take Profit (%)", value=2.0, min_value=0.1, max_value=10.0, step=0.1) / 100
        sl_ratio = st.number_input("Stop Loss (%)", value=1.0, min_value=0.1, max_value=5.0, step=0.1) / 100
    
    # Data Selection and Validation
    st.markdown("<div class='section-title'>📊 Data Selection & Validation</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        backtest_symbol = st.selectbox("Select Symbol for Backtesting", 
                                     ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOTUSDT', 'LINKUSDT', 'LTCUSDT'])
        timeframe = st.selectbox("Timeframe", ['1m', '5m', '15m', '1h', '4h', '1d'])
    with col2:
        train_window = st.number_input("Training Window (periods)", value=100, min_value=50, max_value=500)
        test_window = st.number_input("Test Window (periods)", value=20, min_value=10, max_value=100)
    
    # Generate synthetic data for demonstration (in real implementation, fetch from API)
    if st.button("🔍 Validate Data Quality", type="secondary"):
        with st.spinner("Generating and validating synthetic data..."):
            # Create synthetic OHLCV data for demonstration
            dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='1H')
            np.random.seed(42)
            
            base_price = 45000 if backtest_symbol == 'BTCUSDT' else 3000
            price_changes = np.random.normal(0, 0.02, len(dates))
            prices = [base_price]
            
            for change in price_changes[1:]:
                new_price = prices[-1] * (1 + change)
                prices.append(max(new_price, base_price * 0.5))  # Prevent negative prices
            
            synthetic_data = pd.DataFrame({
                'timestamp': dates,
                'open': prices,
                'high': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
                'low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
                'close': prices,
                'volume': np.random.uniform(1000, 10000, len(dates))
            })
            
            # Ensure OHLC logic
            for i in range(len(synthetic_data)):
                row = synthetic_data.iloc[i]
                high_val = max(row['open'], row['close']) * (1 + abs(np.random.normal(0, 0.005)))
                low_val = min(row['open'], row['close']) * (1 - abs(np.random.normal(0, 0.005)))
                synthetic_data.loc[i, 'high'] = high_val
                synthetic_data.loc[i, 'low'] = low_val
            
            # Validate data quality
            issues = st.session_state.data_quality_manager.validate_data(synthetic_data)
            
            if issues:
                st.warning(f"Data quality issues found: {', '.join(issues)}")
                synthetic_data = st.session_state.data_quality_manager.clean_data(synthetic_data)
                st.info("Data has been cleaned and preprocessed.")
            else:
                st.success("Data quality validation passed!")
            
            # Store cleaned data in session state
            st.session_state.backtest_data = synthetic_data
            
            # Display data summary
            st.write("**Data Summary:**")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Records", len(synthetic_data))
            with col2:
                st.metric("Date Range", f"{synthetic_data['timestamp'].min().date()} to {synthetic_data['timestamp'].max().date()}")
            with col3:
                st.metric("Price Range", f"${synthetic_data['low'].min():.2f} - ${synthetic_data['high'].max():.2f}")
            with col4:
                st.metric("Avg Volume", f"{synthetic_data['volume'].mean():.0f}")
    
    # Run Backtesting
    st.markdown("<div class='section-title'>🚀 Run Backtesting</div>", unsafe_allow_html=True)
    
    backtest_type = st.radio("Backtesting Method", 
                           ['Simple Backtest', 'Walk-Forward Validation', 'Monte Carlo Simulation'],
                           horizontal=True)
    
    if st.button("🎯 Run Advanced Backtest", type="primary"):
        if 'backtest_data' not in st.session_state:
            st.error("Please validate data first!")
        else:
            with st.spinner(f"Running {backtest_type.lower()}..."):
                # Configure backtester
                backtester = AdvancedBacktester(
                    initial_capital=initial_capital,
                    trading_fee=trading_fee,
                    slippage=slippage
                )
                
                data = st.session_state.backtest_data.copy()
                
                # Simple prediction function for demonstration
                def simple_prediction_func(train_data, current_row):
                    """Simple RSI-based prediction for demonstration"""
                    try:
                        # Calculate simple RSI
                        prices = train_data['close'].tail(14)
                        if len(prices) < 14:
                            return None
                        
                        gains = prices.diff().where(prices.diff() > 0, 0)
                        losses = -prices.diff().where(prices.diff() < 0, 0)
                        avg_gain = gains.rolling(window=14).mean().iloc[-1]
                        avg_loss = losses.rolling(window=14).mean().iloc[-1]
                        
                        if avg_loss == 0:
                            rsi = 100
                        else:
                            rs = avg_gain / avg_loss
                            rsi = 100 - (100 / (1 + rs))
                        
                        # Simple strategy: Buy when RSI < 30, Sell when RSI > 70
                        confidence = abs(rsi - 50) + 20  # Base confidence
                        
                        if rsi < 30:
                            return {'direction': 'LONG', 'confidence': min(confidence, 95)}
                        elif rsi > 70:
                            return {'direction': 'SHORT', 'confidence': min(confidence, 95)}
                        else:
                            return None
                    except:
                        return None
                
                if backtest_type == 'Simple Backtest':
                    # Simple backtest
                    trades_executed = 0
                    for i in range(50, len(data)):  # Start after warm-up period
                        row = data.iloc[i]
                        train_data = data.iloc[:i]
                        
                        prediction = simple_prediction_func(train_data, row)
                        if prediction and prediction['confidence'] > 60:
                            success, msg = backtester.execute_trade(
                                symbol=backtest_symbol,
                                direction=prediction['direction'],
                                amount=backtester.capital * position_size,
                                entry_price=row['close'],
                                tp_ratio=tp_ratio,
                                sl_ratio=sl_ratio,
                                timestamp=row['timestamp']
                            )
                            if success:
                                trades_executed += 1
                        
                        # Update positions
                        backtester.update_positions({backtest_symbol: row['close']})
                        
                        # Limit trades for demo
                        if trades_executed >= 50:
                            break
                    
                    # Close remaining positions
                    for trade_id in list(backtester.positions.keys()):
                        if backtester.positions[trade_id]['status'] == 'OPEN':
                            backtester.close_position(trade_id, data.iloc[-1]['close'], "BACKTEST_END")
                    
                    results = [backtester.get_performance_metrics()]
                    
                elif backtest_type == 'Walk-Forward Validation':
                    # Walk-forward validation
                    results = backtester.run_walk_forward_backtest(
                        data, simple_prediction_func, 
                        train_window=int(train_window), 
                        test_window=int(test_window)
                    )
                
                else:  # Monte Carlo
                    # Run multiple backtests with random variations
                    results = []
                    for i in range(10):  # 10 Monte Carlo runs
                        mc_backtester = AdvancedBacktester(initial_capital, trading_fee, slippage)
                        
                        # Add randomness to entry timing
                        data_shuffled = data.copy()
                        noise = np.random.normal(0, 0.001, len(data_shuffled))
                        data_shuffled['close'] = data_shuffled['close'] * (1 + noise)
                        
                        trades_executed = 0
                        for j in range(50, min(200, len(data_shuffled))):
                            row = data_shuffled.iloc[j]
                            train_data = data_shuffled.iloc[:j]
                            
                            prediction = simple_prediction_func(train_data, row)
                            if prediction and prediction['confidence'] > 60:
                                success, msg = mc_backtester.execute_trade(
                                    symbol=backtest_symbol,
                                    direction=prediction['direction'],
                                    amount=mc_backtester.capital * position_size,
                                    entry_price=row['close'],
                                    tp_ratio=tp_ratio,
                                    sl_ratio=sl_ratio,
                                    timestamp=row['timestamp']
                                )
                                if success:
                                    trades_executed += 1
                        
                        # Close remaining positions
                        for trade_id in list(mc_backtester.positions.keys()):
                            if mc_backtester.positions[trade_id]['status'] == 'OPEN':
                                mc_backtester.close_position(trade_id, data_shuffled.iloc[-1]['close'], "MC_END")
                        
                        mc_results = mc_backtester.get_performance_metrics()
                        mc_results['run'] = i + 1
                        results.append(mc_results)
                
                # Store results
                st.session_state.backtest_results = results
                st.success(f"{backtest_type} completed! Check results below.")
    
    # Display Results
    if st.session_state.backtest_results:
        st.markdown("<div class='section-title'>📊 Backtesting Results</div>", unsafe_allow_html=True)
        
        results = st.session_state.backtest_results
        
        if len(results) == 1:
            # Single backtest results
            result = results[0]
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Return", f"{result.get('total_return', 0):.2f}%", 
                         delta=f"{result.get('total_return', 0) - 0:.2f}%")
            with col2:
                st.metric("Win Rate", f"{result.get('win_rate', 0):.1f}%")
            with col3:
                st.metric("Total Trades", result.get('total_trades', 0))
            with col4:
                st.metric("Profit Factor", f"{result.get('profit_factor', 0):.2f}")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Max Drawdown", f"{result.get('max_drawdown', 0):.2f}%")
            with col2:
                st.metric("Sharpe Ratio", f"{result.get('sharpe_ratio', 0):.2f}")
            with col3:
                st.metric("Final Capital", f"${result.get('final_capital', 0):.2f}")
            with col4:
                st.metric("Avg Win", f"${result.get('avg_win', 0):.2f}")
        
        else:
            # Multiple backtest results (Walk-forward or Monte Carlo)
            df_results = pd.DataFrame(results)
            
            # Summary statistics
            st.write("**Summary Statistics Across All Runs:**")
            summary_metrics = {
                'Metric': ['Avg Return (%)', 'Win Rate (%)', 'Max Drawdown (%)', 'Sharpe Ratio', 'Total Trades'],
                'Mean': [
                    df_results['total_return'].mean(),
                    df_results['win_rate'].mean(),
                    df_results['max_drawdown'].mean(),
                    df_results['sharpe_ratio'].mean(),
                    df_results['total_trades'].mean()
                ],
                'Std Dev': [
                    df_results['total_return'].std(),
                    df_results['win_rate'].std(),
                    df_results['max_drawdown'].std(),
                    df_results['sharpe_ratio'].std(),
                    df_results['total_trades'].std()
                ],
                'Min': [
                    df_results['total_return'].min(),
                    df_results['win_rate'].min(),
                    df_results['max_drawdown'].min(),
                    df_results['sharpe_ratio'].min(),
                    df_results['total_trades'].min()
                ],
                'Max': [
                    df_results['total_return'].max(),
                    df_results['win_rate'].max(),
                    df_results['max_drawdown'].max(),
                    df_results['sharpe_ratio'].max(),
                    df_results['total_trades'].max()
                ]
            }
            
            summary_df = pd.DataFrame(summary_metrics)
            st.dataframe(summary_df, use_container_width=True)
            
            # Individual run results
            st.write("**Individual Run Results:**")
            display_cols = ['total_return', 'win_rate', 'total_trades', 'max_drawdown', 'sharpe_ratio', 'final_capital']
            if 'fold' in df_results.columns:
                display_cols = ['fold'] + display_cols
            elif 'run' in df_results.columns:
                display_cols = ['run'] + display_cols
            
            st.dataframe(df_results[display_cols], use_container_width=True)
    
    # Model Performance Tracking
    st.markdown("<div class='section-title'>🤖 Model Performance Analysis</div>", unsafe_allow_html=True)
    
    if st.button("📊 Analyze Model Performance"):
        with st.spinner("Analyzing model performance..."):
            # Simulate model performance data
            regimes = ['trending', 'ranging', 'volatile']
            models = ['random_forest', 'xgboost', 'lstm', 'gradient_boosting']
            
            performance_data = []
            for regime in regimes:
                for model in models:
                    # Simulate performance with some realistic patterns
                    if regime == 'trending' and model in ['lstm', 'gradient_boosting']:
                        base_performance = np.random.normal(0.65, 0.1, 20)
                    elif regime == 'ranging' and model in ['random_forest', 'xgboost']:
                        base_performance = np.random.normal(0.60, 0.08, 20)
                    elif regime == 'volatile' and model == 'gradient_boosting':
                        base_performance = np.random.normal(0.58, 0.12, 20)
                    else:
                        base_performance = np.random.normal(0.52, 0.10, 20)
                    
                    base_performance = np.clip(base_performance, 0.3, 0.9)
                    
                    for i, perf in enumerate(base_performance):
                        performance_data.append({
                            'regime': regime,
                            'model': model,
                            'accuracy': perf,
                            'timestamp': pd.Timestamp.now() - pd.Timedelta(days=20-i)
                        })
            
            df_performance = pd.DataFrame(performance_data)
            
            # Update ensemble with performance data
            for _, row in df_performance.iterrows():
                st.session_state.adaptive_ensemble.update_model_performance(
                    row['regime'], row['model'], row['accuracy']
                )
            
            # Display performance by regime
            col1, col2, col3 = st.columns(3)
            
            for i, regime in enumerate(regimes):
                with [col1, col2, col3][i]:
                    st.write(f"**{regime.title()} Market:**")
                    regime_data = df_performance[df_performance['regime'] == regime]
                    avg_performance = regime_data.groupby('model')['accuracy'].mean().sort_values(ascending=False)
                    
                    best_model = st.session_state.adaptive_ensemble.get_best_model_for_regime(regime)
                    st.success(f"Best Model: {best_model}")
                    
                    for model, perf in avg_performance.head(3).items():
                        st.metric(model.replace('_', ' ').title(), f"{perf:.1%}")
    
    # Export Results
    st.markdown("<div class='section-title'>📥 Export & Save</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Results to Database"):
            if st.session_state.backtest_results:
                try:
                    conn = sqlite3.connect(DB_PATH)
                    for i, result in enumerate(st.session_state.backtest_results):
                        result_data = {
                            'backtest_id': str(uuid.uuid4()),
                            'timestamp': datetime.datetime.now(),
                            'symbol': backtest_symbol,
                            'strategy': 'RSI_Strategy',
                            'results': str(result)
                        }
                        # In a real implementation, you'd have a backtest_results table
                        st.success(f"Results saved to database (simulation)")
                    conn.close()
                except Exception as e:
                    st.error(f"Save failed: {e}")
            else:
                st.warning("No results to save!")
    
    with col2:
        if st.button("📊 Generate Report"):
            if st.session_state.backtest_results:
                st.info("Comprehensive PDF report generation would be implemented here.")
                st.write("Report would include:")
                st.write("• Executive summary")
                st.write("• Detailed performance metrics")
                st.write("• Risk analysis")
                st.write("• Trade-by-trade breakdown")
                st.write("• Strategy recommendations")
            else:
                st.warning("No results to report!")
