# --- Refactored Callbacks for Crypto Trading Dashboard (Step 1: Imports, Globals, App Instance) ---
"""
This file is a step-by-step refactor of the original callbacks.py.
It will be built up in clean, non-redundant, and error-free steps.
"""

from dash.dependencies import Input, Output, State, ALL, MATCH
from dash import dcc, html, ctx, callback_context, dash_table, no_update
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import plotly.graph_objs as go
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dashboard_utils import (
    fetch_sidebar_performance,
    fetch_prediction,
    fetch_analytics,
    fetch_chart,
    fetch_futures_balance,
    fetch_auto_balance,
    fetch_virtual_balance,
    fetch_futures_trading_controls,
    fetch_comprehensive_backtest,
    fetch_model_retrain,
    fetch_notifications,
    send_manual_notification,
    clear_notifications,
    fetch_technical_indicators,
    fetch_advanced_analytics,
    manage_risk_settings,
    test_database_connection,
    test_ml_system,
    show_feature_importance,
    prune_trades,
    tune_models,
    check_drift,
    online_learn,
    refresh_model_versions,
    manage_transfer_learning,
    manage_model_versions,
    fetch_model_metrics,
    fetch_ml_performance_history,
    fetch_backtest_results,
    manage_model_retraining,
    fetch_notification_stats,
    fetch_alert_history,
    manage_data_collection,
    manage_email_config,
    send_test_alert,
    check_auto_alerts,
    manage_hft_analysis,
    manage_online_learning,
    fetch_futures_indicator,
    fetch_sidebar_indicator,
    fetch_sidebar_ml_tools,
    toggle_section
)

# --- App Instance Import (robust) ---
try:
    from .dash_app import app
except ImportError:
    try:
        from dash_app import app
    except ImportError:
        import dash
        app = dash.Dash(__name__)

# --- Global Constants ---
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

# --- Helper Functions ---
def create_empty_figure(title="No Data Available"):
    fig = go.Figure()
    fig.update_layout(title=title)
    return fig

def create_session_with_retries():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
        backoff_factor=1
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

api_session = create_session_with_retries()

# --- Step 1 Complete: Imports, globals, app, helpers ---
# Next step: Add clean, non-duplicated, error-free callback definitions.

# --- Step 2: Tab Content and Status Callbacks (Clean, No Duplication) ---
# The following callbacks are commented out to prevent duplicate output errors. Only one callback per output is allowed in Dash.
# @app.callback(Output('model-analytics-display', 'children'), Input('refresh-model-analytics', 'n_clicks'))
# def update_model_analytics(n):
#     return f"Model analytics refreshed: {n}"

# @app.callback(Output('transfer-learning-performance', 'children'), Input('refresh-transfer-performance', 'n_clicks'))
# def update_transfer_performance(n):
#     return f"Transfer learning performance refreshed: {n}"

# @app.callback(Output('model-metrics-display', 'children'), Input('refresh-model-metrics', 'n_clicks'))
# def update_model_metrics(n):
#     return f"Model metrics refreshed: {n}"

# @app.callback(Output('ml-performance-history', 'children'), Input('refresh-ml-history', 'n_clicks'))
# def update_ml_performance_history(n):
#     return f"ML performance history refreshed: {n}"

# @app.callback(Output('backtest-results-enhanced', 'children'), Input('load-backtest-results', 'n_clicks'))
# def load_backtest_results(n):
#     return f"Backtest results loaded: {n}"

# --- Step 2 Complete: Tab content and status callbacks added ---
# Next step: Add sidebar and quick action callbacks.

# --- Step 3: Sidebar and Quick Action Callbacks ---

@app.callback(
    [Output("sidebar-fixed-amount-section", "style"), Output("sidebar-amount-input", "placeholder")],
    Input("sidebar-amount-type", "value")
)
def sidebar_amount_type_callback(value):
    if value == 'fixed':
        return {'display': 'block'}, 'Enter fixed amount'
    else:
        return {'display': 'none'}, 'Enter % amount'

@app.callback(
    Output("sidebar-amount-input", "value", allow_duplicate=True),
    [Input("sidebar-amount-50", "n_clicks"), Input("sidebar-amount-100", "n_clicks"), Input("sidebar-amount-250", "n_clicks"), Input("sidebar-amount-500", "n_clicks"), Input("sidebar-amount-1000", "n_clicks"), Input("sidebar-amount-max", "n_clicks")],
    prevent_initial_call=True
)
def sidebar_quick_amount_callback(*btns):
    amounts = [50, 100, 250, 500, 1000, 'max']
    ctx_id = ctx.triggered_id if hasattr(ctx, 'triggered_id') else None
    if ctx_id:
        if ctx_id == 'sidebar-amount-max':
            idx = 5
        else:
            try:
                idx = ["sidebar-amount-50", "sidebar-amount-100", "sidebar-amount-250", "sidebar-amount-500", "sidebar-amount-1000"].index(ctx_id)
            except ValueError:
                return no_update
        if 0 <= idx < len(amounts):
            return amounts[idx]
    return no_update

@app.callback(
    [Output("sidebar-winrate", "children"), Output("sidebar-total-trades", "children"), Output("sidebar-daily-pnl", "children")],
    Input("performance-interval", "n_intervals")
)
def sidebar_performance_callback(n):
    return fetch_sidebar_performance(api_session)

@app.callback(
    Output("dummy-div", "children", allow_duplicate=True),
    [Input("sidebar-predict-btn", "n_clicks"), Input("sidebar-analytics-btn", "n_clicks")],
    [State("sidebar-symbol", "value")],
    prevent_initial_call=True
)
def sidebar_quick_action_callback(predict, analytics, symbol):
    ctx_id = ctx.triggered_id if hasattr(ctx, 'triggered_id') else None
    if ctx_id == "sidebar-predict-btn" and predict:
        return fetch_prediction(api_session, symbol)
    elif ctx_id == "sidebar-analytics-btn" and analytics:
        return fetch_analytics(api_session, symbol)
    return no_update

@app.callback(
    Output("dev-tools-collapse", "is_open"),
    Input("toggle-dev-tools", "n_clicks"),
    State("dev-tools-collapse", "is_open"),
    prevent_initial_call=True
)
def dev_tools_toggle_callback(n, is_open):
    return not is_open if n else is_open

# --- Sidebar/Section Toggle Callbacks ---
@app.callback(Output('hft-tools-collapse', 'is_open'), Input('toggle-hft-tools', 'n_clicks'), State('hft-tools-collapse', 'is_open'), prevent_initial_call=True)
def toggle_hft_tools_callback(n_clicks, is_open):
    return toggle_section(is_open)

@app.callback(Output('data-collection-collapse', 'is_open'), Input('toggle-data-collection', 'n_clicks'), State('data-collection-collapse', 'is_open'), prevent_initial_call=True)
def toggle_data_collection_callback(n_clicks, is_open):
    return toggle_section(is_open)

@app.callback(Output('online-learning-collapse', 'is_open'), Input('toggle-online-learning', 'n_clicks'), State('online-learning-collapse', 'is_open'), prevent_initial_call=True)
def toggle_online_learning_callback(n_clicks, is_open):
    return toggle_section(is_open)

@app.callback(Output('risk-management-collapse', 'is_open'), Input('toggle-risk-management', 'n_clicks'), State('risk-management-collapse', 'is_open'), prevent_initial_call=True)
def toggle_risk_management_callback(n_clicks, is_open):
    return toggle_section(is_open)

@app.callback(Output('notifications-collapse', 'is_open'), Input('toggle-notifications', 'n_clicks'), State('notifications-collapse', 'is_open'), prevent_initial_call=True)
def toggle_notifications_callback(n_clicks, is_open):
    return toggle_section(is_open)

@app.callback(Output('email-alerts-collapse', 'is_open'), Input('toggle-email-alerts', 'n_clicks'), State('email-alerts-collapse', 'is_open'), prevent_initial_call=True)
def toggle_email_alerts_callback(n_clicks, is_open):
    return toggle_section(is_open)

@app.callback(Output('analytics-collapse', 'is_open'), Input('toggle-analytics', 'n_clicks'), State('analytics-collapse', 'is_open'), prevent_initial_call=True)
def toggle_analytics_section_callback(n_clicks, is_open):
    return toggle_section(is_open)

@app.callback(Output('ml-tools-collapse', 'is_open'), Input('toggle-ml-tools', 'n_clicks'), State('ml-tools-collapse', 'is_open'), prevent_initial_call=True)
def toggle_ml_tools_section_callback(n_clicks, is_open):
    return toggle_section(is_open)

@app.callback(Output('charts-collapse', 'is_open'), Input('toggle-charts', 'n_clicks'), State('charts-collapse', 'is_open'), prevent_initial_call=True)
def toggle_charts_section_callback(n_clicks, is_open):
    return toggle_section(is_open)

# --- Step 3 Complete: Sidebar and quick action callbacks added ---
# Next step: Add analytics, trading, and notification callbacks.

# --- Step 4: Analytics, Trading, and Notification Callbacks ---

@app.callback(
    [Output('comprehensive-backtest-output', 'children'), Output('backtest-progress', 'value'), Output('backtest-progress', 'children')],
    [Input('run-comprehensive-backtest', 'n_clicks')],
    [State('backtest-start-date', 'date'), State('backtest-end-date', 'date'), State('backtest-symbol', 'value'), State('backtest-strategy', 'value')],
    prevent_initial_call=True
)
def run_comprehensive_backtest(n, start, end, symbol, strategy):
    return fetch_comprehensive_backtest(api_session, n, start, end, symbol, strategy)

# @app.callback(
#     [Output('model-retrain-status', 'children'), Output('retrain-progress', 'value'), Output('retrain-progress', 'children')],
#     [Input('start-model-retrain', 'n_clicks'), Input('retrain-status-refresh', 'n_clicks')],
#     prevent_initial_call=True
# )
# def model_retrain_callback(n1, n2):
#     return fetch_model_retrain(api_session, n1, n2)
#
# This callback is commented out to prevent duplicate output errors. Only the advanced manage_model_retraining_callback is active below.

@app.callback(
    [Output('notifications-display', 'children'), Output('notification-count', 'children')],
    [Input('notification-refresh-interval', 'n_intervals'), Input('refresh-notifications-btn', 'n_clicks'), Input('show-unread-only', 'value')],
    prevent_initial_call=True
)
def notifications_callback(n_intervals, refresh, show_unread):
    return fetch_notifications(api_session, show_unread)

@app.callback(
    Output('manual-notification-collapse', 'is_open'),
    Input('test-notification-btn', 'n_clicks'),
    State('manual-notification-collapse', 'is_open'),
    prevent_initial_call=True
)
def manual_notification_collapse_callback(n, is_open):
    return not is_open if n else is_open

@app.callback(
    Output('notification-send-status', 'children'),
    Input('send-manual-notification-btn', 'n_clicks'),
    [State('manual-notification-type', 'value'), State('manual-notification-message', 'value')],
    prevent_initial_call=True
)
def send_manual_notification_callback(n, notif_type, notif_msg):
    return send_manual_notification(api_session, n, notif_type, notif_msg)

@app.callback(
    Output('clear-notifications-status', 'children'),
    Input('clear-notifications-btn', 'n_clicks'),
    prevent_initial_call=True
)
def clear_notifications_callback(n):
    return clear_notifications(api_session, n)

@app.callback(
    Output({'type': 'delete-notification', 'index': ALL}, 'children'),
    Input({'type': 'delete-notification', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def delete_individual_notifications_callback(n_clicks_list):
    # Actual deletion handled by notification API; UI just updates
    return [no_update for _ in n_clicks_list]

# --- Notification Stats/History Callbacks ---
@app.callback(Output('notification-stats', 'children'), Input('notification-refresh-interval', 'n_intervals'), prevent_initial_call=True)
def update_notification_stats_callback(n_intervals):
    result = fetch_notification_stats(api_session)
    return str(result)

@app.callback(Output('alert-history-display', 'children'), [Input('alert-refresh-interval', 'n_intervals'), Input('clear-alert-history-btn', 'n_clicks')], prevent_initial_call=True)
def update_alert_history_callback(n_intervals, clear_clicks):
    result = fetch_alert_history(api_session)
    return str(result)

# --- Step 4 Complete: Analytics, trading, and notification callbacks added ---
# Next step: Add trading controls, balance, and chart callbacks.

# --- Step 5: Trading Controls, Balance, and Chart Callbacks ---

# The following callback is commented out because it references non-existent component IDs (open-futures-position, close-futures-position, update-futures-positions)
# @app.callback(
#     [Output('futures-trading-controls', 'children'), Output('futures-trading-status', 'children')],
#     [Input('open-futures-position', 'n_clicks'), Input('close-futures-position', 'n_clicks'), Input('update-futures-positions', 'n_clicks'), Input('sidebar-symbol', 'value')],
#     [State('futures-side-select', 'value'), State('futures-quantity-input', 'value'), State('futures-leverage-input', 'value')],
#     prevent_initial_call=True
# )
# def futures_trading_controls_callback(open_n, close_n, update_n, symbol, side, qty, leverage):
#     return fetch_futures_trading_controls(api_session, open_n, close_n, update_n, symbol, side, qty, leverage)

@app.callback(
    [Output('futures-virtual-balance', 'children'), Output('futures-pnl-display', 'children'), Output('futures-virtual-total-balance', 'children'), Output('futures-available-balance', 'children')],
    [Input('live-price-interval', 'n_intervals'), Input('futures-sync-balance-btn', 'n_clicks'), Input('sidebar-symbol', 'value')],
    prevent_initial_call=True
)
def futures_virtual_balance_callback(n, sync, symbol):
    # Pass symbol to backend if needed, else ignore
    return fetch_futures_balance(api_session)

@app.callback(
    Output('price-chart', 'figure'),
    [Input('live-price-interval', 'n_intervals'), Input('sidebar-symbol', 'value')]
)
def price_chart_callback(n, symbol):
    result = fetch_chart(api_session, 'price', symbol)
    if not isinstance(result, go.Figure):
        return create_empty_figure("No Data Available")
    return result

# --- Technical Indicators Chart Callback ---
@app.callback(
    Output('indicators-chart', 'figure'),
    [Input('interval-indicators', 'n_intervals'),
     Input('sidebar-symbol', 'value')]
)
def update_indicators_chart(n_intervals, symbol):
    """Update technical indicators chart using helper."""
    api_session = create_session_with_retries()
    result = fetch_technical_indicators(api_session, symbol)
    if not isinstance(result, go.Figure):
        return create_empty_figure("No Data Available")
    return result

# --- Advanced Analytics Example Callback (modular, no name conflict) ---
@app.callback(
    Output('model-analytics-display', 'children'),
    [Input('refresh-model-analytics', 'n_clicks')]
)
def update_model_analytics_modular(n_clicks):
    """Update model analytics and performance metrics with helper."""
    api_session = create_session_with_retries()
    analytics = fetch_advanced_analytics(api_session, 'ml/analytics/comprehensive')
    if 'error' in analytics:
        return html.Div(f"Error: {analytics['error']}")
    performance = analytics.get('performance', {})
    if not isinstance(performance, dict):
        return html.Div(f"Error: {performance}")
    return html.Div([
        html.H4("Model Analytics"),
        html.P(f"Accuracy: {performance.get('accuracy', 0):.2%}"),
        html.P(f"Precision: {performance.get('precision', 0):.2%}"),
        html.P(f"Recall: {performance.get('recall', 0):.2%}")
    ])

# --- Utility/Maintenance Callbacks (modularized) ---
@app.callback(
    [Output('risk-settings-display', 'children'), Output('risk-settings-status', 'children')],
    [Input('save-risk-settings', 'n_clicks'), Input('load-risk-settings', 'n_clicks')],
    [State('max-drawdown-input', 'value'), State('position-size-input', 'value'), State('stop-loss-pct-input', 'value'), State('take-profit-pct-input', 'value')],
    prevent_initial_call=True
)
def manage_risk_settings_callback(save_clicks, load_clicks, max_drawdown, position_size, stop_loss, take_profit):
    return manage_risk_settings(api_session, save_clicks, load_clicks, max_drawdown, position_size, stop_loss, take_profit)

@app.callback(
    Output('test-db-btn-output', 'children'),
    Input('test-db-btn', 'n_clicks'),
    prevent_initial_call=True
)
def test_db_btn_callback(n):
    return test_database_connection(api_session, n)

@app.callback(
    Output('test-ml-btn-output', 'children'),
    Input('test-ml-btn', 'n_clicks'),
    prevent_initial_call=True
)
def test_ml_btn_callback(n):
    return test_ml_system(api_session, n)

@app.callback(
    Output('show-fi-btn-output', 'children'),
    Input('show-fi-btn', 'n_clicks'),
    prevent_initial_call=True
)
def show_fi_btn_callback(n):
    return show_feature_importance(api_session, n)

@app.callback(
    Output('prune-trades-btn-output', 'children'),
    Input('prune-trades-btn', 'n_clicks'),
    prevent_initial_call=True
)
def prune_trades_btn_callback(n):
    return prune_trades(api_session, n)

@app.callback(
    Output('tune-models-btn-output', 'children'),
    Input('tune-models-btn', 'n_clicks'),
    prevent_initial_call=True
)
def tune_models_btn_callback(n):
    return tune_models(api_session, n)

@app.callback(
    Output('check-drift-btn-output', 'children'),
    Input('check-drift-btn', 'n_clicks'),
    prevent_initial_call=True
)
def check_drift_btn_callback(n):
    return check_drift(api_session, n)

@app.callback(
    Output('online-learn-btn-output', 'children'),
    Input('online-learn-btn', 'n_clicks'),
    prevent_initial_call=True
)
def online_learn_btn_callback(n):
    return online_learn(api_session, n)

@app.callback(
    Output('refresh-model-versions-btn-output', 'children'),
    Input('refresh-model-versions-btn', 'n_clicks'),
    prevent_initial_call=True
)
def refresh_model_versions_btn_callback(n):
    return refresh_model_versions(api_session, n)

# --- Transfer Learning Management Callbacks ---
@app.callback(
    [Output('transfer-learning-setup', 'children'), Output('transfer-learning-training', 'children')],
    [Input('check-transfer-setup', 'n_clicks'), Input('init-transfer-learning', 'n_clicks'), Input('train-target-model', 'n_clicks')],
    [State('source-pairs-input', 'value'), State('target-pair-input', 'value'), State('training-candles-input', 'value')],
    prevent_initial_call=True
)
def manage_transfer_learning_callback(setup_clicks, init_clicks, train_clicks, source_pairs, target_pair, candles):
    ctx = callback_context
    if not ctx.triggered:
        return "", ""
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered_id == 'check-transfer-setup':
        result = manage_transfer_learning(api_session, 'check_setup')
        return str(result), ""
    elif triggered_id == 'init-transfer-learning' and init_clicks:
        result = manage_transfer_learning(api_session, 'init', source_pairs=source_pairs, target_pair=target_pair, candles=candles)
        return "", str(result)
    elif triggered_id == 'train-target-model' and train_clicks:
        result = manage_transfer_learning(api_session, 'train_target')
        return "", str(result)
    return "", ""

@app.callback(Output('transfer-learning-performance', 'children'), Input('refresh-transfer-performance', 'n_clicks'), prevent_initial_call=True)
def update_transfer_performance_callback(n_clicks):
    result = manage_transfer_learning(api_session, 'performance')
    return str(result)

# --- Model Version/History/Metrics Callbacks ---
@app.callback(
    [Output('model-versions-display', 'children'), Output('model-version-status', 'children')],
    [Input('refresh-model-versions', 'n_clicks'), Input('activate-model-version', 'n_clicks')],
    [State('model-version-select', 'value')],
    prevent_initial_call=True
)
def manage_model_versions_callback(refresh_clicks, activate_clicks, selected_version):
    ctx = callback_context
    if not ctx.triggered:
        return "", ""
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered_id == 'activate-model-version' and activate_clicks:
        result = manage_model_versions(api_session, 'activate', version=selected_version)
        return "", str(result)
    else:
        versions = manage_model_versions(api_session, 'list')
        active = manage_model_versions(api_session, 'active')
        return str(versions), str(active)

@app.callback(Output('model-metrics-display', 'children'), Input('refresh-model-metrics', 'n_clicks'), prevent_initial_call=True)
def update_model_metrics_callback(n_clicks):
    result = fetch_model_metrics(api_session)
    return str(result)

@app.callback(Output('ml-performance-history', 'children'), Input('refresh-ml-history', 'n_clicks'), prevent_initial_call=True)
def update_ml_performance_history_callback(n_clicks):
    result = fetch_ml_performance_history(api_session)
    return str(result)

@app.callback(Output('backtest-results-enhanced', 'children'), Input('load-backtest-results', 'n_clicks'), prevent_initial_call=True)
def load_backtest_results_callback(n_clicks):
    result = fetch_backtest_results(api_session)
    return str(result)

@app.callback(
    [Output('model-retrain-status', 'children'), Output('retrain-progress', 'value'), Output('retrain-progress', 'children')],
    [Input('start-model-retrain', 'n_clicks'), Input('retrain-status-refresh', 'n_clicks')],
    prevent_initial_call=True
)
def manage_model_retraining_callback(start_clicks, refresh_clicks):
    ctx = callback_context
    if not ctx.triggered:
        return "", 0, ""
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered_id == 'start-model-retrain' and start_clicks:
        result = manage_model_retraining(api_session, 'start')
        return str(result), 10, "Started"
    else:
        result = manage_model_retraining(api_session, 'status')
        return str(result), 50, "Status"

# --- Data Collection Callbacks ---
@app.callback(
    [Output('data-collection-status', 'children'), Output('data-collection-controls', 'children')],
    [Input('start-data-collection-btn', 'n_clicks'), Input('stop-data-collection-btn', 'n_clicks'), Input('check-data-collection-btn', 'n_clicks')],
    prevent_initial_call=True
)
def manage_data_collection_callback(start_clicks, stop_clicks, check_clicks):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    if triggered_id == 'start-data-collection-btn':
        result = manage_data_collection(api_session, 'start')
        return str(result), "Started"
    elif triggered_id == 'stop-data-collection-btn':
        result = manage_data_collection(api_session, 'stop')
        return str(result), "Stopped"
    elif triggered_id == 'check-data-collection-btn':
        result = manage_data_collection(api_session, 'check')
        return str(result), "Checked"
    return "", ""

# --- Email/Alert System Callbacks ---
@app.callback(
    [Output('email-config-status', 'children'), Output('email-enabled-switch', 'value')],
    [Input('save-email-config-btn', 'n_clicks'), Input('email-config-refresh-interval', 'n_intervals')],
    [State('smtp-server-input', 'value'), State('smtp-port-input', 'value'), State('email-address-input', 'value'), State('email-password-input', 'value'), State('email-enabled-switch', 'value')],
    prevent_initial_call=True
)
def manage_email_config_callback(save_clicks, refresh_intervals, smtp_server, smtp_port, email, password, enabled):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    if triggered_id == 'save-email-config-btn':
        result = manage_email_config(api_session, 'save', smtp_server=smtp_server, smtp_port=smtp_port, email=email, password=password, enabled=enabled)
        return str(result), enabled
    else:
        result = manage_email_config(api_session, 'refresh')
        return str(result), enabled

@app.callback(Output('email-test-result', 'children'), Input('test-email-btn', 'n_clicks'), prevent_initial_call=True)
def test_email_connection_callback(n_clicks):
    result = manage_email_config(api_session, 'test')
    return str(result)

@app.callback(Output('alert-test-result', 'children'), Input('send-test-alert-btn', 'n_clicks'), prevent_initial_call=True)
def send_test_alert_callback(n_clicks):
    return send_test_alert(api_session, n_clicks)

@app.callback(Output('check-auto-alerts-result', 'children'), Input('check-auto-alerts-btn', 'n_clicks'), prevent_initial_call=True)
def check_auto_alerts_callback(n_clicks):
    return check_auto_alerts(api_session, n_clicks)

# --- HFT Analysis Callbacks ---
@app.callback(
    [Output('hft-analysis-display', 'children'), Output('hft-stats-cards', 'children')],
    [Input('run-hft-analysis-btn', 'n_clicks'), Input('hft-refresh-interval', 'n_intervals')],
    [State('hft-symbol-input', 'value'), State('hft-timeframe-dropdown', 'value')],
    prevent_initial_call=True
)
def update_hft_analysis_callback(run_clicks, refresh_intervals, symbol, timeframe):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    if triggered_id == 'run-hft-analysis-btn':
        result = manage_hft_analysis(api_session, 'run', symbol=symbol, timeframe=timeframe)
        return str(result), "Run"
    else:
        result = manage_hft_analysis(api_session, 'refresh', symbol=symbol, timeframe=timeframe)
        return str(result), "Refreshed"

# --- Online Learning System Callbacks ---
@app.callback(
    [Output('online-learning-status', 'children'), Output('online-learning-controls', 'children')],
    [Input('start-online-learning-btn', 'n_clicks'), Input('stop-online-learning-btn', 'n_clicks'), Input('reset-online-learning-btn', 'n_clicks'), Input('check-online-learning-btn', 'n_clicks')],
    [State('online-learning-mode-dropdown', 'value'), State('online-learning-buffer-size', 'value'), State('online-learning-update-frequency', 'value')],
    prevent_initial_call=True
)
def manage_online_learning_system_callback(start_clicks, stop_clicks, reset_clicks, check_clicks, mode, buffer_size, update_freq):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    if triggered_id == 'start-online-learning-btn':
        result = manage_online_learning(api_session, 'start', mode=mode, buffer_size=buffer_size, update_freq=update_freq)
        return str(result), "Started"
    elif triggered_id == 'stop-online-learning-btn':
        result = manage_online_learning(api_session, 'stop')
        return str(result), "Stopped"
    elif triggered_id == 'reset-online-learning-btn':
        result = manage_online_learning(api_session, 'reset')
        return str(result), "Reset"
    elif triggered_id == 'check-online-learning-btn':
        result = manage_online_learning(api_session, 'check')
        return str(result), "Checked"
    return "", ""

@app.callback(Output('online-learning-stats', 'children'), Input('online-learning-refresh-interval', 'n_intervals'), prevent_initial_call=True)
def update_online_learning_stats_callback(n_intervals):
    result = manage_online_learning(api_session, 'stats')
    return str(result)

# --- Advanced Technical Indicators (Futures) Callbacks ---
@app.callback(Output('futures-rsi-indicator', 'children'), [Input('futures-refresh-interval', 'n_intervals'), Input('sidebar-symbol', 'value')], prevent_initial_call=True)
def update_futures_rsi_indicator_callback(n_intervals, symbol):
    result = fetch_futures_indicator(api_session, 'rsi', symbol)
    return str(result)

@app.callback(Output('futures-macd-indicator', 'children'), [Input('futures-refresh-interval', 'n_intervals'), Input('sidebar-symbol', 'value')], prevent_initial_call=True)
def update_futures_macd_indicator_callback(n_intervals, symbol):
    result = fetch_futures_indicator(api_session, 'macd', symbol)
    return str(result)

@app.callback(Output('futures-bollinger-indicator', 'children'), [Input('futures-refresh-interval', 'n_intervals'), Input('sidebar-symbol', 'value')], prevent_initial_call=True)
def update_futures_bollinger_indicator_callback(n_intervals, symbol):
    result = fetch_futures_indicator(api_session, 'bollinger', symbol)
    return str(result)

@app.callback(Output('futures-stochastic-indicator', 'children'), [Input('futures-refresh-interval', 'n_intervals'), Input('sidebar-symbol', 'value')], prevent_initial_call=True)
def update_futures_stochastic_indicator_callback(n_intervals, symbol):
    result = fetch_futures_indicator(api_session, 'stochastic', symbol)
    return str(result)

@app.callback(Output('futures-volume-indicator', 'children'), [Input('futures-refresh-interval', 'n_intervals'), Input('sidebar-symbol', 'value')], prevent_initial_call=True)
def update_futures_volume_indicator_callback(n_intervals, symbol):
    result = fetch_futures_indicator(api_session, 'volume', symbol)
    return str(result)

@app.callback(Output('futures-atr-indicator', 'children'), [Input('futures-refresh-interval', 'n_intervals'), Input('sidebar-symbol', 'value')], prevent_initial_call=True)
def update_futures_atr_indicator_callback(n_intervals, symbol):
    result = fetch_futures_indicator(api_session, 'atr', symbol)
    return str(result)

@app.callback(Output('futures-technical-chart', 'figure'), [Input('futures-refresh-interval', 'n_intervals'), Input('sidebar-symbol', 'value')], prevent_initial_call=True)
def update_futures_technical_chart_callback(n_intervals, symbol):
    result = fetch_futures_indicator(api_session, 'technical_chart', symbol)
    if not isinstance(result, go.Figure):
        return create_empty_figure("No Data Available")
    return result

# --- Sidebar Technical Indicators/ML Tools Callbacks ---
@app.callback([Output('sidebar-rsi-value', 'children'), Output('sidebar-rsi-signal', 'children')], [Input('live-price-interval', 'n_intervals'), Input('sidebar-symbol', 'value')], prevent_initial_call=True)
def update_sidebar_rsi_callback(n_intervals, symbol):
    result = fetch_sidebar_indicator(api_session, 'rsi', symbol)
    return str(result.get('value', '')), str(result.get('signal', ''))

@app.callback([Output('sidebar-macd-value', 'children'), Output('sidebar-macd-signal', 'children')], [Input('live-price-interval', 'n_intervals'), Input('sidebar-symbol', 'value')], prevent_initial_call=True)
def update_sidebar_macd_callback(n_intervals, symbol):
    result = fetch_sidebar_indicator(api_session, 'macd', symbol)
    return str(result.get('value', '')), str(result.get('signal', ''))

@app.callback([Output('sidebar-bb-upper', 'children'), Output('sidebar-bb-middle', 'children'), Output('sidebar-bb-lower', 'children'), Output('sidebar-bb-signal', 'children')], [Input('live-price-interval', 'n_intervals'), Input('sidebar-symbol', 'value')], prevent_initial_call=True)
def update_sidebar_bollinger_callback(n_intervals, symbol):
    result = fetch_sidebar_indicator(api_session, 'bollinger', symbol)
    return str(result.get('upper', '')), str(result.get('middle', '')), str(result.get('lower', '')), str(result.get('signal', ''))

@app.callback([Output('sidebar-model-accuracy', 'children'), Output('sidebar-model-confidence', 'children'), Output('sidebar-model-status', 'children')], [Input('live-price-interval', 'n_intervals')], prevent_initial_call=True)
def update_sidebar_ml_tools_callback(n_intervals):
    result = fetch_sidebar_ml_tools(api_session)
    return str(result.get('accuracy', '')), str(result.get('confidence', '')), str(result.get('status', ''))

# --- Fix for input/output component mismatches ---
# The following IDs must be changed in layout.py to use the correct Dash components:
# - show-unread-only: dcc.Checklist or dcc.Switch (for boolean), or dcc.Input(type='text') if text
# - email-password-input: dcc.Input(type='password')
# - email-address-input: dcc.Input(type='email')
# - smtp-port-input: dcc.Input(type='number')
# - smtp-server-input: dcc.Input(type='text')
# - manual-notification-message: dcc.Textarea or dcc.Input(type='text')
# - manual-notification-type: dcc.Dropdown or dcc.Input(type='text')
# - futures-technical-chart: dcc.Graph
#
# Please update your layout.py as follows:
#
# Replace:
# html.Div(id="show-unread-only", style={"display": "none"}),
# html.Div(id="email-password-input", style={"display": "none"}),
# html.Div(id="email-address-input", style={"display": "none"}),
# html.Div(id="smtp-port-input", style={"display": "none"}),
# html.Div(id="smtp-server-input", style={"display": "none"}),
# html.Div(id="manual-notification-message", style={"display": "none"}),
# html.Div(id="manual-notification-type", style={"display": "none"}),
# html.Div(id="futures-technical-chart", style={"display": "none"}),
#
# With:
# dcc.Checklist(id="show-unread-only", options=[{"label": "Show Unread Only", "value": "unread"}], value=[]),
# dcc.Input(id="email-password-input", type="password"),
# dcc.Input(id="email-address-input", type="email"),
# dcc.Input(id="smtp-port-input", type="number"),
# dcc.Input(id="smtp-server-input", type="text"),
# dcc.Textarea(id="manual-notification-message"),
# dcc.Input(id="manual-notification-type", type="text"),
# dcc.Graph(id="futures-technical-chart"),
#
# This will resolve all callback property errors and allow your dashboard features to work.

# --- Step 6: Auto Trading Controls and Outputs Callbacks ---
# These callbacks wire up the auto trading controls and outputs to the backend helpers in dashboard_utils.py

@app.callback(
    [Output('auto-trading-status', 'children'), Output('auto-trading-toggle', 'value')],
    [Input('auto-trading-interval', 'n_intervals'), Input('auto-trading-toggle', 'value')],
    prevent_initial_call=True
)
def update_auto_trading_status(n_intervals, toggle_value):
    """Fetch and display the current auto trading status and toggle state."""
    from dashboard_utils import fetch_auto_trading_status
    status, enabled = fetch_auto_trading_status(api_session)
    # If user toggled, update backend (not just polling)
    if ctx.triggered_id == 'auto-trading-toggle' and toggle_value is not None:
        from dashboard_utils import execute_auto_trading
        execute_auto_trading(api_session, toggle_value)
        status, enabled = fetch_auto_trading_status(api_session)
    return status, enabled

@app.callback(
    Output('auto-trading-execute-status', 'children'),
    Input('auto-trading-execute-btn', 'n_clicks'),
    prevent_initial_call=True
)
def execute_auto_trading_callback(n_clicks):
    """Manually execute auto trading and show result."""
    if not n_clicks:
        return no_update
    from dashboard_utils import execute_auto_trading
    result = execute_auto_trading(api_session, True)
    return result

@app.callback(
    Output('current-signal-box', 'children'),
    [Input('auto-trading-interval', 'n_intervals'), Input('sidebar-symbol', 'value')],
    prevent_initial_call=True
)
def update_current_signal(n_intervals, symbol):
    """Fetch and display the current trading signal for the selected symbol."""
    from dashboard_utils import fetch_prediction
    signal = fetch_prediction(api_session, symbol)
    return signal

# --- Step 6 Complete: Auto trading controls and outputs wired up ---
# All auto trading features should now update and execute as expected.

# --- Sidebar and Tab Virtual Balance Callbacks ---
# Example: Update sidebar virtual balance display
# (You should add similar callbacks for all places where the virtual balance is shown)
from dash.dependencies import Input, Output

@app.callback(
    [Output('sidebar-virtual-balance', 'children'), Output('virtual-balance-display', 'children')],
    [Input('interval-indicators', 'n_intervals'),  # refresh every 30s
     Input('trade-executed', 'data'),              # custom: fires after trade
     Input('virtual-balance-refresh', 'n_intervals')],  # optional: manual refresh
    prevent_initial_call=True
)
def update_sidebar_virtual_balance(n_intervals, trade_data, manual_refresh):
    # Always fetch the latest virtual balance from backend
    balance = fetch_virtual_balance(api_session)
    return balance, balance

# --- Note ---
# - Make sure every tab or section that displays the virtual balance uses fetch_virtual_balance in its callback.
# - After any trade or balance-changing action, trigger a refresh (e.g., via a Store, Interval, or custom Input).
# - Remove any old or duplicate balance-fetching logic.
# - If you have multiple places showing the balance, add similar callbacks for each Output.
