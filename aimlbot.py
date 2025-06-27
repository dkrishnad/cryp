import threading
import time
import datetime
import pandas as pd
import numpy as np
import sqlite3
import uuid

DB_PATH = "trades.db"

# --- Database Initialization ---
def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
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

initialize_database()

# --- Trade Logic Example ---
def open_virtual_trade(symbol, direction, amount, price, tp_pct, sl_pct):
    trade_id = str(uuid.uuid4())
    tp_price = price * (1 + tp_pct/100) if direction == "LONG" else price * (1 - tp_pct/100)
    sl_price = price * (1 - sl_pct/100) if direction == "LONG" else price * (1 + sl_pct/100)
    trade = {
        'id': trade_id,
        'symbol': symbol,
        'direction': direction,
        'amount': amount,
        'entry_price': price,
        'tp_price': tp_price,
        'sl_price': sl_price,
        'status': 'OPEN',
        'open_time': str(datetime.datetime.now()),
        'close_time': None,
        'pnl': 0.0,
        'current_price': price,
        'close_price': None
    }
    # Save to DB
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO trades (id, symbol, direction, amount, entry_price, tp_price, sl_price, status, open_time, close_time, pnl, current_price, close_price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (trade['id'], trade['symbol'], trade['direction'], trade['amount'], trade['entry_price'],
         trade['tp_price'], trade['sl_price'], trade['status'], trade['open_time'], trade['close_time'],
         trade['pnl'], trade['current_price'], trade['close_price']))
    conn.commit()
    conn.close()
    return trade_id

# --- Example ML Model (Dummy) ---
def dummy_predict(df):
    # Pretend to use ML to predict direction
    return np.random.choice(["LONG", "SHORT"]), np.random.uniform(50, 100)

# --- Example Backtest ---
def run_backtest(symbol, data, initial_capital=10000):
    capital = initial_capital
    trades = []
    for i, row in data.iterrows():
        direction, conf = dummy_predict(row)
        price = row['close']
        amount = capital * 0.1
        trade_id = open_virtual_trade(symbol, direction, amount, price, 2.0, 1.0)
        trades.append(trade_id)
        # Simulate P&L
        pnl = np.random.uniform(-0.02, 0.03) * amount
        capital += pnl
    return trades, capital

# --- Background Task Example ---
class TaskManager:
    def __init__(self):
        self.tasks = {}
    def run_task(self, name, func, *args, **kwargs):
        if name in self.tasks and self.tasks[name].is_alive():
            print(f"Task {name} already running.")
            return
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        self.tasks[name] = thread
    def is_running(self, name):
        return name in self.tasks and self.tasks[name].is_alive()

task_manager = TaskManager()

# --- Example Usage ---
if __name__ == "__main__":
    # Example: open a trade in background
    def trade_job():
        print("Opening trade...")
        tid = open_virtual_trade("BTCUSDT", "LONG", 100, 50000, 2.0, 1.0)
        print(f"Trade opened: {tid}")
    task_manager.run_task("trade", trade_job)
    # Example: run a backtest in background
    def backtest_job():
        print("Running backtest...")
        df = pd.DataFrame({
            'close': np.random.uniform(20000, 60000, 100)
        })
        trades, final_cap = run_backtest("BTCUSDT", df)
        print(f"Backtest done. Final capital: {final_cap}")
    task_manager.run_task("backtest", backtest_job)
    # Wait for tasks to finish
    while task_manager.is_running("trade") or task_manager.is_running("backtest"):
        print("Tasks running...")
        time.sleep(1)
    print("All tasks done.")
