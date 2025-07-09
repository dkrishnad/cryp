# Refactored callbacks.py
# This file will be built up step by step to integrate duplicate callbacks and reduce code size.

print('>>> refactored_callbacks.py imported and executing')

import dash
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash import html, ctx, callback_context, dash_table, no_update, dcc
import json
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import asyncio
import aiohttp
from aiohttp import ClientTimeout

# Handle both direct execution and module import
try:
    from .dash_app import app
    print("[DEBUG] Using relative import for app")
except ImportError:
    try:
        from dash_app import app
        print("[DEBUG] Using absolute import for app")
    except ImportError:
        print("[WARNING] Could not import app, creating fallback")
        app = dash.Dash(__name__)
        print("[DEBUG] Created fallback dash app instance")

# Create a session with retry strategy
def create_session_with_retries():
    """Create requests session with automatic retry logic"""
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

# Global session for reuse
api_session = create_session_with_retries()
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
# Duplicate callback removed - better API-based version exists at line 2655
# Duplicate callback removed - better API-based version exists at line 2656

# Utility imports and callback registration for hybrid learning and email config
try:
    from .utils import (
        fetch_ml_prediction, fetch_notifications, open_trade, fetch_backtests, run_backtest, fetch_analytics, fetch_trades,
        mark_notification_read, delete_notification, fetch_model_metrics, fetch_feature_importance, fetch_portfolio_analytics,
        safety_check, close_trade, cancel_trade, activate_trade, fetch_model_logs, fetch_model_errors, fetch_system_status
    )
except ImportError:
    from utils import (
        fetch_ml_prediction, fetch_notifications, open_trade, fetch_backtests, run_backtest, fetch_analytics, fetch_trades,
        mark_notification_read, delete_notification, fetch_model_metrics, fetch_feature_importance, fetch_portfolio_analytics,
        safety_check, close_trade, cancel_trade, activate_trade, fetch_model_logs, fetch_model_errors, fetch_system_status
    )

try:
    from .hybrid_learning_layout import create_hybrid_learning_layout, register_hybrid_learning_callbacks
    from .email_config_layout import create_email_config_layout, register_email_config_callbacks
except ImportError:
    from hybrid_learning_layout import create_hybrid_learning_layout, register_hybrid_learning_callbacks
    from email_config_layout import create_email_config_layout, register_email_config_callbacks

try:
    register_hybrid_learning_callbacks(app)
    print("[OK] Hybrid learning callbacks registered")
    register_email_config_callbacks(app)
    print("[OK] Email configuration callbacks registered")
    # ...additional tab callback imports and registration...
except Exception as e:
    print(f"WARNING: Could not register dashboard tab callbacks: {e}")

# --- ASYNC UTILS ---

# Async session for API calls
async def async_api_get(url, params=None, timeout=10):
    timeout_obj = ClientTimeout(total=timeout)
    async with aiohttp.ClientSession(timeout=timeout_obj) as session:
        try:
            async with session.get(url, params=params) as resp:
                resp.raise_for_status()
                return await resp.json()
        except Exception as e:
            return {"error": str(e)}

# --- Callback for API health check ---
@app.callback(
    Output("api-status", "children"),
    Input("url", "href"),
    prevent_initial_call=True
)
def check_api_health(url):
    """Check API health and update status indicator (async)"""
    if not url:
        raise dash.exceptions.PreventUpdate
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(async_api_get(f"{API_URL}/health"))
    if "error" in result:
        return f"API Status: Error - {result['error']}"
    status = result.get("status", "unknown")
    return f"API Status: {status}"

# --- Layout and InitialCallbacks Registration ---
# Layouts for different tabs will be registered here as they are defined
# Initial layout set to loading spinner
app.layout = html.Div([
    dcc.Loading(
        id="loading",
        type="default",
        children=[html.Div(id="page-content")]
    )
])

# --- Fallback for missing callbacks ---
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    prevent_initial_call=True
)
def display_page(pathname):
    """Fallback callback to display an error message for missing pages"""
    return html.Div([
        html.H3("404 - Page Not Found", className="text-danger"),
        html.P("The page you are looking for does not exist.", className="text-muted"),
        dcc.Link("Go to Home", href="/", className="btn btn-primary")
    ])

# --- Generic Tab Content Rendering Callback ---
@app.callback(
    Output({'type': 'tab-content', 'tab': MATCH}, 'children'),
    Input({'type': 'tab-content', 'tab': MATCH}, 'id')
)
def render_tab_content(tab_id):
    """Generic callback to render tab content based on tab id"""
    tab_map = {
        'hybrid-learning-tab-content': create_hybrid_learning_layout,
        'email-config-tab-content': create_email_config_layout,
        'auto-trading-tab-content': lambda: html.Div([html.H4("Auto Trading Tab Content")]),
        'futures-trading-tab-content': lambda: html.Div([html.H4("Futures Trading Tab Content")]),
        'binance-exact-tab-content': lambda: html.Div([html.H4("Binance-Exact API Tab Content")]),
    }
    try:
        if tab_id in tab_map:
            return tab_map[tab_id]()
        else:
            return html.Div([
                html.H5("Unknown Tab", style={"color": "red"}),
                html.P(f"Tab id '{tab_id}' not recognized.")
            ])
    except Exception as e:
        return html.Div([
            html.H5("Error loading tab content", style={"color": "red"}),
            html.P(str(e))
        ])

# --- Generic Status Update Callback ---
@app.callback(
    Output({'type': 'status-display', 'section': MATCH}, 'children'),
    Input({'type': 'status-refresh', 'section': MATCH}, 'n_clicks')
)
def generic_status_update(n_clicks, section):
    """Generic callback to update status for any section (async)"""
    async def get_status(section):
        # Map section to endpoint
        endpoint_map = {
            'hybrid': f"{API_URL}/hybrid/status",
            'transfer-learning': f"{API_URL}/transfer_learning/status",
            # Add more as needed
        }
        url = endpoint_map.get(section)
        if not url:
            return html.Div([
                html.H5("Unknown Status Section", style={"color": "red"}),
                html.P(f"Section '{section}' not recognized.")
            ])
        result = await async_api_get(url)
        if "error" in result:
            return html.Div([
                html.H5("Error updating status", style={"color": "red"}),
                html.P(result["error"])
            ])
        return html.Div([html.P(f"{section.replace('-', ' ').title()} status: {result.get('status', 'unknown')}")])
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(get_status(section))

# --- Transfer Learning Status Callback ---
@app.callback(
    Output('transfer-learning-status', 'children'),
    [Input('check-transfer-status', 'n_clicks')]
)
def update_transfer_status(n_clicks):
    """Update transfer learning system status (async)"""
    async def get_transfer_status():
        url = f"{API_URL}/transfer_learning/status"
        result = await async_api_get(url)
        if "error" in result:
            return html.Div([
                html.H5("Error updating transfer learning status", style={"color": "red"}),
                html.P(result["error"])
            ])
        return html.Div([
            html.P(f"Transfer learning status: {result.get('status', 'unknown')}")
        ])
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(get_transfer_status())

# --- Generic Async Action Button Callback ---
@app.callback(
    Output({'type': 'action-output', 'action': MATCH}, 'children'),
    Input({'type': 'action-button', 'action': MATCH}, 'n_clicks'),
    State({'type': 'action-button', 'action': MATCH}, 'action'),
    prevent_initial_call=True
)
def generic_action_button_callback(n_clicks, action):
    """Generic async callback for action buttons (start/stop/toggle/analytics, etc.)"""
    async def perform_action(action):
        # Map action to endpoint
        endpoint_map = {
            'start-trading': f"{API_URL}/trading/start",
            'stop-trading': f"{API_URL}/trading/stop",
            'toggle-feature': f"{API_URL}/feature/toggle",
            'run-analytics': f"{API_URL}/analytics/run",
            # Add more actions as needed
        }
        url = endpoint_map.get(action)
        if not url:
            return html.Div([
                html.H5("Unknown Action", style={"color": "red"}),
                html.P(f"Action '{action}' not recognized.")
            ])
        try:
            timeout_obj = ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return html.Div([
                html.H5("Error performing action", style={"color": "red"}),
                html.P(str(e))
            ])
        return html.Div([
            html.P(f"Action '{action}' result: {result.get('message', 'Success')}")
        ])
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(perform_action(action))

# --- Generic Async Toggle Switch Callback ---
@app.callback(
    Output({'type': 'toggle-output', 'feature': MATCH}, 'children'),
    Input({'type': 'toggle-switch', 'feature': MATCH}, 'value'),
    State({'type': 'toggle-switch', 'feature': MATCH}, 'feature'),
    prevent_initial_call=True
)
def generic_toggle_switch_callback(value, feature):
    """Generic async callback for toggle switches (enable/disable features, etc.)"""
    async def perform_toggle(feature, value):
        # Map feature to endpoint
        endpoint_map = {
            'auto-trading': f"{API_URL}/feature/auto_trading",
            'notifications': f"{API_URL}/feature/notifications",
            'ml-mode': f"{API_URL}/feature/ml_mode",
            # Add more features as needed
        }
        url = endpoint_map.get(feature)
        if not url:
            return html.Div([
                html.H5("Unknown Feature", style={"color": "red"}),
                html.P(f"Feature '{feature}' not recognized.")
            ])
        try:
            timeout_obj = ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url, json={"enabled": value}) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return html.Div([
                html.H5("Error updating feature", style={"color": "red"}),
                html.P(str(e))
            ])
        return html.Div([
            html.P(f"Feature '{feature}' set to: {'Enabled' if value else 'Disabled'} ({result.get('message', 'Success')})")
        ])
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(perform_toggle(feature, value))

# --- Generic Async Analytics/Report Generation Callback ---
@app.callback(
    Output({'type': 'analytics-output', 'report': MATCH}, 'children'),
    Input({'type': 'analytics-button', 'report': MATCH}, 'n_clicks'),
    State({'type': 'analytics-button', 'report': MATCH}, 'report'),
    prevent_initial_call=True
)
def generic_analytics_callback(n_clicks, report):
    """Generic async callback for analytics/report generation buttons"""
    async def run_analytics(report):
        # Map report to endpoint
        endpoint_map = {
            'performance': f"{API_URL}/analytics/performance",
            'backtest': f"{API_URL}/analytics/backtest",
            'portfolio': f"{API_URL}/analytics/portfolio",
            # Add more reports as needed
        }
        url = endpoint_map.get(report)
        if not url:
            return html.Div([
                html.H5("Unknown Report", style={"color": "red"}),
                html.P(f"Report '{report}' not recognized.")
            ])
        try:
            timeout_obj = ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return html.Div([
                html.H5("Error generating report", style={"color": "red"}),
                html.P(str(e))
            ])
        return html.Div([
            html.P(f"Report '{report}' generated: {result.get('message', 'Success')}")
        ])
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(run_analytics(report))

# --- Generic Async Notification Action Callback ---
@app.callback(
    Output({'type': 'notification-output', 'notif_id': MATCH}, 'children'),
    Input({'type': 'notification-action', 'notif_id': MATCH, 'action': MATCH}, 'n_clicks'),
    State({'type': 'notification-action', 'notif_id': MATCH, 'action': MATCH}, 'notif_id'),
    State({'type': 'notification-action', 'notif_id': MATCH, 'action': MATCH}, 'action'),
    prevent_initial_call=True
)
def generic_notification_action_callback(n_clicks, notif_id, action):
    """Generic async callback for notification actions (mark as read, delete, etc.)"""
    async def perform_notification_action(notif_id, action):
        # Map action to endpoint and HTTP method
        endpoint_map = {
            'mark-read': (f"{API_URL}/notifications/{notif_id}/read", 'POST'),
            'delete': (f"{API_URL}/notifications/{notif_id}", 'DELETE'),
            # Add more actions as needed
        }
        endpoint = endpoint_map.get(action)
        if not endpoint:
            return html.Div([
                html.H5("Unknown Notification Action", style={"color": "red"}),
                html.P(f"Action '{action}' not recognized.")
            ])
        url, method = endpoint
        try:
            timeout_obj = ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                if method == 'POST':
                    async with session.post(url) as resp:
                        resp.raise_for_status()
                        result = await resp.json()
                elif method == 'DELETE':
                    async with session.delete(url) as resp:
                        resp.raise_for_status()
                        result = await resp.json()
                else:
                    return html.Div([
                        html.H5("Unsupported HTTP Method", style={"color": "red"}),
                        html.P(f"Method '{method}' not supported.")
                    ])
        except Exception as e:
            return html.Div([
                html.H5("Error performing notification action", style={"color": "red"}),
                html.P(str(e))
            ])
        return html.Div([
            html.P(f"Notification '{notif_id}' action '{action}': {result.get('message', 'Success')}")
        ])
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(perform_notification_action(notif_id, action))

# --- Generic Async Trade Management Callback ---
@app.callback(
    Output({'type': 'trade-output', 'trade_id': MATCH}, 'children'),
    Input({'type': 'trade-action', 'trade_id': MATCH, 'action': MATCH}, 'n_clicks'),
    State({'type': 'trade-action', 'trade_id': MATCH, 'action': MATCH}, 'trade_id'),
    State({'type': 'trade-action', 'trade_id': MATCH, 'action': MATCH}, 'action'),
    prevent_initial_call=True
)
def generic_trade_action_callback(n_clicks, trade_id, action):
    """Generic async callback for trade management actions (open, close, activate, cancel, etc.)"""
    async def perform_trade_action(trade_id, action):
        # Map action to endpoint
        endpoint_map = {
            'open': f"{API_URL}/trades/{trade_id}/open",
            'close': f"{API_URL}/trades/{trade_id}/close",
            'activate': f"{API_URL}/trades/{trade_id}/activate",
            'cancel': f"{API_URL}/trades/{trade_id}/cancel",
            # Add more actions as needed
        }
        url = endpoint_map.get(action)
        if not url:
            return html.Div([
                html.H5("Unknown Trade Action", style={"color": "red"}),
                html.P(f"Action '{action}' not recognized.")
            ])
        try:
            timeout_obj = ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return html.Div([
                html.H5("Error performing trade action", style={"color": "red"}),
                html.P(str(e))
            ])
        return html.Div([
            html.P(f"Trade '{trade_id}' action '{action}': {result.get('message', 'Success')}")
        ])
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(perform_trade_action(trade_id, action))

# --- Generic Async Data Collection/Synchronization Callback ---
@app.callback(
    Output({'type': 'data-output', 'dataset': MATCH}, 'children'),
    Input({'type': 'data-action', 'dataset': MATCH, 'action': MATCH}, 'n_clicks'),
    State({'type': 'data-action', 'dataset': MATCH, 'action': MATCH}, 'dataset'),
    State({'type': 'data-action', 'dataset': MATCH, 'action': MATCH}, 'action'),
    prevent_initial_call=True
)
def generic_data_action_callback(n_clicks, dataset, action):
    """Generic async callback for data collection/sync actions (sync, refresh, collect, etc.)"""
    async def perform_data_action(dataset, action):
        # Map action to endpoint
        endpoint_map = {
            'sync': f"{API_URL}/data/{dataset}/sync",
            'refresh': f"{API_URL}/data/{dataset}/refresh",
            'collect': f"{API_URL}/data/{dataset}/collect",
            # Add more actions as needed
        }
        url = endpoint_map.get(action)
        if not url:
            return html.Div([
                html.H5("Unknown Data Action", style={"color": "red"}),
                html.P(f"Action '{action}' not recognized for dataset '{dataset}'.")
            ])
        try:
            timeout_obj = ClientTimeout(total=20)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return html.Div([
                html.H5("Error performing data action", style={"color": "red"}),
                html.P(str(e))
            ])
        return html.Div([
            html.P(f"Dataset '{dataset}' action '{action}': {result.get('message', 'Success')}")
        ])
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(perform_data_action(dataset, action))

# --- Generic Async Model Management Callback ---
@app.callback(
    Output({'type': 'model-output', 'model': MATCH}, 'children'),
    Input({'type': 'model-action', 'model': MATCH, 'action': MATCH}, 'n_clicks'),
    State({'type': 'model-action', 'model': MATCH, 'action': MATCH}, 'model'),
    State({'type': 'model-action', 'model': MATCH, 'action': MATCH}, 'action'),
    prevent_initial_call=True
)
def generic_model_action_callback(n_clicks, model, action):
    """Generic async callback for model management actions (metrics, retrain, version, backtest, etc.)"""
    async def perform_model_action(model, action):
        # Map action to endpoint
        endpoint_map = {
            'update-metrics': f"{API_URL}/models/{model}/metrics/update",
            'retrain': f"{API_URL}/models/{model}/retrain",
            'manage-version': f"{API_URL}/models/{model}/version/manage",
            'load-backtest': f"{API_URL}/models/{model}/backtest/load",
            # Add more actions as needed
        }
        url = endpoint_map.get(action)
        if not url:
            return html.Div([
                html.H5("Unknown Model Action", style={"color": "red"}),
                html.P(f"Action '{action}' not recognized for model '{model}'.")
            ])
        try:
            timeout_obj = ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return html.Div([
                html.H5("Error performing model action", style={"color": "red"}),
                html.P(str(e))
            ])
        return html.Div([
            html.P(f"Model '{model}' action '{action}': {result.get('message', 'Success')}")
        ])
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(perform_model_action(model, action))

# --- Generic Async Log/Error Fetch Callback ---
@app.callback(
    Output({'type': 'log-output', 'target': MATCH, 'logtype': MATCH}, 'children'),
    Input({'type': 'log-action', 'target': MATCH, 'logtype': MATCH}, 'n_clicks'),
    State({'type': 'log-action', 'target': MATCH, 'logtype': MATCH}, 'target'),
    State({'type': 'log-action', 'target': MATCH, 'logtype': MATCH}, 'logtype'),
    prevent_initial_call=True
)
def generic_log_fetch_callback(n_clicks, target, logtype):
    """Generic async callback for fetching logs or error traces"""
    async def fetch_logs(target, logtype):
        # Map logtype to endpoint
        endpoint_map = {
            'model-log': f"{API_URL}/models/{target}/logs",
            'model-error': f"{API_URL}/models/{target}/errors",
            'system-log': f"{API_URL}/system/logs",
            # Add more log types as needed
        }
        url = endpoint_map.get(logtype)
        if not url:
            return html.Div([
                html.H5("Unknown Log Type", style={"color": "red"}),
                html.P(f"Log type '{logtype}' not recognized for target '{target}'.")
            ])
        try:
            timeout_obj = ClientTimeout(total=20)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.get(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return html.Div([
                html.H5("Error fetching logs", style={"color": "red"}),
                html.P(str(e))
            ])
        # Display logs or errors as preformatted text
        return html.Div([
            html.H5(f"{logtype.replace('-', ' ').title()} for {target}"),
            html.Pre(result.get('log', result.get('error', 'No log data found')))
        ])
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetch_logs(target, logtype))

# --- Generic Async Advanced Analytics/Hybrid/Ensemble Action Callback ---
@app.callback(
    Output({'type': 'advanced-output', 'target': MATCH, 'action': MATCH}, 'children'),
    Input({'type': 'advanced-action', 'target': MATCH, 'action': MATCH}, 'n_clicks'),
    State({'type': 'advanced-action', 'target': MATCH, 'action': MATCH}, 'target'),
    State({'type': 'advanced-action', 'target': MATCH, 'action': MATCH}, 'action'),
    prevent_initial_call=True
)
def generic_advanced_action_callback(n_clicks, target, action):
    """Generic async callback for advanced analytics, hybrid, or ensemble actions"""
    async def perform_advanced_action(target, action):
        # Map action to endpoint
        endpoint_map = {
            'run-hybrid': f"{API_URL}/hybrid/{target}/run",
            'ensemble-predict': f"{API_URL}/ensemble/{target}/predict",
            'advanced-analytics': f"{API_URL}/analytics/{target}/advanced",
            # Add more advanced actions as needed
        }
        url = endpoint_map.get(action)
        if not url:
            return html.Div([
                html.H5("Unknown Advanced Action", style={"color": "red"}),
                html.P(f"Action '{action}' not recognized for target '{target}'.")
            ])
        try:
            timeout_obj = ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return html.Div([
                html.H5("Error performing advanced action", style={"color": "red"}),
                html.P(str(e))
            ])
        return html.Div([
            html.P(f"Advanced action '{action}' for '{target}': {result.get('message', 'Success')}")
        ])
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(perform_advanced_action(target, action))

# --- Generic Async System/Backend Maintenance Callback ---
@app.callback(
    Output({'type': 'maintenance-output', 'task': MATCH}, 'children'),
    Input({'type': 'maintenance-action', 'task': MATCH}, 'n_clicks'),
    State({'type': 'maintenance-action', 'task': MATCH}, 'task'),
    prevent_initial_call=True
)
def generic_maintenance_action_callback(n_clicks, task):
    """Generic async callback for system/backend maintenance actions (restart, clear cache, update, etc.)"""
    async def perform_maintenance_action(task):
        # Map task to endpoint
        endpoint_map = {
            'restart-backend': f"{API_URL}/system/restart",
            'clear-cache': f"{API_URL}/system/cache/clear",
            'update-system': f"{API_URL}/system/update",
            # Add more maintenance tasks as needed
        }
        url = endpoint_map.get(task)
        if not url:
            return html.Div([
                html.H5("Unknown Maintenance Task", style={"color": "red"}),
                html.P(f"Task '{task}' not recognized.")
            ])
        try:
            timeout_obj = ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return html.Div([
                html.H5("Error performing maintenance task", style={"color": "red"}),
                html.P(str(e))
            ])
        return html.Div([
            html.P(f"Maintenance task '{task}': {result.get('message', 'Success')}")
        ])
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(perform_maintenance_action(task))

# --- Generic Multi-Output Async Callback (Progress/Status/Data) ---
@app.callback(
    [
        Output({'type': 'multi-output', 'target': MATCH}, 'children'),
        Output({'type': 'multi-output', 'target': MATCH}, 'style'),
    ],
    [
        Input({'type': 'multi-action', 'target': MATCH, 'action': MATCH}, 'n_clicks'),
        State({'type': 'multi-action', 'target': MATCH, 'action': MATCH}, 'target'),
        State({'type': 'multi-action', 'target': MATCH, 'action': MATCH}, 'action'),
    ],
    prevent_initial_call=True
)
def generic_multi_output_callback(n_clicks, target, action):
    """Generic async callback for multi-output actions (progress, status, data, etc.)"""
    async def perform_multi_action(target, action):
        endpoint_map = {
            'progress': f"{API_URL}/progress/{target}",
            'status-data': f"{API_URL}/status_data/{target}",
            # Add more as needed
        }
        url = endpoint_map.get(action)
        if not url:
            return [html.Div([
                html.H5("Unknown Multi-Output Action", style={"color": "red"}),
                html.P(f"Action '{action}' not recognized for target '{target}'.")
            ]), {"color": "red"}]
        try:
            timeout_obj = ClientTimeout(total=20)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.get(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return [html.Div([
                html.H5("Error performing multi-output action", style={"color": "red"}),
                html.P(str(e))
            ]), {"color": "red"}]
        # Example: progress bar and status
        progress = result.get('progress', 0)
        status = result.get('status', 'unknown')
        return [
            html.Div([
                dbc.Progress(value=progress, striped=True, animated=True, style={"height": "20px"}),
                html.P(f"Status: {status}")
            ]),
            {"color": "green" if progress == 100 else "blue"}
        ]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(perform_multi_action(target, action))

# --- Generic Async Interval/Periodic Update Callback ---
@app.callback(
    Output({'type': 'interval-output', 'target': MATCH}, 'children'),
    Input({'type': 'interval-component', 'target': MATCH}, 'n_intervals'),
    State({'type': 'interval-component', 'target': MATCH}, 'target'),
    prevent_initial_call=True
)
def generic_interval_update_callback(n_intervals, target):
    """Generic async callback for periodic/interval updates (e.g., live price, chart)"""
    async def fetch_interval_data(target):
        endpoint_map = {
            'live-price': f"{API_URL}/price/live",
            'live-chart': f"{API_URL}/chart/live",
            'system-status': f"{API_URL}/system/status",
            # Add more as needed
        }
        url = endpoint_map.get(target)
        if not url:
            return html.Div([html.H5("Unknown Interval Target", style={"color": "red"}), html.P(f"Target '{target}' not recognized.")])
        try:
            timeout_obj = ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.get(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return html.Div([html.H5("Error fetching interval data", style={"color": "red"}), html.P(str(e))])
        # Example: display live data
        return html.Div([html.P(f"{target.replace('-', ' ').title()}: {result.get('value', 'N/A')}")])
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetch_interval_data(target))

# --- Sidebar/Advanced Tool Callback Example ---
@app.callback(
    Output('sidebar-content', 'children'),
    Input('sidebar-toggle', 'n_clicks'),
    State('sidebar-toggle', 'n_clicks_timestamp'),
    prevent_initial_call=True
)
def sidebar_toggle_callback(n_clicks, n_clicks_timestamp):
    """Callback to toggle sidebar content (special-case example)"""
    # This is a simple synchronous example; adapt as needed for async or API-based sidebar content
    if n_clicks % 2 == 1:
        return html.Div([
            html.H4("Sidebar Expanded"),
            html.P(f"Toggled at {datetime.now().strftime('%H:%M:%S')}")
        ])
    else:
        return html.Div([
            html.H4("Sidebar Collapsed"),
            html.P(f"Toggled at {datetime.now().strftime('%H:%M:%S')}")
        ])

# --- Unique/Special-Case Callback Placeholder ---
@app.callback(
    Output('special-case-output', 'children'),
    Input('special-case-button', 'n_clicks'),
    prevent_initial_call=True
)
def special_case_callback(n_clicks):
    """Special-case callback for unique dashboard logic (customize as needed)"""
    # Insert unique logic here
    return html.Div([
        html.H5("Special Case Triggered!"),
        html.P(f"Button clicked {n_clicks} times.")
    ])

# --- Multi-Output Backtest/Progress/Analytics Callback ---
@app.callback(
    [
        Output('comprehensive-backtest-output', 'children'),
        Output('backtest-progress', 'value'),
        Output('backtest-progress', 'children')
    ],
    [Input('run-comprehensive-backtest', 'n_clicks')],
    [State('backtest-start-date', 'date'),
     State('backtest-end-date', 'date'),
     State('backtest-symbol', 'value'),
     State('backtest-strategy', 'value')],
    prevent_initial_call=True
)
def comprehensive_backtest_callback(n_clicks, start_date, end_date, symbol, strategy):
    """Async callback for comprehensive backtest with progress bar and output"""
    async def run_backtest():
        url = f"{API_URL}/backtest/run"
        payload = {
            'start_date': start_date,
            'end_date': end_date,
            'symbol': symbol,
            'strategy': strategy
        }
        try:
            timeout_obj = ClientTimeout(total=120)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url, json=payload) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return [html.Div([html.H5("Backtest Error", style={"color": "red"}), html.P(str(e))]), 0, "Error"]
        progress = result.get('progress', 100)
        msg = result.get('message', 'Complete')
        output = html.Div([
            html.H5("Backtest Results"),
            html.Pre(json.dumps(result.get('results', {}), indent=2))
        ])
        return [output, progress, f"{progress}% - {msg}"]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(run_backtest())

# --- Multi-Output Model Retrain Callback ---
@app.callback(
    [
        Output('model-retrain-status', 'children'),
        Output('retrain-progress', 'value'),
        Output('retrain-progress', 'children')
    ],
    [Input('start-model-retrain', 'n_clicks'),
     Input('retrain-status-refresh', 'n_clicks')],
    prevent_initial_call=True
)
def model_retrain_callback(n_clicks1, n_clicks2):
    """Async callback for model retraining with progress bar and status"""
    async def retrain():
        url = f"{API_URL}/model/retrain"
        try:
            timeout_obj = ClientTimeout(total=120)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return [html.Div([html.H5("Retrain Error", style={"color": "red"}), html.P(str(e))]), 0, "Error"]
        progress = result.get('progress', 100)
        msg = result.get('message', 'Complete')
        output = html.Div([
            html.H5("Retrain Results"),
            html.Pre(json.dumps(result.get('results', {}), indent=2))
        ])
        return [output, progress, f"{progress}% - {msg}"]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(retrain())

# --- Sidebar Quick Amount Buttons Callback ---
@app.callback(
    Output("sidebar-amount-input", "value", allow_duplicate=True),
    [Input("sidebar-amount-50", "n_clicks"),
     Input("sidebar-amount-100", "n_clicks"),
     Input("sidebar-amount-250", "n_clicks"),
     Input("sidebar-amount-500", "n_clicks"),
     Input("sidebar-amount-1000", "n_clicks"),
     Input("sidebar-amount-max", "n_clicks")],
    prevent_initial_call=True
)
def sidebar_quick_amount_callback(*btns):
    amounts = [50, 100, 250, 500, 1000, 'max']
    ctx_id = ctx.triggered_id
    if ctx_id:
        idx = [f"sidebar-amount-{amt}" for amt in amounts].index(ctx_id)
        return amounts[idx]
    return no_update

# --- Sidebar Amount Type Toggle Callback ---
@app.callback(
    [Output("sidebar-fixed-amount-section", "style"),
     Output("sidebar-amount-input", "placeholder")],
    Input("sidebar-amount-type", "value")
)
def sidebar_amount_type_callback(value):
    if value == 'fixed':
        return {"display": "block"}, "Enter fixed amount"
    else:
        return {"display": "none"}, "Enter percentage"

# --- Sidebar Performance Updates ---
@app.callback(
    [Output("sidebar-winrate", "children"),
     Output("sidebar-total-trades", "children"),
     Output("sidebar-daily-pnl", "children")],
    Input("performance-interval", "n_intervals")
)
def sidebar_performance_callback(n):
    async def fetch_perf():
        url = f"{API_URL}/sidebar/performance"
        try:
            timeout_obj = ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.get(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return ["-", "-", f"Error: {e}"]
        return [result.get('winrate', '-'), result.get('total_trades', '-'), result.get('daily_pnl', '-')]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetch_perf())

# --- Advanced Tools Collapse Toggles (Pattern-Matching) ---
for tool in [
    'hft-tools', 'data-collection', 'online-learning', 'risk-management', 'notifications', 'email-alerts',
    'analytics', 'ml-tools', 'charts', 'dev-tools']:
    @app.callback(
        Output(f"{tool}-collapse", "is_open"),
        Input(f"toggle-{tool}", "n_clicks"),
        State(f"{tool}-collapse", "is_open"),
        prevent_initial_call=True
    )
    def toggle_collapse(n, is_open):
        return not is_open if n else is_open

# --- Technical Indicator Interval Callbacks (Pattern-Matching) ---
for indicator in [
    'futures-rsi-indicator', 'futures-macd-indicator', 'futures-bollinger-indicator',
    'futures-stochastic-indicator', 'futures-volume-indicator', 'futures-atr-indicator']:
    @app.callback(
        Output(indicator, 'children'),
        [Input('futures-refresh-interval', 'n_intervals'),
         Input('futures-symbol-dropdown', 'value')],
        prevent_initial_call=True
    )
    def indicator_callback(n, symbol):
        async def fetch_indicator():
            url = f"{API_URL}/futures/indicator/{indicator.split('-')[1]}"
            try:
                timeout_obj = ClientTimeout(total=10)
                async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                    async with session.get(url, params={'symbol': symbol}) as resp:
                        resp.raise_for_status()
                        result = await resp.json()
            except Exception as e:
                return f"Error: {e}"
            return result.get('value', '-')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(fetch_indicator())

# --- End of refactored_callbacks.py ---
# --- Transfer Learning Management Multi-Output Callback ---
@app.callback(
    [Output('transfer-learning-setup', 'children'), Output('transfer-learning-training', 'children')],
    [Input('check-transfer-setup', 'n_clicks'), Input('init-transfer-learning', 'n_clicks'), Input('train-target-model', 'n_clicks')],
    [State('source-pairs-input', 'value'), State('target-pair-input', 'value'), State('training-candles-input', 'value')],
    prevent_initial_call=True
)
def transfer_learning_management_callback(*args):
    async def manage_transfer():
        url = f"{API_URL}/transfer_learning/manage"
        payload = {
            'source_pairs': args[3],
            'target_pair': args[4],
            'candles': args[5]
        }
        try:
            timeout_obj = ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url, json=payload) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return [f"Error: {e}", f"Error: {e}"]
        return [result.get('setup', '-'), result.get('training', '-')]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(manage_transfer())

# --- Futures Trading Controls Multi-Output Callback ---
@app.callback(
    [Output('futures-trading-controls', 'children'), Output('futures-trading-status', 'children')],
    [Input('open-futures-position', 'n_clicks'), Input('close-futures-position', 'n_clicks'), Input('update-futures-positions', 'n_clicks')],
    [State('futures-symbol-input', 'value'), State('futures-side-select', 'value'), State('futures-quantity-input', 'value'), State('futures-leverage-input', 'value')],
    prevent_initial_call=True
)
def futures_trading_controls_callback(*args):
    async def manage_futures():
        url = f"{API_URL}/futures/manage"
        payload = {
            'symbol': args[3],
            'side': args[4],
            'quantity': args[5],
            'leverage': args[6]
        }
        try:
            timeout_obj = ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url, json=payload) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return [f"Error: {e}", f"Error: {e}"]
        return [result.get('controls', '-'), result.get('status', '-')]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(manage_futures())

# --- Virtual Balance Sync for Futures Multi-Output Callback ---
@app.callback(
    [Output('futures-virtual-balance', 'children'), Output('futures-pnl-display', 'children'), Output('futures-virtual-total-balance', 'children'), Output('futures-available-balance', 'children')],
    [Input('live-price-interval', 'n_intervals'), Input('futures-sync-balance-btn', 'n_clicks')],
    prevent_initial_call=True
)
def futures_virtual_balance_callback(*args):
    async def fetch_balance():
        url = f"{API_URL}/futures/balance"
        try:
            timeout_obj = ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.get(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return [f"Error: {e}"]*4
        return [result.get('virtual_balance', '-'), result.get('pnl', '-'), result.get('total_balance', '-'), result.get('available_balance', '-')]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetch_balance())

# --- Auto Trading Virtual Balance Sync Multi-Output Callback ---
@app.callback(
    [Output('auto-balance-display', 'children'), Output('auto-pnl-display', 'children')],
    [Input('live-price-interval', 'n_intervals')],
    prevent_initial_call=True
)
def auto_trading_virtual_balance_callback(n):
    async def fetch_auto_balance():
        url = f"{API_URL}/auto/balance"
        try:
            timeout_obj = ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.get(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return [f"Error: {e}", f"Error: {e}"]
        return [result.get('balance', '-'), result.get('pnl', '-')]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetch_auto_balance())

# --- Risk Management Settings Multi-Output Callback ---
@app.callback(
    [Output('risk-settings-display', 'children'), Output('risk-settings-status', 'children')],
    [Input('save-risk-settings', 'n_clicks'), Input('load-risk-settings', 'n_clicks')],
    [State('max-drawdown-input', 'value'), State('position-size-input', 'value'), State('stop-loss-pct-input', 'value'), State('take-profit-pct-input', 'value')],
    prevent_initial_call=True
)
def risk_management_settings_callback(*args):
    async def manage_risk():
        url = f"{API_URL}/risk/manage"
        payload = {
            'max_drawdown': args[2],
            'position_size': args[3],
            'stop_loss_pct': args[4],
            'take_profit_pct': args[5]
        }
        try:
            timeout_obj = ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url, json=payload) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return [f"Error: {e}", f"Error: {e}"]
        return [result.get('display', '-'), result.get('status', '-')]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(manage_risk())

# --- Notification System Multi-Output Callback ---
@app.callback(
    [Output('notifications-display', 'children'), Output('notification-count', 'children')],
    [Input('notification-refresh-interval', 'n_intervals'), Input('refresh-notifications-btn', 'n_clicks'), Input('show-unread-only', 'value')],
    prevent_initial_call=True
)
def notifications_callback(*args):
    async def fetch_notifications():
        url = f"{API_URL}/notifications"
        params = {'unread_only': args[2]}
        try:
            timeout_obj = ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.get(url, params=params) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return [f"Error: {e}", 0]
        return [result.get('notifications', []), result.get('count', 0)]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetch_notifications())

# --- Data Collection Automation Multi-Output Callback ---
@app.callback(
    [Output('data-collection-status', 'children'), Output('data-collection-controls', 'children')],
    [Input('start-data-collection-btn', 'n_clicks'), Input('stop-data-collection-btn', 'n_clicks'), Input('check-data-collection-btn', 'n_clicks')],
    prevent_initial_call=True
)
def data_collection_callback(*args):
    async def manage_data_collection():
        url = f"{API_URL}/data/collection/manage"
        # Only include 'action' in payload if it is not None
        ctx_id = ctx.triggered_id if hasattr(ctx, 'triggered_id') else None
        action = None
        if ctx_id == 'start-data-collection-btn':
            action = 'start'
        elif ctx_id == 'stop-data-collection-btn':
            action = 'stop'
        elif ctx_id == 'check-data-collection-btn':
            action = 'check'
        payload = {'action': action} if action is not None else {}
        try:
            timeout_obj = ClientTimeout(total=20)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url, json=payload) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return [f"Error: {e}", f"Error: {e}"]
        return [result.get('status', '-'), result.get('controls', '-')]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(manage_data_collection())

# --- Email/Alert System Multi-Output Callback ---
@app.callback(
    [Output('email-config-status', 'children'), Output('email-enabled-switch', 'value')],
    [Input('save-email-config-btn', 'n_clicks'), Input('email-config-refresh-interval', 'n_intervals')],
    [State('smtp-server-input', 'value'), State('smtp-port-input', 'value'), State('email-address-input', 'value'), State('email-password-input', 'value'), State('email-enabled-switch', 'value')],
    prevent_initial_call=True
)
def email_config_callback(*args):
    async def manage_email():
        url = f"{API_URL}/email/config"
        payload = {
            'smtp_server': args[2],
            'smtp_port': args[3],
            'email_address': args[4],
            'email_password': args[5],
            'enabled': args[6]
        }
        try:
            timeout_obj = ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url, json=payload) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return [f"Error: {e}", False]
        return [result.get('status', '-'), result.get('enabled', False)]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(manage_email())

# --- HFT Analysis Multi-Output Callback ---
@app.callback(
    [Output('hft-analysis-display', 'children'), Output('hft-stats-cards', 'children')],
    [Input('run-hft-analysis-btn', 'n_clicks'), Input('hft-refresh-interval', 'n_intervals')],
    [State('hft-symbol-input', 'value'), State('hft-timeframe-dropdown', 'value')],
    prevent_initial_call=True
)
def hft_analysis_callback(*args):
    async def run_hft():
        url = f"{API_URL}/hft/analysis"
        payload = {'symbol': args[2], 'timeframe': args[3]}
        try:
            timeout_obj = ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url, json=payload) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return [f"Error: {e}", f"Error: {e}"]
        return [result.get('display', '-'), result.get('stats', '-')]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(run_hft())

# --- Online Learning Multi-Output Callback ---
@app.callback(
    [Output('online-learning-status', 'children'), Output('online-learning-controls', 'children')],
    [Input('start-online-learning-btn', 'n_clicks'), Input('stop-online-learning-btn', 'n_clicks'), Input('reset-online-learning-btn', 'n_clicks'), Input('check-online-learning-btn', 'n_clicks')],
    [State('online-learning-mode-dropdown', 'value'), State('online-learning-buffer-size', 'value'), State('online-learning-update-frequency', 'value')],
    prevent_initial_call=True
)
def online_learning_callback(*args):
    async def manage_online_learning():
        url = f"{API_URL}/online_learning/manage"
        payload = {
            'mode': args[4],
            'buffer_size': args[5],
            'update_freq': args[6]
        }
        try:
            timeout_obj = ClientTimeout(total=20)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url, json=payload) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return [f"Error: {e}", f"Error: {e}"]
        return [result.get('status', '-'), result.get('controls', '-')]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(manage_online_learning())

# --- Analytics Tables Multi-Output Callback ---
@app.callback(
    [Output('analytics-table', 'data'), Output('analytics-table', 'columns'), Output('analytics-table-status', 'children')],
    [Input('refresh-analytics-table-btn', 'n_clicks'), Input('analytics-table-interval', 'n_intervals')],
    [State('analytics-table-type-dropdown', 'value')],
    prevent_initial_call=True
)
def analytics_table_callback(*args):
    async def fetch_table():
        url = f"{API_URL}/analytics/table"
        params = {'type': args[2]}
        try:
            timeout_obj = ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.get(url, params=params) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return [[], [], f"Error: {e}"]
        data = result.get('data', [])
        columns = result.get('columns', [])
        status = result.get('status', '-')
        return [data, columns, status]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetch_table())

# --- Chart Update Multi-Output Callback ---
@app.callback(
    [Output('main-chart', 'figure'), Output('main-chart-status', 'children')],
    [Input('refresh-main-chart-btn', 'n_clicks'), Input('main-chart-interval', 'n_intervals')],
    [State('main-chart-symbol-dropdown', 'value'), State('main-chart-type-dropdown', 'value')],
    prevent_initial_call=True
)
def main_chart_callback(*args):
    async def fetch_chart():
        url = f"{API_URL}/chart/main"
        params = {'symbol': args[2], 'type': args[3]}
        try:
            timeout_obj = ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.get(url, params=params) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return [go.Figure(), f"Error: {e}"]
        fig = go.Figure(result.get('figure', {}))
        status = result.get('status', '-')
        return [fig, status]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetch_chart())

# --- Quick Action Multi-Output Callback ---
@app.callback(
    [Output({'type': 'quick-action-output', 'action': MATCH}, 'children'), Output({'type': 'quick-action-output', 'action': MATCH}, 'style')],
    [Input({'type': 'quick-action-btn', 'action': MATCH}, 'n_clicks')],
    [State({'type': 'quick-action-btn', 'action': MATCH}, 'action')],
    prevent_initial_call=True
)
def quick_action_callback(n_clicks, action):
    async def perform_quick_action(action):
        endpoint_map = {
            'close-all-trades': f"{API_URL}/trades/close_all",
            'cancel-all-orders': f"{API_URL}/orders/cancel_all",
            'reset-dashboard': f"{API_URL}/dashboard/reset",
            # Add more quick actions as needed
        }
        url = endpoint_map.get(action)
        if not url:
            return [f"Unknown quick action: {action}", {"color": "red"}]
        try:
            timeout_obj = ClientTimeout(total=20)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return [f"Error: {e}", {"color": "red"}]
        return [result.get('message', 'Success'), {"color": "green"}]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(perform_quick_action(action))

# --- Pattern-Matching Analytics/Chart/Table/Quick-Action Generic Callback ---
@app.callback(
    Output({'type': 'dashboard-generic-output', 'target': MATCH, 'action': MATCH}, 'children'),
    Input({'type': 'dashboard-generic-btn', 'target': MATCH, 'action': MATCH}, 'n_clicks'),
    State({'type': 'dashboard-generic-btn', 'target': MATCH, 'action': MATCH}, 'target'),
    State({'type': 'dashboard-generic-btn', 'target': MATCH, 'action': MATCH}, 'action'),
    prevent_initial_call=True
)
def dashboard_generic_callback(n_clicks, target, action):
    async def perform_dashboard_action(target, action):
        endpoint_map = {
            'analytics': f"{API_URL}/analytics/{target}",
            'table': f"{API_URL}/table/{target}",
            'chart': f"{API_URL}/chart/{target}",
            'quick-action': f"{API_URL}/quick_action/{target}",
            # Add more as needed
        }
        url = endpoint_map.get(action)
        if not url:
            return html.Div([f"Unknown dashboard action: {action} for {target}"])
        try:
            timeout_obj = ClientTimeout(total=20)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return html.Div([f"Error: {e}"])
        return html.Div([result.get('message', 'Success')])
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(perform_dashboard_action(target, action))

# --- Manual Notification Collapse Callback ---
@app.callback(
    Output('manual-notification-collapse', 'is_open'),
    Input('test-notification-btn', 'n_clicks'),
    State('manual-notification-collapse', 'is_open'),
    prevent_initial_call=True
)
def manual_notification_collapse_callback(n_clicks, is_open):
    return not is_open if n_clicks else is_open

# --- Manual Notification Send Callback ---
@app.callback(
    Output('notification-send-status', 'children'),
    Input('send-manual-notification-btn', 'n_clicks'),
    [State('manual-notification-type', 'value'), State('manual-notification-message', 'value')],
    prevent_initial_call=True
)
def send_manual_notification_callback(n_clicks, notif_type, notif_msg):
    async def send_notification():
        url = f"{API_URL}/notifications/manual"
        payload = {'type': notif_type, 'message': notif_msg}
        try:
            timeout_obj = ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url, json=payload) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return f"Error: {e}"
        return result.get('status', 'Sent')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(send_notification())

# --- Clear Notifications Callback ---
@app.callback(
    Output('clear-notifications-status', 'children'),
    Input('clear-notifications-btn', 'n_clicks'),
    prevent_initial_call=True
)
def clear_notifications_callback(n_clicks):
    async def clear_notifications():
        url = f"{API_URL}/notifications/clear"
        try:
            timeout_obj = ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return f"Error: {e}"
        return result.get('status', 'Cleared')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(clear_notifications())

# --- Delete Individual Notifications Callback ---
@app.callback(
    Output({'type': 'delete-notification', 'index': ALL}, 'children'),
    Input({'type': 'delete-notification', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def delete_individual_notifications_callback(n_clicks_list):
    # This callback is a placeholder; actual deletion is handled by the generic notification action callback
    return [no_update for _ in n_clicks_list]

# --- Test/Dev/Utility Buttons ---
@app.callback(
    Output('test-db-btn-output', 'children'),
    Input('test-db-btn', 'n_clicks'),
    prevent_initial_call=True
)
def test_db_btn_callback(n_clicks):
    async def test_db():
        url = f"{API_URL}/test/db"
        try:
            timeout_obj = ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return f"Error: {e}"
        return result.get('message', 'Success')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(test_db())

@app.callback(
    Output('test-ml-btn-output', 'children'),
    Input('test-ml-btn', 'n_clicks'),
    prevent_initial_call=True
)
def test_ml_btn_callback(n_clicks):
    async def test_ml():
        url = f"{API_URL}/test/ml"
        try:
            timeout_obj = ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return f"Error: {e}"
        return result.get('message', 'Success')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(test_ml())

@app.callback(
    Output('email-test-result', 'children'),
    Input('test-email-btn', 'n_clicks'),
    prevent_initial_call=True
)
def test_email_btn_callback(n_clicks):
    async def test_email():
        url = f"{API_URL}/email/test"
        try:
            timeout_obj = ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return f"Error: {e}"
        return result.get('message', 'Success')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(test_email())

@app.callback(
    Output('alert-test-result', 'children'),
    Input('send-test-alert-btn', 'n_clicks'),
    prevent_initial_call=True
)
def send_test_alert_btn_callback(n_clicks):
    async def test_alert():
        url = f"{API_URL}/alert/test"
        try:
            timeout_obj = ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return f"Error: {e}"
        return result.get('message', 'Success')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(test_alert())

@app.callback(
    Output('check-auto-alerts-result', 'children'),
    Input('check-auto-alerts-btn', 'n_clicks'),
    prevent_initial_call=True
)
def check_auto_alerts_btn_callback(n_clicks):
    async def check_alerts():
        url = f"{API_URL}/alert/check_auto"
        try:
            timeout_obj = ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return f"Error: {e}"
        return result.get('message', 'Success')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(check_alerts())

# --- Optimize Buttons (Multi-Output Example) ---
@app.callback(
    [Output('optimize-kaia-btn', 'children'), Output('optimize-jasmy-btn', 'children'), Output('optimize-gala-btn', 'children')],
    [Input('optimize-kaia-btn', 'n_clicks'), Input('optimize-jasmy-btn', 'n_clicks'), Input('optimize-gala-btn', 'n_clicks')],
    prevent_initial_call=True
)
def optimize_buttons_callback(n1, n2, n3):
    async def optimize(symbol):
        url = f"{API_URL}/optimize/{symbol}"
        try:
            timeout_obj = ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                async with session.post(url) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
        except Exception as e:
            return f"Error: {e}"
        return result.get('message', 'Optimized')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    kaia = loop.run_until_complete(optimize('kaia')) if n1 else no_update
    jasmy = loop.run_until_complete(optimize('jasmy')) if n2 else no_update
    gala = loop.run_until_complete(optimize('gala')) if n3 else no_update
    return [kaia, jasmy, gala]

# --- Add more as needed for analytics, tables, charts, quick actions, etc. ---
# --- End of refactored_callbacks.py ---
