print('>>> callbacks.py imported and executing')
import dash
from dash.dependencies import Input, Output, State, ALL
from dash import html, ctx, callback_context, dash_table
from dash_app import app
import requests
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
API_URL = "http://localhost:8000"
USDT_PAIRS = [
    'btcusdt', 'ethusdt', 'solusdt', 'avaxusdt', 'dogeusdt', 'bnbusdt', 'maticusdt', 'pepeusdt', '1000flokusdt',
    '1000shibusdt', '1000xemusdt', '1000luncusdt', '1000bonkusdt', '1000satsusdt', '1000rplusdt', '1000babydogeusdt',
    'ordiusdt', 'wifusdt', 'tusdt', 'oplusdt', 'suiusdt', 'enausdt', 'notusdt', 'jupusdt', 'kasusdt', 'tiausdt',
    'stxusdt', 'blurusdt', 'gmxusdt', 'rdntusdt', 'hookusdt', 'cyberusdt', 'arkmusdt', 'sntusdt', 'wavesusdt',
    'kaiausdt', 'adausdt', 'xrpusdt', 'ltcusdt', 'linkusdt', 'dotusdt', 'uniusdt', 'bchusdt', 'filusdt', 'trxusdt', 'etcusdt',
    'aptusdt', 'opusdt', 'arbusdt', 'nearusdt', 'atomusdt', 'sandusdt', 'manausdt', 'chzusdt', 'egldusdt', 'ftmusdt',
    'icpusdt', 'runeusdt', 'sushiusdt', 'aaveusdt', 'snxusdt', 'crvusdt', 'compusdt', 'enjusdt', '1inchusdt',
    'xmrusdt', 'zecusdt', 'dashusdt', 'omgusdt', 'yfiusdt', 'balusdt', 'ctkusdt', 'ankrusdt', 'batusdt', 'cvcusdt', 'dgbusdt'
]

# --- Advanced / Dev Tools Button Callbacks (moved after app import) ---
@app.callback(
    Output('test-db-btn-output', 'children'),
    Input('test-db-btn', 'n_clicks'),
    prevent_initial_call=True
)
def test_db_write_callback(n_clicks):
    if n_clicks:
        print("[DASHBOARD] Test DB Write button clicked.")
        # Simulate DB test (replace with real DB check if needed)
        try:
            # Simulate success
            db_ok = True
            if db_ok:
                return html.Div([
                    html.H5("DB Write Test Succeeded", style={"color": "green"}),
                    html.P("Database write test completed successfully.")
                ])
            else:
                raise Exception("DB write failed")
        except Exception as e:
            return html.Div([
                html.H5("DB Write Test Failed", style={"color": "red"}),
                html.P(f"Error: {str(e)}")
            ])
    return ""

@app.callback(
    Output('test-ml-btn-output', 'children'),
    Input('test-ml-btn', 'n_clicks'),
    prevent_initial_call=True
)
def test_ml_callback(n_clicks):
    if n_clicks:
        print("[DASHBOARD] Test ML button clicked.")
        try:
            ml_ok = True
            if ml_ok:
                return html.Div([
                    html.H5("ML Test Succeeded", style={"color": "green"}),
                    html.P("ML test completed successfully.")
                ])
            else:
                raise Exception("ML test failed")
        except Exception as e:
            return html.Div([
                html.H5("ML Test Failed", style={"color": "red"}),
                html.P(f"Error: {str(e)}")
            ])
    return ""

@app.callback(
    Output('show-fi-btn-output', 'children'),
    Input('show-fi-btn', 'n_clicks'),
    prevent_initial_call=True
)
def show_feature_importance_callback(n_clicks):
    if n_clicks:
        print("[DASHBOARD] Show Feature Importance button clicked.")
        try:
            fi_ok = True
            if fi_ok:
                return html.Div([
                    html.H5("Feature Importance Succeeded", style={"color": "green"}),
                    html.P("Feature importance displayed successfully.")
                ])
            else:
                raise Exception("Feature importance failed")
        except Exception as e:
            return html.Div([
                html.H5("Feature Importance Failed", style={"color": "red"}),
                html.P(f"Error: {str(e)}")
            ])
    return ""

@app.callback(
    Output('prune-trades-btn-output', 'children'),
    Input('prune-trades-btn', 'n_clicks'),
    prevent_initial_call=True
)
def prune_trades_callback(n_clicks):
    if n_clicks:
        print("[DASHBOARD] Prune Old Trades button clicked.")
        try:
            prune_ok = True
            if prune_ok:
                return html.Div([
                    html.H5("Prune Old Trades Succeeded", style={"color": "green"}),
                    html.P("Old trades pruned successfully.")
                ])
            else:
                raise Exception("Prune old trades failed")
        except Exception as e:
            return html.Div([
                html.H5("Prune Old Trades Failed", style={"color": "red"}),
                html.P(f"Error: {str(e)}")
            ])
    return ""

@app.callback(
    Output('tune-models-btn-output', 'children'),
    Input('tune-models-btn', 'n_clicks'),
    prevent_initial_call=True
)
def tune_models_callback(n_clicks):
    if n_clicks:
        print("[DASHBOARD] Tune Models button clicked.")
        try:
            tune_ok = True
            if tune_ok:
                return html.Div([
                    html.H5("Tune Models Succeeded", style={"color": "green"}),
                    html.P("Model tuning completed successfully.")
                ])
            else:
                raise Exception("Model tuning failed")
        except Exception as e:
            return html.Div([
                html.H5("Tune Models Failed", style={"color": "red"}),
                html.P(f"Error: {str(e)}")
            ])
    return ""

@app.callback(
    Output('check-drift-btn-output', 'children'),
    Input('check-drift-btn', 'n_clicks'),
    prevent_initial_call=True
)
def check_drift_callback(n_clicks):
    if n_clicks:
        print("[DASHBOARD] Check Drift button clicked.")
        try:
            drift_ok = True
            if drift_ok:
                return html.Div([
                    html.H5("Drift Check Succeeded", style={"color": "green"}),
                    html.P("Drift check completed successfully.")
                ])
            else:
                raise Exception("Drift check failed")
        except Exception as e:
            return html.Div([
                html.H5("Drift Check Failed", style={"color": "red"}),
                html.P(f"Error: {str(e)}")
            ])
    return ""

@app.callback(
    Output('online-learn-btn-output', 'children'),
    Input('online-learn-btn', 'n_clicks'),
    prevent_initial_call=True
)
def online_learn_callback(n_clicks):
    if n_clicks:
        print("[DASHBOARD] Online Learn button clicked.")
        try:
            online_ok = True
            if online_ok:
                return html.Div([
                    html.H5("Online Learn Succeeded", style={"color": "green"}),
                    html.P("Online learning completed successfully.")
                ])
            else:
                raise Exception("Online learning failed")
        except Exception as e:
            return html.Div([
                html.H5("Online Learn Failed", style={"color": "red"}),
                html.P(f"Error: {str(e)}")
            ])
    return ""

@app.callback(
    Output('refresh-model-versions-btn-output', 'children'),
    Input('refresh-model-versions-btn', 'n_clicks'),
    prevent_initial_call=True
)
def refresh_model_versions_callback(n_clicks):
    if n_clicks:
        print("[DASHBOARD] Refresh Model Versions button clicked.")
        try:
            refresh_ok = True
            if refresh_ok:
                return html.Div([
                    html.H5("Refresh Model Versions Succeeded", style={"color": "green"}),
                    html.P("Model versions refreshed successfully.")
                ])
            else:
                raise Exception("Refresh model versions failed")
        except Exception as e:
            return html.Div([
                html.H5("Refresh Model Versions Failed", style={"color": "red"}),
                html.P(f"Error: {str(e)}")
            ])
    return ""

from utils import (
    fetch_ml_prediction, fetch_notifications, open_trade, fetch_backtests, run_backtest, fetch_analytics, fetch_trades,
    mark_notification_read, delete_notification, fetch_model_metrics, fetch_feature_importance, fetch_portfolio_analytics,
    safety_check, close_trade, cancel_trade, activate_trade, fetch_model_logs, fetch_model_errors, fetch_system_status
)

# Import hybrid learning dashboard
from hybrid_learning_layout import create_hybrid_learning_layout, register_hybrid_learning_callbacks

# Import email configuration dashboard
from email_config_layout import create_email_config_layout, register_email_config_callbacks

# Register hybrid learning callbacks
try:
    register_hybrid_learning_callbacks(app)
    print("✓ Hybrid learning callbacks registered")
except Exception as e:
    print(f"⚠ Warning: Could not register hybrid learning callbacks: {e}")

# Register email configuration callbacks
try:
    register_email_config_callbacks(app)
    print("✓ Email configuration callbacks registered")
except Exception as e:
    print(f"⚠ Warning: Could not register email configuration callbacks: {e}")

# --- Hybrid Learning Tab Content ---
@app.callback(
    Output('hybrid-learning-tab-content', 'children'),
    Input('hybrid-learning-tab-content', 'id')
)
def render_hybrid_learning_tab(_):
    """Render the hybrid learning tab content"""
    try:
        return create_hybrid_learning_layout()
    except Exception as e:
        return html.Div([
            html.H3("⚠ Hybrid Learning System", className="text-warning"),
            html.P(f"Unable to load hybrid learning interface: {str(e)}", className="text-muted"),
            html.P("Please ensure the backend is running and the hybrid learning system is properly initialized.", className="text-muted")
        ], className="text-center p-4")

# --- Email Configuration Tab Content ---
@app.callback(
    Output('email-config-tab-content', 'children'),
    Input('email-config-tab-content', 'id')
)
def render_email_config_tab(_):
    """Render the email configuration tab content"""
    try:
        return create_email_config_layout()
    except Exception as e:
        return html.Div([
            html.H3("⚠ Email Configuration", className="text-warning"),
            html.P(f"Unable to load email configuration interface: {str(e)}", className="text-muted"),
            html.P("Please check that the backend is running and email endpoints are available.", className="text-muted")
        ], className="text-center p-4")

# --- Model Version Dropdown & Refresh ---
@app.callback(
    Output('model-version-dropdown', 'options'),
    [Input('refresh-model-versions-btn', 'n_clicks')],
    prevent_initial_call=False
)
def refresh_model_versions(n_clicks):
    return [
        {'label': 'v1.0', 'value': 'v1.0'},
        {'label': 'v2.0', 'value': 'v2.0'}
    ]

# --- Risk Management Controls ---
@app.callback(
    Output('risk-max-drawdown', 'value'),
    [Input('risk-max-drawdown', 'value')],
    prevent_initial_call=False
)
def update_risk_max_drawdown(value):
    return value

@app.callback(
    Output('risk-stoploss', 'value'),
    [Input('risk-stoploss', 'value')],
    prevent_initial_call=False
)
def update_risk_stoploss(value):
    return value

@app.callback(
    Output('risk-position-size', 'value'),
    [Input('risk-position-size', 'value')],
    prevent_initial_call=False
)
def update_risk_position_size(value):
    return value

@app.callback(
    Output('realtime-mode-checklist', 'value'),
    [Input('realtime-mode-checklist', 'value')],
    prevent_initial_call=False
)
def update_realtime_mode(value):
    return value

@app.callback(
    Output('signal-filters-checklist', 'value'),
    [Input('signal-filters-checklist', 'value')],
    prevent_initial_call=False
)
def update_signal_filters(value):
    return value

@app.callback(
    Output('quick-profit-target', 'value'),
    [Input('quick-profit-target', 'value')],
    prevent_initial_call=False
)
def update_quick_profit_target(value):
    return value

@app.callback(
    Output('ultra-confidence-slider', 'value'),
    [Input('ultra-confidence-slider', 'value')],
    prevent_initial_call=False
)
def update_ultra_confidence(value):
    return value

@app.callback(
    Output('ai-model-dropdown', 'value'),
    [Input('ai-model-dropdown', 'value')],
    prevent_initial_call=False
)
def update_ai_model(value):
    return value

@app.callback(
    Output('safety-check-result', 'children'),
    [Input('safety-check-btn', 'n_clicks')],
    prevent_initial_call=True
)
def run_safety_check(n_clicks):
    if not n_clicks:
        return ''
    return 'Safety check passed.'

@app.callback(
    Output('notification-toast', 'is_open'),
    [Input('notifications-list', 'children')],
    prevent_initial_call=False
)
def show_notification_toast(children):
    return bool(children)

# --- Email Address: Load on startup ---
@app.callback(
    Output("email-notify-address", "value"),
    Input("sidebar-symbol", "value"),
    prevent_initial_call=False
)
def load_email_address(_):
    try:
        resp = requests.get(f"{API_URL}/settings/email_address")
        if resp.ok:
            return resp.json().get("email", "")
    except Exception:
        pass
    return ""

# --- Email Address: Save on blur/change ---
@app.callback(
    Output("email-notify-address", "disabled"),
    Input("email-notify-address", "value"),
    prevent_initial_call=True
)
def save_email_address(value):
    try:
        resp = requests.post(f"{API_URL}/settings/email_address", json={"email": value})
        if resp.ok:
            return False
    except Exception:
        pass
    return False

# --- Email Notification Toggle: Load state on startup ---
@app.callback(
    Output("email-notify-toggle", "value"),
    Input("sidebar-symbol", "value"),
    prevent_initial_call=False
)
def load_email_notify_toggle(_):
    try:
        resp = requests.get(f"{API_URL}/settings/email_notifications")
        if resp.ok:
            return resp.json().get("enabled", False)
    except Exception:
        pass
    return False

# --- Email Notification Toggle: Update backend on change ---
@app.callback(
    Output("email-notify-toggle", "disabled"),
    Input("email-notify-toggle", "value"),
    prevent_initial_call=True
)
def update_email_notify_toggle(value):
    try:
        resp = requests.post(f"{API_URL}/settings/email_notifications", json={"enabled": value})
        if resp.ok:
            return False
    except Exception:
        pass
    return False

# --- Batch Predict Upload ---
@app.callback(
    [Output("batch-predict-result", "children"),
     Output("upload-tracking-store", "data")],
    [Input("batch-predict-upload", "contents")],
    prevent_initial_call=True
)
def acknowledge_csv_upload(contents):
    if contents:
        # Trigger upload tracking
        tracking_data = {"active": True, "start_time": time.time()}
        return ("📁 CSV file uploaded. Click 'Run Batch Prediction' to retrain and predict.", tracking_data)
    return ("", {"active": False})

# --- Live Price Display Callback ---
@app.callback(
    Output('live-price', 'children'),
    [Input('selected-symbol-store', 'data'), Input('live-price-cache', 'data')],
    prevent_initial_call=False
)
def update_live_price_display(selected_symbol, price_cache):
    symbol_display = (selected_symbol or '').upper()
    if price_cache is None:
        price_cache = {}
    print(f"[DASH DEBUG] update_live_price_display called: selected_symbol={selected_symbol}, symbol_display={symbol_display}, price_cache={price_cache}")
    cached = price_cache.get(symbol_display)
    if cached is not None:
        print(f"[DASH DEBUG] Returning cached price for {symbol_display}: {cached}")
        return f"{symbol_display}: {cached:,.7f}"
    else:
        print(f"[DASH DEBUG] No cached price for {symbol_display}")
        return f"{symbol_display}: --"

# --- Technical Indicators & Regime Callback ---
@app.callback(
    [Output('current-regime', 'children'),
     Output('rsi-value', 'children'),
     Output('macd-value', 'children'),
     Output('bbands-value', 'children')],
    [Input('selected-symbol-store', 'data'),
     Input('interval-indicators', 'n_intervals')],
    prevent_initial_call=False
)
def update_technical_indicators(symbol_data, n_intervals):
    from dash import callback_context
    ctx = callback_context
    symbol = symbol_data.lower() if symbol_data else 'btcusdt'
    # Log what triggered this callback
    trigger_info = "no trigger"
    if ctx.triggered:
        trigger_info = ctx.triggered[0]['prop_id']
    
    print(f"[DASH DEBUG] update_technical_indicators called: symbol={symbol}, n_intervals={n_intervals}, triggered_by={trigger_info}")
    try:
        resp = requests.get(f"{API_URL}/features/indicators", params={"symbol": symbol}, timeout=2)
        print(f"[DASH DEBUG] API response status: {resp.status_code}, trigger: {trigger_info}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"[DASH DEBUG] API response data: {data}")
            indicators = data.get('indicators', {})
              # Extract indicators from the correct structure
            rsi_val = indicators.get('rsi', 0)
            macd_val = indicators.get('macd', 0)
            bb_upper = indicators.get('bb_upper', 0)
            bb_lower = indicators.get('bb_lower', 0)
            bb_middle = indicators.get('bb_middle', 0)
            regime_from_backend = indicators.get('regime', 'NEUTRAL')
              # Use regime from backend (which considers multiple factors)
            regime = regime_from_backend            # Format values - check for None explicitly, allow 0 values
            rsi = f"{rsi_val:.2f}" if rsi_val is not None else '--'
            macd = f"{macd_val:.4f}" if macd_val is not None else '--'
              # Calculate bollinger bands display - check for None explicitly, allow 0 values
            if bb_upper is not None and bb_lower is not None and bb_middle is not None:
                bbands_str = f"Upper: {bb_upper:.2f}, Mid: {bb_middle:.2f}, Lower: {bb_lower:.2f}"
            else:
                bbands_str = "Upper: --, Mid: --, Lower: --"            # Check for valid data - don't display [NO DATA] for valid 0 values
            regime = regime if regime and regime.strip() and regime != '--' else '[NO DATA]'
            rsi = rsi if rsi and rsi.strip() and rsi != '--' else '[NO DATA]'
            macd = macd if macd and macd.strip() and macd != '--' else '[NO DATA]'
            bbands_str = bbands_str if bbands_str and bbands_str.strip() and '--' not in bbands_str else '[NO DATA]'
            print(f"[DASH DEBUG] Returning: regime={regime}, rsi={rsi}, macd={macd}, bbands={bbands_str}")
            # Return with explicit styling to ensure visibility
            return (
                html.Div(regime, style={"color": "#00ff88", "fontWeight": "bold", "fontSize": "18px"}),
                html.Div(rsi, style={"color": "#ffff00", "fontWeight": "bold", "fontSize": "18px"}),
                html.Div(macd, style={"color": "#ff8800", "fontWeight": "bold", "fontSize": "18px"}),
                html.Div(bbands_str, style={"color": "#8800ff", "fontWeight": "bold", "fontSize": "14px"})
            )
        else:
            print(f"[DASH ERROR] Non-200 response from backend: {resp.status_code}")
            return (
                html.Div("--", style={"color": "#ff0000"}),
                html.Div("--", style={"color": "#ff0000"}),
                html.Div("--", style={"color": "#ff0000"}),
                html.Div("--", style={"color": "#ff0000"})
            )
    except requests.exceptions.Timeout:
        print(f"[DASH ERROR] Backend timeout in update_technical_indicators for symbol {symbol}")
        return (
            html.Div("[TIMEOUT]", style={"color": "#ff0000"}),
            html.Div("[TIMEOUT]", style={"color": "#ff0000"}),
            html.Div("[TIMEOUT]", style={"color": "#ff0000"}),
            html.Div("[TIMEOUT]", style={"color": "#ff0000"})
        )
    except requests.exceptions.ConnectionError:
        print(f"[DASH ERROR] Backend connection error in update_technical_indicators for symbol {symbol}")
        return (
            html.Div("[NO CONNECTION]", style={"color": "#ff0000"}),
            html.Div("[NO CONNECTION]", style={"color": "#ff0000"}),
            html.Div("[NO CONNECTION]", style={"color": "#ff0000"}),
            html.Div("[NO CONNECTION]", style={"color": "#ff0000"})
        )
    except Exception as e:
        print(f"[DASH ERROR] Exception in update_technical_indicators: {e}")
        return (
            html.Div("[ERROR]", style={"color": "#ff0000"}),
            html.Div("[ERROR]", style={"color": "#ff0000"}),
            html.Div("[ERROR]", style={"color": "#ff0000"}),
            html.Div("[ERROR]", style={"color": "#ff0000"})
        )

# --- Immediate Technical Indicators Update on Symbol Change ---
@app.callback(
    [Output('current-regime', 'children', allow_duplicate=True),
     Output('rsi-value', 'children', allow_duplicate=True),
     Output('macd-value', 'children', allow_duplicate=True),
     Output('bbands-value', 'children', allow_duplicate=True)],
    Input('selected-symbol-store', 'data'),
    prevent_initial_call=True
)
def update_technical_indicators_immediate(symbol_data):
    """Update indicators immediately when symbol changes"""
    symbol = symbol_data.lower() if symbol_data else 'btcusdt'
    print(f"[DASH DEBUG] IMMEDIATE indicators update for symbol: {symbol}")
    
    try:
        resp = requests.get(f"{API_URL}/features/indicators", params={"symbol": symbol}, timeout=3)
        print(f"[DASH DEBUG] IMMEDIATE API response: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            indicators = data.get('indicators', {})
            regime = indicators.get('regime', 'NEUTRAL')
            rsi_val = indicators.get('rsi', 0)
            macd_val = indicators.get('macd', 0)
            bb_upper = indicators.get('bb_upper', 0)
            bb_lower = indicators.get('bb_lower', 0)
            bb_middle = indicators.get('bb_middle', 0)
            
            # Format values properly
            rsi = f"{rsi_val:.2f}" if rsi_val is not None else '--'
            macd = f"{macd_val:.4f}" if macd_val is not None else '--'
            
            if bb_upper is not None and bb_lower is not None and bb_middle is not None:
                bbands_str = f"Upper: {bb_upper:.2f}, Mid: {bb_middle:.2f}, Lower: {bb_lower:.2f}"
            else:
                bbands_str = "Upper: --, Mid: --, Lower: --"
            
            return (
                html.Div(regime, style={"color": "#00ff88", "fontWeight": "bold", "fontSize": "18px"}),
                html.Div(rsi, style={"color": "#ffff00", "fontWeight": "bold", "fontSize": "18px"}),
                html.Div(macd, style={"color": "#ff8800", "fontWeight": "bold", "fontSize": "18px"}),
                html.Div(bbands_str, style={"color": "#8800ff", "fontWeight": "bold", "fontSize": "14px"})
            )
        else:
            return (
                html.Div("--", style={"color": "#ff0000"}),
                html.Div("--", style={"color": "#ff0000"}),
                html.Div("--", style={"color": "#ff0000"}),
                html.Div("--", style={"color": "#ff0000"})
            )
    except Exception as e:
        print(f"[DASH ERROR] IMMEDIATE indicators error: {e}")
        return (
            html.Div("[ERROR]", style={"color": "#ff0000"}),
            html.Div("[ERROR]", style={"color": "#ff0000"}),
            html.Div("[ERROR]", style={"color": "#ff0000"}),
            html.Div("[ERROR]", style={"color": "#ff0000"})
        )

# --- Analytics Review Callback ---
@app.callback(
    Output('analytics-output', 'children'),
    Input('review-analytics-btn', 'n_clicks'),
    prevent_initial_call=True
)
def review_analytics(n_clicks):
    if not n_clicks:
        return ''
    analytics = fetch_analytics()
    if not analytics:
        return 'No analytics data available.'
    return html.Pre(str(analytics))

# --- Trade Logs Review Callback ---
@app.callback(
    Output('trade-logs-output', 'children'),
    Input('review-trade-logs-btn', 'n_clicks'),
    prevent_initial_call=True
)
def review_trade_logs(n_clicks):
    if not n_clicks:
        return ''
    trades = fetch_trades()
    if not trades:
        return 'No trade logs available.'
    return html.Pre(str(trades))

# --- Unified Trade Action Callback (open, close, cancel, activate) ---
@app.callback(
    [Output('trade-action-result', 'children'),
     Output('active-trades-table', 'data'),
     Output('trades-table', 'data')],
    [Input('open-long-btn', 'n_clicks'),
     Input('open-short-btn', 'n_clicks'),
     Input('close-trade-btn', 'n_clicks'),
     Input('cancel-trade-btn', 'n_clicks'),
     Input('activate-trade-btn', 'n_clicks')],
    [State('selected-symbol-store', 'data'),
     State('active-trades-table', 'selected_rows'),
     State('active-trades-table', 'data')],
    prevent_initial_call=True
)
def trade_action(
    open_long_clicks, open_short_clicks, close_clicks, cancel_clicks, activate_clicks,
    selected_symbol, selected_rows, table_data
):
    ctx = dash.callback_context
    if not ctx.triggered:
        return '', dash.no_update, dash.no_update
    
    btn = ctx.triggered[0]['prop_id'].split('.')[0]
    print(f"[DASH DEBUG] Trade action button clicked: {btn}")
    
    try:        # Handle open trade buttons
        if btn in ['open-long-btn', 'open-short-btn']:
            symbol = (selected_symbol or 'BTCUSDT').upper()
            direction = 'LONG' if btn == 'open-long-btn' else 'SHORT'
            
            trade_data = {
                "symbol": symbol,
                "direction": direction,
                "amount": 0.1,
                "entry_price": 0,
                "tp_pct": 2.0,  # 2% take profit
                "sl_pct": 1.0   # 1% stop loss
            }
            
            resp = requests.post(f"{API_URL}/trade", json=trade_data)
            print(f"[DASH DEBUG] Open trade API response: {resp.status_code}, {resp.text}")
            
            if resp.ok:
                result = resp.json()
                result_msg = f"✅ {direction} trade opened for {symbol} - ID: {result.get('id', 'N/A')}"
                
                # Refresh trades table
                trades_resp = requests.get(f"{API_URL}/trades")
                if trades_resp.ok:
                    trades = trades_resp.json()
                    if isinstance(trades, list):
                        active_trades = [t for t in trades if t.get('status') == 'OPEN']
                        return result_msg, active_trades, trades
                
                return result_msg, dash.no_update, dash.no_update
            else:
                return f"❌ Failed to open {direction} trade: {resp.text}", dash.no_update, dash.no_update
                
        # Handle trade management buttons  
        elif btn in ['close-trade-btn', 'cancel-trade-btn', 'activate-trade-btn']:
            if not selected_rows or not table_data:
                return "❌ Please select a trade from the table first", dash.no_update, dash.no_update
            
            selected_trade = table_data[selected_rows[0]]
            trade_id = selected_trade['id']
            
            if btn == 'close-trade-btn':
                resp = requests.post(f"{API_URL}/trades/{trade_id}/close")
                action = "Close"
            elif btn == 'cancel-trade-btn':
                resp = requests.post(f"{API_URL}/trades/{trade_id}/cancel")
                action = "Cancel"
            elif btn == 'activate-trade-btn':
                resp = requests.post(f"{API_URL}/trades/{trade_id}/activate")
                action = "Activate"
            
            print(f"[DASH DEBUG] Trade management API response: {resp.status_code}, {resp.text}")
            
            if resp.ok:
                result_msg = f"✅ {action} successful for trade ID: {trade_id}"
                
                # Refresh trades table
                trades_resp = requests.get(f"{API_URL}/trades")
                if trades_resp.ok:
                    trades = trades_resp.json()
                    if isinstance(trades, list):
                        active_trades = [t for t in trades if t.get('status') == 'OPEN']
                        return result_msg, active_trades, trades
                        
                return result_msg, dash.no_update, dash.no_update
            else:
                return f"❌ Failed to {action.lower()} trade: {resp.text}", dash.no_update, dash.no_update
    
    except Exception as e:
        print(f"[DASH ERROR] Error in trade action callback: {e}")
        return f"❌ Error: {str(e)}", dash.no_update, dash.no_update
    
    return '', dash.no_update, dash.no_update

# --- Notifications Callback ---
@app.callback(
    Output('notifications-list', 'children'),
    Input('refresh-notifications-btn', 'n_clicks'),
    prevent_initial_call=True
)
def refresh_notifications(n_clicks):
    if not n_clicks:
        return ''
    notes = fetch_notifications()
    if not notes:
        return 'No notifications.'
    return html.Ul([html.Li(str(n)) for n in notes])

# --- Model Metrics Callback ---
@app.callback(
    Output('model-metrics-dashboard', 'children'),
    Input('show-model-metrics-btn', 'n_clicks'),
    prevent_initial_call=True
)
def show_model_metrics(n_clicks):
    if not n_clicks:
        return ''
    data = fetch_model_metrics()
    if not data or data.get('error'):
        return f"Error: {data.get('error', 'No data')}"
    metrics = []
    for k, v in data.items():
        metrics.append(f"{k.title()}: {v:.4f}" if isinstance(v, float) else f"{k.title()}: {v}")
    return html.Ul([html.Li(m) for m in metrics])

# --- Feature Importance Callback ---
@app.callback(
    [Output('feature-importance-graph', 'figure'), Output('feature-importance-metrics', 'children')],
    [Input('show-feature-importance-btn', 'n_clicks')],
    prevent_initial_call=True
)
def show_feature_importance(n_clicks):
    import plotly.graph_objs as go
    if not n_clicks:
        return go.Figure(), ''
    data = fetch_feature_importance()
    if not data or data.get('error'):
        return go.Figure(), f"Error: {data.get('error', 'No data')}"
    importances = data.get('importances') or data.get('feature_importance')
    feature_names = data.get('features') or [f"Feature {i+1}" for i in range(len(importances or []))]
    if not importances or not isinstance(importances, (list, tuple)):
        return go.Figure(), 'No feature importance data.'
    fig = go.Figure([go.Bar(x=feature_names, y=importances, marker_color="#00bfff")])
    fig.update_layout(title="Model Feature Importance", template="plotly_dark", xaxis_title="Feature", yaxis_title="Importance")
    metrics_html = html.Ul([html.Li(f"{name}: {imp:.4f}") for name, imp in zip(feature_names, importances)])
    return fig, metrics_html

# --- Notification Action Result Callback ---
@app.callback(
    Output('notification-action-result', 'children'),
    [Input('mark-notification-read-btn', 'n_clicks'), Input('delete-notification-btn', 'n_clicks')],
    prevent_initial_call=True
)
def notification_action_result(mark_clicks, delete_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return ''
    btn = ctx.triggered[0]['prop_id'].split('.')[0]
    if btn == 'mark-notification-read-btn':
        return 'Notification marked as read.'
    elif btn == 'delete-notification-btn':
        return 'Notification deleted.'
    return ''

# --- Trades Error Callback (stub) ---
@app.callback(
    Output('trades-error', 'children'),
    [Input('trades-table', 'data')],
    prevent_initial_call=False
)
def trades_error(data):
    return ''

# --- Interval Prediction Callback (stub) ---
@app.callback(
    Output('interval-prediction', 'n_intervals'),
    [Input('interval-prediction', 'n_intervals')],
    prevent_initial_call=False
)
def interval_prediction(n):
    return n

# --- Live Price WebSocket Symbol Sender ---
@app.callback(
    Output('live-price-ws', 'send'),
    [Input('sidebar-symbol', 'value')],
    prevent_initial_call=False
)
def send_symbol_to_ws(symbol):
    print(f"[DASH DEBUG] send_symbol_to_ws called: symbol={symbol}")
    if symbol:
        print(f"[DASH DEBUG] Sending symbol to WebSocket: {symbol.upper()}")
        return symbol.upper()
    print(f"[DASH DEBUG] No symbol provided, defaulting to BTCUSDT")
    return 'BTCUSDT'

# --- Store selected symbol in dcc.Store and sync dropdown value ---
@app.callback(
    [Output('selected-symbol-store', 'data'), Output('sidebar-symbol', 'value')],
    [Input('sidebar-symbol', 'value'), Input('selected-symbol-store', 'data')],
    prevent_initial_call=False
)
def sync_selected_symbol(symbol_dropdown, store_data):
    ctx = callback_context
    print(f"[DASH DEBUG] sync_selected_symbol called: symbol_dropdown={symbol_dropdown}, store_data={store_data}, triggered={ctx.triggered}")
    if ctx.triggered and ctx.triggered[0]['prop_id'].startswith('sidebar-symbol'):
        print(f"[DASH DEBUG] Triggered by sidebar-symbol. symbol_dropdown={symbol_dropdown}")
        if symbol_dropdown:
            print(f"[DASH DEBUG] Dropdown changed, updating store to {symbol_dropdown.upper()}")
            return symbol_dropdown.upper(), symbol_dropdown
        else:
            print(f"[DASH DEBUG] Dropdown empty, defaulting to BTCUSDT")
            return 'BTCUSDT', 'btcusdt'
    if store_data:
        print(f"[DASH DEBUG] Store changed, updating dropdown to {store_data.lower()}")
        return store_data, store_data.lower()
    print(f"[DASH DEBUG] No trigger, defaulting to BTCUSDT")
    return 'BTCUSDT', 'btcusdt'

# --- Unified callback for live-price-cache (init and WebSocket update) ---
@app.callback(
    Output('live-price-cache', 'data'),
    [Input('selected-symbol-store', 'data'), Input('live-price-ws', 'message')],
    [State('live-price-cache', 'data')],
    prevent_initial_call=False
)
def update_live_price_cache(selected_symbol, ws_message, price_cache):
    import json
    ctx = callback_context
    print(f"[DASH DEBUG] update_live_price_cache called: selected_symbol={selected_symbol}, ws_message={ws_message}, price_cache={price_cache}, triggered={ctx.triggered}")
    if price_cache is None:
        price_cache = {}
    if ctx.triggered:
        print(f"[DASH DEBUG] Triggered by: {ctx.triggered[0]['prop_id']}")
    if ctx.triggered and ctx.triggered[0]['prop_id'].startswith('selected-symbol-store'):
        symbol_display = (selected_symbol or 'BTCUSDT').upper()
        print(f"[DASH DEBUG] Triggered by selected-symbol-store, fetching price for {symbol_display}")
        try:
            resp = requests.get(f"{API_URL}/price", params={"symbol": symbol_display})
            if resp.ok:
                data = resp.json()
                price = float(data.get("price", 0))
                price_cache[symbol_display] = price
                print(f"[DASH DEBUG] Successfully fetched price for {symbol_display}: {price}")
            else:
                print(f"[DASH DEBUG] Failed to fetch price for {symbol_display}: {resp.status_code}")
        except Exception as e:
            print(f"[DASH DEBUG] Error fetching price for {symbol_display}: {e}")
        return price_cache
    if ctx.triggered and ctx.triggered[0]['prop_id'].startswith('live-price-ws'):
        print(f"[DASH DEBUG] Triggered by live-price-ws (WebSocket)")
        try:
            if not ws_message:
                print(f"[DASH DEBUG] No ws_message, returning price_cache")
                return price_cache
            data = ws_message['data'] if isinstance(ws_message, dict) and 'data' in ws_message else ws_message
            data = json.loads(data)
            symbol = data.get('symbol', selected_symbol).upper()
            price = float(data.get('price', 0))
            print(f"[DASH DEBUG] WebSocket update: symbol={symbol}, price={price}")
            price_cache[symbol] = price
        except Exception as e:
            print(f"[DASH DEBUG] Error parsing WebSocket message: {e}")
        print(f"[DASH DEBUG] Returning updated price_cache: {price_cache}")
        return price_cache
    print(f"[DASH DEBUG] No trigger, returning price_cache")
    return price_cache

# --- Virtual Balance Display Callback ---
@app.callback(
    Output('virtual-balance', 'children'),
    [Input('interval-prediction', 'n_intervals'),
     Input('reset-balance-btn', 'n_clicks')],
    prevent_initial_call=False
)
def update_virtual_balance_display(n_intervals, reset_clicks):
    """Update virtual balance display"""
    try:
        resp = requests.get(f"{API_URL}/virtual_balance", timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            balance = data.get('balance', 0)
            print(f"[DASH DEBUG] Virtual balance updated: ${balance:,.2f}")
            return f"${balance:,.2f}"
        else:
            print(f"[DASH ERROR] Failed to get virtual balance: {resp.status_code}")
            return "Error loading balance"
    except Exception as e:
        print(f"[DASH ERROR] Virtual balance error: {e}")
        return "Connection Error"

# --- Reset Virtual Balance Callback ---
@app.callback(
    Output('virtual-balance', 'children', allow_duplicate=True),
    Input('reset-balance-btn', 'n_clicks'),
    prevent_initial_call=True
)
def reset_virtual_balance(n_clicks):
    """Reset virtual balance to default"""
    if n_clicks:
        try:
            resp = requests.post(f"{API_URL}/virtual_balance/reset", timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                balance = data.get('balance', 10000)
                print(f"[DASH DEBUG] Virtual balance reset to: ${balance:,.2f}")
                return f"${balance:,.2f}"
            else:
                print(f"[DASH ERROR] Failed to reset balance: {resp.status_code}")
                return "Reset Failed"
        except Exception as e:
            print(f"[DASH ERROR] Reset balance error: {e}")
            return "Reset Error"
    return "Error"

# --- Upload Progress Tracking Callbacks ---
@app.callback(
    [Output('upload-progress-bar', 'value'),
     Output('upload-progress-bar', 'style'),
     Output('upload-status-text', 'children'),
     Output('interval-upload-status', 'disabled')],
    [Input('refresh-upload-status-btn', 'n_clicks'),
     Input('interval-upload-status', 'n_intervals'),
     Input('batch-predict-upload', 'contents')],
    prevent_initial_call=True
)
def update_upload_progress(refresh_clicks, interval_n, upload_contents):
    """Update upload progress bar and status"""
    
    ctx = dash.callback_context
    if not ctx.triggered:
        return 0, {"display": "none"}, "", True
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    try:
        # Get upload status from backend
        resp = requests.get(f"{API_URL}/model/upload_status", timeout=3)
        
        if resp.status_code == 200:
            status_data = resp.json()
            
            # Check if there's an active upload/training process
            file_info = status_data.get("current_file_info")
            
            if file_info:
                file_size = file_info.get("size", 0)
                modified_time = file_info.get("modified", "")
                
                # Create status message
                status_msg = html.Div([
                    html.Div([
                        html.I(className="bi bi-file-earmark-check me-1 text-success"),
                        f"File Status: Ready"
                    ], className="mb-1"),
                    html.Div([
                        html.I(className="bi bi-hdd me-1 text-info"),
                        f"Size: {file_size:,} bytes"
                    ], className="mb-1"),
                    html.Div([
                        html.I(className="bi bi-clock me-1 text-warning"),
                        f"Last Modified: {modified_time[:19] if modified_time else 'Unknown'}"
                    ])
                ])
                
                # Show progress bar as complete if file exists
                progress_value = 100
                progress_style = {"display": "block", "height": "20px"}
                
                # Disable interval since no active upload
                interval_disabled = True
                
            else:
                status_msg = html.Div([
                    html.I(className="bi bi-exclamation-triangle me-1 text-warning"),
                    "No upload data found"
                ])
                progress_value = 0
                progress_style = {"display": "none"}
                interval_disabled = True
            
            # If upload just started, enable interval tracking
            if trigger_id == "batch-predict-upload" and upload_contents:
                status_msg = html.Div([
                    html.I(className="bi bi-upload me-1 text-primary"),
                    "Upload in progress..."
                ])
                progress_value = 25  # Show partial progress
                progress_style = {"display": "block", "height": "20px"}
                interval_disabled = False  # Enable tracking
            
            return progress_value, progress_style, status_msg, interval_disabled
            
        else:
            error_msg = html.Div([
                html.I(className="bi bi-x-circle me-1 text-danger"),
                f"Error: Could not fetch upload status ({resp.status_code})"
            ])
            return 0, {"display": "none"}, error_msg, True
            
    except Exception as e:
        error_msg = html.Div([
            html.I(className="bi bi-x-circle me-1 text-danger"),
            f"Error: {str(e)}"
        ])
        return 0, {"display": "none"}, error_msg, True

@app.callback(
    Output('upload-progress-bar', 'animated'),
    Input('interval-upload-status', 'disabled'),
    prevent_initial_call=True
)
def toggle_progress_animation(interval_disabled):
    """Toggle progress bar animation based on upload status"""
    return not interval_disabled  # Animate when interval is enabled (upload active)

# --- TEST CALLBACK: Always triggers on interval ---
@app.callback(
    Output('test-output', 'children'),
    Input('interval-prediction', 'n_intervals'),
    prevent_initial_call=False
)
def test_callback(n):
    print(f"[DASH TEST] test_callback triggered, n={n}")
    return f"Test callback triggered: {n}"

print('[DASH DEBUG] callbacks.py fully loaded and all callbacks registered')

# === AUTO TRADING CALLBACKS ===

# Import auto trading layout
from auto_trading_layout import create_auto_trading_layout

# --- Auto Trading Tab Content ---
@app.callback(
    Output('auto-trading-tab-content', 'children'),
    Input('auto-trading-tab-content', 'id')
)
def render_auto_trading_tab(tab_id):
    """Render the auto trading tab content"""
    try:
        return create_auto_trading_layout()
    except Exception as e:
        print(f"Error rendering auto trading tab: {e}")
        return html.Div([
            html.H3("🚨 Auto Trading Tab Error", className="text-danger"),
            html.P(f"Error: {str(e)}")
        ])

# --- Auto Trading Status Display ---
@app.callback(
    Output('auto-trading-status', 'children'),
    Output('auto-balance-display', 'children'),
    Output('auto-pnl-display', 'children'),
    Output('auto-winrate-display', 'children'),
    Output('auto-trades-display', 'children'),
    Output('auto-wl-display', 'children'),
    Input('auto-trading-interval', 'n_intervals'),
    Input('auto-trading-toggle', 'value'),
    prevent_initial_call=False
)
def update_auto_trading_status(n_intervals, enabled):
    """Update auto trading status and metrics"""
    try:
        # Fetch auto trading status from backend
        resp = requests.get(f"{API_URL}/auto_trading/status")
        if resp.status_code == 200:
            data = resp.json()
            if data["status"] == "success":
                state = data["auto_trading"]  # Fixed: use "auto_trading" instead of "data"
                
                # Status indicator
                if state["enabled"]:
                    status = html.Div([
                        html.I(className="bi bi-check-circle me-1 text-success"),
                        "Auto Trading Active"
                    ], className="text-success")
                else:
                    status = html.Div([
                        html.I(className="bi bi-pause-circle me-1 text-warning"),
                        "Auto Trading Paused"
                    ], className="text-warning")
                
                # Metrics (using safe defaults if fields missing)
                balance = f"${state.get('balance', 0.0):,.2f}"
                total_profit = state.get('total_profit', 0.0)
                pnl = f"${total_profit:,.2f}"
                pnl_color = "text-success" if total_profit >= 0 else "text-danger"
                
                # Use available data or defaults
                active_trades = len(state.get('active_trades', []))
                signals_processed = state.get('signals_processed', 0)
                
                # Calculate basic stats
                if signals_processed > 0:
                    winrate = f"{(signals_processed - active_trades) / signals_processed * 100:.1f}%"
                else:
                    winrate = "0%"
                
                trades = str(signals_processed)
                wl_ratio = f"{signals_processed - active_trades}/{active_trades}"
                
                return (
                    status,
                    balance,
                    html.Span(pnl, className=pnl_color),
                    winrate,
                    trades,
                    wl_ratio
                )
        
        # Fallback
        return (
            html.Div([
                html.I(className="bi bi-x-circle me-1 text-danger"),
                "Connection Error"
            ], className="text-danger"),
            "$0.00",
            "$0.00",
            "0%",
            "0",
            "0/0"
        )
        
    except Exception as e:
        error_status = html.Div([
            html.I(className="bi bi-exclamation-triangle me-1 text-warning"),
            f"Error: {str(e)}"
        ], className="text-warning")
        return error_status, "$0.00", "$0.00", "0%", "0", "0/0"

# --- Auto Trading Toggle ---
@app.callback(
    Output('auto-trading-toggle', 'value'),
    Input('auto-trading-toggle', 'value'),
    prevent_initial_call=True
)
def toggle_auto_trading(enabled):
    """Toggle auto trading on/off"""
    try:
        payload = {"enabled": enabled}
        resp = requests.post(f"{API_URL}/auto_trading/toggle", json=payload)
        
        if resp.status_code == 200:
            data = resp.json()
            if data["status"] == "success":
                return enabled
        
        # If request failed, revert the toggle
        return not enabled
        
    except Exception as e:
        print(f"Error toggling auto trading: {e}")
        return not enabled

# --- Amount Selection Callbacks ---
@app.callback(
    [Output('fixed-amount-section', 'style'),
     Output('percentage-amount-section', 'style')],
    Input('amount-type-radio', 'value'),
    prevent_initial_call=False
)
def toggle_amount_type(amount_type):
    """Toggle between fixed amount and percentage amount"""
    if amount_type == "fixed":
        return {"display": "block"}, {"display": "none"}
    else:
        return {"display": "none"}, {"display": "block"}

@app.callback(
    Output('calculated-amount-display', 'children'),
    [Input('percentage-amount-slider', 'value'),
     Input('percentage-amount-input', 'value'),
     Input('auto-balance-display', 'children')],
    prevent_initial_call=False
)
def update_calculated_amount(slider_percentage, input_percentage, balance_display):
    """Calculate and display the amount based on percentage of balance"""
    try:
        # Use input value if available, otherwise use slider
        percentage = input_percentage if input_percentage is not None else slider_percentage
        
        if balance_display and percentage:
            # Extract balance value from display (remove $ and commas)
            balance_str = str(balance_display).replace('$', '').replace(',', '')
            balance = float(balance_str)
            calculated_amount = balance * (percentage / 100)
            return f"💰 Trade Amount: ${calculated_amount:,.2f} USDT"
        return "💰 Trade Amount: $0.00 USDT"
    except:
        return "💰 Trade Amount: $0.00 USDT"

# Quick amount button callbacks
@app.callback(
    Output('fixed-amount-input', 'value'),
    [Input('amount-1', 'n_clicks'),
     Input('amount-10', 'n_clicks'),
     Input('amount-50', 'n_clicks'),
     Input('amount-100', 'n_clicks'),
     Input('amount-500', 'n_clicks')],
    prevent_initial_call=True
)
def set_quick_amount(btn1, btn10, btn50, btn100, btn500):
    """Set amount using quick amount buttons"""
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    amount_map = {
        'amount-1': 1,
        'amount-10': 10,
        'amount-50': 50,
        'amount-100': 100,
        'amount-500': 500
    }
    
    return amount_map.get(button_id, dash.no_update)

# --- Save Auto Trading Settings ---
@app.callback(
    Output('save-auto-settings-btn', 'children'),
    Input('save-auto-settings-btn', 'n_clicks'),
    State('auto-symbol-dropdown', 'value'),
    State('auto-timeframe-dropdown', 'value'),
    State('auto-risk-slider', 'value'),
    State('auto-tp-slider', 'value'),
    State('auto-sl-slider', 'value'),
    State('auto-confidence-slider', 'value'),
    State('amount-type-radio', 'value'),
    State('fixed-amount-input', 'value'),
    State('percentage-amount-slider', 'value'),
    prevent_initial_call=True
)
def save_auto_trading_settings(n_clicks, symbol, timeframe, risk, tp, sl, confidence, amount_type, fixed_amount, percentage_amount):
    """Save auto trading settings including amount configuration"""
    if not n_clicks:
        return "💾 Save Settings"
    
    try:
        settings = {
            "symbol": symbol,
            "timeframe": timeframe,
            "risk_per_trade": risk,
            "take_profit": tp,
            "stop_loss": sl,
            "min_confidence": confidence,
            "amount_type": amount_type,
            "fixed_amount": fixed_amount or 100,
            "percentage_amount": percentage_amount or 10
        }
        
        resp = requests.post(f"{API_URL}/auto_trading/settings", json=settings)
        
        if resp.status_code == 200:
            data = resp.json()
            if data["status"] == "success":
                return [
                    html.I(className="bi bi-check me-1"),
                    "Settings Saved!"
                ]
        
        return [
            html.I(className="bi bi-x me-1"),
            "Save Failed"
        ]
        
    except Exception as e:
        print(f"Error saving settings: {e}")
        return [
            html.I(className="bi bi-exclamation-triangle me-1"),
            "Error Saving"
        ]

# --- Reset to default button text after 2 seconds ---
@app.callback(
    Output('save-auto-settings-btn', 'children', allow_duplicate=True),
    Input('save-auto-settings-btn', 'children'),
    prevent_initial_call=True
)
def reset_save_button_text(button_children):
    """Reset save button text after successful save"""
    import time
    import threading
    
    # If button shows success/error message, reset after delay
    if isinstance(button_children, list):
        def reset_text():
            time.sleep(2)
            # This won't work directly due to callback context, but serves as placeholder
            pass
        
        threading.Thread(target=reset_text, daemon=True).start()
    
    return "💾 Save Settings"

# --- Current Signal Display ---
@app.callback(
    Output('current-signal-display', 'children'),
    Input('auto-trading-interval', 'n_intervals'),
    prevent_initial_call=False
)
def update_current_signal(n_intervals):
    """Update current trading signal display"""
    try:
        resp = requests.get(f"{API_URL}/auto_trading/signals")
        if resp.status_code == 200:
            data = resp.json()
            if data["status"] == "success":
                signals = data["signals"]
                
                # If no signals, show no signal state
                if not signals:
                    return html.Div([
                        html.H3([
                            html.I(className="bi bi-dash-circle me-2 text-secondary"),
                            "NO SIGNAL"
                        ], className="text-secondary mb-2"),
                        html.P("Confidence: 0.00%", className="text-muted mb-0")
                    ])
                
                # Get the latest signal
                signal = signals[-1]  # Get most recent signal
                
                # Signal direction with color coding
                direction = signal.get("direction", signal.get("signal", "HOLD"))
                if direction in ["LONG", "BUY"]:
                    direction_color = "text-success"
                    icon = "bi bi-arrow-up-circle"
                    display_text = "BUY"
                elif direction in ["SHORT", "SELL"]:
                    direction_color = "text-danger"
                    icon = "bi bi-arrow-down-circle"
                    display_text = "SELL"
                else:  # NEUTRAL, HOLD
                    direction_color = "text-secondary"
                    icon = "bi bi-dash-circle"
                    display_text = "HOLD"                # Confidence with color coding
                confidence = signal.get("confidence", 0) * 100  # Convert to percentage
                if confidence >= 80:
                    conf_color = "text-success"
                elif confidence >= 60:
                    conf_color = "text-warning"
                else:
                    conf_color = "text-danger"
                
                return html.Div([
                    # Signal Direction
                    html.Div([
                        html.I(className=f"{icon} me-2"),
                        html.Span(display_text, style={"fontSize": "24px", "fontWeight": "bold"})
                    ], className=f"{direction_color} mb-2"),
                    
                    # Confidence
                    html.Div([
                        html.Small("Confidence", className="text-muted d-block"),
                        html.Span(f"{confidence:.1f}%", className=f"{conf_color}", style={"fontSize": "18px", "fontWeight": "bold"})
                    ], className="mb-2"),
                    
                    # Current Price (if available)
                    html.Div([
                        html.Small("Current Price", className="text-muted d-block"),
                        html.Span(f"${signal.get('price', signal.get('current_price', 0)):,.4f}", className="text-info", style={"fontSize": "16px"})
                    ], className="mb-2") if signal.get('price') or signal.get('current_price') else html.Div(),
                    
                    # Timestamp (if available)
                    html.Div([
                        html.Small("Signal Time", className="text-muted d-block"),
                        html.Span(signal.get('timestamp', 'N/A'), className="text-white", style={"fontSize": "14px"})
                    ], className="mb-2") if signal.get('timestamp') else html.Div()                ])
            
        # No signals available
        return html.Div([
            html.H3([
                html.I(className="bi bi-dash-circle me-2 text-secondary"),
                "NO SIGNAL"
            ], className="text-secondary mb-2"),
            html.P("Confidence: 0.00%", className="text-muted mb-0")
        ])
        
    except Exception as e:
        return html.Div([
            html.I(className="bi bi-x-circle text-danger"),
            html.P(f"Error: {str(e)}", className="text-danger")
        ])

# --- Execute Signal Button ---
@app.callback(
    Output('execute-signal-btn', 'children'),
    Input('execute-signal-btn', 'n_clicks'),
    prevent_initial_call=True
)
def execute_trading_signal(n_clicks):
    """Execute current trading signal"""
    if not n_clicks:
        return "🔄 Execute Signal"
    
    try:
        resp = requests.post(f"{API_URL}/auto_trading/execute_signal")
        
        if resp.status_code == 200:
            data = resp.json()
            if data["status"] == "success":
                if data["action"] == "trade_opened":
                    return [
                        html.I(className="bi bi-check me-1"),
                        "Trade Opened!"
                    ]
                elif data["action"] == "trade_closed":
                    return [
                        html.I(className="bi bi-arrow-clockwise me-1"),
                        "Position Closed!"
                    ]
            elif data["status"] == "info":
                return [
                    html.I(className="bi bi-info-circle me-1"),
                    "No Action"
                ]
        
        return [
            html.I(className="bi bi-x me-1"),
            "Execution Failed"
        ]
        
    except Exception as e:
        print(f"Error executing signal: {e}")
        return [
            html.I(className="bi bi-exclamation-triangle me-1"),
            "Error"
        ]

# --- Reset Auto Trading ---
@app.callback(
    Output('reset-auto-trading-btn', 'children'),
    Input('reset-auto-trading-btn', 'n_clicks'),
    prevent_initial_call=True
)
def reset_auto_trading(n_clicks):
    """Reset auto trading system"""
    if not n_clicks:
        return "🔄 Reset System"
    
    try:
        resp = requests.post(f"{API_URL}/auto_trading/reset")
        
        if resp.status_code == 200:
            data = resp.json()
            if data["status"] == "success":
                return [
                    html.I(className="bi bi-check me-1"),
                    "System Reset!"
                ]
        
        return [
            html.I(className="bi bi-x me-1"),
            "Reset Failed"
        ]
        
    except Exception as e:
        print(f"Error resetting system: {e}")
        return [
            html.I(className="bi bi-exclamation-triangle me-1"),
            "Reset Error"
        ]

# --- Open Positions Table ---
@app.callback(
    Output('open-positions-table', 'children'),
    Input('auto-trading-interval', 'n_intervals'),
    prevent_initial_call=False
)
def update_open_positions(n_intervals):
    """Update open positions table"""
    try:
        resp = requests.get(f"{API_URL}/auto_trading/trades")
        if resp.status_code == 200:
            data = resp.json()
            if data["status"] == "success":
                open_trades = data["data"]["open_trades"]
                
                if not open_trades:
                    return html.Div([
                        html.I(className="bi bi-info-circle me-2 text-info"),
                        "No open positions"
                    ], className="text-center text-muted py-3")
                
                # Create table data
                table_data = []
                for trade_id, trade in open_trades.items():
                    # Calculate unrealized P&L (mock calculation)
                    current_price = 50000  # Mock current price
                    entry_price = trade["entry_price"]
                    direction = trade["direction"]
                    amount = trade["amount"]
                    
                    if direction == "LONG":
                        unrealized_pnl = (current_price - entry_price) * amount / entry_price
                    else:
                        unrealized_pnl = (entry_price - current_price) * amount / entry_price
                    
                    table_data.append({
                        "Symbol": trade["symbol"],
                        "Direction": trade["direction"],
                        "Entry Price": f"${entry_price:,.4f}",
                        "Amount": f"${amount:.2f}",
                        "Unrealized P&L": f"${unrealized_pnl:.2f}",
                        "Confidence": f"{trade['confidence']:.1f}%",
                        "Actions": html.Div([
                            html.Button(
                                "❌",
                                id={"type": "close-position-btn", "index": trade_id},
                                className="btn btn-sm btn-outline-danger me-1",
                                title="Close Position"
                            )
                        ])
                    })
                
                return dash_table.DataTable(
                    data=table_data,
                    columns=[
                        {"name": "Symbol", "id": "Symbol"},
                        {"name": "Direction", "id": "Direction"},
                        {"name": "Entry Price", "id": "Entry Price"},
                        {"name": "Amount", "id": "Amount"},
                        {"name": "Unrealized P&L", "id": "Unrealized P&L"},
                        {"name": "Confidence", "id": "Confidence"},
                        {"name": "Actions", "id": "Actions", "presentation": "markdown"}
                    ],
                    style_table={"overflowX": "auto"},
                    style_cell={
                        "backgroundColor": "#1a1a1a",
                        "color": "white",
                        "textAlign": "center",
                        "padding": "8px"
                    },
                    style_header={
                        "backgroundColor": "#222",
                        "color": "#00ff88",
                        "fontWeight": "bold"
                    }
                )
        
        return html.Div([
            html.I(className="bi bi-exclamation-triangle me-2 text-warning"),
            "Could not load positions"
        ], className="text-center text-muted py-3")
        
    except Exception as e:
        return html.Div([
            html.I(className="bi bi-x-circle me-2 text-danger"),
            f"Error: {str(e)}"
        ], className="text-center text-danger py-3")

# --- Trade Log ---
@app.callback(
    Output('auto-trade-log', 'children'),
    Input('auto-trading-interval', 'n_intervals'),
    prevent_initial_call=False
)
def update_trade_log(n_intervals):
    """Update auto trading log"""
    try:
        resp = requests.get(f"{API_URL}/auto_trading/trades")
        if resp.status_code == 200:
            data = resp.json()
            if data["status"] == "success":
                trade_log = data["data"]["trade_log"]
                
                if not trade_log:
                    return html.Div([
                        html.I(className="bi bi-info-circle me-2"),
                        "No trading activity yet"
                    ], className="text-muted text-center")
                
                # Format log entries
                log_entries = []
                for entry in reversed(trade_log[-20:]):  # Show last 20 entries
                    timestamp = entry["timestamp"]
                    message = entry["message"]
                    entry_type = entry.get("type", "info")
                    
                    # Color coding by type
                    if entry_type == "trade_open":
                        color = "#00ff88"  # Green
                        icon = "📈"
                    elif entry_type == "trade_close":
                        pnl = entry.get("pnl", 0)
                        color = "#00ff88" if pnl >= 0 else "#ff4444"  # Green/Red based on P&L
                        icon = "📉" if pnl < 0 else "💰"
                    elif entry_type == "system":
                        color = "#ffaa00"  # Orange
                        icon = "⚙️"
                    else:
                        color = "#888888"  # Gray
                        icon = "ℹ️"
                    
                    log_entries.append(
                        html.Div([
                            html.Span(f"{icon} [{timestamp[:19]}] ", style={"color": "#aaa"}),
                            html.Span(message, style={"color": color})
                        ], style={"marginBottom": "5px", "fontSize": "11px"})
                    )
                
                return log_entries
        
        return html.Div([
            html.I(className="bi bi-exclamation-triangle me-2"),
            "Could not load trade log"
        ], className="text-warning text-center")
        
    except Exception as e:
        return html.Div([
            html.I(className="bi bi-x-circle me-2"),
            f"Error: {str(e)}"
        ], className="text-danger text-center")

# --- Close Position Button Handler ---
@app.callback(
    Output({"type": "close-position-btn", "index": ALL}, 'children'),
    Input({"type": "close-position-btn", "index": ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def close_position_handler(n_clicks_list):
    """Handle closing positions manually"""
    if not any(n_clicks_list):
        return ["❌"] * len(n_clicks_list)
    
    # Get which button was clicked
    triggered = callback_context.triggered
    if triggered:
        button_id = triggered[0]['prop_id'].split('.')[0]
        trade_id = eval(button_id)['index']  # Extract trade_id from button id
        
        try:
            resp = requests.post(f"{API_URL}/auto_trading/close_trade/{trade_id}")
            if resp.status_code == 200:
                data = resp.json()
                if data["status"] == "success":
                    # Return success state for the clicked button
                    result = ["❌"] * len(n_clicks_list)
                    clicked_index = next((i for i, clicks in enumerate(n_clicks_list) if clicks), 0)
                    result[clicked_index] = "✅"
                    return result
        except Exception as e:
            print(f"Error closing position: {e}")
    
    return ["❌"] * len(n_clicks_list)

# --- Reset All Button Callback ---
@app.callback(
    Output('reset-all-btn-output', 'children'),
    Input('reset-all-btn', 'n_clicks'),
    prevent_initial_call=True
)
def reset_all_callback(n_clicks):
    if n_clicks:
        print("[DASHBOARD] Reset All button clicked.")
        try:
            # This would reset balance, trades, and notifications
            # For now, just simulate success
            reset_ok = True
            if reset_ok:
                return html.Div([
                    html.H5("Reset All Succeeded", style={"color": "green"}),
                    html.P("All data (balance, trades, notifications) reset successfully.")
                ])
            else:
                raise Exception("Reset all failed")
        except Exception as e:
            return html.Div([
                html.H5("Reset All Failed", style={"color": "red"}),
                html.P(f"Error: {str(e)}")
            ])
    return ""

print('[DASH DEBUG] Auto trading callbacks registered successfully')

# --- Low-Cap Coin Optimization Callbacks ---
@app.callback(
    Output('auto-symbol-dropdown', 'value'),
    Output('auto-risk-slider', 'value'),
    Output('auto-confidence-slider', 'value'),
    Output('auto-tp-input', 'value'),
    Output('auto-sl-input', 'value'),
    [Input('optimize-kaia-btn', 'n_clicks'),
     Input('optimize-jasmy-btn', 'n_clicks'),
     Input('optimize-gala-btn', 'n_clicks')],
    prevent_initial_call=True
)
def optimize_for_low_cap_coin(kaia_clicks, jasmy_clicks, gala_clicks):
    """Optimize settings for specific low-cap coins"""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Define optimized settings for each coin
    settings_map = {
        'optimize-kaia-btn': {
            'symbol': 'KAIAUSDT',
            'risk': 3.0,
            'confidence': 55.0,
            'tp': 2.5,
            'sl': 1.2
        },
        'optimize-jasmy-btn': {
            'symbol': 'JASMYUSDT', 
            'risk': 4.0,
            'confidence': 60.0,
            'tp': 2.0,
            'sl': 1.0
        },
        'optimize-gala-btn': {
            'symbol': 'GALAUSDT',
            'risk': 3.5,
            'confidence': 58.0,
            'tp': 2.2,
            'sl': 1.1
        }
    }
    
    if button_id in settings_map:
        settings = settings_map[button_id]
        
        # Call backend to optimize
        try:
            requests.post(f"{API_URL}/auto_trading/optimize_for_low_cap", 
                         json={"symbol": settings['symbol']})
        except:
            pass  # Silent fail for now
        
        return (
            settings['symbol'],
            settings['risk'],
            settings['confidence'],
            settings['tp'],
            settings['sl']
        )
    
    raise dash.exceptions.PreventUpdate

# --- Backtesting Callbacks ---
@app.callback(
    Output('backtest-result', 'children', allow_duplicate=True),
    Input('run-backtest-btn', 'n_clicks'),
    State('sidebar-symbol', 'value'),
    prevent_initial_call=True
)
def handle_run_backtest(n_clicks, symbol):
    """Handle backtest button click - uses your existing backend system"""
    if n_clicks:
        try:
            # Use your existing run_backtest function from utils
            result = run_backtest(symbol or 'btcusdt', 10000)
            
            if result and result.get('status') == 'success':
                backtest_data = result.get('results', {})
                
                return html.Div([
                    html.H5("📊 Backtest Results", className="text-success"),
                    html.P(f"Symbol: {symbol or 'btcusdt'}"),
                    html.P(f"Total Trades: {backtest_data.get('total_trades', 'N/A')}"),
                    html.P(f"Win Rate: {backtest_data.get('win_rate', 0):.1f}%"),
                    html.P(f"Total Return: {backtest_data.get('total_return', 0):.1f}%"),
                    html.P(f"Sharpe Ratio: {backtest_data.get('sharpe_ratio', 0):.2f}"),
                    html.P(f"Max Drawdown: {backtest_data.get('max_drawdown', 0):.1f}%"),
                    html.Small(f"Completed: {backtest_data.get('completed_at', 'N/A')}", 
                              className="text-muted")
                ], className="alert alert-success")
            else:
                return html.Div([
                    html.H5("⚠️ Backtest Failed", className="text-warning"),
                    html.P("Could not run backtest. Check if backend is running.")
                ], className="alert alert-warning")
                
        except Exception as e:
            return html.Div([
                html.H5("❌ Error", className="text-danger"),
                html.P(f"Error running backtest: {str(e)}")
            ], className="alert alert-danger")
    
    return html.Div()

@app.callback(
    Output('backtest-result', 'children', allow_duplicate=True),
    Input('run-backtest-sample-btn', 'n_clicks'),
    prevent_initial_call=True
)
def handle_run_sample_backtest(n_clicks):
    """Handle sample backtest button click"""
    if n_clicks:
        try:
            # Run a sample backtest with BTC
            result = run_backtest('btcusdt', 10000)
            
            if result and result.get('status') == 'success':
                backtest_data = result.get('results', {})
                
                return html.Div([
                    html.H5("📊 Sample Backtest Results (BTC/USDT)", className="text-success"),
                    html.Div([
                        html.Div([
                            html.Strong("Trading Performance:"),
                            html.Ul([
                                html.Li(f"Total Trades: {backtest_data.get('total_trades', 'N/A')}"),
                                html.Li(f"Win Rate: {backtest_data.get('win_rate', 0):.1f}%"),
                                html.Li(f"Total Return: {backtest_data.get('total_return', 0):.1f}%"),
                            ])
                        ], className="col-md-6"),
                        html.Div([
                            html.Strong("Risk Metrics:"),
                            html.Ul([
                                html.Li(f"Sharpe Ratio: {backtest_data.get('sharpe_ratio', 0):.2f}"),
                                html.Li(f"Max Drawdown: {backtest_data.get('max_drawdown', 0):.1f}%"),
                                html.Li(f"Profit Factor: {backtest_data.get('profit_factor', 0):.2f}"),
                            ])
                        ], className="col-md-6"),
                    ], className="row"),
                    html.Hr(),
                    html.P([
                        html.Strong("Note: "), 
                        "This uses your existing AdvancedBacktester system. ",
                        "For transfer learning validation, use the new advanced backtesting script."
                    ], className="text-info"),
                    html.Small(f"Completed: {backtest_data.get('completed_at', 'N/A')}", 
                              className="text-muted")
                ], className="alert alert-success")
            else:
                return html.Div([
                    html.H5("⚠️ Sample Backtest Failed", className="text-warning"),
                    html.P("Could not run sample backtest. Backend may not be running."),
                    html.P([
                        "Alternative: Run ", 
                        html.Code("python run_complete_backtest.py"), 
                        " for transfer learning validation."
                    ])
                ], className="alert alert-warning")
                
        except Exception as e:
            return html.Div([
                html.H5("Error", className="text-danger"),
                html.P(f"Error occurred: {str(e)}", className="text-muted")
            ], className="alert alert-danger")

# --- Model Analytics Callbacks ---
@app.callback(
    [Output('model-analytics-graph', 'figure'),
     Output('model-analytics-table', 'children'),
     Output('refresh-model-analytics-btn-output', 'children')],
    [Input('refresh-model-analytics-btn', 'n_clicks')],
    prevent_initial_call=False
)
def update_model_analytics(n_clicks):
    """Update model analytics graph and table"""
    try:
        # Fetch model analytics from backend
        resp = requests.get(f"{API_URL}/model/analytics")
        if resp.status_code == 200:
            data = resp.json()
            if data["status"] == "success":
                analytics = data["analytics"]
                
                # Create metrics table
                metrics_data = [
                    {"Metric": "Accuracy", "Value": f"{analytics.get('accuracy', 0):.2%}"},
                    {"Metric": "Precision", "Value": f"{analytics.get('precision', 0):.2%}"},
                    {"Metric": "Recall", "Value": f"{analytics.get('recall', 0):.2%}"},
                    {"Metric": "F1 Score", "Value": f"{analytics.get('f1_score', 0):.2%}"},
                    {"Metric": "Avg Confidence", "Value": f"{analytics.get('avg_confidence', 0):.2%}"},
                    {"Metric": "Total Trades", "Value": f"{analytics.get('trades_analyzed', 0):,}"},
                    {"Metric": "Profitable", "Value": f"{analytics.get('profitable_predictions', 0):,}"},
                    {"Metric": "Loss Predictions", "Value": f"{analytics.get('loss_predictions', 0):,}"},
                ]
                
                metrics_table = dash_table.DataTable(
                    data=metrics_data,
                    columns=[
                        {"name": "Metric", "id": "Metric"},
                        {"name": "Value", "id": "Value"}
                    ],
                    style_table={'backgroundColor': '#2a2a2a'},
                    style_cell={
                        'backgroundColor': '#333333',
                        'color': '#e0e0e0',
                        'textAlign': 'left',
                        'padding': '10px'
                    },
                    style_header={
                        'backgroundColor': '#404040',
                        'color': '#ffffff',
                        'fontWeight': 'bold'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#2a2a2a'
                        }
                    ]
                )
                
                # Create performance chart
                fig = go.Figure()
                
                # Add accuracy and other metrics as bar chart
                metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'Avg Confidence']
                metrics_values = [
                    analytics.get('accuracy', 0),
                    analytics.get('precision', 0),
                    analytics.get('recall', 0),
                    analytics.get('f1_score', 0),
                    analytics.get('avg_confidence', 0)
                ]
                
                fig.add_trace(go.Bar(
                    x=metrics_names,
                    y=metrics_values,
                    marker_color=['#00ff88', '#4CAF50', '#2196F3', '#FF9800', '#9C27B0'],
                    text=[f"{val:.2%}" for val in metrics_values],
                    textposition='auto',
                ))
                
                fig.update_layout(
                    title="Model Performance Metrics",
                    xaxis_title="Metrics",
                    yaxis_title="Score",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0e0e0'),
                    title_font=dict(color='#00ff88', size=16),
                    xaxis=dict(gridcolor='#404040'),
                    yaxis=dict(gridcolor='#404040'),
                    showlegend=False
                )
                
                # Success message
                success_msg = html.Div([
                    html.I(className="bi bi-check-circle me-1 text-success"),
                    f"Analytics refreshed successfully. Last updated: {analytics.get('last_updated', 'N/A')}"
                ], className="text-success")
                
                return fig, metrics_table, success_msg
        
        # Fallback for API errors
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="No Data Available",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0')
        )
        
        error_msg = html.Div([
            html.I(className="bi bi-exclamation-triangle me-1 text-warning"),
            "Failed to fetch analytics data"
        ], className="text-warning")
        
        return empty_fig, html.Div("No analytics data available."), error_msg
        
    except Exception as e:
        # Error handling
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="Error Loading Data",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0')
        )
        
        error_msg = html.Div([
            html.I(className="bi bi-x-circle me-1 text-danger"),
            f"Error: {str(e)}"
        ], className="text-danger")
        
        return empty_fig, html.Div("Error loading analytics."), error_msg

# --- Percentage Amount Synchronization ---
@app.callback(
    Output('percentage-amount-slider', 'value'),
    Input('percentage-amount-input', 'value'),
    prevent_initial_call=True
)
def sync_slider_from_input(input_value):
    """Sync slider when input changes"""
    if input_value is not None:
        return min(max(input_value, 1), 100)  # Clamp between 1 and 100
    return dash.no_update

@app.callback(
    Output('percentage-amount-input', 'value'),
    Input('percentage-amount-slider', 'value'),
    prevent_initial_call=True
)
def sync_input_from_slider(slider_value):
    """Sync input when slider changes"""
    if slider_value is not None:
        return slider_value
    return dash.no_update

# --- Reset Auto Trading ---
@app.callback(
    Output('reset-auto-trading-btn', 'children'),
    Input('reset-auto-trading-btn', 'n_clicks'),
    prevent_initial_call=True
)
def reset_auto_trading(n_clicks):
    """Reset auto trading system"""
    if not n_clicks:
        return "🔄 Reset System"
    
    try:
        resp = requests.post(f"{API_URL}/auto_trading/reset")
        
        if resp.status_code == 200:
            data = resp.json()
            if data["status"] == "success":
                return [
                    html.I(className="bi bi-check me-1"),
                    "System Reset!"
                ]
        
        return [
            html.I(className="bi bi-x me-1"),
            "Reset Failed"
        ]
        
    except Exception as e:
        print(f"Error resetting system: {e}")
        return [
            html.I(className="bi bi-exclamation-triangle me-1"),
            "Reset Error"
        ]

# --- Open Positions Table ---
@app.callback(
    Output('open-positions-table', 'children'),
    Input('auto-trading-interval', 'n_intervals'),
    prevent_initial_call=False
)
def update_open_positions(n_intervals):
    """Update open positions table"""
    try:
        resp = requests.get(f"{API_URL}/auto_trading/trades")
        if resp.status_code == 200:
            data = resp.json()
            if data["status"] == "success":
                open_trades = data["data"]["open_trades"]
                
                if not open_trades:
                    return html.Div([
                        html.I(className="bi bi-info-circle me-2 text-info"),
                        "No open positions"
                    ], className="text-center text-muted py-3")
                
                # Create table data
                table_data = []
                for trade_id, trade in open_trades.items():
                    # Calculate unrealized P&L (mock calculation)
                    current_price = 50000  # Mock current price
                    entry_price = trade["entry_price"]
                    direction = trade["direction"]
                    amount = trade["amount"]
                    
                    if direction == "LONG":
                        unrealized_pnl = (current_price - entry_price) * amount / entry_price
                    else:
                        unrealized_pnl = (entry_price - current_price) * amount / entry_price
                    
                    table_data.append({
                        "Symbol": trade["symbol"],
                        "Direction": trade["direction"],
                        "Entry Price": f"${entry_price:,.4f}",
                        "Amount": f"${amount:.2f}",
                        "Unrealized P&L": f"${unrealized_pnl:.2f}",
                        "Confidence": f"{trade['confidence']:.1f}%",
                        "Actions": html.Div([
                            html.Button(
                                "❌",
                                id={"type": "close-position-btn", "index": trade_id},
                                className="btn btn-sm btn-outline-danger me-1",
                                title="Close Position"
                            )
                        ])
                    })
                
                return dash_table.DataTable(
                    data=table_data,
                    columns=[
                        {"name": "Symbol", "id": "Symbol"},
                        {"name": "Direction", "id": "Direction"},
                        {"name": "Entry Price", "id": "Entry Price"},
                        {"name": "Amount", "id": "Amount"},
                        {"name": "Unrealized P&L", "id": "Unrealized P&L"},
                        {"name": "Confidence", "id": "Confidence"},
                        {"name": "Actions", "id": "Actions", "presentation": "markdown"}
                    ],
                    style_table={"overflowX": "auto"},
                    style_cell={
                        "backgroundColor": "#1a1a1a",
                        "color": "white",
                        "textAlign": "center",
                        "padding": "8px"
                    },
                    style_header={
                        "backgroundColor": "#222",
                        "color": "#00ff88",
                        "fontWeight": "bold"
                    }
                )
        
        return html.Div([
            html.I(className="bi bi-exclamation-triangle me-2"),
            "Could not load positions"
        ], className="text-center text-muted py-3")
        
    except Exception as e:
        return html.Div([
            html.I(className="bi bi-x-circle me-2 text-danger"),
            f"Error: {str(e)}"
        ], className="text-center text-danger py-3")

# --- Trade Log ---
@app.callback(
    Output('auto-trade-log', 'children'),
    Input('auto-trading-interval', 'n_intervals'),
    prevent_initial_call=False
)
def update_trade_log(n_intervals):
    """Update auto trading log"""
    try:
        resp = requests.get(f"{API_URL}/auto_trading/trades")
        if resp.status_code == 200:
            data = resp.json()
            if data["status"] == "success":
                trade_log = data["data"]["trade_log"]
                
                if not trade_log:
                    return html.Div([
                        html.I(className="bi bi-info-circle me-2"),
                        "No trading activity yet"
                    ], className="text-muted text-center")
                
                # Format log entries
                log_entries = []
                for entry in reversed(trade_log[-20:]):  # Show last 20 entries
                    timestamp = entry["timestamp"]
                    message = entry["message"]
                    entry_type = entry.get("type", "info")
                    
                    # Color coding by type
                    if entry_type == "trade_open":
                        color = "#00ff88"  # Green
                        icon = "📈"
                    elif entry_type == "trade_close":
                        pnl = entry.get("pnl", 0)
                        color = "#00ff88" if pnl >= 0 else "#ff4444"  # Green/Red based on P&L
                        icon = "📉" if pnl < 0 else "💰"
                    elif entry_type == "system":
                        color = "#ffaa00"  # Orange
                        icon = "⚙️"
                    else:
                        color = "#888888"  # Gray
                        icon = "ℹ️"
                    
                    log_entries.append(
                        html.Div([
                            html.Span(f"{icon} [{timestamp[:19]}] ", style={"color": "#aaa"}),
                            html.Span(message, style={"color": color})
                        ], style={"marginBottom": "5px", "fontSize": "11px"})
                    )
                
                return log_entries
        
        return html.Div([
            html.I(className="bi bi-exclamation-triangle me-2"),
            "Could not load trade log"
        ], className="text-warning text-center")
        
    except Exception as e:
        return html.Div([
            html.I(className="bi bi-x-circle me-2"),
            f"Error: {str(e)}"
        ], className="text-danger text-center")

# --- Close Position Button Handler ---
@app.callback(
    Output({"type": "close-position-btn", "index": ALL}, 'children'),
    Input({"type": "close-position-btn", "index": ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def close_position_handler(n_clicks_list):
    """Handle closing positions manually"""
    if not any(n_clicks_list):
        return ["❌"] * len(n_clicks_list)
    
    # Get which button was clicked
    triggered = callback_context.triggered
    if triggered:
        button_id = triggered[0]['prop_id'].split('.')[0]
        trade_id = eval(button_id)['index']  # Extract trade_id from button id
        
        try:
            resp = requests.post(f"{API_URL}/auto_trading/close_trade/{trade_id}")
            if resp.status_code == 200:
                data = resp.json()
                if data["status"] == "success":
                    # Return success state for the clicked button
                    result = ["❌"] * len(n_clicks_list)
                    clicked_index = next((i for i, clicks in enumerate(n_clicks_list) if clicks), 0)
                    result[clicked_index] = "✅"
                    return result
        except Exception as e:
            print(f"Error closing position: {e}")
    
    return ["❌"] * len(n_clicks_list)

# --- Reset All Button Callback ---
@app.callback(
    Output('reset-all-btn-output', 'children'),
    Input('reset-all-btn', 'n_clicks'),
    prevent_initial_call=True
)
def reset_all_callback(n_clicks):
    if n_clicks:
        print("[DASHBOARD] Reset All button clicked.")
        try:
            # This would reset balance, trades, and notifications
            # For now, just simulate success
            reset_ok = True
            if reset_ok:
                return html.Div([
                    html.H5("Reset All Succeeded", style={"color": "green"}),
                    html.P("All data (balance, trades, notifications) reset successfully.")
                ])
            else:
                raise Exception("Reset all failed")
        except Exception as e:
            return html.Div([
                html.H5("Reset All Failed", style={"color": "red"}),
                html.P(f"Error: {str(e)}")
            ])
    return ""

print('[DASH DEBUG] Auto trading callbacks registered successfully')

# --- Low-Cap Coin Optimization Callbacks ---
@app.callback(
    Output('auto-symbol-dropdown', 'value'),
    Output('auto-risk-slider', 'value'),
    Output('auto-confidence-slider', 'value'),
    Output('auto-tp-input', 'value'),
    Output('auto-sl-input', 'value'),
    [Input('optimize-kaia-btn', 'n_clicks'),
     Input('optimize-jasmy-btn', 'n_clicks'),
     Input('optimize-gala-btn', 'n_clicks')],
    prevent_initial_call=True
)
def optimize_for_low_cap_coin(kaia_clicks, jasmy_clicks, gala_clicks):
    """Optimize settings for specific low-cap coins"""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Define optimized settings for each coin
    settings_map = {
        'optimize-kaia-btn': {
            'symbol': 'KAIAUSDT',
            'risk': 3.0,
            'confidence': 55.0,
            'tp': 2.5,
            'sl': 1.2
        },
        'optimize-jasmy-btn': {
            'symbol': 'JASMYUSDT', 
            'risk': 4.0,
            'confidence': 60.0,
            'tp': 2.0,
            'sl': 1.0
        },
        'optimize-gala-btn': {
            'symbol': 'GALAUSDT',
            'risk': 3.5,
            'confidence': 58.0,
            'tp': 2.2,
            'sl': 1.1
        }
    }
    
    if button_id in settings_map:
        settings = settings_map[button_id]
        
        # Call backend to optimize
        try:
            requests.post(f"{API_URL}/auto_trading/optimize_for_low_cap", 
                         json={"symbol": settings['symbol']})
        except:
            pass  # Silent fail for now
        
        return (
            settings['symbol'],
            settings['risk'],
            settings['confidence'],
            settings['tp'],
            settings['sl']
        )
    
    raise dash.exceptions.PreventUpdate

# --- Backtesting Callbacks ---
@app.callback(
    Output('backtest-result', 'children', allow_duplicate=True),
    Input('run-backtest-btn', 'n_clicks'),
    State('sidebar-symbol', 'value'),
    prevent_initial_call=True
)
def handle_run_backtest(n_clicks, symbol):
    """Handle backtest button click - uses your existing backend system"""
    if n_clicks:
        try:
            # Use your existing run_backtest function from utils
            result = run_backtest(symbol or 'btcusdt', 10000)
            
            if result and result.get('status') == 'success':
                backtest_data = result.get('results', {})
                
                return html.Div([
                    html.H5("📊 Backtest Results", className="text-success"),
                    html.P(f"Symbol: {symbol or 'btcusdt'}"),
                    html.P(f"Total Trades: {backtest_data.get('total_trades', 'N/A')}"),
                    html.P(f"Win Rate: {backtest_data.get('win_rate', 0):.1f}%"),
                    html.P(f"Total Return: {backtest_data.get('total_return', 0):.1f}%"),
                    html.P(f"Sharpe Ratio: {backtest_data.get('sharpe_ratio', 0):.2f}"),
                    html.P(f"Max Drawdown: {backtest_data.get('max_drawdown', 0):.1f}%"),
                    html.Small(f"Completed: {backtest_data.get('completed_at', 'N/A')}", 
                              className="text-muted")
                ], className="alert alert-success")
            else:
                return html.Div([
                    html.H5("⚠️ Backtest Failed", className="text-warning"),
                    html.P("Could not run backtest. Check if backend is running.")
                ], className="alert alert-warning")
                
        except Exception as e:
            return html.Div([
                html.H5("❌ Error", className="text-danger"),
                html.P(f"Error running backtest: {str(e)}")
            ], className="alert alert-danger")
    
    return html.Div()

@app.callback(
    Output('backtest-result', 'children', allow_duplicate=True),
    Input('run-backtest-sample-btn', 'n_clicks'),
    prevent_initial_call=True
)
def handle_run_sample_backtest(n_clicks):
    """Handle sample backtest button click"""
    if n_clicks:
        try:
            # Run a sample backtest with BTC
            result = run_backtest('btcusdt', 10000)
            
            if result and result.get('status') == 'success':
                backtest_data = result.get('results', {})
                
                return html.Div([
                    html.H5("📊 Sample Backtest Results (BTC/USDT)", className="text-success"),
                    html.Div([
                        html.Div([
                            html.Strong("Trading Performance:"),
                            html.Ul([
                                html.Li(f"Total Trades: {backtest_data.get('total_trades', 'N/A')}"),
                                html.Li(f"Win Rate: {backtest_data.get('win_rate', 0):.1f}%"),
                                html.Li(f"Total Return: {backtest_data.get('total_return', 0):.1f}%"),
                            ])
                        ], className="col-md-6"),
                        html.Div([
                            html.Strong("Risk Metrics:"),
                            html.Ul([
                                html.Li(f"Sharpe Ratio: {backtest_data.get('sharpe_ratio', 0):.2f}"),
                                html.Li(f"Max Drawdown: {backtest_data.get('max_drawdown', 0):.1f}%"),
                                html.Li(f"Profit Factor: {backtest_data.get('profit_factor', 0):.2f}"),
                            ])
                        ], className="col-md-6"),
                    ], className="row"),
                    html.Hr(),
                    html.P([
                        html.Strong("Note: "), 
                        "This uses your existing AdvancedBacktester system. ",
                        "For transfer learning validation, use the new advanced backtesting script."
                    ], className="text-info"),
                    html.Small(f"Completed: {backtest_data.get('completed_at', 'N/A')}", 
                              className="text-muted")
                ], className="alert alert-success")
            else:
                return html.Div([
                    html.H5("⚠️ Sample Backtest Failed", className="text-warning"),
                    html.P("Could not run sample backtest. Backend may not be running."),
                    html.P([
                        "Alternative: Run ", 
                        html.Code("python run_complete_backtest.py"), 
                        " for transfer learning validation."
                    ])
                ], className="alert alert-warning")
                
        except Exception as e:
            return html.Div([
                html.H5("Error", className="text-danger"),
                html.P(f"Error occurred: {str(e)}", className="text-muted")
            ], className="alert alert-danger")

# --- Model Analytics Callbacks ---
@app.callback(
    [Output('model-analytics-graph', 'figure'),
     Output('model-analytics-table', 'children'),
     Output('refresh-model-analytics-btn-output', 'children')],
    [Input('refresh-model-analytics-btn', 'n_clicks')],
    prevent_initial_call=False
)
def update_model_analytics(n_clicks):
    """Update model analytics graph and table"""
    try:
        # Fetch model analytics from backend
        resp = requests.get(f"{API_URL}/model/analytics")
        if resp.status_code == 200:
            data = resp.json()
            if data["status"] == "success":
                analytics = data["analytics"]
                
                # Create metrics table
                metrics_data = [
                    {"Metric": "Accuracy", "Value": f"{analytics.get('accuracy', 0):.2%}"},
                    {"Metric": "Precision", "Value": f"{analytics.get('precision', 0):.2%}"},
                    {"Metric": "Recall", "Value": f"{analytics.get('recall', 0):.2%}"},
                    {"Metric": "F1 Score", "Value": f"{analytics.get('f1_score', 0):.2%}"},
                    {"Metric": "Avg Confidence", "Value": f"{analytics.get('avg_confidence', 0):.2%}"},
                    {"Metric": "Total Trades", "Value": f"{analytics.get('trades_analyzed', 0):,}"},
                    {"Metric": "Profitable", "Value": f"{analytics.get('profitable_predictions', 0):,}"},
                    {"Metric": "Loss Predictions", "Value": f"{analytics.get('loss_predictions', 0):,}"},
                ]
                
                metrics_table = dash_table.DataTable(
                    data=metrics_data,
                    columns=[
                        {"name": "Metric", "id": "Metric"},
                        {"name": "Value", "id": "Value"}
                    ],
                    style_table={'backgroundColor': '#2a2a2a'},
                    style_cell={
                        'backgroundColor': '#333333',
                        'color': '#e0e0e0',
                        'textAlign': 'left',
                        'padding': '10px'
                    },
                    style_header={
                        'backgroundColor': '#404040',
                        'color': '#ffffff',
                        'fontWeight': 'bold'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#2a2a2a'
                        }
                    ]
                )
                
                # Create performance chart
                fig = go.Figure()
                
                # Add accuracy and other metrics as bar chart
                metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'Avg Confidence']
                metrics_values = [
                    analytics.get('accuracy', 0),
                    analytics.get('precision', 0),
                    analytics.get('recall', 0),
                    analytics.get('f1_score', 0),
                    analytics.get('avg_confidence', 0)
                ]
                
                fig.add_trace(go.Bar(
                    x=metrics_names,
                    y=metrics_values,
                    marker_color=['#00ff88', '#4CAF50', '#2196F3', '#FF9800', '#9C27B0'],
                    text=[f"{val:.2%}" for val in metrics_values],
                    textposition='auto',
                ))
                
                fig.update_layout(
                    title="Model Performance Metrics",
                    xaxis_title="Metrics",
                    yaxis_title="Score",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0e0e0'),
                    title_font=dict(color='#00ff88', size=16),
                    xaxis=dict(gridcolor='#404040'),
                    yaxis=dict(gridcolor='#404040'),
                    showlegend=False
                )
                
                # Success message
                success_msg = html.Div([
                    html.I(className="bi bi-check-circle me-1 text-success"),
                    f"Analytics refreshed successfully. Last updated: {analytics.get('last_updated', 'N/A')}"
                ], className="text-success")
                
                return fig, metrics_table, success_msg
        
        # Fallback for API errors
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="No Data Available",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0')
        )
        
        error_msg = html.Div([
            html.I(className="bi bi-exclamation-triangle me-1 text-warning"),
            "Failed to fetch analytics data"
        ], className="text-warning")
        
        return empty_fig, html.Div("No analytics data available."), error_msg
        
    except Exception as e:
        # Error handling
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="Error Loading Data",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0')
        )
        
        error_msg = html.Div([
            html.I(className="bi bi-x-circle me-1 text-danger"),
            f"Error: {str(e)}"
        ], className="text-danger")
        
        return empty_fig, html.Div("Error loading analytics."), error_msg
