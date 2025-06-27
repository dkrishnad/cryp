

#!/usr/bin/env python3
"""
SIMPLE BACKEND API SERVER
Basic Flask API server for crypto bot dashboard
"""
#!/usr/bin/env python3
"""
SIMPLE BACKEND API SERVER
Basic Flask API server for crypto bot dashboard
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import time

app = Flask(__name__)
CORS(app)
# --- Dashboard Data Endpoints (MOVED HERE for correct app context) ---
@app.route('/positions/open')
def get_open_positions():
    # Simulate open positions
    open_positions = [
        {
            "id": 1,
            "symbol": "BTCUSDT",
            "action": "LONG",
            "amount": 0.01,
            "entry_price": 43000.0,
            "current_price": 43500.0,
            "stop_loss": 42000.0,
            "take_profit": 44000.0
        },
        {
            "id": 2,
            "symbol": "ETHUSDT",
            "action": "SHORT",
            "amount": 0.5,
            "entry_price": 2700.0,
            "current_price": 2650.0,
            "stop_loss": 2750.0,
            "take_profit": 2600.0
        }
    ]
    return jsonify({"positions": open_positions})

@app.route('/indicators/technical')
def get_technical_indicators():
    # Simulate technical indicators
    indicators = {
        "current_regime": "Bullish",
        "rsi": 62.5,
        "macd": 1.2,
        "bollinger_bands": {
            "upper": 44000.0,
            "lower": 42000.0
        }
    }
    return jsonify(indicators)

@app.route('/trades/active')
def get_active_trades():
    # Simulate active trades
    active_trades = [
        {
            "id": 101,
            "symbol": "BTCUSDT",
            "direction": "LONG",
            "amount": 0.01,
            "entry_price": 43000.0
        },
        {
            "id": 102,
            "symbol": "ETHUSDT",
            "direction": "SHORT",
            "amount": 0.5,
            "entry_price": 2700.0
        }
    ]
    return jsonify({"active_trades": active_trades})

@app.route('/portfolio/status')
def get_portfolio_status():
    # Simulate portfolio status
    status = {
        "balance": 1000.0,
        "total_pnl": 120.5,
        "active_trades": 2,
        "low_balance": False
    }
    return jsonify(status)

@app.route('/performance/monitor')
def get_performance_monitor():
    # Simulate performance monitor
    monitor = {
        "win_rate": 67.5,
        "total_trades": 100,
        "avg_return": 2.3
    }
    return jsonify(monitor)

# Sample data
virtual_balance = 1000.0
trades = []
signals = []
notifications = []

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": time.time()})

@app.route('/virtual_balance')
def get_virtual_balance():
    return jsonify({"balance": virtual_balance})

@app.route('/trading/reset_balance', methods=['POST'])
def reset_balance():
    global virtual_balance
    virtual_balance = 1000.0
    return jsonify({"balance": virtual_balance, "message": "Balance reset"})

@app.route('/trading/open_long', methods=['POST'])
def open_long():
    data = request.get_json() or {}
    symbol = data.get('symbol', 'btcusdt')
    amount = data.get('amount', 100)
    
    trade = {
        "id": len(trades) + 1,
        "symbol": symbol,
        "side": "long",
        "amount": amount,
        "timestamp": time.time()
    }
    trades.append(trade)
    
    return jsonify({"success": True, "trade": trade})

@app.route('/trading/open_short', methods=['POST'])
def open_short():
    data = request.get_json() or {}
    symbol = data.get('symbol', 'btcusdt')
    amount = data.get('amount', 100)
    
    trade = {
        "id": len(trades) + 1,
        "symbol": symbol,
        "side": "short", 
        "amount": amount,
        "timestamp": time.time()
    }
    trades.append(trade)
    
    return jsonify({"success": True, "trade": trade})

@app.route('/trading/close_all', methods=['POST'])
def close_all():
    global trades
    closed_count = len(trades)
    trades = []
    return jsonify({"success": True, "closed_trades": closed_count})

@app.route('/trading/status')
def trading_status():
    return jsonify({
        "active_trades": len(trades),
        "trades": trades[-5:],
        "total_pnl": random.uniform(-50, 100)
    })

# NEW ENDPOINTS FOR DASHBOARD
@app.route('/trades')
def get_trades():
    return jsonify({
        "trades": trades[-20:],  # Last 20 trades
        "total_trades": len(trades)
    })

@app.route('/trades/analytics')
def trades_analytics():
    return jsonify({
        "total_trades": len(trades),
        "profitable_trades": random.randint(0, len(trades)),
        "win_rate": random.uniform(55, 85),
        "total_profit": random.uniform(-100, 500),
        "avg_profit": random.uniform(5, 25)
    })

@app.route('/auto_trading/signals')
def auto_trading_signals():
    # Generate some sample signals
    sample_signals = [
        {"signal": "BUY", "symbol": "btcusdt", "confidence": random.uniform(0.6, 0.9), "timestamp": time.time() - random.randint(0, 3600)},
        {"signal": "SELL", "symbol": "ethusdt", "confidence": random.uniform(0.6, 0.9), "timestamp": time.time() - random.randint(0, 3600)},
        {"signal": "HOLD", "symbol": "adausdt", "confidence": random.uniform(0.6, 0.9), "timestamp": time.time() - random.randint(0, 3600)}
    ]
    return jsonify({"signals": sample_signals})

@app.route('/auto_trading/current_signal')
def auto_trading_current_signal():
    signals = ["BUY", "SELL", "HOLD"]
    return jsonify({
        "signal": random.choice(signals),
        "symbol": "btcusdt",
        "confidence": random.uniform(0.5, 0.95),
        "timestamp": time.time()
    })

@app.route('/auto_trading/trades')
def auto_trading_trades():
    return jsonify({
        "recent_trades": trades[-10:],
        "active_positions": random.randint(0, 5),
        "daily_profit": random.uniform(-50, 100)
    })

@app.route('/ml/predict')
def ml_predict():
    symbol = request.args.get('symbol', 'btcusdt')
    
    signals = ['BUY', 'SELL', 'HOLD']
    signal = random.choice(signals)
    confidence = random.uniform(0.5, 0.95)
    
    return jsonify({
        "symbol": symbol,
        "signal": signal,
        "confidence": confidence,
        "timestamp": time.time()
    })

@app.route('/ml/hybrid/status')
def ml_hybrid_status():
    return jsonify({
        "status": "active",
        "accuracy": random.uniform(70, 90),
        "last_update": time.time(),
        "models_running": random.randint(2, 5)
    })

@app.route('/ml/hybrid/predict')
def ml_hybrid_predict():
    symbol = request.args.get('symbol', 'btcusdt')
    return jsonify({
        "symbol": symbol,
        "prediction": random.choice(["BUY", "SELL", "HOLD"]),
        "confidence": random.uniform(0.6, 0.95),
        "models_consensus": random.uniform(0.5, 1.0),
        "timestamp": time.time()
    })

@app.route('/ml/online/stats')
def ml_online_stats():
    return jsonify({
        "learning_rate": random.uniform(0.001, 0.01),
        "samples_processed": random.randint(1000, 10000),
        "accuracy": random.uniform(65, 88),
        "last_training": time.time() - random.randint(300, 3600)
    })

@app.route('/ml/data_collection/stats')
def ml_data_collection_stats():
    return jsonify({
        "total_samples": random.randint(50000, 200000),
        "recent_samples": random.randint(100, 1000),
        "collection_rate": random.uniform(10, 50),
        "last_collection": time.time() - random.randint(0, 300)
    })

@app.route('/ml/performance/history')
def ml_performance_history():
    history = []
    for i in range(10):
        history.append({
            "timestamp": time.time() - (i * 3600),
            "accuracy": random.uniform(60, 90),
            "profit": random.uniform(-20, 50),
            "trades": random.randint(5, 20)
        })
    return jsonify({"history": history})

@app.route('/notifications')
def get_notifications():
    sample_notifications = [
        {"type": "success", "message": "Trade executed successfully", "timestamp": time.time() - random.randint(0, 3600)},
        {"type": "info", "message": "New signal generated", "timestamp": time.time() - random.randint(0, 3600)},
        {"type": "warning", "message": "High volatility detected", "timestamp": time.time() - random.randint(0, 3600)}
    ]
    return jsonify({"notifications": sample_notifications})

@app.route('/features/indicators')
def features_indicators():
    symbol = request.args.get('symbol', 'btcusdt')
    return jsonify({
        "symbol": symbol,
        "rsi": random.uniform(20, 80),
        "macd": random.uniform(-5, 5),
        "bollinger_upper": random.uniform(45000, 50000),
        "bollinger_lower": random.uniform(40000, 45000),
        "volume": random.uniform(1000000, 5000000),
        "timestamp": time.time()
    })

@app.route('/auto_trading/status')
def auto_trading_status():
    return jsonify({
        "status": "enabled",
        "active": True,
        "trades_today": random.randint(0, 10),
        "profit_today": random.uniform(-50, 150),
        "running_time": random.randint(3600, 86400)
    })

@app.route('/auto_trading/start', methods=['POST'])
def start_auto_trading():
    return jsonify({"success": True, "message": "Auto trading started"})

@app.route('/auto_trading/stop', methods=['POST'])
def stop_auto_trading():
    return jsonify({"success": True, "message": "Auto trading stopped"})

@app.route('/analytics/summary')
def analytics_summary():
    return jsonify({
        "total_trades": len(trades),
        "success_rate": random.uniform(60, 85),
        "avg_profit": random.uniform(10, 50),
        "win_rate": random.uniform(55, 75),
        "total_profit": random.uniform(100, 1000),
        "daily_profit": random.uniform(-50, 100)
    })

@app.route('/backtest/run', methods=['POST'])
def run_backtest():
    data = request.get_json() or {}
    symbol = data.get('symbol', 'btcusdt')
    days = data.get('days', 30)
    
    return jsonify({
        "symbol": symbol,
        "days": days,
        "total_profit": random.uniform(50, 200),
        "total_trades": random.randint(20, 100),
        "win_rate": random.uniform(60, 80),
        "max_drawdown": random.uniform(5, 20),
        "sharpe_ratio": random.uniform(0.5, 2.0)
    })

@app.route('/ml/tune', methods=['POST'])
def tune_models():
    return jsonify({"success": True, "message": "Model tuning started"})

@app.route('/ml/online_learn', methods=['POST'])
def online_learn():
    return jsonify({"success": True, "message": "Online learning started"})

@app.route('/ml/analytics')
def ml_analytics():
    return jsonify({
        "model_accuracy": random.uniform(70, 90),
        "predictions_today": random.randint(50, 200),
        "confidence_avg": random.uniform(60, 80),
        "best_model": "ensemble_v2",
        "training_samples": random.randint(10000, 50000)
    })

@app.route('/price')
def get_price():
    """Get current price for a symbol"""
    symbol = request.args.get('symbol', 'btcusdt').upper()
    
    # Simulate realistic price data
    price_map = {
        'BTCUSDT': random.uniform(42000, 45000),
        'ETHUSDT': random.uniform(2500, 2800),
        'ADAUSDT': random.uniform(0.35, 0.45),
        'SOLUSDT': random.uniform(80, 120),
        'DOGEUSDT': random.uniform(0.08, 0.12)
    }
    
    price = price_map.get(symbol, random.uniform(1, 100))
    
    return jsonify({
        "symbol": symbol,
        "price": round(price, 4),
        "timestamp": time.time()
    })

if __name__ == '__main__':
    print("🚀 Starting Crypto Bot Backend API...")
    print("📊 API available at: http://localhost:8001")
    print("🔗 All endpoints now supported!")
    app.run(debug=False, host='127.0.0.1', port=8001)
