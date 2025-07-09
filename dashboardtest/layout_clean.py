#!/usr/bin/env python3
"""
CLEAN DASHBOARD LAYOUT - No Duplicate IDs
This file contains only the main layout structure and imports specialized layouts
"""
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px

# Import all the tab layouts - Fixed for direct execution
try:
    from .auto_trading_layout import create_auto_trading_layout
    from .futures_trading_layout import create_futures_trading_layout
    from .binance_exact_layout import create_binance_exact_layout
    from .email_config_layout import create_email_config_layout
    from .hybrid_learning_layout import create_hybrid_learning_layout
except ImportError:
    # Fallback for direct execution
    from auto_trading_layout import create_auto_trading_layout
    from futures_trading_layout import create_futures_trading_layout
    from binance_exact_layout import create_binance_exact_layout
    from email_config_layout import create_email_config_layout
    from hybrid_learning_layout import create_hybrid_learning_layout

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
    """Graph with fallback for loading errors and proper sizing"""
    try:
        # Add default styling if not provided
        if 'style' not in kwargs:
            kwargs['style'] = {'height': '400px'}
        elif 'height' not in kwargs['style']:
            kwargs['style']['height'] = '400px'
        
        # Add config for better chart behavior
        if 'config' not in kwargs:
            kwargs['config'] = {
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d'],
                'responsive': True
            }
        
        return dcc.Graph(id=id, figure=figure or {}, **kwargs)
    except Exception as e:
        print(f"[LAYOUT FIX] Graph {id} fallback: {e}")
        return html.Div([
            html.H6("📊 Chart Loading..."),
            html.P("Chart will appear when data is available")
        ], id=id, className="text-center p-4 border", style={'height': '400px'}, **{k: v for k, v in kwargs.items() if k in ['className']})

# Stores and intervals - NO DUPLICATES
stores_and_intervals = html.Div([
    dcc.Store(id="selected-symbol-store", storage_type="memory"),
    dcc.Store(id="live-price-cache", storage_type="memory"),
    dcc.Store(id="upload-tracking-store", storage_type="memory", data={"active": False}),
    dcc.Store(id="notifications-cache", storage_type="memory"),
    dcc.Store(id="email-config-store", storage_type="local"),
    dcc.Store(id="alert-history-store", storage_type="memory"),
    dcc.Interval(id="live-price-interval", interval=2000, n_intervals=0),
    dcc.Interval(id="interval-prediction", interval=5*1000, n_intervals=0),
    dcc.Interval(id="interval-indicators", interval=30*1000, n_intervals=0),
    dcc.Interval(id="auto-trading-interval", interval=5*1000, n_intervals=0),
    dcc.Interval(id="notifications-interval", interval=10*1000, n_intervals=0),
    dcc.Interval(id="alert-history-interval", interval=30*1000, n_intervals=0),
    dcc.Interval(id="performance-interval", interval=10*1000, n_intervals=0),
    dcc.Interval(id="balance-sync-interval", interval=5*1000, n_intervals=0),
])

# Main Dashboard Content - NO DUPLICATES, ONLY MAIN INTERFACE
main_dashboard_content = html.Div([
    html.H2([html.I(className="bi bi-speedometer2 me-2 text-info"), "📊 Trading Dashboard"], className="mb-4"),
    
    # Live price row
    dbc.Row([
        dbc.Col([
            html.H4([html.I(className="bi bi-currency-exchange me-1 text-warning"), "💹 Live Price"]),
            html.Div(id="live-price", style={"fontSize": 32, "fontWeight": "bold", "color": "#00ff88"}),
        ], width=3),
        dbc.Col([
            html.H4([html.I(className="bi bi-wallet2 me-1 text-success"), "💰 Portfolio Status"]),
            html.Div(id="portfolio-status", style={"fontSize": 18, "color": "#00bfff"}),
            html.Div(id="main-virtual-balance-display", className="text-center"),
        ], width=3),
        dbc.Col([
            html.H4([html.I(className="bi bi-graph-up me-1 text-info"), "📈 Performance"]),
            html.Div(id="performance-monitor", style={"fontSize": 18, "color": "#ffa500"}),
        ], width=6),
    ], className="mb-4"),
    
    # Charts row
    dbc.Row([
        dbc.Col([
            html.H4("📊 Price Chart"),
            html.Div([
                safe_graph("main-price-chart", figure={})
            ], className="chart-container"),
        ], width=6),
        dbc.Col([
            html.H4("📈 Technical Indicators"),
            html.Div([
                safe_graph("main-indicators-chart", figure={})
            ], className="chart-container"),
        ], width=6),
    ], className="mb-4"),
    
    # AI Predictions
    html.Div([
        html.H4([html.I(className="bi bi-cpu me-1 text-primary"), "🤖 AI Predictions"]),
        html.Div(id="main-prediction-output"),
        dbc.Button("🔮 Get Prediction", id="main-get-prediction-btn", color="primary", className="mt-2"),
    ], className="mb-4"),
    
    # Quick Trading Actions
    dbc.Row([
        dbc.Col([
            dbc.Button("💰 Buy", id="main-buy-btn", color="success", size="lg", className="me-2"),
            dbc.Button("💸 Sell", id="main-sell-btn", color="danger", size="lg", className="me-2"),
            dbc.Button("🔮 Quick Prediction", id="main-quick-prediction-btn", color="primary", size="lg"),
        ], width=12),
    ], className="mb-4"),
    
    # Trading Results
    html.Div([
        html.H4([html.I(className="bi bi-activity me-1 text-info"), "💹 Trading Activity"], className="mb-3"),
        html.Div(id="main-trading-results-output")
    ], className="mb-4"),
])

# Sidebar - SIMPLIFIED, NO DUPLICATES
sidebar = html.Div([
    html.H4([html.I(className="bi bi-gear-fill me-2 text-primary"), "⚙️ Trading Controls"], className="mb-3 mt-2"),
    
    # Symbol selection
    html.Div([
        dbc.Label([html.I(className="bi bi-currency-bitcoin me-1 text-warning"), "🪙 Symbol"]),
        dcc.Dropdown(
            id="main-sidebar-symbol",
            options=[{"label": s.upper(), "value": s} for s in [
                'btcusdt', 'ethusdt', 'solusdt', 'avaxusdt', 'dogeusdt', 'bnbusdt', 'adausdt', 'xrpusdt'
            ]],
            value="btcusdt",
            className="bg-dark",
            style={"color": "#fff"},
        ),
    ], className="mb-3"),
    
    # Quick amount buttons
    html.Div([
        dbc.Label("💰 Quick Amounts", className="text-white mb-2"),
        dbc.ButtonGroup([
            dbc.Button("$50", id="main-amount-50", size="sm", color="outline-info"),
            dbc.Button("$100", id="main-amount-100", size="sm", color="outline-info"),
            dbc.Button("$250", id="main-amount-250", size="sm", color="outline-info"),
        ], className="w-100 mb-1"),
        dbc.ButtonGroup([
            dbc.Button("$500", id="main-amount-500", size="sm", color="outline-info"),
            dbc.Button("$1K", id="main-amount-1000", size="sm", color="outline-info"),
            dbc.Button("Max", id="main-amount-max", size="sm", color="outline-warning"),
        ], className="w-100"),
    ], className="mb-3"),
    
    # Backend connection status
    html.Div([
        html.Hr(className="border-secondary my-3"),
        html.H6("🔗 System Status", className="text-white mb-2"),
        html.Div(id="main-backend-status", className="small"),
        html.Div("Make sure the backend is running on port 5000", className="small text-muted"),
    ]),
    
], id="main-sidebar", style={
    "width": "300px", 
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

# MAIN LAYOUT - Clean tab structure with NO DUPLICATES
layout = html.Div([
    stores_and_intervals,
    
    # Main container with sidebar
    html.Div([
        sidebar,
        
        # Main content area
        html.Div([
            # Navigation tabs
            dbc.Tabs([
                dbc.Tab(label="📊 Dashboard", tab_id="main-dashboard"),
                dbc.Tab(label="🤖 Auto Trading", tab_id="auto-trading"),
                dbc.Tab(label="🚀 Futures Trading", tab_id="futures-trading"),
                dbc.Tab(label="🔗 Binance Exact", tab_id="binance-exact"),
                dbc.Tab(label="📧 Email Config", tab_id="email-config"),
                dbc.Tab(label="🧠 Hybrid Learning", tab_id="hybrid-learning"),
            ], id="main-tabs", active_tab="main-dashboard", className="mb-4"),
            
            # Tab content area
            html.Div(id="main-tab-content")
            
        ], style={"marginLeft": "320px", "padding": "2rem"})
    ])
])

# Export the layout
__all__ = ['layout']

# Tab content callback function (to be registered in callbacks.py)
def get_tab_content(active_tab):
    """Return content for the active tab - NO DUPLICATES"""
    if active_tab == "main-dashboard":
        return main_dashboard_content
    elif active_tab == "auto-trading":
        try:
            return create_auto_trading_layout()
        except Exception as e:
            print(f"Error loading auto trading layout: {e}")
            return html.Div([
                html.H3("🤖 Auto Trading"),
                html.P("Auto trading layout will load here."),
                html.Div(id="auto-trading-tab-content")
            ])
    elif active_tab == "futures-trading":
        try:
            return create_futures_trading_layout()
        except Exception as e:
            print(f"Error loading futures trading layout: {e}")
            return html.Div([
                html.H3("🚀 Futures Trading"),
                html.P("Futures trading layout will load here."),
                html.Div(id="futures-trading-tab-content")
            ])
    elif active_tab == "binance-exact":
        try:
            return create_binance_exact_layout()
        except Exception as e:
            print(f"Error loading binance exact layout: {e}")
            return html.Div([
                html.H3("🔗 Binance Exact"),
                html.P("Binance exact layout will load here."),
                html.Div(id="binance-exact-tab-content")
            ])
    elif active_tab == "email-config":
        try:
            return create_email_config_layout()
        except Exception as e:
            print(f"Error loading email config layout: {e}")
            return html.Div([
                html.H3("📧 Email Config"),
                html.P("Email config layout will load here."),
                html.Div(id="email-config-tab-content")
            ])
    elif active_tab == "hybrid-learning":
        try:
            return create_hybrid_learning_layout()
        except Exception as e:
            print(f"Error loading hybrid learning layout: {e}")
            return html.Div([
                html.H3("🧠 Hybrid Learning"),
                html.P("Hybrid learning layout will load here."),
                html.Div(id="hybrid-learning-tab-content")
            ])
    else:
        return main_dashboard_content
