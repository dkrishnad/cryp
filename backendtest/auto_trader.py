import os
import time
import joblib
import pandas as pd
import numpy as np
from datetime import datetime

# List of model files and their names
MODEL_FILES = {
    'lgbm': 'kaia_rf_model.joblib',
    'rf': 'rf_model.joblib',
    'gb': 'gb_model.joblib',
    'xgb': 'xgb_model.joblib',
    'cat': 'cat_model.joblib',
    'voting': 'voting_model.joblib',
}

# Load all available models
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

# Feature columns (must match training)
FEATURE_COLS = [
    'open', 'high', 'low', 'close', 'volume', 'rsi', 'stoch_k', 'stoch_d', 'williams_r', 'roc', 'ao',
    'macd', 'macd_signal', 'macd_diff', 'adx', 'cci', 'sma_20', 'ema_20', 'bb_high', 'bb_low', 'atr', 'obv', 'cmf'
]

# Virtual trading state
VIRTUAL_BALANCE = {name: 10000.0 for name in MODELS}
TRADE_LOG = []

# Simulate trading loop (one row = one time step)
for idx, row in df.iterrows():
    features = np.array([row.get(col, 0) for col in FEATURE_COLS]).reshape(1, -1)
    true_price = row['close']
    timestamp = row.get('timestamp', str(idx))
    for name, model in MODELS.items():
        try:
            pred = model.predict(features)[0]
            # For binary: 1=LONG, 0=SHORT
            direction = 'LONG' if pred else 'SHORT'
            # Simulate trade: +1% for correct, -1% for wrong (using next row's price if available)
            next_idx = idx + 1
            if next_idx < len(df):
                next_price = df.iloc[next_idx]['close']
                profit = (next_price - true_price) / true_price if direction == 'LONG' else (true_price - next_price) / true_price
                pnl = VIRTUAL_BALANCE[name] * profit * 1.0  # 100% position size for demo
                VIRTUAL_BALANCE[name] += pnl
            else:
                pnl = 0.0
            TRADE_LOG.append({
                'timestamp': timestamp,
                'model': name,
                'direction': direction,
                'entry_price': true_price,
                'pnl': pnl,
                'balance': VIRTUAL_BALANCE[name],
            })
        except Exception as e:
            print(f"Model {name} failed to predict: {e}")
    # Simulate time delay (remove or adjust for real-time)
    # time.sleep(0.1)

# Save trade log to CSV for analysis
trade_log_df = pd.DataFrame(TRADE_LOG)
trade_log_df.to_csv('virtual_trade_log.csv', index=False)

print("Auto trading simulation complete. Final balances:")
for name, bal in VIRTUAL_BALANCE.items():
    print(f"{name}: {bal:.2f}")
print("Trade log saved to virtual_trade_log.csv")
