# dashboard_utils.py
"""
Helper functions for dashboard callbacks.
All API calls, data processing, and repeated logic are centralized here.
"""
import requests
from plotly import graph_objs as go

API_URL = "http://localhost:5000"

# --- Sidebar Helpers ---
def fetch_sidebar_performance(api_session):
    try:
        resp = api_session.get(f"{API_URL}/sidebar/performance", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return [f"Winrate: {data.get('winrate', '-')}", f"Total trades: {data.get('total_trades', '-')}", f"Daily PnL: {data.get('daily_pnl', '-')}"]
        else:
            return ["Winrate: -", "Total trades: -", "Daily PnL: -"]
    except Exception as e:
        return [f"Error: {e}", "-", "-"]

def fetch_prediction(api_session, symbol):
    try:
        resp = api_session.post(f"{API_URL}/predict", json={"symbol": symbol}, timeout=10)
        if resp.status_code == 200:
            result = resp.json()
            return f"Prediction: {result.get('prediction', '-')} | Confidence: {result.get('confidence', '-')}"
        else:
            return f"Prediction error: {resp.text}"
    except Exception as e:
        return f"Prediction error: {e}"

def fetch_analytics(api_session, symbol):
    try:
        resp = api_session.get(f"{API_URL}/analytics/{symbol}", timeout=10)
        if resp.status_code == 200:
            result = resp.json()
            return f"Analytics: {result.get('summary', '-')}"
        else:
            return f"Analytics error: {resp.text}"
    except Exception as e:
        return f"Analytics error: {e}"

# --- Chart Helpers ---
def fetch_chart(api_session, endpoint, symbol):
    try:
        resp = api_session.get(f"{API_URL}/chart/{endpoint}", params={"symbol": symbol}, timeout=10)
        if resp.status_code == 200:
            result = resp.json()
            return go.Figure(result.get('figure', {}))
        else:
            return go.Figure(layout={'title': f"Error: {resp.text}"})
    except Exception as e:
        return go.Figure(layout={'title': f"Error: {e}"})

# --- Balance Helpers ---
def fetch_futures_balance(api_session):
    try:
        resp = api_session.get(f"{API_URL}/futures/balance", timeout=10)
        if resp.status_code == 200:
            result = resp.json()
            return [result.get('virtual_balance', '-'), result.get('pnl', '-'), result.get('total_balance', '-'), result.get('available_balance', '-')]
        return ["-", "-", "-", "-"]
    except Exception as e:
        return [f"Error: {e}", "-", "-", "-"]

def fetch_virtual_balance(api_session):
    """Fetch the current virtual balance from the backend and handle errors robustly."""
    try:
        resp = api_session.get(f"{API_URL}/balance/virtual", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success":
                # Return the balance as a string for display
                return str(data.get("virtual_balance", "-"))
            else:
                # Backend returned an error status
                return f"Error: {data.get('message', 'Unknown error')}"
        else:
            return f"Error: HTTP {resp.status_code}"
    except Exception as e:
        return f"Error: {e}"

# For compatibility, fetch_auto_balance should just call fetch_virtual_balance
fetch_auto_balance = fetch_virtual_balance

# --- Trading Helpers ---
def fetch_futures_trading_controls(api_session, open_n, close_n, update_n, symbol, side, qty, leverage):
    ctx = None
    try:
        import dash
        ctx = dash.callback_context
    except Exception:
        pass
    ctx_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx and ctx.triggered else None
    try:
        if ctx_id == 'open-futures-position' and open_n:
            resp = api_session.post(f"{API_URL}/futures/open", json={"symbol": symbol, "side": side, "qty": qty, "leverage": leverage}, timeout=10)
            if resp.status_code == 200:
                result = resp.json()
                return [result.get('controls', 'Opened'), result.get('status', 'Success')]
            else:
                return [f"Open error: {resp.text}", "Error"]
        elif ctx_id == 'close-futures-position' and close_n:
            resp = api_session.post(f"{API_URL}/futures/close", json={"symbol": symbol}, timeout=10)
            if resp.status_code == 200:
                result = resp.json()
                return [result.get('controls', 'Closed'), result.get('status', 'Success')]
            else:
                return [f"Close error: {resp.text}", "Error"]
        elif ctx_id == 'update-futures-positions' and update_n:
            resp = api_session.get(f"{API_URL}/futures/update", timeout=10)
            if resp.status_code == 200:
                result = resp.json()
                return [result.get('controls', 'Updated'), result.get('status', 'Success')]
            else:
                return [f"Update error: {resp.text}", "Error"]
    except Exception as e:
        return [f"Futures error: {e}", "Error"]
    return [None, None]

# --- Backtest Helpers ---
def fetch_comprehensive_backtest(api_session, n, start, end, symbol, strategy):
    if not n:
        return [None, None, None]
    try:
        resp = api_session.post(f"{API_URL}/backtest/run", json={"start": start, "end": end, "symbol": symbol, "strategy": strategy}, timeout=60)
        if resp.status_code == 200:
            result = resp.json()
            return [result.get('output', 'Done'), result.get('progress', 100), result.get('status', 'Complete')]
        else:
            return [f"Backtest error: {resp.text}", 0, "Error"]
    except Exception as e:
        return [f"Backtest error: {e}", 0, "Error"]

# --- Model Retrain Helpers ---
def fetch_model_retrain(api_session, n1, n2):
    try:
        resp = api_session.post(f"{API_URL}/model/retrain", json={"start": n1, "refresh": n2}, timeout=60)
        if resp.status_code == 200:
            result = resp.json()
            return [result.get('status', 'Retrain done'), result.get('progress', 100), result.get('message', 'Retrain Complete')]
        else:
            return [f"Retrain error: {resp.text}", 0, "Error"]
    except Exception as e:
        return [f"Retrain error: {e}", 0, "Error"]

# --- Notification Helpers ---
def fetch_notifications(api_session, show_unread):
    try:
        params = {"unread_only": show_unread}
        resp = api_session.get(f"{API_URL}/notifications", params=params, timeout=10)
        if resp.status_code == 200:
            result = resp.json()
            return [result.get('notifications', []), result.get('count', 0)]
        else:
            return [f"Notification error: {resp.text}", 0]
    except Exception as e:
        return [f"Notification error: {e}", 0]

def send_manual_notification(api_session, n, notif_type, notif_msg):
    if n and notif_msg:
        try:
            resp = api_session.post(f"{API_URL}/notifications/manual", json={"type": notif_type, "message": notif_msg}, timeout=10)
            if resp.status_code == 200:
                result = resp.json()
                return result.get('status', 'Sent')
            else:
                return f"Notification send error: {resp.text}"
        except Exception as e:
            return f"Notification send error: {e}"
    return None

def clear_notifications(api_session, n):
    if n:
        try:
            resp = api_session.post(f"{API_URL}/notifications/clear", timeout=10)
            if resp.status_code == 200:
                result = resp.json()
                return result.get('status', 'Cleared')
            else:
                return f"Clear error: {resp.text}"
        except Exception as e:
            return f"Clear error: {e}"
    return None

# --- Technical Indicators Helpers ---
def fetch_technical_indicators(api_session, symbol):
    """Fetch and format technical indicators (RSI, MACD, etc.) for a given symbol."""
    import plotly.graph_objs as go
    from datetime import datetime
    try:
        symbol = symbol or "BTCUSDT"
        resp = api_session.get(f"{API_URL}/features/indicators", params={"symbol": symbol.lower()}, timeout=10)
        if resp.status_code == 200:
            indicators_data = resp.json()
            fig = go.Figure()
            # Add RSI if available
            if 'rsi' in indicators_data:
                rsi = indicators_data['rsi']
                fig.add_trace(go.Scatter(
                    x=[0, 1],
                    y=[rsi, rsi],
                    mode='lines+markers',
                    name='RSI',
                    line=dict(color='#ff6b6b', width=2)
                ))
            # Add MACD if available
            if 'macd' in indicators_data:
                macd = indicators_data['macd']
                fig.add_trace(go.Scatter(
                    x=[0, 1],
                    y=[macd, macd],
                    mode='lines+markers',
                    name='MACD',
                    line=dict(color='#00bfff', width=2)
                ))
            fig.update_layout(
                title="Technical Indicators",
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=300,
                showlegend=True,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            return fig
        else:
            fig = go.Figure()
            fig.add_annotation(
                text="Indicators Loading...",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(color='white', size=16)
            )
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=300,
                showlegend=False,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            return fig
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(
            text=f"Indicators Error: {str(e)[:50]}",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(color='red', size=14)
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300,
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig


def fetch_advanced_analytics(api_session, endpoint):
    """Fetch and return advanced analytics/model monitoring data from a given endpoint."""
    try:
        resp = api_session.get(f"{API_URL}/{endpoint}", timeout=10)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": resp.text}
    except Exception as e:
        return {"error": str(e)}

# --- Risk Settings Helpers ---
def manage_risk_settings(api_session, save_clicks, load_clicks, max_drawdown, position_size, stop_loss, take_profit):
    import dash
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx and ctx.triggered else None
    try:
        if triggered_id == 'save-risk-settings' and save_clicks:
            settings = {
                "max_drawdown": max_drawdown or 0.05,
                "position_size": position_size or 0.02,
                "stop_loss_pct": stop_loss or 0.02,
                "take_profit_pct": take_profit or 0.04
            }
            resp = api_session.post(f"{API_URL}/risk_settings", json=settings)
            if resp.status_code == 200:
                return "", "Risk settings saved successfully!"
            else:
                return "", "Failed to save risk settings"
        elif triggered_id == 'load-risk-settings':
            resp = api_session.get(f"{API_URL}/risk_settings")
            if resp.status_code == 200:
                settings = resp.json()
                display = f"Max Drawdown: {settings.get('max_drawdown', 0.05):.2%}, Position Size: {settings.get('position_size', 0.02):.2%}, Stop Loss: {settings.get('stop_loss_pct', 0.02):.2%}, Take Profit: {settings.get('take_profit_pct', 0.04):.2%}"
                return display, ""
            else:
                return "", "Failed to load risk settings"
    except Exception as e:
        return "", f"Error: {str(e)}"
    return "", ""

# --- Test/Dev Tool Helpers ---
def test_database_connection(api_session, n_clicks):
    if not n_clicks:
        return ""
    try:
        resp = api_session.get(f"{API_URL}/test/db", timeout=5)
        if resp.ok:
            return "[OK] Database OK"
        else:
            return "[ERROR] Database Error"
    except:
        return "[ERROR] Connection Failed"

def test_ml_system(api_session, n_clicks):
    if not n_clicks:
        return ""
    try:
        resp = api_session.get(f"{API_URL}/test/ml", timeout=5)
        if resp.ok:
            return "[OK] ML System OK"
        else:
            return "[ERROR] ML Error"
    except:
        return "[ERROR] ML Test Failed"

# --- Advanced/Dev Tools Helpers ---
def show_feature_importance(api_session, n_clicks):
    if not n_clicks:
        return ""
    try:
        resp = api_session.get(f"{API_URL}/ml/features/importance", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return f"Feature Importance: {data.get('summary', 'Success')}"
        else:
            return f"Feature importance error: {resp.text}"
    except Exception as e:
        return f"Feature importance error: {e}"

def prune_trades(api_session, n_clicks):
    if not n_clicks:
        return ""
    try:
        resp = api_session.post(f"{API_URL}/trades/prune", timeout=10)
        if resp.status_code == 200:
            return "Old trades pruned successfully."
        else:
            return f"Prune error: {resp.text}"
    except Exception as e:
        return f"Prune error: {e}"

def tune_models(api_session, n_clicks):
    if not n_clicks:
        return ""
    try:
        resp = api_session.post(f"{API_URL}/ml/tune", timeout=10)
        if resp.status_code == 200:
            return "Model tuning completed successfully."
        else:
            return f"Tune error: {resp.text}"
    except Exception as e:
        return f"Tune error: {e}"

def check_drift(api_session, n_clicks):
    if not n_clicks:
        return ""
    try:
        resp = api_session.get(f"{API_URL}/ml/drift/check", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return f"Drift Score: {data.get('drift_score', 0)}"
        else:
            return f"Drift check error: {resp.text}"
    except Exception as e:
        return f"Drift check error: {e}"

def online_learn(api_session, n_clicks):
    if not n_clicks:
        return ""
    try:
        resp = api_session.post(f"{API_URL}/ml/online_learning/start", timeout=10)
        if resp.status_code == 200:
            return "Online learning started."
        else:
            return f"Online learning error: {resp.text}"
    except Exception as e:
        return f"Online learning error: {e}"

def refresh_model_versions(api_session, n_clicks):
    if not n_clicks:
        return ""
    try:
        resp = api_session.get(f"{API_URL}/ml/models/versions", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return f"Latest Version: {data.get('latest_version', 'N/A')}"
        else:
            return f"Model versions error: {resp.text}"
    except Exception as e:
        return f"Model versions error: {e}"

# --- Transfer Learning Helpers ---
def manage_transfer_learning(api_session, action, **kwargs):
    try:
        if action == 'check_setup':
            resp = api_session.get(f"{API_URL}/model/crypto_transfer/initial_setup_required")
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
        elif action == 'init':
            resp = api_session.post(f"{API_URL}/model/crypto_transfer/initial_train", json=kwargs, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
        elif action == 'train_target':
            resp = api_session.post(f"{API_URL}/model/crypto_transfer/train_target", json=kwargs, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
        elif action == 'performance':
            resp = api_session.get(f"{API_URL}/model/crypto_transfer/performance")
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
    except Exception as e:
        return {"error": str(e)}

# --- Model Version/History Helpers ---
def manage_model_versions(api_session, action, **kwargs):
    try:
        if action == 'activate':
            resp = api_session.post(f"{API_URL}/model/active_version", json=kwargs, timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
        elif action == 'list':
            resp = api_session.get(f"{API_URL}/model/versions", timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
        elif action == 'active':
            resp = api_session.get(f"{API_URL}/model/active_version", timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
    except Exception as e:
        return {"error": str(e)}

def fetch_model_metrics(api_session):
    try:
        resp = api_session.get(f"{API_URL}/model/metrics", timeout=10)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": resp.text}
    except Exception as e:
        return {"error": str(e)}

def fetch_ml_performance_history(api_session):
    try:
        resp = api_session.get(f"{API_URL}/ml/performance/history", timeout=10)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": resp.text}
    except Exception as e:
        return {"error": str(e)}

def fetch_backtest_results(api_session):
    try:
        resp = api_session.get(f"{API_URL}/backtest/results", timeout=10)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": resp.text}
    except Exception as e:
        return {"error": str(e)}

def manage_model_retraining(api_session, action, **kwargs):
    try:
        if action == 'start':
            resp = api_session.post(f"{API_URL}/ml/retrain/start", json=kwargs, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
        elif action == 'status':
            resp = api_session.get(f"{API_URL}/ml/retrain/status", timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
    except Exception as e:
        return {"error": str(e)}

# --- Notification Stats/History Helpers ---
def fetch_notification_stats(api_session):
    try:
        resp = api_session.get(f"{API_URL}/notifications/stats", timeout=10)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": resp.text}
    except Exception as e:
        return {"error": str(e)}

def fetch_alert_history(api_session):
    try:
        resp = api_session.get(f"{API_URL}/alerts/history", timeout=10)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": resp.text}
    except Exception as e:
        return {"error": str(e)}

# --- Data Collection Helpers ---
def manage_data_collection(api_session, action, **kwargs):
    try:
        if action == 'start':
            resp = api_session.post(f"{API_URL}/data_collection/start", timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
        elif action == 'stop':
            resp = api_session.post(f"{API_URL}/data_collection/stop", timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
        elif action == 'check':
            resp = api_session.get(f"{API_URL}/data_collection/status", timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
        elif action == 'stats':
            resp = api_session.get(f"{API_URL}/data_collection/stats", timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
    except Exception as e:
        return {"error": str(e)}

# --- Email/Alert System Helpers ---
def manage_email_config(api_session, action, **kwargs):
    try:
        if action == 'save':
            resp = api_session.post(f"{API_URL}/email/config", json=kwargs, timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
        elif action == 'refresh':
            resp = api_session.get(f"{API_URL}/email/config", timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
        elif action == 'test':
            resp = api_session.post(f"{API_URL}/email/test", timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
    except Exception as e:
        return {"error": str(e)}

def send_test_alert(api_session, n_clicks):
    if not n_clicks:
        return ""
    try:
        resp = api_session.post(f"{API_URL}/alerts/test", timeout=10)
        if resp.status_code == 200:
            return resp.json().get('result', 'Alert sent')
        else:
            return f"Alert error: {resp.text}"
    except Exception as e:
        return f"Alert error: {e}"

def check_auto_alerts(api_session, n_clicks):
    if not n_clicks:
        return ""
    try:
        resp = api_session.post(f"{API_URL}/alerts/auto_check", timeout=10)
        if resp.status_code == 200:
            return resp.json().get('result', 'Checked')
        else:
            return f"Auto alert error: {resp.text}"
    except Exception as e:
        return f"Auto alert error: {e}"

# --- HFT Analysis Helpers ---
def manage_hft_analysis(api_session, action, **kwargs):
    try:
        if action == 'run':
            resp = api_session.post(f"{API_URL}/hft/analysis", json=kwargs, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
        elif action == 'refresh':
            resp = api_session.get(f"{API_URL}/hft/analysis", params=kwargs, timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
    except Exception as e:
        return {"error": str(e)}

# --- Online Learning System Helpers ---
def manage_online_learning(api_session, action, **kwargs):
    try:
        if action == 'start':
            resp = api_session.post(f"{API_URL}/ml/online_learning/start", json=kwargs, timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
        elif action == 'stop':
            resp = api_session.post(f"{API_URL}/ml/online_learning/stop", timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
        elif action == 'reset':
            resp = api_session.post(f"{API_URL}/ml/online_learning/reset", timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
        elif action == 'check':
            resp = api_session.get(f"{API_URL}/ml/online_learning/status", timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
        elif action == 'stats':
            resp = api_session.get(f"{API_URL}/ml/online_learning/stats", timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                return {"error": resp.text}
    except Exception as e:
        return {"error": str(e)}

# --- Advanced Technical Indicators (Futures) ---
def fetch_futures_indicator(api_session, indicator, symbol):
    try:
        resp = api_session.get(f"{API_URL}/futures/indicators/{indicator}", params={"symbol": symbol}, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": resp.text}
    except Exception as e:
        return {"error": str(e)}

# --- Sidebar Technical Indicators/ML Tools ---
def fetch_sidebar_indicator(api_session, indicator, symbol):
    try:
        resp = api_session.get(f"{API_URL}/sidebar/indicators/{indicator}", params={"symbol": symbol}, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": resp.text}
    except Exception as e:
        return {"error": str(e)}

def fetch_sidebar_ml_tools(api_session):
    try:
        resp = api_session.get(f"{API_URL}/sidebar/ml_tools", timeout=10)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": resp.text}
    except Exception as e:
        return {"error": str(e)}

# --- Sidebar/Section Toggles ---
def toggle_section(is_open):
    return not is_open

# --- Auto Trading Helpers ---
def fetch_auto_trading_status(api_session):
    """Fetch the current auto trading status (on/off, last signal, etc.)"""
    try:
        resp = api_session.get(f"{API_URL}/auto_trading/status", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            status = data.get('auto_trading', {})
            enabled = status.get('enabled', False)
            return f"{'ENABLED' if enabled else 'DISABLED'}", enabled
        else:
            return "Status error", False
    except Exception as e:
        return f"Error: {e}", False

def execute_auto_trading(api_session, enabled):
    """Toggle auto trading on/off."""
    try:
        payload = {"enabled": enabled}
        resp = api_session.post(f"{API_URL}/auto_trading/toggle", json=payload, timeout=10)
        if resp.status_code == 200:
            return resp.json().get('message', 'Toggled')
        else:
            return f"Toggle error: {resp.status_code}"
    except Exception as e:
        return f"Error: {e}"

def fetch_auto_pnl(api_session):
    """Fetch the current auto trading P&L and win rate."""
    try:
        resp = api_session.get(f"{API_URL}/calculate_pnl", timeout=10)
        if resp.status_code == 200:
            result = resp.json()
            return result.get('total_pnl', '-'), result.get('pnl_percentage', '-')
        else:
            # Show HTTP error code and message in both fields for clarity
            msg = f"HTTP {resp.status_code}: {resp.text}"
            return msg, msg
    except Exception as e:
        err = f"Error: {e}"
        return err, err
