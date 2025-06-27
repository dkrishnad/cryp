import sqlite3
import datetime
import uuid

DB_PATH = "trades.db"

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
    c.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            type TEXT,
            message TEXT,
            read INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_trade(trade):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO trades (id, symbol, direction, amount, entry_price, tp_price, sl_price, status, open_time, close_time, pnl, current_price, close_price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (trade['id'], trade['symbol'], trade['direction'], trade['amount'], trade['entry_price'],
         trade['tp_price'], trade['sl_price'], trade['status'], trade['open_time'], trade['close_time'],
         trade['pnl'], trade['current_price'], trade['close_price']))
    conn.commit()
    conn.close()

def get_trades(limit=100):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM trades ORDER BY open_time DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    keys = ["id", "symbol", "direction", "amount", "entry_price", "tp_price", "sl_price", "status", "open_time", "close_time", "pnl", "current_price", "close_price"]
    return [dict(zip(keys, row)) for row in rows]

# --- Trade CRUD ---
def update_trade(trade_id, updates):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
    values = list(updates.values()) + [trade_id]
    c.execute(f"UPDATE trades SET {set_clause} WHERE id = ?", values)
    conn.commit()
    conn.close()

def delete_trade(trade_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM trades WHERE id = ?", (trade_id,))
    conn.commit()
    conn.close()

# --- Backtest Results CRUD ---
def save_backtest_result(result):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO backtest_results (backtest_id, timestamp, symbol, strategy, results)
        VALUES (?, ?, ?, ?, ?)''',
        (result['backtest_id'], result['timestamp'], result['symbol'], result['strategy'], result['results']))
    conn.commit()
    conn.close()

def get_backtest_results(limit=100):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM backtest_results ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    keys = ["backtest_id", "timestamp", "symbol", "strategy", "results"]
    return [dict(zip(keys, row)) for row in rows]

def delete_backtest_result(backtest_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM backtest_results WHERE backtest_id = ?", (backtest_id,))
    conn.commit()
    conn.close()

# --- Notifications CRUD ---
def save_notification(notification):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO notifications (id, timestamp, type, message, read)
        VALUES (?, ?, ?, ?, ?)''',
        (notification['id'], notification['timestamp'], notification['type'], notification['message'], int(notification.get('read', 0))))
    conn.commit()
    conn.close()

def get_notifications(limit=100, unread_only=False):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if unread_only:
        c.execute("SELECT * FROM notifications WHERE read = 0 ORDER BY timestamp DESC LIMIT ?", (limit,))
    else:
        c.execute("SELECT * FROM notifications ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    keys = ["id", "timestamp", "type", "message", "read"]
    return [dict(zip(keys, row)) for row in rows]

def mark_notification_read(notification_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE notifications SET read = 1 WHERE id = ?", (notification_id,))
    conn.commit()
    conn.close()

def delete_notification(notification_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
    conn.commit()
    conn.close()

# --- Settings CRUD ---
def set_setting(key, value):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)''', (key, value))
    conn.commit()
    conn.close()

def get_setting(key, default=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT value FROM settings WHERE key = ?''', (key,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    return default
