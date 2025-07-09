from backend.db import get_trades
from backend.db import initialize_database

# Ensure database tables exist before anything else
initialize_database()
# --- Resume open trades and simulation state on startup ---
def resume_state():
    # Load open trades from DB
    open_trades = [t for t in get_trades(limit=10000) if t['status'] == 'OPEN']
    for trade in open_trades:
        name = trade.get('model') or trade.get('strategy') or 'unknown'
        if name in MODEL_STATS:
            MODEL_STATS[name]['balance'] = trade.get('balance', MODEL_STATS[name]['balance'])
            # Optionally, add to history if not present
            MODEL_STATS[name]['history'].append({
                'timestamp': trade.get('open_time'),
                'direction': trade.get('direction'),
                'pnl': trade.get('pnl', 0),
                'balance': trade.get('balance', MODEL_STATS[name]['balance'])
            })
    # Optionally, reload analytics, notifications, etc. from disk/db if needed

from backend.db import save_notification, get_setting
from backend.email_utils import send_email
def notify(message, type_="info"):
    note = {
        "id": str(uuid.uuid4()),
        "timestamp": str(datetime.datetime.now()),
        "type": type_,
        "message": message,
        "read": 0
    }
    save_notification(note)
    # Send email if enabled
    email_enabled = get_setting("email_notifications", default="false") == "true"
    if email_enabled:
        subject = f"Crypto Bot Notification: {type_.capitalize()}"
        to_email = get_setting("email_address", default=None)
        send_email(subject, message, to_email=to_email)
import os
import joblib
import pandas as pd
import numpy as np
import uuid
import datetime
from backend.db import save_trade
from backend.trading import open_virtual_trade

MODEL_FILES = {
    'lgbm': 'kaia_rf_model.joblib',
    'rf': 'rf_model.joblib',
    'gb': 'gb_model.joblib',
    'xgb': 'xgb_model.joblib',
    'cat': 'cat_model.joblib',
    'voting': 'voting_model.joblib',
}

MODELS = {}
for name, path in MODEL_FILES.items():
    if os.path.exists(path):
        try:
            MODELS[name] = joblib.load(path)
        except Exception as e:
            print(f"Failed to load {name}: {e}")

if not MODELS:
    raise RuntimeError("No models found. Please train models first.")

# Load test data (simulate live data by iterating rows)
data_path = os.path.join(os.path.dirname(__file__), '../test.csv')
df = pd.read_csv(data_path)

FEATURE_COLS = [
    'open', 'high', 'low', 'close', 'volume', 'rsi', 'stoch_k', 'stoch_d', 'williams_r', 'roc', 'ao',
    'macd', 'macd_signal', 'macd_diff', 'adx', 'cci', 'sma_20', 'ema_20', 'bb_high', 'bb_low', 'atr', 'obv', 'cmf'
]


# --- Risk Management Enforcement ---
def get_risk_settings():
    risk_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/risk_settings.json'))
    if os.path.exists(risk_path):
        with open(risk_path, 'r') as f:
            return json.load(f)
    return {"max_drawdown": 1000, "stoploss": 1.0, "position_size": 100}

RISK = get_risk_settings()
MAX_DRAWDOWN = float(RISK.get("max_drawdown", 1000))
STOPLOSS = float(RISK.get("stoploss", 1.0))
POSITION_SIZE = float(RISK.get("position_size", 100))

VIRTUAL_BALANCE = {name: 10000.0 for name in MODELS}
PEAK_BALANCE = {name: 10000.0 for name in MODELS}
TRADING_HALTED = {name: False for name in MODELS}


# Advanced tracking structures
MODEL_STATS = {name: {'win': 0, 'loss': 0, 'mistakes': 0, 'trades': 0, 'balance': 10000.0, 'history': []} for name in MODELS}
MISTAKE_MEMORY = {name: set() for name in MODELS}  # To avoid repeating mistakes

# Call resume_state() after MODEL_STATS is initialized
resume_state()

for idx, row in df.iterrows():
    features = np.array([row.get(col, 0) for col in FEATURE_COLS]).reshape(1, -1)
    true_price = row['close']
    timestamp = row.get('timestamp', str(idx))
    symbol = 'SIMCOIN'
    next_idx = idx + 1
    next_price = df.iloc[next_idx]['close'] if next_idx < len(df) else true_price
    for name, model in MODELS.items():
        try:
            if TRADING_HALTED[name]:
                continue
            # Avoid repeating mistakes: skip if this feature set led to a loss before
            feat_hash = hash(tuple(features.flatten()))
            if feat_hash in MISTAKE_MEMORY[name]:
                continue
            pred = model.predict(features)[0]
            direction = 'LONG' if pred else 'SHORT'
            # Enforce position size
            amount = POSITION_SIZE
            # Enforce stop-loss
            tp_pct = 2.0
            sl_pct = STOPLOSS
            trade_id = open_virtual_trade(symbol, direction, amount, true_price, tp_pct, sl_pct)
            # Simulate PnL
            if direction == 'LONG':
                profit = (next_price - true_price) / true_price
            else:
                profit = (true_price - next_price) / true_price
            # Apply stop-loss
            max_loss = -sl_pct / 100.0 * amount
            pnl = max(profit * amount, max_loss)
            MODEL_STATS[name]['balance'] += pnl
            PEAK_BALANCE[name] = max(PEAK_BALANCE[name], MODEL_STATS[name]['balance'])
            drawdown = PEAK_BALANCE[name] - MODEL_STATS[name]['balance']
            # Enforce max drawdown
            if drawdown > MAX_DRAWDOWN:
                TRADING_HALTED[name] = True
                msg = f"[RISK] Trading halted for {name} due to max drawdown. Drawdown: {drawdown:.2f} > Limit: {MAX_DRAWDOWN:.2f}"
                print(msg)
                notify(msg, type_="danger")
                continue
            MODEL_STATS[name]['trades'] += 1
            win = pnl > 0
            if win:
                MODEL_STATS[name]['win'] += 1
                if pnl > 0.05 * amount:
                    notify(f"{name} made a large profit: {pnl:.2f}", type_="success")
            else:
                MODEL_STATS[name]['loss'] += 1
                MODEL_STATS[name]['mistakes'] += 1
                MISTAKE_MEMORY[name].add(feat_hash)
                if pnl < -0.05 * amount:
                    notify(f"{name} made a large loss: {pnl:.2f}", type_="danger")
            MODEL_STATS[name]['history'].append({'timestamp': timestamp, 'direction': direction, 'pnl': pnl, 'balance': MODEL_STATS[name]['balance']})
            print(f"{timestamp} | {name} | {direction} | Trade ID: {trade_id} | PnL: {pnl:.2f} | Balance: {MODEL_STATS[name]['balance']:.2f}")
        except Exception as e:
            print(f"Model {name} failed to predict: {e}")

# Output analytics

# Save analytics for dashboard API (with PnL and drawdown curves)
import json
analytics = {}
def compute_drawdown(balance_curve):
    peak = balance_curve[0] if balance_curve else 0
    drawdowns = []
    for b in balance_curve:
        if b > peak:
            peak = b
        drawdowns.append(peak - b)
    return drawdowns

for name, stats in MODEL_STATS.items():
    total = stats['trades']
    win = stats['win']
    loss = stats['loss']
    mistakes = stats['mistakes']
    balance = stats['balance']
    win_rate = (win / total * 100) if total else 0
    # PnL curve (balance over time)
    balance_curve = [h['balance'] for h in stats['history']]
    drawdown_curve = compute_drawdown(balance_curve)
    analytics[name] = {
        'trades': total,
        'win': win,
        'loss': loss,
        'mistakes': mistakes,
        'win_rate': win_rate,
        'final_balance': balance,
        'pnl_curve': balance_curve,
        'drawdown_curve': drawdown_curve
    }
with open('model_analytics.json', 'w') as f:
    json.dump(analytics, f, indent=2)

print("\nModel Performance Summary:")
for name, stats in analytics.items():
    print(f"{name}: Trades={stats['trades']}, Win={stats['win']}, Loss={stats['loss']}, Mistakes={stats['mistakes']}, WinRate={stats['win_rate']:.2f}%, FinalBalance={stats['final_balance']:.2f}")

print("\nAuto trading backend integration complete. Trades are logged in the database and analytics are saved for dashboard.")
