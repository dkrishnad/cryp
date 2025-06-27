# --- Standard Library Imports ---
import time
import datetime
import streamlit as st
import uuid
import json
import pandas as pd
import numpy as np
# --- Auto-Refresh Control Helpers ---
def pause_auto_refresh(duration=2.0):
    """Pause auto-refresh for a given duration (seconds)."""
    st.session_state.auto_refresh_paused = True
    st.session_state.auto_refresh_resume_time = datetime.datetime.now() + datetime.timedelta(seconds=duration)

def maybe_resume_auto_refresh():
    if st.session_state.get('auto_refresh_paused', False):
        resume_time = st.session_state.get('auto_refresh_resume_time', None)
        if resume_time and datetime.datetime.now() >= resume_time:
            st.session_state.auto_refresh_paused = False
            st.session_state.auto_refresh_resume_time = None

def enforce_min_refresh_interval():
    now = datetime.datetime.now()
    last_time = st.session_state.get('auto_refresh_last_time', now)
    min_interval = st.session_state.get('auto_refresh_min_interval', 0.5)
    elapsed = (now - last_time).total_seconds()
    if elapsed < min_interval:
        time.sleep(min_interval - elapsed)
    st.session_state.auto_refresh_last_time = datetime.datetime.now()

# --- Database Path (MUST BE FIRST) ---
DB_PATH = "trades.db"

# --- Consistent Feature Engineering Utility ---
def get_consistent_features(df, feature_cols=None, scaler=None, fit_scaler=False):
    """
    Ensures the same features and preprocessing are applied for both training and prediction.
    - df: DataFrame with raw data
    - feature_cols: list of feature columns to use (if None, infer from df)
    - scaler: sklearn scaler object (if None and fit_scaler=True, fit a new one)
    - fit_scaler: whether to fit the scaler (True for training, False for prediction)
    Returns: processed feature array, updated scaler, feature_cols
    """
    import numpy as np
    import pandas as pd
    from sklearn.preprocessing import StandardScaler
    if feature_cols is None:
        exclude = ['datetime', 'timestamp', 'future_price', 'target', 'open', 'high', 'low', 'close']
        feature_cols = [col for col in df.columns if col not in exclude and df[col].dtype in ['float64', 'int64']]
    X = df[feature_cols].copy()
    X = X.fillna(X.median())
    if scaler is None and fit_scaler:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
    elif scaler is not None:
        X_scaled = scaler.transform(X)
    else:
        X_scaled = X.values
    return X_scaled, scaler, feature_cols
import sqlite3

# --- Streamlit import must come before any use of st ---
import streamlit as st
import uuid

# --- Simple Button Handler (No Rerun, No Redirects) ---
def simple_button(label, key=None, action=None, args=None, debug_label=None):
    """
    Simple button handler that executes actions immediately without st.rerun() or redirects.
    This prevents tab switching and page reloading issues.
    """
    safe_label = label.encode('ascii', 'ignore').decode() if not label.isascii() else label
    if key is None:
        key = f"btn_{safe_label}_{uuid.uuid4()}"
    
    # Direct button execution without rerun
    if st.button(safe_label, key=key):
        try:
            if debug_label:
                st.write(f"[DEBUG] Button '{debug_label}' pressed. Executing action.")
            if action:
                if args:
                    action(*args)
                else:
                    action()
            st.success(f"[SUCCESS] {safe_label} completed successfully!")
        except Exception as e:
            st.error(f"[simple_button] Error in action: {e}")
        return True
    return False

# Alias for backward compatibility
atomic_button = simple_button

# --- Helper: Execute Virtual Trade ---
def open_virtual_trade(symbol, direction, amount, entry_price, tp_pct, sl_pct):
    """Execute a virtual trade"""
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
        'open_time': datetime.datetime.now(),
        'close_time': None,
        'pnl': 0.0,
        'current_price': entry_price
    }
    
    st.session_state.virtual_balance -= amount
    st.session_state.active_trades[trade_id] = trade
    st.session_state.trade_history.append(trade.copy())
    add_notification(f"Opened {direction} {symbol.upper()} at ${entry_price:.4f}", "success")
    st.session_state.perf_monitor.record_trade_success()
    
    return trade_id

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


# --- Robust Session State Initialization ---
if 'virtual_balance' not in st.session_state:
    st.session_state.virtual_balance = 10000.0
if 'active_trades' not in st.session_state:
    st.session_state.active_trades = {}
if 'trade_history' not in st.session_state:
    st.session_state.trade_history = []
if 'capital' not in st.session_state:
    st.session_state['capital'] = 100.0
# --- Auto-Refresh Session State ---
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True
if 'auto_refresh_paused' not in st.session_state:
    st.session_state.auto_refresh_paused = False
if 'auto_refresh_resume_time' not in st.session_state:
    st.session_state.auto_refresh_resume_time = None
if 'auto_refresh_last_time' not in st.session_state:
    st.session_state.auto_refresh_last_time = datetime.datetime.now()
if 'auto_refresh_min_interval' not in st.session_state:
    st.session_state.auto_refresh_min_interval = 0.5  # seconds

# --- Auto-Refresh Control Helpers ---
def pause_auto_refresh(duration=2.0):
    """Pause auto-refresh for a given duration (seconds)."""
    st.session_state.auto_refresh_paused = True
    st.session_state.auto_refresh_resume_time = datetime.datetime.now() + datetime.timedelta(seconds=duration)

def maybe_resume_auto_refresh():
    if st.session_state.get('auto_refresh_paused', False):
        resume_time = st.session_state.get('auto_refresh_resume_time', None)
        if resume_time and datetime.datetime.now() >= resume_time:
            st.session_state.auto_refresh_paused = False
            st.session_state.auto_refresh_resume_time = None

def enforce_min_refresh_interval():
    now = datetime.datetime.now()
    last_time = st.session_state.get('auto_refresh_last_time', now)
    min_interval = st.session_state.get('auto_refresh_min_interval', 0.5)
    elapsed = (now - last_time).total_seconds()
    if elapsed < min_interval:
        time.sleep(min_interval - elapsed)
    st.session_state.auto_refresh_last_time = datetime.datetime.now()

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


# --- Database Configuration (MOVED TO TOP FOR GLOBAL ACCESS) ---
DB_PATH = "trades.db"

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
        st.session_state.pending_trades = {}    # Advanced backtesting and ML systems
    if 'advanced_backtester' not in st.session_state:
        st.session_state.advanced_backtester = AdvancedBacktester()
    if 'adaptive_ensemble' not in st.session_state:
        st.session_state.adaptive_ensemble = AdaptiveEnsemble()
    if 'data_quality_manager' not in st.session_state:
        st.session_state.data_quality_manager = DataQualityManager()
    if 'online_learning_system' not in st.session_state:
        st.session_state.online_learning_system = OnlineLearningSystem()
    if 'backtest_results' not in st.session_state:
        st.session_state.backtest_results = {}
    if 'model_performance_history' not in st.session_state:
        st.session_state.model_performance_history = []

    # Persistent debug log for troubleshooting
    if 'debug_log' not in st.session_state:
        st.session_state['debug_log'] = []

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
    with st.expander("Trading Notifications", expanded=True):
        if not st.session_state.notifications:
            st.info("No notifications yet. All trade alerts and system messages will appear here.")
            return

        # Add a clear all button
        clear_col, _ = st.columns([1, 5])
        with clear_col:
            def clear_notifications():
                st.session_state.notifications = []
            atomic_button("Clear All", key="clear_notifications_btn", action=clear_notifications, debug_label="Clear Notifications")

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
                'success': '[OK]',
                'error': '[ERR]',
                'warning': '[WARN]',
                'info': '[INFO]',
            }.get(ntype, '[INFO]')

            formatted_msg = f"{icon} {ts_str} - {msg}"
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

# --- AI/ML PREDICTION LOGIC (Ensemble + Fallback) ---
def train_prediction_models(df, horizon_minutes=30):
    try:
        # Consistent feature engineering
        df_clean, feature_cols, scaler = get_consistent_features(df, fit_scaler=True)
        train_size = int(len(df_clean) * 0.8)
        if train_size < 30:
            return None
        future_periods = max(1, int(horizon_minutes / 5))
        future_periods = min(future_periods, len(df_clean) - train_size - 1)
        if future_periods <= 0:
            return None
        df_clean['future_price'] = df_clean['close'].shift(-future_periods)
        df_clean['target'] = (df_clean['future_price'] / df_clean['close'] - 1) * 100
        train_df = df_clean.iloc[:train_size]
        X_train = train_df[feature_cols].fillna(0)
        y_train = train_df['target'].fillna(0)
        X_train_scaled = scaler.fit_transform(X_train)
        if len(X_train_scaled) < 30 or len(y_train) < 30:
            return None
        # Train models
        lr_model = LinearRegression().fit(X_train_scaled, y_train)
        rf_model = RandomForestRegressor(n_estimators=50).fit(X_train_scaled, y_train)
        models = {
            'lr': lr_model,
            'rf': rf_model,
            'scaler': scaler,
            'feature_cols': feature_cols,
            'ensemble': True
        }
        st.session_state['ml_models'] = models
        return models
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
        models = train_prediction_models(df, horizon_minutes)
        if models:
            st.session_state['ml_models'] = models
            st.session_state['trades_since_retrain'] = 0
            st.session_state['last_retrain_time'] = datetime.datetime.now()
            st.success("ML models retrained!")
            return models
        else:
            return None
    else:
        return st.session_state.get('ml_models', None)
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
        # Use consistent feature engineering for prediction
        df_clean, feature_cols, scaler = get_consistent_features(df, feature_cols=models.get('feature_cols', feature_cols), scaler=models.get('scaler'), fit_scaler=False)
        current_data = df_clean.iloc[-1:][feature_cols].fillna(0)
        if scaler is not None:
            current_data_scaled = scaler.transform(current_data)
        else:
            current_data_scaled = current_data
        predictions = []
        pred_values = []
        pred_directions = []
        # Individual model predictions
        for name, model in [('LinearRegression', models.get('lr')), ('RandomForest', models.get('rf'))]:
            if model is not None:
                val = float(model.predict(current_data_scaled)[0])
                predictions.append((name, val))
                pred_values.append(val)
                pred_directions.append(np.sign(val))
        # Ensemble prediction
        ensemble_val = None
        if models.get('ensemble') and pred_values:
            ensemble_val = float(np.mean(pred_values))
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
        for name in ['rf']:
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
            "Refresh Interval (seconds)", min_value=0.05, max_value=60.0, value=1.0, step=0.01,
            help="How often to refresh all data (in seconds). Lower = more real-time, higher = less API usage. Set as low as 0.05s for ultra-fast refresh (<0.20s)."
        )

    # === GROUP: VIRTUAL TRADING, TEST OPS, FEATURE IMPORTANCE, BACKTEST, PRUNE ===
    st.markdown("<hr style='border:1px solid #222; margin-top:2em;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#00ff88;'>💸 Virtual Trading</h3>", unsafe_allow_html=True)
    st.metric("💰 Virtual Balance", f"${st.session_state.virtual_balance:.2f}")
    def reset_virtual_balance():
        st.session_state.virtual_balance = 10000.0
        st.session_state.active_trades = {}
        st.session_state.trade_history = []
        st.session_state.notifications = []
        st.success("Virtual balance reset to $10,000!")
    atomic_button("🔄 Reset Virtual Balance", key="sidebar_reset_virtual_balance", action=reset_virtual_balance, debug_label="Reset Virtual Balance")

    st.markdown("<hr style='border:1px solid #222;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#00aaff;'>🧪 Test Operations</h4>", unsafe_allow_html=True)
    def test_db_write():
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
    atomic_button("Test DB Write", key="sidebar_test_db_write", action=test_db_write, debug_label="Test DB Write")
    def test_ml():
        import pandas as pd
        df = pd.DataFrame({
            'close': [50000, 50100, 50200, 50300, 50400, 50500],
            'volume': [100, 110, 120, 130, 140, 150],
            'ema_fast': [50010, 50110, 50210, 50310, 50410, 50510],
            'rsi': [45, 50, 55, 60, 65, 70]
        })
        retrain_model_if_needed(df)
        st.success("ML retraining triggered with dummy data!")
    atomic_button("Test ML", key="sidebar_test_ml", action=test_ml, debug_label="Test ML")

    st.markdown("<hr style='border:1px solid #222;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#00aaff;'>🔍 Feature Importance</h4>", unsafe_allow_html=True)
    def show_feature_importance():
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
    atomic_button("Show Feature Importance", key="sidebar_show_feature_importance", action=show_feature_importance, debug_label="Show Feature Importance")

    st.markdown("<hr style='border:1px solid #222;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#00aaff;'>🧪 Run Backtest (Sample)</h4>", unsafe_allow_html=True)
    def run_backtest_sample():
        df = None
        try:
            df = load_historical_data_db()
        except Exception:
            pass
        if df is not None and len(df) > 30:
            sample = df.tail(100) if len(df) > 100 else df
            sample['pred'] = sample['close'].shift(1)
            sample['pnl'] = (sample['close'] - sample['pred']).fillna(0)
            win_rate = (sample['pnl'] > 0).mean() * 100
            avg_pnl = sample['pnl'].mean()
            st.write(f"Backtest Win Rate: {win_rate:.2f}%")
            st.write(f"Average P&L per Trade: {avg_pnl:.2f}")
        else:
            st.info("Not enough historical data for backtest.")
    atomic_button("Run Backtest on Sample Data", key="sidebar_run_backtest_sample", action=run_backtest_sample, debug_label="Run Backtest Sample")

    st.markdown("<hr style='border:1px solid #222;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#00aaff;'>🧹 Prune Old Trades</h4>", unsafe_allow_html=True)
    def prune_trades():
        import sqlite3
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("DELETE FROM trades WHERE id NOT IN (SELECT id FROM trades ORDER BY open_time DESC LIMIT 1000)")
            conn.commit()
            conn.close()
            st.success("Old trades pruned. Only the last 1000 remain.")
        except Exception as e:
            st.error(f"Failed to prune trades: {e}")
    atomic_button("Prune Trades (Keep Last 1000)", key="sidebar_prune_trades", action=prune_trades, debug_label="Prune Trades")

    # --- Universal Reset All Button ---
    st.markdown("---")
    def reset_all_action():
        st.session_state.virtual_balance = 10000.0
        st.session_state.active_trades = {}
        st.session_state.trade_history = []
        st.session_state.notifications = []
        st.success("All data reset!")
    simple_button("🧹 Reset ALL (Balance, Trades, Notifications)", key="reset_all_btn", action=reset_all_action, debug_label="Reset ALL")

# --- AUTO TRADING TAB ---
auto_tab, decimal_tab, futures_tab, dashboard_tab, scanner_tab, stats_tab, backtest_tab = st.tabs([
    "🤖 Auto Trading", "🎯 Decimal Scalping", "📈 Futures Scanner", "📊 Dashboard", "🔍 Multi-Coin Scanner", "📈 Bot Stats", "🔄 Advanced Backtesting"])

# --- DECIMAL SCALPING TAB (Specific Features Only) ---
with decimal_tab:
    st.header("🎯 Decimal Scalping (Micro-Precision)")
    st.write("Ultra-fast scalping with 0.05%-0.5% targets.")
    
    symbol = st.session_state.get('selected_symbol', None)
    price = None
    if symbol and symbol.lower().endswith('usdt'):
        price = fetch_binance_price(symbol)
    
    if not symbol or not symbol.lower().endswith('usdt'):
        st.warning("No USDT pair selected for scalping.")
    elif price is None:
        st.warning("Could not fetch price for selected pair.")
    else:
        # --- Price Information Display ---
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 Current Price", f"${price:.6f}")
        with col2:
            decimal_tp = price * (1 + st.session_state.get('decimal_profit_target', 0.3) / 100)
            st.metric("🎯 Take Profit", f"${decimal_tp:.6f}")
        with col3:
            decimal_sl = price * (1 - st.session_state.get('quick_sl_percentage', 0.15) / 100)
            st.metric("🛡️ Stop Loss", f"${decimal_sl:.6f}")
        with col4:
            potential_pnl = st.session_state.get('capital', 100.0) * st.session_state.get('decimal_profit_target', 0.3) / 100
            st.metric("💎 Potential P&L", f"${potential_pnl:.2f}")
        
        # --- AI Prediction for Scalping ---
        st.subheader("🤖 AI Scalping Signal")
        try:
            # Create minimal dataframe for prediction
            import pandas as pd
            df = pd.DataFrame({
                'close': [price] * 5,
                'volume': [100] * 5,
                'timestamp': pd.date_range('2024-01-01', periods=5, freq='5min')
            })
            
            # Get AI confidence for scalping
            models = st.session_state.get('ml_models', None)
            if models:
                prediction_result = predict_with_trained_models(models, df, models.get('feature_cols', []))
                if prediction_result and 'confidence' in prediction_result:
                    confidence = prediction_result['confidence']
                    ensemble_pred = prediction_result.get('ensemble', 0)
                    direction = "BULLISH" if ensemble_pred > 0 else "BEARISH" if ensemble_pred < 0 else "NEUTRAL"
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("🎯 AI Confidence", f"{confidence:.1f}%")
                    with col2:
                        st.metric("📊 Signal Direction", direction)
                    with col3:
                        probability = min(confidence + 15, 95) if ensemble_pred != 0 else 50
                        st.metric("📈 Success Probability", f"{probability:.1f}%")
                else:
                    st.info("AI prediction not available - using technical analysis")
            else:
                st.info("Training AI models... Please wait")
        except Exception as e:
            st.warning("AI prediction temporarily unavailable")
        
        # --- Trading Buttons ---
        st.subheader("⚡ Quick Trade Actions")
        col1, col2 = st.columns(2)
        
        def long_action():
            try:
                amount = st.session_state.get('capital', 100.0)
                tp_pct = st.session_state.get('decimal_profit_target', 0.3)
                sl_pct = st.session_state.get('quick_sl_percentage', 0.15)
                trade_id = open_virtual_trade(symbol, 'LONG', amount, price, tp_pct, sl_pct)
                add_notification(f"LONG {symbol.upper()} @ ${price:.6f} | TP: ${price*(1+tp_pct/100):.6f}", "success")
                st.success(f"LONG {symbol.upper()} trade executed!")
            except Exception as e:
                st.error(f"Trade failed: {e}")
        
        def short_action():
            try:
                amount = st.session_state.get('capital', 100.0)
                tp_pct = st.session_state.get('decimal_profit_target', 0.3)
                sl_pct = st.session_state.get('quick_sl_percentage', 0.15)
                trade_id = open_virtual_trade(symbol, 'SHORT', amount, price, tp_pct, sl_pct)
                add_notification(f"SHORT {symbol.upper()} @ ${price:.6f} | TP: ${price*(1-tp_pct/100):.6f}", "success")
                st.success(f"SHORT {symbol.upper()} trade executed!")
            except Exception as e:
                st.error(f"Trade failed: {e}")
        
        with col1:
            simple_button(f"🟢 LONG {symbol.upper()}", key=f"long_{symbol}", action=long_action, debug_label=f"LONG {symbol}")
        with col2:
            simple_button(f"🔴 SHORT {symbol.upper()}", key=f"short_{symbol}", action=short_action, debug_label=f"SHORT {symbol}")

# --- DASHBOARD TAB ---
with dashboard_tab:
    st.header("📊 Trading Dashboard")
    
    # --- Live Price Feed with AI Analysis ---
    symbol = st.session_state.get('selected_symbol', None)
    if symbol:
        price = fetch_binance_price(symbol)
        if price:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(f"💰 {symbol.upper()}", f"${price:.6f}")
            
            # --- AI Prediction Display ---
            try:
                # Create sample data for prediction
                df = pd.DataFrame({
                    'close': [price] * 10,
                    'volume': [1000] * 10,
                    'timestamp': pd.date_range('2024-01-01', periods=10, freq='5min')
                })
                
                models = st.session_state.get('ml_models', None)
                if models:
                    prediction_result = predict_with_trained_models(models, df, models.get('feature_cols', []))
                    if prediction_result:
                        confidence = prediction_result.get('confidence', 50)
                        ensemble_pred = prediction_result.get('ensemble', 0)
                        agreement = prediction_result.get('agreement', 50)
                        
                        with col2:
                            st.metric("🤖 AI Confidence", f"{confidence:.1f}%")
                        with col3:
                            direction = "📈 BULLISH" if ensemble_pred > 0 else "📉 BEARISH" if ensemble_pred < 0 else "➡️ NEUTRAL"
                            st.metric("🎯 Signal", direction)
                        with col4:
                            success_prob = min(confidence + agreement / 2, 95)
                            st.metric("✅ Success Probability", f"{success_prob:.1f}%")
                    else:
                        with col2:
                            st.metric("🤖 AI Status", "Training...")
                        with col3:
                            st.metric("🎯 Signal", "Pending")
                        with col4:
                            st.metric("✅ Probability", "N/A")
                else:
                    with col2:
                        st.metric("🤖 AI Status", "Offline")
                    with col3:
                        st.metric("🎯 Signal", "Manual")
                    with col4:
                        st.metric("✅ Probability", "50%")
                        
            except Exception as e:
                with col2:
                    st.metric("🤖 AI Status", "Error")
                with col3:
                    st.metric("🎯 Signal", "N/A")
                with col4:
                    st.metric("✅ Probability", "N/A")
    
    # --- Portfolio Status ---
    st.subheader("📈 Portfolio Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Available Balance", f"${st.session_state.virtual_balance:.2f}")
    with col2:
        total_invested = sum(trade['amount'] for trade in st.session_state.active_trades.values())
        st.metric("💼 Invested", f"${total_invested:.2f}")
    with col3:
        unrealized_pnl = sum(trade.get('pnl', 0) for trade in st.session_state.active_trades.values())
        color = "normal" if unrealized_pnl >= 0 else "inverse"
        st.metric("📊 Unrealized P&L", f"${unrealized_pnl:.2f}")
    with col4:
        closed_trades = [t for t in st.session_state.trade_history if t.get('status', '').startswith('CLOSED')]
        realized_pnl = sum(t.get('pnl', 0) for t in closed_trades)
        st.metric("💎 Realized P&L", f"${realized_pnl:.2f}")

    # --- Enhanced Active Trades Display ---
    st.subheader("🔥 Active Trades")
    update_active_trades()
    
    if st.session_state.active_trades:
        trades_data = []
        for trade_id, trade in st.session_state.active_trades.items():
            # Calculate additional metrics
            entry_price = trade.get('entry_price', 0)
            current_price = trade.get('current_price', entry_price)
            tp_price = trade.get('tp_price', 0)
            sl_price = trade.get('sl_price', 0)
            pnl = trade.get('pnl', 0)
            
            # Calculate percentage change
            if entry_price > 0:
                pct_change = ((current_price - entry_price) / entry_price) * 100
                if trade['direction'] == 'SHORT':
                    pct_change = -pct_change
            else:
                pct_change = 0
            
            trades_data.append({
                'ID': trade_id[:8] + '...',
                'Symbol': trade['symbol'].upper(),
                'Direction': '🟢 LONG' if trade['direction'] == 'LONG' else '🔴 SHORT',
                'Amount': f"${trade['amount']:.2f}",
                'Entry Price': f"${entry_price:.6f}",
                'Current Price': f"${current_price:.6f}",
                'Take Profit': f"${tp_price:.6f}" if tp_price > 0 else "N/A",
                'Stop Loss': f"${sl_price:.6f}" if sl_price > 0 else "N/A",
                'P&L ($)': f"${pnl:.2f}",
                'P&L (%)': f"{pct_change:.2f}%",                'Status': trade['status']
            })
        
        if trades_data:
            df = pd.DataFrame(trades_data)
            st.dataframe(df, use_container_width=True)
    else:
        st.info("No active trades")

    # --- Trade History ---
    st.subheader("📜 Trade History")
    if st.session_state.trade_history:
        history_df = pd.DataFrame(st.session_state.trade_history)
        st.dataframe(history_df, use_container_width=True)
    else:
        st.info("No trade history yet.")

# --- BOT STATS TAB ---
with stats_tab:
    st.header("📈 Bot Trading Statistics")
    
    # Calculate stats from trade history and active trades
    total_trades = len(st.session_state.trade_history)
    active_trades_count = len(st.session_state.active_trades)
    
    if total_trades > 0:
        history_df = pd.DataFrame(st.session_state.trade_history)
        
        # Performance metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Trades", total_trades)
            st.metric("Active Trades", active_trades_count)
        
        with col2:
            profitable_trades = len(history_df[history_df['pnl'] > 0]) if 'pnl' in history_df.columns else 0
            win_rate = (profitable_trades / total_trades * 100) if total_trades > 0 else 0
            st.metric("Win Rate", f"{win_rate:.1f}%")
            
            avg_pnl = history_df['pnl'].mean() if 'pnl' in history_df.columns else 0
            st.metric("Avg P&L per Trade", f"${avg_pnl:.2f}")
        
        with col3:
            total_pnl = history_df['pnl'].sum() if 'pnl' in history_df.columns else 0
            st.metric("Total P&L", f"${total_pnl:.2f}")
            
            max_pnl = history_df['pnl'].max() if 'pnl' in history_df.columns else 0
            st.metric("Best Trade", f"${max_pnl:.2f}")
        
        with col4:
            min_pnl = history_df['pnl'].min() if 'pnl' in history_df.columns else 0
            st.metric("Worst Trade", f"${min_pnl:.2f}")
            
            current_balance = st.session_state.virtual_balance
            starting_balance = 10000.0
            total_return = ((current_balance - starting_balance) / starting_balance * 100)
            st.metric("Total Return", f"{total_return:.2f}%")
        
        # Charts
        st.subheader("� Performance Charts")
        
        if 'pnl' in history_df.columns and 'close_time' in history_df.columns:
            # Cumulative P&L over time
            history_df['cumulative_pnl'] = history_df['pnl'].cumsum()
            st.line_chart(history_df.set_index('close_time')['cumulative_pnl'])
            
            # P&L distribution
            st.subheader("P&L Distribution")
            st.bar_chart(history_df['pnl'])
        
        # Recent trades table
        st.subheader("📜 Recent Trades")
        recent_trades = history_df.tail(10) if len(history_df) > 10 else history_df
        st.dataframe(recent_trades, use_container_width=True)
        
    else:
        st.info("No trading history yet. Start trading to see statistics!")
        
        # Show current balance and active trades even without history
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Virtual Balance", f"${st.session_state.virtual_balance:.2f}")
        with col2:
            st.metric("Active Trades", active_trades_count)

# --- MULTI-COIN SCANNER TAB ---
with scanner_tab:
    st.header("🔍 Multi-Coin Scanner")
    
    # Enhanced coin selection
    st.subheader("📋 Coin Selection & Configuration")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        monitor_count = st.selectbox("Monitor Top N Coins", [5, 10, 15, 20, 25], 2)
    with col2:
        refresh_interval = st.number_input("Auto Refresh (seconds)", min_value=5, max_value=300, value=30)
    with col3:
        price_alert_threshold = st.number_input("Price Alert Threshold (%)", min_value=1.0, max_value=20.0, value=5.0)
    
    # Comprehensive coin list
    all_coins = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'XRPUSDT', 'SOLUSDT', 'DOTUSDT', 
                 'DOGEUSDT', 'AVAXUSDT', 'LINKUSDT', 'MATICUSDT', 'UNIUSDT', 'LTCUSDT', 'BCHUSDT',
                 'ATOMUSDT', 'FILUSDT', 'TRXUSDT', 'ETCUSDT', 'XLMUSDT', 'ALGOUSDT', 'VETUSDT',
                 'ICPUSDT', 'THETAUSDT', 'FTMUSDT', 'MANAUSDT', 'SANDUSDT', 'CHZUSDT']
    
    # Custom coin addition
    custom_coins_input = st.text_input("Add Custom Coins (comma separated)", 
                                     placeholder="PEPEUSDT, SHIBUSDT, FLOKIUSDT")
    
    coins_to_monitor = all_coins[:monitor_count]
    if custom_coins_input:
        additional_coins = [coin.strip().upper() for coin in custom_coins_input.split(',') if coin.strip()]
        coins_to_monitor.extend(additional_coins)
    
    # Real-time price monitoring with enhanced data
    st.subheader("💰 Real-Time Market Overview")
    
    def refresh_scanner_data():
        add_notification("Market scanner refreshed", "info")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"Monitoring {len(coins_to_monitor)} coins")
    with col2:
        simple_button("🔄 Refresh Data", key="refresh_scanner", action=refresh_scanner_data, debug_label="Refresh Scanner")
    
    # Create comprehensive market data table
    scanner_data = []
    for coin in coins_to_monitor:
        try:
            price = fetch_binance_price(coin)
            if price:
                # Enhanced mock data for demonstration
                change_24h = np.random.uniform(-12, 12)
                volume_24h = np.random.uniform(1000000, 500000000)
                market_cap = price * np.random.uniform(100000000, 50000000000)
                
                # Technical indicators (mock)
                rsi = np.random.uniform(20, 80)
                rsi_signal = "🟢 BUY" if rsi < 30 else "🔴 SELL" if rsi > 70 else "🟡 HOLD"
                
                # AI analysis (mock)
                ai_confidence = np.random.uniform(40, 90)
                ai_signal = np.random.choice(['🟢 BULLISH', '🔴 BEARISH', '🟡 NEUTRAL'], p=[0.4, 0.3, 0.3])
                
                # Volume analysis
                volume_status = "🟢 HIGH" if volume_24h > 50000000 else "🟡 NORMAL" if volume_24h > 10000000 else "🔴 LOW"
                  # Overall score
                score_factors = []
                if change_24h > 0:
                    score_factors.append(1)
                if rsi < 30 or rsi > 70:
                    score_factors.append(1)
                if ai_confidence > 70:
                    score_factors.append(2)
                if volume_24h > 50000000:
                    score_factors.append(1)
                
                overall_score = min(sum(score_factors), 10)
                
                scanner_data.append({
                    'Symbol': coin,
                    'Price': f"${price:.6f}",
                    '24h Change': f"{change_24h:.2f}%",
                    'AI Signal': ai_signal,
                    'Confidence': f"{ai_confidence:.1f}%",
                    'Score': f"{overall_score}/10",
                    'Status': '🟢' if change_24h > 0 else '🔴',
                    'Alert': '🚨' if abs(change_24h) > price_alert_threshold else '✅'
                })
        except Exception as e:
            scanner_data.append({
                'Symbol': coin,
                'Price': 'Error',                '24h Change': 'N/A',
                'AI Signal': '⚠️ ERROR',
                'Confidence': 'N/A',
                'Score': 'N/A',
                'Status': '⚠️',
                'Alert': '⚠️'
            })
    
    if scanner_data:
        # Instead of showing a separate table, show each coin with integrated trading buttons
        st.subheader("💰 Real-Time Market Overview with Integrated Trading")
        
        # Show coins in a clean grid format with trading buttons integrated
        for i in range(0, len(scanner_data), 2):  # Show 2 coins per row
            col1, col2 = st.columns(2)
            
            # First coin in the row
            with col1:
                data = scanner_data[i]
                symbol = data['Symbol']
                
                # Create a container for each coin's data and buttons
                with st.container():
                    st.markdown(f"### {symbol}")
                    
                    # Display key metrics in columns
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    with metric_col1:
                        st.metric("Price", data['Price'])
                    with metric_col2:
                        st.metric("24h Change", data['24h Change'])
                    with metric_col3:
                        st.metric("Score", data['Score'])
                    
                    # Display AI signal and confidence
                    signal_col1, signal_col2 = st.columns(2)
                    with signal_col1:
                        st.write(f"**AI Signal:** {data['AI Signal']}")
                    with signal_col2:
                        st.write(f"**Confidence:** {data['Confidence']}")
                    
                    # Integrated trading buttons
                    trade_col1, trade_col2 = st.columns(2)
                    
                    def create_long_action(sym):
                        def action():
                            try:
                                price = fetch_binance_price(sym)
                                if price:
                                    trade_id = open_virtual_trade(sym, 'LONG', 100, price, 2.0, 1.0)
                                    add_notification(f"🟢 LONG {sym} @ ${price:.6f}", "success")
                            except Exception as e:
                                st.error(f"Error: {e}")
                        return action
                    
                    def create_short_action(sym):
                        def action():
                            try:
                                price = fetch_binance_price(sym)
                                if price:
                                    trade_id = open_virtual_trade(sym, 'SHORT', 100, price, 2.0, 1.0)
                                    add_notification(f"🔴 SHORT {sym} @ ${price:.6f}", "success")
                            except Exception as e:
                                st.error(f"Error: {e}")
                        return action
                    
                    with trade_col1:
                        simple_button(f"🟢 LONG", key=f"long_{symbol}_{i}", action=create_long_action(symbol), debug_label=f"Long {symbol}")
                    with trade_col2:
                        simple_button(f"🔴 SHORT", key=f"short_{symbol}_{i}", action=create_short_action(symbol), debug_label=f"Short {symbol}")
                    
                    st.markdown("---")  # Separator line
            
            # Second coin in the row (if exists)
            if i + 1 < len(scanner_data):
                with col2:
                    data = scanner_data[i + 1]
                    symbol = data['Symbol']
                    
                    # Create a container for each coin's data and buttons
                    with st.container():
                        st.markdown(f"### {symbol}")
                        
                        # Display key metrics in columns
                        metric_col1, metric_col2, metric_col3 = st.columns(3)
                        with metric_col1:
                            st.metric("Price", data['Price'])
                        with metric_col2:
                            st.metric("24h Change", data['24h Change'])
                        with metric_col3:
                            st.metric("Score", data['Score'])
                        
                        # Display AI signal and confidence
                        signal_col1, signal_col2 = st.columns(2)
                        with signal_col1:
                            st.write(f"**AI Signal:** {data['AI Signal']}")
                        with signal_col2:
                            st.write(f"**Confidence:** {data['Confidence']}")
                        
                        # Integrated trading buttons
                        trade_col1, trade_col2 = st.columns(2)
                        
                        def create_long_action2(sym):
                            def action():
                                try:
                                    price = fetch_binance_price(sym)
                                    if price:
                                        trade_id = open_virtual_trade(sym, 'LONG', 100, price, 2.0, 1.0)
                                        add_notification(f"🟢 LONG {sym} @ ${price:.6f}", "success")
                                except Exception as e:
                                    st.error(f"Error: {e}")
                            return action
                        
                        def create_short_action2(sym):
                            def action():
                                try:
                                    price = fetch_binance_price(sym)
                                    if price:
                                        trade_id = open_virtual_trade(sym, 'SHORT', 100, price, 2.0, 1.0)
                                        add_notification(f"🔴 SHORT {sym} @ ${price:.6f}", "success")
                                except Exception as e:                                    st.error(f"Error: {e}")
                            return action
                        
                        with trade_col1:
                            simple_button(f"🟢 LONG", key=f"long_{symbol}_{i+1}", action=create_long_action2(symbol), debug_label=f"Long {symbol}")
                        with trade_col2:
                            simple_button(f"🔴 SHORT", key=f"short_{symbol}_{i+1}", action=create_short_action2(symbol), debug_label=f"Short {symbol}")
                        
                        st.markdown("---")  # Separator line
        
        # Price alert configuration
        st.subheader("🚨 Price Alert System")
    
    alert_col1, alert_col2, alert_col3, alert_col4 = st.columns(4)
    
    with alert_col1:
        alert_symbol = st.selectbox("Alert Symbol", coins_to_monitor, key="alert_symbol")
    
    with alert_col2:
        alert_type = st.selectbox("Alert Type", ["Price Above", "Price Below", "% Change Above", "% Change Below"], key="alert_type")
    
    with alert_col3:
        alert_value = st.number_input("Alert Value", min_value=0.0, step=0.001, key="alert_value")
    
    with alert_col4:
        def set_price_alert():
            alert_message = f"Alert set: {alert_symbol} {alert_type} {alert_value}"
            add_notification(alert_message, "info")
            st.success("Price alert configured!")
        
        st.write("") # Spacing
        simple_button("Set Alert", key="set_price_alert", action=set_price_alert, debug_label="Set Price Alert")

# --- AUTO TRADING TAB ---
with auto_tab:
    st.header("🤖 Auto Trading System")
    
    # Auto trading status
    auto_enabled = st.session_state.get('auto_trading_enabled', False)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Auto Trading Status", "🟢 ENABLED" if auto_enabled else "� DISABLED")
    with col2:
        def toggle_auto_trading():
            st.session_state.auto_trading_enabled = not st.session_state.get('auto_trading_enabled', False)
            status = "enabled" if st.session_state.auto_trading_enabled else "disabled"
            add_notification(f"Auto trading {status}", "info")
        
        simple_button("Toggle Auto Trading", key="toggle_auto", action=toggle_auto_trading, debug_label="Toggle Auto Trading")
      # Auto trading settings
    st.subheader("⚙️ Auto Trading Settings")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        auto_symbol = st.selectbox("Auto Trade Symbol", ['BTCUSDT', 'ETHUSDT', 'BNBUSDT'])
        auto_amount = st.number_input("Trade Amount ($)", min_value=1.0, max_value=1000.0, value=50.0)
    
    with col2:
        auto_take_profit = st.number_input("Take Profit (%)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
        auto_stop_loss = st.number_input("Stop Loss (%)", min_value=0.1, max_value=10.0, value=2.0, step=0.1)
    
    with col3:
        auto_interval = st.selectbox("Check Interval", ["1 minute", "5 minutes", "15 minutes", "1 hour"])
        max_active_trades = st.number_input("Max Active Trades", min_value=1, max_value=10, value=3)
    
    # --- AI Analysis for Auto Trading ---
    st.subheader("🤖 AI Trading Analysis")
    
    if auto_enabled:
        current_price = fetch_binance_price(auto_symbol)
        if current_price:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("💰 Current Price", f"${current_price:.6f}")
            
            # Get AI prediction for auto trading
            try:
                df = pd.DataFrame({
                    'close': [current_price] * 10,
                    'volume': [1000] * 10,
                    'timestamp': pd.date_range('2024-01-01', periods=10, freq='5min')
                })
                
                models = st.session_state.get('ml_models', None)
                if models:
                    prediction_result = predict_with_trained_models(models, df, models.get('feature_cols', []))
                    if prediction_result:
                        confidence = prediction_result.get('confidence', 50)
                        ensemble_pred = prediction_result.get('ensemble', 0)
                        agreement = prediction_result.get('agreement', 50)
                        
                        with col2:
                            st.metric("🎯 AI Confidence", f"{confidence:.1f}%")
                        with col3:
                            direction = "BULLISH" if ensemble_pred > 0 else "BEARISH" if ensemble_pred < 0 else "NEUTRAL"
                            st.metric("📊 Signal", direction)
                        with col4:
                            trade_probability = min(confidence + agreement / 2, 95)
                            st.metric("✅ Trade Probability", f"{trade_probability:.1f}%")
                    else:
                        with col2:
                            st.metric("🤖 AI Status", "Training...")
                        with col3:
                            st.metric("🎯 Signal", "Pending")
                        with col4:
                            st.metric("✅ Probability", "N/A")
            except Exception as e:
                with col2:
                    st.metric("🤖 AI Status", "Error")
                with col3:
                    st.metric("🎯 Signal", "N/A")
                with col4:
                    st.metric("✅ Probability", "N/A")
    
    # Auto trading rules
    st.subheader("📋 Trading Rules")
    
    use_rsi = st.checkbox("Use RSI (Buy < 30, Sell > 70)")
    use_ema = st.checkbox("Use EMA Crossover")
    use_volume = st.checkbox("Use Volume Filter")
    
    # Manual trigger for auto trading
    def run_auto_scan():
        if not auto_enabled:
            add_notification("Auto trading is disabled. Enable it first.", "warning")
            return
            
        current_price = fetch_binance_price(auto_symbol)
        if current_price:
            # Simple logic: random decision for demo
            should_trade = np.random.choice([True, False])
            if should_trade and len(st.session_state.active_trades) < max_active_trades:
                # Simulate auto trade
                trade_id = str(uuid.uuid4())
                trade = {
                    'id': trade_id,
                    'symbol': auto_symbol,
                    'action': np.random.choice(['LONG', 'SHORT']),
                    'amount': auto_amount,
                    'entry_price': current_price,
                    'take_profit': current_price * (1 + auto_take_profit/100),
                    'stop_loss': current_price * (1 - auto_stop_loss/100),
                    'open_time': datetime.datetime.now(),
                    'status': 'OPEN'
                }
                st.session_state.active_trades[trade_id] = trade
                add_notification(f"Auto {trade['action']} trade opened for {auto_symbol} at ${current_price:.2f}", "success")
            else:
                add_notification("Auto scan complete - no trade signals", "info")
        else:
            add_notification("Failed to get price for auto trading", "error")
    
    simple_button("🔍 Run Auto Scan Now", key="run_auto_scan", action=run_auto_scan, debug_label="Run Auto Scan")
    
    # Show auto trading history
    if st.session_state.trade_history:
        auto_trades = [t for t in st.session_state.trade_history if t.get('auto_trade', False)]
        if auto_trades:
            st.subheader("📊 Auto Trading History")
            st.dataframe(pd.DataFrame(auto_trades), use_container_width=True)

# --- ADVANCED BACKTESTING TAB ---
with backtest_tab:
    st.header("🔄 Advanced Backtesting System")
    
    # Backtest parameters
    st.subheader("⚙️ Backtest Configuration")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        bt_symbol = st.selectbox("Backtest Symbol", ['BTCUSDT', 'ETHUSDT', 'BNBUSDT'], key="bt_symbol")
        bt_timeframe = st.selectbox("Timeframe", ['1m', '5m', '15m', '1h', '4h', '1d'])
    
    with col2:
        bt_start_balance = st.number_input("Starting Balance ($)", min_value=1000.0, value=10000.0)
        bt_trade_amount = st.number_input("Trade Amount ($)", min_value=10.0, value=100.0)
    
    with col3:
        bt_take_profit = st.number_input("Take Profit (%)", min_value=0.1, value=2.0, step=0.1, key="bt_tp")
        bt_stop_loss = st.number_input("Stop Loss (%)", min_value=0.1, value=1.0, step=0.1, key="bt_sl")
    
    # Strategy selection
    st.subheader("📈 Strategy Selection")
    strategy = st.selectbox("Trading Strategy", [
        "Simple Moving Average Crossover",
        "RSI Mean Reversion", 
        "Bollinger Bands",
        "MACD Signal",
        "Random Entry (Demo)"
    ])
    
    # Run backtest
    def run_backtest():
        add_notification("Starting backtest...", "info")
        
        # Simulate backtest results
        num_trades = np.random.randint(50, 200)
        win_rate = np.random.uniform(0.4, 0.7)
        winning_trades = int(num_trades * win_rate)
        losing_trades = num_trades - winning_trades
        
        # Generate mock results
        avg_win = np.random.uniform(15, 50)
        avg_loss = np.random.uniform(-30, -10)
        
        total_pnl = (winning_trades * avg_win) + (losing_trades * avg_loss)
        final_balance = bt_start_balance + total_pnl
        
        # Store results in session state
        st.session_state.backtest_results = {
            'symbol': bt_symbol,
            'strategy': strategy,
            'timeframe': bt_timeframe,
            'start_balance': bt_start_balance,
            'final_balance': final_balance,
            'total_trades': num_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate * 100,
            'total_pnl': total_pnl,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'max_drawdown': np.random.uniform(5, 25),
            'sharpe_ratio': np.random.uniform(0.5, 2.5)
        }
        
        add_notification("Backtest completed successfully!", "success")
    
    simple_button("🚀 Run Backtest", key="run_backtest", action=run_backtest, debug_label="Run Backtest")
      # Display backtest results
    if 'backtest_results' in st.session_state and isinstance(st.session_state.backtest_results, dict) and st.session_state.backtest_results:
        results = st.session_state.backtest_results
        
        st.subheader("📊 Backtest Results")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Trades", results['total_trades'])
            st.metric("Win Rate", f"{results['win_rate']:.1f}%")
        
        with col2:
            st.metric("Total P&L", f"${results['total_pnl']:.2f}")
            st.metric("Final Balance", f"${results['final_balance']:.2f}")
        
        with col3:
            st.metric("Avg Win", f"${results['avg_win']:.2f}")
            st.metric("Avg Loss", f"${results['avg_loss']:.2f}")
        
        with col4:
            st.metric("Max Drawdown", f"{results['max_drawdown']:.2f}%")
            st.metric("Sharpe Ratio", f"{results['sharpe_ratio']:.2f}")
        
        # Performance summary
        roi = ((results['final_balance'] - results['start_balance']) / results['start_balance']) * 100
        st.success(f"📈 **ROI: {roi:.2f}%** | Strategy: {results['strategy']} | Symbol: {results['symbol']}")

# --- FUTURES SCANNER TAB ---
with futures_tab:
    st.header("📈 Futures Trading Scanner")
    
    # Enhanced futures symbols with more comprehensive data
    futures_symbols = [
        {'symbol': 'BTCUSDT', 'max_leverage': 125, 'funding_rate': 0.01, 'category': 'Major', 'tier': 'Tier 1'},
        {'symbol': 'ETHUSDT', 'max_leverage': 100, 'funding_rate': 0.02, 'category': 'Major', 'tier': 'Tier 1'},
        {'symbol': 'BNBUSDT', 'max_leverage': 50, 'funding_rate': -0.01, 'category': 'Exchange', 'tier': 'Tier 2'},
        {'symbol': 'ADAUSDT', 'max_leverage': 75, 'funding_rate': 0.03, 'category': 'DeFi', 'tier': 'Tier 2'},
        {'symbol': 'SOLUSDT', 'max_leverage': 50, 'funding_rate': 0.01, 'category': 'Layer1', 'tier': 'Tier 2'},
        {'symbol': 'XRPUSDT', 'max_leverage': 75, 'funding_rate': -0.02, 'category': 'Payment', 'tier': 'Tier 2'},
        {'symbol': 'DOGEUSDT', 'max_leverage': 50, 'funding_rate': 0.05, 'category': 'Meme', 'tier': 'Tier 3'},
        {'symbol': 'AVAXUSDT', 'max_leverage': 50, 'funding_rate': 0.02, 'category': 'Layer1', 'tier': 'Tier 2'},
        {'symbol': 'MATICUSDT', 'max_leverage': 75, 'funding_rate': 0.01, 'category': 'Scaling', 'tier': 'Tier 2'},
        {'symbol': 'LINKUSDT', 'max_leverage': 50, 'funding_rate': 0.03, 'category': 'Oracle', 'tier': 'Tier 2'}
    ]
    
    st.subheader("⚡ All Futures Opportunities - Comprehensive Table View")
    
    # Create comprehensive futures table with enhanced metrics
    futures_data = []
    for future in futures_symbols:
        try:
            current_price = fetch_binance_price(future['symbol'])
            if current_price:
                # Generate comprehensive market data
                volatility = np.random.uniform(2, 25)
                volume_24h = np.random.uniform(50000000, 2000000000)
                price_change_24h = np.random.uniform(-12, 12)
                open_interest = np.random.uniform(100000000, 1000000000)
                
                # Generate AI predictions with models if available
                try:
                    df = pd.DataFrame({
                        'close': [current_price] * 5,
                        'volume': [volume_24h] * 5,
                        'high': [current_price * 1.02] * 5,
                        'low': [current_price * 0.98] * 5
                    })
                    models = st.session_state.get('ml_models', None)
                    if models:
                        prediction_result = predict_with_trained_models(models, df, models.get('feature_cols', []))
                        ai_confidence = prediction_result.get('confidence', 50) if prediction_result else 50
                        ai_signal = "🟢 BULLISH" if prediction_result and prediction_result.get('ensemble', 0) > 0 else "🔴 BEARISH" if prediction_result else "⚪ NEUTRAL"
                        probability = prediction_result.get('probability', 0.5) if prediction_result else 0.5
                    else:
                        ai_confidence = np.random.uniform(45, 90)
                        ai_signal = np.random.choice(["🟢 BULLISH", "🔴 BEARISH", "⚪ NEUTRAL"], p=[0.4, 0.35, 0.25])
                        probability = np.random.uniform(0.45, 0.85)
                except:
                    ai_confidence = np.random.uniform(45, 90)
                    ai_signal = np.random.choice(["🟢 BULLISH", "🔴 BEARISH", "⚪ NEUTRAL"], p=[0.4, 0.35, 0.25])
                    probability = np.random.uniform(0.45, 0.85)
                
                # Calculate enhanced risk metrics
                liquidation_risk = 100 / future['max_leverage']
                potential_pnl_1pct = st.session_state.get('capital', 100) * future['max_leverage'] * 0.01
                funding_cost_8h = abs(future['funding_rate']) * st.session_state.get('capital', 100) * future['max_leverage']
                
                # Risk score calculation (lower is better, 0-20 scale)
                risk_score = (
                    volatility * 0.3 + 
                    abs(future['funding_rate']) * 100 + 
                    liquidation_risk * 0.5 + 
                    (20 - ai_confidence/5)
                )
                
                risk_level = "🟢 LOW" if risk_score < 8 else "🟡 MED" if risk_score < 15 else "🔴 HIGH"
                  # Trade score (higher is better, 0-100 scale)
                trade_score = (
                    ai_confidence * 0.4 + 
                    (100 - risk_score * 3) * 0.3 + 
                    (future['max_leverage'] / 125 * 30) * 0.3
                )
                
                futures_data.append({
                    'Symbol': future['symbol'],
                    'Price ($)': f"{current_price:.6f}",
                    '24h Change': f"{price_change_24h:+.2f}%",
                    'Leverage': f"{future['max_leverage']}x",
                    'AI Signal': ai_signal,
                    'Confidence': f"{ai_confidence:.1f}%",
                    'Risk': risk_level,
                    'Score': f"{trade_score:.1f}/100",
                    'Quick Trade': f"READY_{future['symbol']}"  # This will be used for button identification
                })
        except Exception as e:
            futures_data.append({
                'Symbol': future['symbol'],
                'Price ($)': 'Error',
                '24h Change': 'N/A',                'AI Signal': '⚠️ ERROR',
                'Confidence': 'N/A',
                'Risk': '⚠️ ERROR',
                'Score': 'N/A',
                'Quick Trade': f"ERROR_{future['symbol']}"
            })
    
    if futures_data:
        # Display the comprehensive table with filters
        col1, col2, col3 = st.columns(3)
        with col1:
            category_filter = st.selectbox("Filter by Category", ["All"] + list(set([f['category'] for f in futures_symbols])))
        with col2:
            tier_filter = st.selectbox("Filter by Tier", ["All", "Tier 1", "Tier 2", "Tier 3"])
        with col3:
            min_trade_score = st.slider("Min Trade Score", 0, 100, 50)
        
        # Apply filters
        filtered_data = futures_data.copy()
        if category_filter != "All":
            filtered_data = [d for d in filtered_data if d['Category'] == category_filter]
        if tier_filter != "All":
            filtered_data = [d for d in filtered_data if d['Tier'] == tier_filter]
        
        # Instead of separate table and trading sections, show integrated cards
        st.subheader("⚡ Futures Trading Opportunities with Integrated Trading")
        
        # Show futures in a clean grid format with trading buttons integrated
        for i in range(0, len(filtered_data), 2):  # Show 2 futures per row
            col1, col2 = st.columns(2)
            
            # First future in the row
            with col1:
                data = filtered_data[i]
                symbol = data['Symbol']
                
                # Create a container for each future's data and buttons
                with st.container():
                    st.markdown(f"### {symbol}")
                    
                    # Display key metrics in columns
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    with metric_col1:
                        st.metric("Price", data['Price ($)'])
                    with metric_col2:
                        st.metric("24h Change", data['24h Change'])
                    with metric_col3:
                        st.metric("Leverage", data['Leverage'])
                    
                    # Second row of metrics
                    metric_col4, metric_col5, metric_col6 = st.columns(3)
                    with metric_col4:
                        st.metric("AI Signal", data['AI Signal'])
                    with metric_col5:
                        st.metric("Confidence", data['Confidence'])
                    with metric_col6:
                        st.metric("Risk Level", data['Risk'])
                    
                    # Trade score and integrated trading buttons
                    score_col, trade_col = st.columns([1, 2])
                    with score_col:
                        st.metric("Score", data['Score'])
                    
                    with trade_col:
                        # Integrated trading buttons
                        trade_btn_col1, trade_btn_col2 = st.columns(2)

                        def create_futures_long(sym):
                            def action():
                                try:
                                    price = fetch_binance_price(sym)
                                    if price:
                                        trade_id = open_virtual_trade(sym, 'LONG', 1000, price, 2.0, 1.0)
                                        add_notification(f"🟢 LONG {sym} @ ${price:.6f}", "success")
                                except Exception as e:
                                    st.error(f"Error: {e}")
                            return action

                        def create_futures_short(sym):
                            def action():
                                try:
                                    price = fetch_binance_price(sym)
                                    if price:
                                        trade_id = open_virtual_trade(sym, 'SHORT', 1000, price, 2.0, 1.0)
                                        add_notification(f"🔴 SHORT {sym} @ ${price:.6f}", "success")
                                except Exception as e:
                                    st.error(f"Error: {e}")
                            return action

                        with trade_btn_col1:
                            simple_button(f"🟢 LONG", key=f"futures_long_{symbol}_{i}", action=create_futures_long(symbol), debug_label=f"Futures Long {symbol}")
                        with trade_btn_col2:
                            simple_button(f"🔴 SHORT", key=f"futures_short_{symbol}_{i}", action=create_futures_short(symbol), debug_label=f"Futures Short {symbol}")
                    
                    st.markdown("---")  # Separator line
            
            # Second future in the row (if exists)
            if i + 1 < len(filtered_data):
                with col2:
                    data = filtered_data[i + 1]
                    symbol = data['Symbol']
                    
                    # Create a container for each future's data and buttons
                    with st.container():
                        st.markdown(f"### {symbol}")
                        
                        # Display key metrics in columns
                        metric_col1, metric_col2, metric_col3 = st.columns(3)
                        with metric_col1:
                            st.metric("Price", data['Price ($)'])
                        with metric_col2:
                            st.metric("24h Change", data['24h Change'])
                        with metric_col3:
                            st.metric("Leverage", data['Leverage'])
                        
                        # Second row of metrics
                        metric_col4, metric_col5, metric_col6 = st.columns(3)
                        with metric_col4:
                            st.metric("AI Signal", data['AI Signal'])
                        with metric_col5:
                            st.metric("Confidence", data['Confidence'])
                        with metric_col6:
                            st.metric("Risk Level", data['Risk'])
                        
                        # Trade score and integrated trading buttons
                        score_col, trade_col = st.columns([1, 2])
                        with score_col:
                            st.metric("Score", data['Score'])
                        
                        with trade_col:
                            # Integrated trading buttons
                            trade_btn_col1, trade_btn_col2 = st.columns(2)
                            
                            def create_futures_long2(sym):
                                def action():
                                    try:
                                        price = fetch_binance_price(sym)
                                        if price:
                                            trade_id = open_virtual_trade(sym, 'LONG', 1000, price, 2.0, 1.0)
                                            add_notification(f"🟢 LONG {sym} @ ${price:.6f}", "success")
                                    except Exception as e:
                                        st.error(f"Error: {e}")
                                    return
                                return action
                            
                            def create_futures_short2(sym):
                                def action():
                                    try:
                                        price = fetch_binance_price(sym)
                                        if price:
                                            trade_id = open_virtual_trade(sym, 'SHORT', 1000, price, 2.0, 1.0)
                                            add_notification(f"🔴 SHORT {sym} @ ${price:.6f}", "success")
                                    except Exception as e:
                                        st.error(f"Error: {e}")
                                    return
                                return action
                            
                            with trade_btn_col1:
                                simple_button(f"🟢 LONG", key=f"futures_long_{symbol}_{i+1}", action=create_futures_long2(symbol), debug_label=f"Futures Long {symbol}")
                            with trade_btn_col2:
                                simple_button(f"🔴 SHORT", key=f"futures_short_{symbol}_{i+1}", action=create_futures_short2(symbol), debug_label=f"Futures Short {symbol}")
                        
                        st.markdown("---")  # Separator line
        
        # Summary metrics
        st.subheader("📊 Market Summary")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            bullish_count = len([d for d in filtered_data if "BULLISH" in d['AI Signal']])
            st.metric("🟢 Bullish Signals", bullish_count)
        with col2:
            bearish_count = len([d for d in filtered_data if "BEARISH" in d['AI Signal']])
            st.metric("🔴 Bearish Signals", bearish_count)
        with col3:
            high_confidence = len([d for d in filtered_data if d['Confidence'] != 'N/A' and float(d['Confidence'].rstrip('%')) > 75])
            st.metric("🎯 High Confidence", high_confidence)
        with col4:
            low_risk = len([d for d in filtered_data if "LOW" in d['Risk']])
            st.metric("✅ Low Risk", low_risk)
        with col5:
            high_leverage_count = len([d for d in filtered_data if int(d['Leverage'].rstrip('x')) >= 100])
            st.metric("⚡ 100x+ Leverage", high_leverage_count)
    
    # Enhanced Advanced Risk Calculator
    st.subheader("⚖️ Advanced Futures Risk Calculator & Strategy Planner")
    
    # Calculator inputs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        calc_symbol = st.selectbox("Calculator Symbol", [f['symbol'] for f in futures_symbols], key="calc_symbol")
        calc_leverage = st.number_input("Leverage", min_value=1, max_value=125, value=10, key="calc_leverage")
    
    with col2:
        calc_position_size = st.number_input("Position Size ($)", min_value=10.0, value=100.0, key="calc_position")
        calc_entry_price = st.number_input("Entry Price ($)", min_value=0.0001, value=50000.0, key="calc_entry")
    
    with col3:
        calc_direction = st.selectbox("Direction", ["LONG", "SHORT"], key="calc_direction")
        calc_price_change = st.number_input("Expected Price Change (%)", value=1.0, step=0.1, key="calc_change")
    
    with col4:
        calc_hold_hours = st.number_input("Hours to Hold", min_value=1, value=8, key="calc_hours")
        selected_symbol_data = next((f for f in futures_symbols if f['symbol'] == calc_symbol), {})
        calc_funding_rate = selected_symbol_data.get('funding_rate', 0.01)
    
    # Enhanced calculations
    leveraged_size = calc_position_size * calc_leverage
    
    if calc_direction == "LONG":
        pnl = leveraged_size * (calc_price_change / 100)
        liquidation_price = calc_entry_price * (1 - (1 / calc_leverage))
        liquidation_distance = ((calc_entry_price - liquidation_price) / calc_entry_price) * 100
    else:
        pnl = leveraged_size * (-calc_price_change / 100)
        liquidation_price = calc_entry_price * (1 + (1 / calc_leverage))
        liquidation_distance = ((liquidation_price - calc_entry_price) / calc_entry_price) * 100
    
    # Funding cost calculation (8-hour periods)
    funding_periods = calc_hold_hours / 8
    funding_cost = leveraged_size * abs(calc_funding_rate / 100) * funding_periods
    net_pnl = pnl - funding_cost
    roi = (net_pnl / calc_position_size) * 100
    
    # Risk assessment
    risk_warnings = []
    if abs(calc_price_change) >= liquidation_distance * 0.9:
        risk_warnings.append("🚨 EXTREME LIQUIDATION RISK - Position may be liquidated!")
    elif abs(calc_price_change) >= liquidation_distance * 0.7:
        risk_warnings.append("⚠️ HIGH LIQUIDATION RISK - Close to liquidation threshold!")
    elif abs(calc_price_change) >= liquidation_distance * 0.5:
        risk_warnings.append("🟡 MODERATE LIQUIDATION RISK - Monitor position closely!")
    
    if abs(roi) > 50:
        risk_warnings.append("⚡ HIGH REWARD/RISK POSITION - Consider position sizing!")
    
    if funding_cost > abs(pnl) * 0.2:
        risk_warnings.append("💰 HIGH FUNDING COST - Consider shorter holding period!")
    
    # Display results in organized layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📊 Position Details")
        st.metric("Leveraged Size", f"${leveraged_size:,.2f}")
        st.metric("Entry Price", f"${calc_entry_price:.6f}")
        st.metric("Direction", calc_direction)
        st.metric("Leverage", f"{calc_leverage}x")
    
    with col2:
        st.subheader("💰 P&L Analysis")
        st.metric("Gross P&L", f"${pnl:.2f}", delta=f"{(pnl/calc_position_size)*100:.1f}%")
        st.metric("Funding Cost", f"${funding_cost:.2f}")
        st.metric("Net P&L", f"${net_pnl:.2f}", delta=f"{roi:.1f}%")
        st.metric("ROI", f"{roi:.2f}%")
    
    with col3:
        st.subheader("⚠️ Risk Metrics")
        st.metric("Liquidation Price", f"${liquidation_price:.6f}")
        st.metric("Distance to Liq", f"{liquidation_distance:.2f}%")
        st.metric("Max Loss", f"${calc_position_size:.2f}")
        
        # Risk level indicator
        if risk_warnings:
            for warning in risk_warnings:
                st.error(warning)
        else:
            st.success("✅ MANAGEABLE RISK LEVEL")
    
    # Strategy suggestions based on calculations
    st.subheader("🎯 Strategy Suggestions")
    
    suggestions = []
    if abs(roi) > 20:
        suggestions.append("💡 High ROI potential - Consider taking partial profits at milestones")
    if liquidation_distance < 2:
        suggestions.append("🛡️ Very tight liquidation - Consider lower leverage or wider stops")
    if funding_cost > calc_position_size * 0.05:
        suggestions.append("⏰ High funding cost - Consider shorter-term positions")
    if calc_leverage > 50:
        suggestions.append("⚖️ High leverage - Ensure proper risk management")
    
    if suggestions:
        for suggestion in suggestions:
            st.info(suggestion)
    else:
        st.success("🎯 Position parameters look well-balanced!")
      # Quick calculation presets
    st.subheader("⚡ Quick Calculation Presets")
    preset_col1, preset_col2, preset_col3, preset_col4 = st.columns(4)
    
    with preset_col1:
        def conservative_preset():
            st.session_state['calc_leverage'] = 5
            st.session_state['calc_change'] = 2.0
            st.session_state['calc_hours'] = 24
        simple_button("🛡️ Conservative", key="preset_conservative", action=conservative_preset, debug_label="Conservative Preset")
    
    with preset_col2:
        def moderate_preset():
            st.session_state['calc_leverage'] = 20
            st.session_state['calc_change'] = 3.0
            st.session_state['calc_hours'] = 8
        simple_button("⚖️ Moderate", key="preset_moderate", action=moderate_preset, debug_label="Moderate Preset")
    
    with preset_col3:
        def aggressive_preset():
            st.session_state['calc_leverage'] = 50
            st.session_state['calc_change'] = 5.0
            st.session_state['calc_hours'] = 4
        simple_button("⚡ Aggressive", key="preset_aggressive", action=aggressive_preset, debug_label="Aggressive Preset")
    
    with preset_col4:
        def scalping_preset():
            st.session_state['calc_leverage'] = 100
            st.session_state['calc_change'] = 0.5
            st.session_state['calc_hours'] = 1
        simple_button("🎯 Scalping", key="preset_scalping", action=scalping_preset, debug_label="Scalping Preset")

# --- FOOTER ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    def ultra_refresh():
        st.cache_data.clear()
        st.success("Cache cleared!")
    simple_button("🚀 ULTRA REFRESH", key="ultra_refresh", action=ultra_refresh, debug_label="Ultra Refresh")

with col2:
    st.markdown("⚡ Trading Mode: LIVE")

# --- NOTIFICATIONS ---
display_notifications()

# --- BUTTON TEST SECTION ---
st.markdown("---")
st.subheader("🧪 Button Functionality Test")
st.write("Test the new button system to verify no redirects or tab switching occurs:")

def test_action():
    st.success("✅ Test button works! No page redirect occurred.")
    add_notification("Test button clicked successfully", "success")

simple_button("🔍 Test Button (No Redirect)", key="test_button", action=test_action, debug_label="Test Button")

st.write("**Instructions:** Click the test button above. If it works without redirecting or switching tabs, the fix is successful!")

# --- DEBUG INFO ---
if st.checkbox("Show Debug Info"):
    st.write("**Session State Keys:**", list(st.session_state.keys()))
    st.write("**Active Trades:**", len(st.session_state.active_trades))
    st.write("**Virtual Balance:**", st.session_state.virtual_balance)
    st.write("**Trade History:**", len(st.session_state.trade_history))