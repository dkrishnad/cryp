#!/usr/bin/env python3
"""
FIXED DASHBOARD LAYOUT - Optimized for stability and performance
"""
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px

# Fallback components for loading errors
def safe_dropdown(id, options=None, value=None, **kwargs):
    """Dropdown with fallback for loading errors"""
    try:
        return dcc.Dropdown(id=id, options=options or [], value=value, **kwargs)
    except Exception as e:
        print(f"[LAYOUT FIX] Dropdown {id} fallback: {e}")
        return html.Select(
            id=id,
            children=[html.Option(opt['label'], value=opt['value']) for opt in (options or [])],
            value=value,
            **{k: v for k, v in kwargs.items() if k in ['className', 'style']}
        )

def safe_graph(id, figure=None, **kwargs):
    """Graph with fallback for loading errors"""
    try:
        return dcc.Graph(id=id, figure=figure or {}, **kwargs)
    except Exception as e:
        print(f"[LAYOUT FIX] Graph {id} fallback: {e}")
        return html.Div([
            html.H6("📊 Chart Loading..."),
            html.P("Chart will appear when data is available")
        ], id=id, className="text-center p-4 border", **kwargs)

# Stores and intervals
stores_and_intervals = html.Div([
    dcc.Store(id="selected-symbol-store", storage_type="memory"),
    dcc.Store(id="live-price-cache", storage_type="memory"),
    dcc.Store(id="upload-tracking-store", storage_type="memory", data={"active": False}),
    dcc.Interval(id="live-price-interval", interval=2000, n_intervals=0),
    dcc.Interval(id="interval-prediction", interval=5*1000, n_intervals=0),
    dcc.Interval(id="interval-indicators", interval=30*1000, n_intervals=0),
    dcc.Interval(id="auto-trading-interval", interval=5*1000, n_intervals=0),
])

# Sidebar with essential controls
sidebar = html.Div([
    html.H4([html.I(className="bi bi-gear-fill me-2 text-primary"), "Trading Controls"], className="mb-3 mt-2"),
    
    # Symbol selection
    html.Div([
        dbc.Label([html.I(className="bi bi-currency-bitcoin me-1 text-warning"), "Symbol"]),
        dcc.Dropdown(
            id="sidebar-symbol",
            options=[{"label": s.upper(), "value": s} for s in [
                'btcusdt', 'ethusdt', 'solusdt', 'kaiausdt', 'avaxusdt', 'dogeusdt', 'bnbusdt'
            ]],
            value='kaiausdt',
            clearable=False,
            style={"backgroundColor": "#ffffff", "color": "#2f3542"}
        ),
    ], className="mb-3"),
    
    # Virtual balance
    html.Div([
        dbc.Label([html.I(className="bi bi-wallet2 me-1 text-success"), "Virtual Balance"]),
        html.Div(id="virtual-balance", style={"fontWeight": "bold", "fontSize": 18, "color": "#00ff88"}),
    ], className="mb-3"),
    
    # Quick actions
    html.Div([
        dbc.Button("Reset Balance", id="reset-balance-btn", color="secondary", className="mb-2 w-100"),
        html.Div(id="reset-balance-btn-output"),
    ]),
    
], id="sidebar-fixed", style={
    "width": "350px", 
    "backgroundColor": "#2a2a2a", 
    "color": "#e0e0e0", 
    "position": "fixed", 
    "top": 0, 
    "left": 0, 
    "height": "100vh", 
    "overflowY": "auto", 
    "padding": "1rem",
    "boxShadow": "2px 0 8px rgba(0,0,0,0.3)", 
    "borderRight": "1px solid #404040"
}, className="sidebar")

# Main dashboard tab
dashboard_tab = html.Div([
    html.H2([html.I(className="bi bi-speedometer2 me-2 text-info"), "Trading Dashboard"], className="mb-4"),
    
    # Live price row
    dbc.Row([
        dbc.Col([
            html.H4([html.I(className="bi bi-currency-exchange me-1 text-warning"), "Live Price"]),
            html.Div(id="live-price", style={"fontSize": 32, "fontWeight": "bold", "color": "#00ff88"}),
        ], width=3),
        dbc.Col([
            html.H4([html.I(className="bi bi-wallet2 me-1 text-success"), "Portfolio Status"]),
            html.Div(id="portfolio-status", style={"fontSize": 18, "color": "#00bfff"}),
        ], width=3),
        dbc.Col([
            html.H4([html.I(className="bi bi-graph-up me-1 text-info"), "Performance"]),
            html.Div(id="performance-monitor", style={"fontSize": 18, "color": "#ffa500"}),
        ], width=6),
    ], className="mb-4"),
    
    # Charts row
    dbc.Row([
        dbc.Col([
            html.H4("Price Chart"),
            safe_graph("price-chart", figure={}),
        ], width=6),
        dbc.Col([
            html.H4("Technical Indicators"),
            safe_graph("indicators-chart", figure={}),
        ], width=6),
    ], className="mb-4"),
    
    # Hybrid predictions
    html.Div([
        html.H4([html.I(className="bi bi-cpu me-1 text-primary"), "AI Predictions"]),
        html.Div(id="hybrid-prediction-output"),
        dbc.Button("Get Prediction", id="get-prediction-btn", color="primary", className="mt-2"),
    ], className="mb-4"),
])

# Auto Trading tab content
auto_trading_tab = html.Div([
    html.H2([html.I(className="bi bi-robot me-2 text-success"), "Auto Trading"], className="mb-4"),
    html.Div(id="auto-trading-content", children=[
        html.P("Auto trading controls will be loaded here..."),
        dbc.Button("Enable Auto Trading", id="auto-trading-toggle", color="success"),
        html.Div(id="auto-trading-status-display", className="mt-3"),
    ])
])

# Futures Trading tab content
futures_trading_tab = html.Div([
    html.H2([html.I(className="bi bi-graph-up me-2 text-warning"), "Futures Trading"], className="mb-4"),
    html.Div(id="futures-trading-content", children=[
        html.P("Futures trading interface will be loaded here..."),
        dbc.Button("Load Futures Interface", id="load-futures-btn", color="warning"),
        html.Div(id="futures-status-display", className="mt-3"),
    ])
])

# Binance Exact tab content
binance_exact_tab = html.Div([
    html.H2([html.I(className="bi bi-lightning me-2 text-info"), "Binance-Exact API"], className="mb-4"),
    html.Div(id="binance-exact-content", children=[
        html.P("Binance-Exact API interface will be loaded here..."),
        dbc.Button("Load Binance Interface", id="load-binance-btn", color="info"),
        html.Div(id="binance-status-display", className="mt-3"),
    ])
])

# Email Config tab content
email_config_tab = html.Div([
    html.H2([html.I(className="bi bi-envelope me-2 text-secondary"), "Email Configuration"], className="mb-4"),
    html.Div(id="email-config-content", children=[
        html.P("Email configuration will be loaded here..."),
        dbc.Button("Load Email Config", id="load-email-btn", color="secondary"),
        html.Div(id="email-config-display", className="mt-3"),
    ])
])

# Tabs component
tabs = dcc.Tabs([
    dcc.Tab(label="Dashboard", children=[dashboard_tab], value="dashboard"),
    dcc.Tab(label="Auto Trading", children=[auto_trading_tab], value="auto-trading"),
    dcc.Tab(label="Futures Trading", children=[futures_trading_tab], value="futures-trading"),
    dcc.Tab(label="Binance-Exact API", children=[binance_exact_tab], value="binance-exact"),
    dcc.Tab(label="Email Config", children=[email_config_tab], value="email-config"),
], id="main-tabs", value="dashboard")

# Notification toast
notification_toast = dbc.Toast(
    id="notification-toast",
    header="Notification",
    dismissable=True,
    icon="primary",
    style={"position": "fixed", "top": 70, "right": 30, "minWidth": 350, "zIndex": 2000},
)

# Hidden components for callbacks
hidden_components = html.Div([
    # Hidden outputs for callbacks
    html.Div(id="dummy-div", style={"display": "none"}),
    html.Div(id="test-output", style={"display": "none"}),
    html.Div(id="backtest-result", style={"display": "none"}),
    
    # Hidden inputs wrapped in divs to avoid style prop issues
    html.Div([
        dcc.Dropdown(id="auto-symbol-dropdown"),
        dcc.Input(id="fixed-amount-input", type="number", value=100),
        dcc.Input(id="percentage-amount-input", type="number", value=10),
    ], style={"display": "none"}),
], style={"display": "none"})

# Main layout
layout = html.Div([
    stores_and_intervals,
    
    # Navigation bar
    dbc.Navbar(
        dbc.Container([
            html.Span([
                html.I(className="bi bi-robot me-2 text-success"), 
                "Crypto Trading Bot Dashboard"
            ], style={"fontWeight": "bold", "fontSize": 24, "color": "#00ff88"}),
        ], fluid=True),
        color="dark",
        dark=True,
        style={"marginBottom": "0.5em", "borderRadius": "0 0 10px 10px", "marginLeft": "350px"}
    ),
    
    sidebar,
    
    # Main content area
    html.Div([
        notification_toast,
        tabs,
        hidden_components,
    ], style={
        "marginLeft": "350px", 
        "padding": "1em", 
        "minHeight": "100vh", 
        "backgroundColor": "#2a2a2a"
    }, className="main-content"),
])

if __name__ == "__main__":
    print("Layout module loaded successfully")
