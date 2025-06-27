"""
Binance Futures-Style Trading Dashboard Callbacks
"""

import requests
from dash import html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
from datetime import datetime
import json

# API URL
API_URL = "http://127.0.0.1:8000"

# Import layout functions with fallback
try:
    from .futures_trading_layout import create_futures_positions_table, create_futures_history_table
except ImportError:
    import sys
    import os
    # Ensure dashboard directory is in path
    dashboard_dir = os.path.dirname(os.path.abspath(__file__))
    if dashboard_dir not in sys.path:
        sys.path.insert(0, dashboard_dir)
    from futures_trading_layout import create_futures_positions_table, create_futures_history_table

def register_futures_callbacks(app):
    """Register all futures trading callbacks"""
    
    # Auto-refresh account and positions
    @app.callback(
        [Output("futures-total-balance", "children"),
         Output("futures-available-balance", "children"),
         Output("futures-margin-used", "children"),
         Output("futures-margin-ratio", "children"),
         Output("futures-unrealized-pnl", "children"),
         Output("futures-open-positions", "children"),
         Output("futures-trading-status", "children"),
         Output("futures-can-trade", "children"),
         Output("futures-positions-table", "children"),
         Output("futures-history-table", "children")],
        [Input("futures-refresh-interval", "n_intervals"),
         Input("futures-refresh-positions-btn", "n_clicks")],
        prevent_initial_call=False
    )
    def update_futures_dashboard(n_intervals, refresh_clicks):
        """Update the entire futures dashboard"""
        try:
            # Get account info
            account_resp = requests.get(f"{API_URL}/futures/account", timeout=5)
            positions_resp = requests.get(f"{API_URL}/futures/positions", timeout=5)
            history_resp = requests.get(f"{API_URL}/futures/history", timeout=5)
            
            # Default values
            total_balance = "$0.00"
            available_balance = "$0.00"
            margin_used = "$0.00"
            margin_ratio = "0.00%"
            unrealized_pnl = "$0.00"
            open_positions_count = "0"
            trading_status = "🔴 Inactive"
            can_trade = "No"
            positions_table = html.P("No data available", className="text-muted text-center p-3")
            history_table = html.P("No data available", className="text-muted text-center p-3")
            
            # Update account info
            if account_resp.status_code == 200:
                account_data = account_resp.json()
                if account_data.get("status") == "success":
                    account = account_data["account"]
                    
                    total_balance = f"${account['total_wallet_balance']:,.2f}"
                    available_balance = f"${account['available_balance']:,.2f}"
                    margin_used = f"${account['total_margin_used']:,.2f}"
                    margin_ratio = f"{account['margin_ratio']*100:.2f}%"
                    unrealized_pnl = f"${account['total_unrealized_pnl']:,.2f}"
                    trading_status = "🟢 Active" if account['can_trade'] else "🔴 Risk Limit"
                    can_trade = "Yes" if account['can_trade'] else "No"
            
            # Update positions
            if positions_resp.status_code == 200:
                positions_data = positions_resp.json()
                if positions_data.get("status") == "success":
                    positions = positions_data["positions"]
                    open_positions_count = str(len(positions))
                    positions_table = create_futures_positions_table(positions)
            
            # Update history
            if history_resp.status_code == 200:
                history_data = history_resp.json()
                if history_data.get("status") == "success":
                    trades = history_data["trades"]
                    history_table = create_futures_history_table(trades[-20:])  # Last 20 trades
            
            return (
                total_balance, available_balance, margin_used, margin_ratio,
                unrealized_pnl, open_positions_count, trading_status, can_trade,
                positions_table, history_table
            )
            
        except Exception as e:
            print(f"Error updating futures dashboard: {e}")
            return (
                "$0.00", "$0.00", "$0.00", "0.00%",
                "$0.00", "0", "🔴 Error", "No",
                html.P("Error loading data", className="text-danger text-center p-3"),
                html.P("Error loading data", className="text-danger text-center p-3")
            )
    
    # Manual Long Position
    @app.callback(
        Output("futures-trade-result", "children"),
        [Input("futures-long-btn", "n_clicks")],
        [State("futures-symbol-dropdown", "value"),
         State("futures-leverage-slider", "value"),
         State("futures-margin-input", "value"),
         State("futures-sl-input", "value"),
         State("futures-tp-input", "value")],
        prevent_initial_call=True
    )
    def execute_long_position(n_clicks, symbol, leverage, margin, sl_percent, tp_percent):
        """Execute a manual long position"""
        if not n_clicks:
            return ""
        
        try:
            # Get current price
            price_resp = requests.get(f"{API_URL}/price/{symbol.lower()}")
            if price_resp.status_code != 200:
                return dbc.Alert("Failed to get current price", color="danger", dismissable=True)
            
            current_price = price_resp.json()["price"]
            
            # Create futures signal
            signal_data = {
                "symbol": symbol,
                "side": "LONG",
                "confidence": 1.0,  # Manual trade
                "price": current_price,
                "timestamp": datetime.now().isoformat(),
                "leverage": leverage,
                "stop_loss_percent": sl_percent,
                "take_profit_percent": tp_percent
            }
            
            # Execute position
            resp = requests.post(f"{API_URL}/futures/open_position", json=signal_data)
            result = resp.json()
            
            if result.get("status") == "success":
                position = result["position"]
                return dbc.Alert([
                    html.H5("🟢 LONG Position Opened!", className="alert-heading"),
                    html.P(f"Symbol: {position['symbol']}"),
                    html.P(f"Size: {position['size']:.4f}"),
                    html.P(f"Entry Price: ${position['entry_price']:.4f}"),
                    html.P(f"Leverage: {position['leverage']}x"),
                    html.P(f"Margin Used: ${position['margin_used']:.2f}"),
                    html.P(f"Liquidation Price: ${position['liquidation_price']:.4f}")
                ], color="success", dismissable=True)
            else:
                return dbc.Alert(f"Error: {result.get('message', 'Unknown error')}", color="danger", dismissable=True)
                
        except Exception as e:
            return dbc.Alert(f"Error: {str(e)}", color="danger", dismissable=True)
    
    # Manual Short Position
    @app.callback(
        Output("futures-trade-result", "children", allow_duplicate=True),
        [Input("futures-short-btn", "n_clicks")],
        [State("futures-symbol-dropdown", "value"),
         State("futures-leverage-slider", "value"),
         State("futures-margin-input", "value"),
         State("futures-sl-input", "value"),
         State("futures-tp-input", "value")],
        prevent_initial_call=True
    )
    def execute_short_position(n_clicks, symbol, leverage, margin, sl_percent, tp_percent):
        """Execute a manual short position"""
        if not n_clicks:
            return ""
        
        try:
            # Get current price
            price_resp = requests.get(f"{API_URL}/price/{symbol.lower()}")
            if price_resp.status_code != 200:
                return dbc.Alert("Failed to get current price", color="danger", dismissable=True)
            
            current_price = price_resp.json()["price"]
            
            # Create futures signal
            signal_data = {
                "symbol": symbol,
                "side": "SHORT",
                "confidence": 1.0,  # Manual trade
                "price": current_price,
                "timestamp": datetime.now().isoformat(),
                "leverage": leverage,
                "stop_loss_percent": sl_percent,
                "take_profit_percent": tp_percent
            }
            
            # Execute position
            resp = requests.post(f"{API_URL}/futures/open_position", json=signal_data)
            result = resp.json()
            
            if result.get("status") == "success":
                position = result["position"]
                return dbc.Alert([
                    html.H5("🔴 SHORT Position Opened!", className="alert-heading"),
                    html.P(f"Symbol: {position['symbol']}"),
                    html.P(f"Size: {position['size']:.4f}"),
                    html.P(f"Entry Price: ${position['entry_price']:.4f}"),
                    html.P(f"Leverage: {position['leverage']}x"),
                    html.P(f"Margin Used: ${position['margin_used']:.2f}"),
                    html.P(f"Liquidation Price: ${position['liquidation_price']:.4f}")
                ], color="danger", dismissable=True)
            else:
                return dbc.Alert(f"Error: {result.get('message', 'Unknown error')}", color="danger", dismissable=True)
                
        except Exception as e:
            return dbc.Alert(f"Error: {str(e)}", color="danger", dismissable=True)
    
    # Save Futures Settings
    @app.callback(
        Output("futures-settings-result", "children"),
        [Input("futures-save-settings-btn", "n_clicks")],
        [State("futures-auto-leverage-dropdown", "value"),
         State("futures-auto-margin-input", "value"),
         State("futures-auto-sl-input", "value"),
         State("futures-auto-tp-input", "value"),
         State("futures-max-margin-ratio", "value"),
         State("futures-risk-per-trade", "value")],
        prevent_initial_call=True
    )
    def save_futures_settings(n_clicks, leverage, margin, sl, tp, max_margin_ratio, risk_per_trade):
        """Save futures trading settings"""
        if not n_clicks:
            return ""
        
        try:
            settings_data = {
                "default_leverage": leverage,
                "max_leverage": 125,
                "default_margin_per_trade": margin,
                "auto_stop_loss": True,
                "auto_take_profit": True,
                "default_stop_loss_percent": sl,
                "default_take_profit_percent": tp,
                "liquidation_buffer_percent": 0.5,
                "risk_per_trade_percent": risk_per_trade
            }
            
            resp = requests.post(f"{API_URL}/futures/settings", json=settings_data)
            result = resp.json()
            
            if result.get("status") == "success":
                return dbc.Alert("✅ Settings saved successfully!", color="success", dismissable=True)
            else:
                return dbc.Alert(f"Error: {result.get('message', 'Unknown error')}", color="danger", dismissable=True)
                
        except Exception as e:
            return dbc.Alert(f"Error: {str(e)}", color="danger", dismissable=True)
    
    # Auto Trading Toggle
    @app.callback(
        Output("futures-settings-result", "children", allow_duplicate=True),
        [Input("futures-auto-trading-switch", "value")],
        prevent_initial_call=True
    )
    def toggle_futures_auto_trading(enabled):
        """Toggle futures auto trading"""
        try:
            # Update the regular auto trading toggle to use futures system
            toggle_data = {"enabled": enabled}
            resp = requests.post(f"{API_URL}/auto_trading/toggle", json=toggle_data)
            result = resp.json()
            
            if result.get("status") == "success":
                status = "enabled" if enabled else "disabled"
                color = "success" if enabled else "warning"
                return dbc.Alert(f"🤖 Futures auto trading {status}!", color=color, dismissable=True)
            else:
                return dbc.Alert(f"Error: {result.get('message', 'Unknown error')}", color="danger", dismissable=True)
                
        except Exception as e:
            return dbc.Alert(f"Error: {str(e)}", color="danger", dismissable=True)
    
    print("✅ Futures trading callbacks registered successfully")
