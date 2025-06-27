# Perfectbot V2 – Crypto Trading Bot

Perfectbot V2 is an advanced, AI-powered crypto trading bot with a Streamlit web interface. It supports live trading simulation, technical analysis, machine learning predictions, and performance monitoring. The bot is designed for flexibility, transparency, and continuous improvement.

## Features
- **Streamlit UI**: Modern, interactive dashboard and sidebar for configuration and monitoring.
- **AI/ML Integration**: Uses RandomForest, XGBoost, LightGBM, CatBoost, and ensemble models for price prediction.
- **Mistake Avoidance**: Learns from past losing trades to avoid repeating mistakes.
- **Trade Management**: Supports virtual trading, pending orders, and real-time trade execution.
- **Performance Analytics**: Tracks win rate, P&L, Sharpe ratio, drawdown, and more.
- **Database Persistence**: All trades and model data are stored in a local SQLite database (`trades.db`).
- **Resource Friendly**: Designed to run efficiently on cloud free tiers (e.g., AWS Free Tier).
- **Notifications**: Detailed notifications for trade execution, including entry price, execution price, and TP/SL status.
- **Feature Importance**: Visualize which features are most important to the ML models.
- **Backtesting**: Run lightweight backtests on historical data samples.
- **Prune Old Trades**: Keep your database size manageable with a single click.
- **Background Backtesting**: Runs in a background thread, continuously evaluating strategies on historical data.
- **Multiple Strategies**: Supports PrevClose, Moving Average Cross, and RSI-based strategies for backtesting.
- **Advanced Metrics**: Tracks win rate, average P&L, Sharpe ratio, and max drawdown for each strategy.
- **Backtest Log**: Maintains a log of recent backtest results, viewable in the sidebar.
- **Sidebar Controls**: Adjust backtest frequency, select strategy, and restart background backtesting from the sidebar.
- **Performance Notifications**: Alerts if win rate drops below 50% or a new best result is found during background backtesting.

## Requirements
- Python 3.8+
- Streamlit
- pandas, numpy, requests, scikit-learn
- xgboost, lightgbm, catboost (optional, for advanced ML)
- ta (technical analysis indicators)
- sqlite3 (standard library)

Install dependencies:
```bash
pip install streamlit pandas numpy requests scikit-learn xgboost lightgbm catboost ta
```

## Usage
1. Place all files in a folder (e.g., `Crypto bot`).
2. Open a terminal in that folder.
3. Run the app:
   ```bash
   streamlit run "#Perfectbot V2.txt"
   ```
4. Use the sidebar to configure trading pairs, risk, AI settings, and background backtesting options.
5. Monitor trades, analytics, notifications, and backtest results in the dashboard tabs and sidebar.

## Notes
- The bot is for educational and research purposes. Do not use with real funds without thorough testing.
- The app uses Binance public API for price data.
- All trades are virtual (paper trading) by default.
- For best results, keep your Python environment and dependencies up to date.

## License
MIT License

## Author
Hari (and contributors)

---
For questions or improvements, open an issue or pull request.
