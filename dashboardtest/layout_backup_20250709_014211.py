#!/usr/bin/env python3
"""
FIXED DASHBOARD LAYOUT - Optimized for stability and performance
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

# Stores and intervals
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

# Sidebar with comprehensive controls
sidebar = html.Div([
    html.H4([html.I(className="bi bi-gear-fill me-2 text-primary"), "⚙️ Trading Controls"], className="mb-3 mt-2"),
    
    # Symbol selection
    html.Div([
        dbc.Label([html.I(className="bi bi-currency-bitcoin me-1 text-warning"), "🪙 Symbol"]),
        dcc.Dropdown(
            id="sidebar-symbol",
            options=[{"label": s.upper(), "value": s} for s in [
                'btcusdt', 'ethusdt', 'solusdt', 'avaxusdt', 'dogeusdt', 'bnbusdt', 'maticusdt', 'pepeusdt', '1000flokusdt',
                '1000shibusdt', '1000xemusdt', '1000luncusdt', '1000bonkusdt', '1000satsusdt', '1000rplusdt', '1000babydogeusdt',
                'ordiusdt', 'wifusdt', 'tusdt', 'oplusdt', 'suiusdt', 'enausdt', 'notusdt', 'jupusdt', 'kasusdt', 'tiausdt',
                'stxusdt', 'blurusdt', 'gmxusdt', 'rdntusdt', 'hookusdt', 'cyberusdt', 'arkmusdt', 'sntusdt', 'wavesusdt',
                'kaiausdt', 'adausdt', 'xrpusdt', 'ltcusdt', 'linkusdt', 'dotusdt', 'uniusdt', 'bchusdt', 'filusdt', 'trxusdt', 'etcusdt',
                'aptusdt', 'opusdt', 'arbusdt', 'nearusdt', 'atomusdt', 'sandusdt', 'manausdt', 'chzusdt', 'egldusdt', 'ftmusdt',
                'icpusdt', 'runeusdt', 'sushiusdt', 'aaveusdt', 'snxusdt', 'crvusdt', 'compusdt', 'enjusdt', '1inchusdt',
                'xmrusdt', 'zecusdt', 'dashusdt', 'omgusdt', 'yfiusdt', 'balusdt', 'ctkusdt', 'ankrusdt', 'batusdt', 'cvcusdt', 'dgbusdt'
            ]],
            value='kaiausdt',
            clearable=False,
            style={"backgroundColor": "#ffffff", "color": "#2f3542"}
        ),
    ], className="mb-3"),
    
    # Virtual balance with enhanced display
    html.Div([
        dbc.Label([html.I(className="bi bi-wallet2 me-1 text-success"), "💰 Virtual Balance"]),
        html.Div(id="virtual-balance", style={"fontWeight": "bold", "fontSize": 18, "color": "#00ff88"}),
        html.Div(id="sidebar-virtual-balance", className="text-center"),
        html.Small(id="balance-pnl-display", className="text-muted"),
    ], className="mb-3"),
    
    # Trading Amount Controls
    html.Hr(className="border-secondary my-3"),
    html.H5([html.I(className="bi bi-cash me-1 text-info"), "💵 Trading Amount"], className="mb-2"),
    
    html.Div([
        dbc.Label("Amount Type", className="text-white mb-2"),
        dcc.RadioItems(
            id="sidebar-amount-type",
            options=[
                {"label": " Fixed USDT", "value": "fixed"},
                {"label": " % of Balance", "value": "percentage"}
            ],
            value="fixed",
            className="text-white mb-2",
            inputStyle={"margin-right": "5px"},
            labelStyle={"margin-right": "15px", "fontSize": "14px"}
        ),
    ], className="mb-2"),
    
    # Fixed Amount Section
    html.Div([
        dbc.Label("Amount (USDT)", className="text-white mb-1"),
        dbc.InputGroup([
            dbc.InputGroupText("$"),
            dbc.Input(
                id="sidebar-amount-input",
                type="number",
                value=100,
                min=10,
                max=10000,
                step=10,
                className="bg-dark text-white border-secondary",
                style={"fontSize": "14px"}
            ),
        ], size="sm", className="mb-2"),
        
        # Quick amount buttons
        dbc.ButtonGroup([
            dbc.Button("$50", id="sidebar-amount-50", size="sm", color="outline-info", className="px-2"),
            dbc.Button("$100", id="sidebar-amount-100", size="sm", color="outline-info", className="px-2"),
            dbc.Button("$250", id="sidebar-amount-250", size="sm", color="outline-info", className="px-2"),
        ], className="w-100 mb-1"),
        dbc.ButtonGroup([
            dbc.Button("$500", id="sidebar-amount-500", size="sm", color="outline-info", className="px-2"),
            dbc.Button("$1K", id="sidebar-amount-1000", size="sm", color="outline-info", className="px-2"),
            dbc.Button("Max", id="sidebar-amount-max", size="sm", color="outline-warning", className="px-2"),
        ], className="w-100"),
    ], id="sidebar-fixed-amount-section", className="mb-3"),
    
    # Risk Management
    html.Hr(className="border-secondary my-3"),
    html.H5([html.I(className="bi bi-shield me-1 text-warning"), "⚠️ Risk Settings"], className="mb-2"),
    
    html.Div([
        dbc.Label("Risk per Trade", className="text-white mb-1"),
        dcc.Slider(
            id="sidebar-risk-slider",
            min=1,
            max=10,
            step=0.5,
            value=3,
            marks={i: f"{i}%" for i in range(1, 11, 2)},
            className="mb-2"
        ),
        html.Small(id="sidebar-risk-display", className="text-info"),
    ], className="mb-2"),
    
    html.Div([
        dbc.Label("Stop Loss %", className="text-white mb-1"),
        dbc.InputGroup([
            dbc.Input(
                id="sidebar-sl-input",
                type="number",
                value=2.0,
                min=0.5,
                max=10,
                step=0.1,
                className="bg-dark text-white border-secondary",
                style={"fontSize": "14px"}
            ),
            dbc.InputGroupText("%", className="bg-secondary text-white"),
        ], size="sm", className="mb-2"),
    ], className="mb-2"),
    
    html.Div([
        dbc.Label("Take Profit %", className="text-white mb-1"),
        dbc.InputGroup([
            dbc.Input(
                id="sidebar-tp-input",
                type="number",
                value=4.0,
                min=1,
                max=20,
                step=0.1,
                className="bg-dark text-white border-secondary",
                style={"fontSize": "14px"}
            ),
            dbc.InputGroupText("%", className="bg-secondary text-white"),
        ], size="sm", className="mb-3"),
    ], className="mb-3"),
    
    # Quick Actions
    html.Hr(className="border-secondary my-3"),
    html.H5([html.I(className="bi bi-lightning me-1 text-primary"), "⚡ Quick Actions"], className="mb-2"),
    
    html.Div([
        dbc.Button("� Get ML Prediction", id="sidebar-predict-btn", color="primary", size="sm", className="mb-2 w-100"),
        dbc.Button("📊 Show Analytics", id="sidebar-analytics-btn", color="info", size="sm", className="mb-2 w-100"),
        dbc.Button("�🔄 Reset Balance", id="reset-balance-btn", color="secondary", size="sm", className="mb-2 w-100"),
        html.Div(id="reset-balance-btn-output"),
    ]),
    
    # Performance Monitor
    html.Hr(className="border-secondary my-3"),
    html.H5([html.I(className="bi bi-graph-up me-1 text-success"), "📈 Performance"], className="mb-2"),
    
    html.Div([
        html.Div([
            html.Small("Win Rate", className="text-muted"),
            html.Div(id="sidebar-winrate", className="text-success", style={"fontWeight": "bold"}),
        ], className="mb-2"),
        html.Div([
            html.Small("Total Trades", className="text-muted"),
            html.Div(id="sidebar-total-trades", className="text-info", style={"fontWeight": "bold"}),
        ], className="mb-2"),
        html.Div([
            html.Small("Today's P&L", className="text-muted"),
            html.Div(id="sidebar-daily-pnl", className="text-warning", style={"fontWeight": "bold"}),
        ], className="mb-2"),
        html.Div([
            html.Small("Sharpe Ratio", className="text-muted"),
            html.Div(id="sidebar-sharpe-ratio", className="text-success", style={"fontWeight": "bold"}),
        ], className="mb-2"),
        html.Div([
            html.Small("Max Drawdown", className="text-muted"),
            html.Div(id="sidebar-max-drawdown", className="text-danger", style={"fontWeight": "bold"}),
        ], className="mb-2"),
        dbc.Button([html.I(className="bi bi-graph-up me-1"), "Full Dashboard"], 
                  id="show-performance-dashboard-btn", color="outline-primary", size="sm", className="w-100 mt-2"),
    ]),
    
    # Advanced Tools (Expanded and organized)
    html.Hr(className="border-secondary my-3"),
    html.H5([html.I(className="bi bi-tools me-1 text-primary"), "🔧 Advanced Tools"], className="mb-2"),
    
    # HFT Analysis Tools
    dbc.Collapse([
        html.H6([html.I(className="bi bi-lightning me-1"), "⚡ HFT Analysis"], className="mb-2"),
        dbc.Button("▶️ Start HFT", id="start-hft-analysis-btn", color="success", size="sm", className="mb-1 w-100"),
        dbc.Button("⏹️ Stop HFT", id="stop-hft-analysis-btn", color="danger", size="sm", className="mb-1 w-100"),
        dbc.Badge(id="hft-status-badge", color="secondary", pill=True, className="mb-2 w-100"),
        dbc.Switch(id="hft-enabled-switch", label="Enable HFT", value=False, className="mb-2"),
        html.Div(id="hft-action-output"),
        html.Div(id="hft-config-output"),
    ], id="hft-tools-collapse", is_open=False),
    
    # Data Collection Tools  
    dbc.Collapse([
        html.H6([html.I(className="bi bi-database me-1"), "🗄️ Data Collection"], className="mb-2"),
        dbc.Button("▶️ Start Collection", id="start-data-collection-btn-duplicate", color="success", size="sm", className="mb-1 w-100"),
        dbc.Button("⏹️ Stop Collection", id="stop-data-collection-btn-duplicate", color="danger", size="sm", className="mb-1 w-100"),
        dbc.Badge(id="data-collection-status", color="secondary", pill=True, className="mb-2 w-100"),
        dbc.Switch(id="auto-collection-switch", label="Auto Collection", value=True, className="mb-2"),
        html.Div(id="data-collection-action-output"),
        html.Div(id="collection-config-output"),
    ], id="data-collection-collapse", is_open=False),
    
    # Online Learning Tools
    dbc.Collapse([
        html.H6([html.I(className="bi bi-brain me-1"), "🧠 Online Learning"], className="mb-2"),
        dbc.Button("▶️ Enable Learning", id="enable-online-learning-btn", color="success", size="sm", className="mb-1 w-100"),
        dbc.Button("⏹️ Disable Learning", id="disable-online-learning-btn", color="danger", size="sm", className="mb-1 w-100"),
        dbc.Badge(id="online-learning-status", color="secondary", pill=True, className="mb-2 w-100"),
        dbc.Switch(id="auto-learning-switch", label="Auto Learning", value=True, className="mb-2"),
        html.Div(id="online-learning-action-output"),
        html.Div(id="learning-config-output"),
    ], id="online-learning-collapse", is_open=False),
    
    # Risk Management Tools
    dbc.Collapse([
        html.H6([html.I(className="bi bi-shield me-1"), "⚠️ Risk Management"], className="mb-2"),
        dbc.Button("📊 Calculate Position", id="calculate-position-size-btn", color="primary", size="sm", className="mb-1 w-100"),
        dbc.Button("✅ Check Risk", id="check-trade-risk-btn", color="info", size="sm", className="mb-1 w-100"),
        dbc.Badge(id="risk-status-badge", color="success", pill=True, className="mb-2 w-100"),
        html.Div(id="risk-management-output"),
        html.Div(id="position-sizing-output"),
        html.Div(id="trade-risk-check-output"),
    ], id="risk-management-collapse", is_open=False),
    
    # Notification Tools
    dbc.Collapse([
        html.H6([html.I(className="bi bi-bell me-1"), "📣 Notifications"], className="mb-2"),
        dbc.Button("🔄 Refresh", id="refresh-notifications-btn", color="info", size="sm", className="mb-1 w-100"),
        dbc.Button("🗑️ Clear All", id="clear-notifications-btn", color="warning", size="sm", className="mb-1 w-100"),
        dbc.Badge(id="notification-count", color="danger", pill=True, className="mb-2 w-100"),
        html.Div(id="notification-action-output"),
        html.Div(id="manual-notification-output"),
    ], id="notifications-collapse", is_open=False),
    
    # Email/Alert Tools
    dbc.Collapse([
        html.H6([html.I(className="bi bi-envelope me-1"), "📧 Email/Alerts"], className="mb-2"),
        dbc.Button("✉️ Test Email", id="test-email-btn", color="success", size="sm", className="mb-1 w-100"),
        dbc.Button("� Send Alert", id="send-test-alert-btn", color="warning", size="sm", className="mb-1 w-100"),
        dbc.Switch(id="email-enabled-switch", label="Email Alerts", value=False, className="mb-1"),
        dbc.Switch(id="auto-alerts-switch", label="Auto Alerts", value=True, className="mb-2"),
        html.Div(id="email-config-output"),
        html.Div(id="alert-send-output"),
    ], id="email-alerts-collapse", is_open=False),
    
    # Basic Dev Tools
    dbc.Collapse([
        html.H6([html.I(className="bi bi-code me-1"), "🛠️ Dev Tools"], className="mb-2"),
        dbc.Button("🧪 Test DB", id="test-db-btn", color="outline-secondary", size="sm", className="mb-1 w-100"),
        dbc.Button("🤖 Test ML", id="test-ml-btn", color="outline-secondary", size="sm", className="mb-1 w-100"),
        html.Div(id="test-db-btn-output"),
        html.Div(id="test-ml-btn-output"),
    ], id="dev-tools-collapse", is_open=False),
    
    # Analytics Tools
    html.Hr(className="border-secondary my-3"),
    html.H5([html.I(className="bi bi-graph-up me-1 text-success"), "📊 Analytics"], className="mb-2"),
    
    dbc.Collapse([
        html.H6([html.I(className="bi bi-bar-chart me-1"), "📈 Technical Analysis"], className="mb-2"),
        dbc.Button("📊 Price Chart", id="show-price-chart-btn", color="info", size="sm", className="mb-1 w-100"),
        dbc.Button("📈 Indicators Chart", id="show-indicators-chart-btn", color="info", size="sm", className="mb-1 w-100"),
        dbc.Button("🔄 Refresh Charts", id="refresh-charts-btn", color="primary", size="sm", className="mb-2 w-100"),
        
        # Technical Indicator Cards (moved from futures tab)
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("🎯 RSI", className="mb-1"),
                        html.H5(id="sidebar-rsi-value", className="text-center mb-0"),
                        html.Small(id="sidebar-rsi-signal", className="text-center")
                    ])
                ], style={"backgroundColor": "#3a3a3a", "border": "1px solid #555"})
            ], width=6, className="mb-2"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("⚡ MACD", className="mb-1"),
                        html.H5(id="sidebar-macd-value", className="text-center mb-0"),
                        html.Small(id="sidebar-macd-signal", className="text-center")
                    ])
                ], style={"backgroundColor": "#3a3a3a", "border": "1px solid #555"})
            ], width=6, className="mb-2"),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("🔵 Stochastic", className="mb-1"),
                        html.H5(id="sidebar-stoch-value", className="text-center mb-0"),
                        html.Small(id="sidebar-stoch-signal", className="text-center")
                    ])
                ], style={"backgroundColor": "#3a3a3a", "border": "1px solid #555"})
            ], width=6, className="mb-2"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("📊 ATR", className="mb-1"),
                        html.H5(id="sidebar-atr-value", className="text-center mb-0"),
                        html.Small("Volatility", className="text-center")
                    ])
                ], style={"backgroundColor": "#3a3a3a", "border": "1px solid #555"})
            ], width=6, className="mb-2"),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("🔼 BB Upper", className="mb-1"),
                        html.H5(id="sidebar-bb-upper", className="text-center mb-0"),
                        html.Small("Resistance", className="text-center")
                    ])
                ], style={"backgroundColor": "#3a3a3a", "border": "1px solid #555"})
            ], width=6, className="mb-2"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("🔽 BB Lower", className="mb-1"),
                        html.H5(id="sidebar-bb-lower", className="text-center mb-0"),
                        html.Small("Support", className="text-center")
                    ])
                ], style={"backgroundColor": "#3a3a3a", "border": "1px solid #555"})
            ], width=6, className="mb-2"),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("📈 BB Signal", className="mb-1"),
                        html.H5(id="sidebar-bb-signal", className="text-center mb-0"),
                        html.Small(id="sidebar-bb-middle", className="text-center")
                    ])
                ], style={"backgroundColor": "#3a3a3a", "border": "1px solid #555"})
            ], width=12, className="mb-2"),
        ]),
        html.Div(id="analytics-output"),
    ], id="analytics-collapse", is_open=False),
    
    # ML Tools
    dbc.Collapse([
        html.H6([html.I(className="bi bi-cpu me-1"), "🤖 ML Predictions"], className="mb-2"),
        dbc.Button("🔮 Get AI Prediction", id="sidebar-ml-predict-btn", color="success", size="sm", className="mb-1 w-100"),
        dbc.Button("🧠 Model Status", id="sidebar-ml-status-btn", color="info", size="sm", className="mb-1 w-100"),
        dbc.Button("📊 Feature Importance", id="sidebar-feature-importance-btn", color="primary", size="sm", className="mb-1 w-100"),
        
        # AI Signal Card (moved from futures tab)
        dbc.Card([
            dbc.CardBody([
                html.H6("🤖 AI Signal", className="mb-1"),
                html.H5(id="sidebar-ai-signal", className="text-center mb-0"),
                html.Small(id="sidebar-ai-confidence", className="text-center")
            ])
        ], style={"backgroundColor": "#3a3a3a", "border": "1px solid #555"}, className="mb-2"),
        
        # Model Performance
        html.Div([
            html.H6("📈 Model Performance", className="mb-1"),
            html.Div(id="sidebar-model-performance", className="text-info"),
            html.Div([
                html.Small("Accuracy:", className="text-muted me-2"),
                html.Span(id="sidebar-model-accuracy", className="text-success"),
            ], className="mb-1"),
            html.Div([
                html.Small("Confidence:", className="text-muted me-2"),
                html.Span(id="sidebar-model-confidence", className="text-warning"),
            ], className="mb-1"),
            html.Div([
                html.Small("Status:", className="text-muted me-2"),
                html.Span(id="sidebar-model-status", className="text-info"),
            ], className="mb-2"),
        ], className="mb-2"),
        html.Div(id="ml-tools-output"),
    ], id="ml-tools-collapse", is_open=False),
    
    # Charts Section
    dbc.Collapse([
        html.H6([html.I(className="bi bi-graph-up me-1"), "📈 Advanced Charts"], className="mb-2"),
        dbc.Button("📊 Volume Analysis", id="sidebar-volume-chart-btn", color="info", size="sm", className="mb-1 w-100"),
        dbc.Button("🎯 Momentum Chart", id="sidebar-momentum-chart-btn", color="info", size="sm", className="mb-1 w-100"),
        dbc.Button("📈 Bollinger Bands", id="sidebar-bollinger-btn", color="primary", size="sm", className="mb-1 w-100"),
        
        # Volume and Momentum Cards (moved from futures tab)
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("📈 Volume", className="mb-1"),
                        html.H5(id="sidebar-volume-ratio", className="text-center mb-0"),
                        html.Small(id="sidebar-volume-signal", className="text-center")
                    ])
                ], style={"backgroundColor": "#3a3a3a", "border": "1px solid #555"})
            ], width=6, className="mb-2"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("🎯 Momentum", className="mb-1"),
                        html.H5(id="sidebar-momentum-value", className="text-center mb-0"),
                        html.Small(id="sidebar-momentum-signal", className="text-center")
                    ])
                ], style={"backgroundColor": "#3a3a3a", "border": "1px solid #555"})
            ], width=6, className="mb-2"),
        ]),
        html.Div(id="charts-output"),
    ], id="charts-collapse", is_open=False),
    
    # Toggle buttons for sections
    html.Div([
        dbc.ButtonGroup([
            dbc.Button("⚡", id="toggle-hft-tools", color="outline-info", size="sm", title="Toggle HFT Tools"),
            dbc.Button("�️", id="toggle-data-collection", color="outline-info", size="sm", title="Toggle Data Collection"),
            dbc.Button("🧠", id="toggle-online-learning", color="outline-info", size="sm", title="Toggle Online Learning"),
        ], className="w-100 mb-1"),
        dbc.ButtonGroup([
            dbc.Button("⚠️", id="toggle-risk-management", color="outline-warning", size="sm", title="Toggle Risk Management"),
            dbc.Button("📣", id="toggle-notifications", color="outline-warning", size="sm", title="Toggle Notifications"),
            dbc.Button("📧", id="toggle-email-alerts", color="outline-warning", size="sm", title="Toggle Email/Alerts"),
        ], className="w-100 mb-1"),
        dbc.ButtonGroup([
            dbc.Button("📊", id="toggle-analytics", color="outline-success", size="sm", title="Toggle Analytics"),
            dbc.Button("🤖", id="toggle-ml-tools", color="outline-primary", size="sm", title="Toggle ML Tools"),
            dbc.Button("📈", id="toggle-charts", color="outline-info", size="sm", title="Toggle Charts"),
        ], className="w-100 mb-1"),
        dbc.Button("🛠️ Dev Tools", id="toggle-dev-tools", color="outline-secondary", size="sm", className="w-100"),
    ], className="mt-2"),
    
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
            html.Div(id="sidebar-virtual-balance-main", className="text-center"),
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
                html.Div(id="price-chart", children=[
                    safe_graph("price-chart-graph", figure={})
                ])
            ], className="chart-container"),
        ], width=6),
        dbc.Col([
            html.H4("📈 Technical Indicators"),
            html.Div([
                html.Div(id="indicators-chart", children=[
                    safe_graph("indicators-chart-graph", figure={})
                ])
            ], className="chart-container"),
        ], width=6),
    ], className="mb-4"),
    
    # Hybrid predictions
    html.Div([
        html.H4([html.I(className="bi bi-cpu me-1 text-primary"), "🤖 AI Predictions"]),
        html.Div(id="hybrid-prediction-output"),
        dbc.Button("🔮 Get Prediction", id="get-prediction-btn", color="primary", className="mt-2"),
    ], className="mb-4"),
    
    # Trading Actions
    dbc.Row([
        dbc.Col([
            dbc.Button("💰 Buy", id="buy-btn", color="success", size="lg", className="me-2"),
            dbc.Button("💸 Sell", id="sell-btn", color="danger", size="lg", className="me-2"),
            dbc.Button("🔮 Quick Prediction", id="quick-prediction-btn", color="primary", size="lg"),
        ], width=12),
    ], className="mb-4"),
    
    # Trading Results Area
    html.Div([
        html.H4([html.I(className="bi bi-activity me-1 text-info"), "💹 Trading Activity"], className="mb-3"),
        html.Div(id="trading-results-output")
    ], className="mb-4"),
    
    # AI/ML Model Monitoring Dashboard
    html.Div([
        html.H4([html.I(className="bi bi-brain me-1 text-success"), "🧠 AI/ML Model Dashboard"], className="mb-3"),
        
        # Model Status Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🤖 Model Health"),
                    dbc.CardBody([
                        html.Div(id="model-health-display")
                    ])
                ])
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📊 Model Analytics"),
                    dbc.CardBody([
                        html.Div(id="model-analytics-display")
                    ])
                ])
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📈 Feature Importance"),
                    dbc.CardBody([
                        html.Div(id="feature-importance-display")
                    ])
                ])
            ], width=4),
        ], className="mb-3"),
        
        # Model Management Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🔄 Model Versions"),
                    dbc.CardBody([
                        html.Div(id="model-versions-display"),
                        html.Hr(),
                        html.Div(id="model-version-status")
                    ])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("⚙️ Model Retraining"),
                    dbc.CardBody([
                        html.Div(id="model-retrain-status"),
                        dbc.Progress(id="retrain-progress", value=0, className="mt-2"),
                        html.Div(id="auto-rollback-status", className="mt-2")
                    ])
                ])
            ], width=6),
        ], className="mb-3"),
        
        # Advanced ML Features Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📡 Online Learning"),
                    dbc.CardBody([
                        html.Div(id="online-learning-controls"),
                        html.Div(id="sgd-classifier-status", className="mt-2"),
                        html.Div(id="passive-aggressive-status", className="mt-1"),
                        html.Div(id="perceptron-status", className="mt-1")
                    ])
                ])
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🔍 Drift Detection"),
                    dbc.CardBody([
                        html.Div(id="check-drift-btn-output"),
                        html.Div(id="incremental-learning-buffer", className="mt-2"),
                        html.Div(id="model-adaptation-chart", className="mt-2")
                    ])
                ])
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📊 Performance"),
                    dbc.CardBody([
                        html.Div(id="ml-performance-history"),
                        html.Div(id="learning-rate-optimization", className="mt-2"),
                        html.Div(id="online-learning-trade-integration", className="mt-2")
                    ])
                ])
            ], width=4),
        ], className="mb-3"),
    ], className="mb-4"),
    
    # Enhanced Balance Display
    html.Div([
        html.H4([html.I(className="bi bi-wallet2 me-1 text-success"), "💰 Enhanced Balance Monitor"], className="mb-3"),
        dbc.Card([
            dbc.CardBody([
                html.Div(id="virtual-balance-display", className="text-center"),
                html.Div(id="sidebar-virtual-balance-duplicate", className="text-center"),  # <-- FIXED: Changed duplicate ID
            ])
        ])
    ], className="mb-4"),
    
    # Transfer Learning Dashboard
    html.Div([
        html.H4([html.I(className="bi bi-share me-1 text-info"), "🔄 Transfer Learning"], className="mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("⚙️ Setup & Training"),
                    dbc.CardBody([
                        html.Div(id="transfer-learning-setup"),
                        html.Hr(),
                        html.Div(id="transfer-learning-training")
                    ])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📈 Performance"),
                    dbc.CardBody([
                        html.Div(id="transfer-learning-performance"),
                        html.Div(id="transfer-learning-status", className="mt-2")
                    ])
                ])
            ], width=6),
        ]),
    ], className="mb-4"),
    
    # Comprehensive Backtest Results
    html.Div([
        html.H4([html.I(className="bi bi-graph-up me-1 text-warning"), "📊 Enhanced Backtest Results"], className="mb-3"),
        dbc.Card([
            dbc.CardBody([
                html.Div(id="comprehensive-backtest-output"),
                dbc.Progress(id="backtest-progress", value=0, className="mt-2"),
                html.Div(id="backtest-results-enhanced", className="mt-3")
            ])
        ])
    ], className="mb-4"),
    
    # HFT Analysis Dashboard
    html.Div([
        html.H4([html.I(className="bi bi-lightning me-1 text-danger"), "⚡ HFT Analysis"], className="mb-3"),
        dbc.Row([
            dbc.Col([
                html.Div(id="hft-analysis-display")
            ], width=8),
            dbc.Col([
                html.Div(id="hft-stats-cards")
            ], width=4),
        ]),
    ], className="mb-4"),
    
    # Risk Management Dashboard
    html.Div([
        html.H4([html.I(className="bi bi-shield me-1 text-warning"), "⚠️ Risk Management"], className="mb-3"),
        dbc.Row([
            dbc.Col([
                html.Div(id="risk-settings-display")
            ], width=6),
            dbc.Col([
                html.Div(id="risk-settings-status")
            ], width=6),
        ]),
    ], className="mb-4"),
    
    # Notification System Dashboard
    html.Div([
        html.H4([html.I(className="bi bi-bell me-1 text-primary"), "📢 Notification System"], className="mb-3"),
        dbc.Card([
            dbc.CardBody([
                html.Div(id="notification-send-status"),
                html.Div(id="clear-notifications-status", className="mt-2")
            ])
        ])
    ], className="mb-4"),
    
    # Data Collection Controls
    html.Div([
        html.H4([html.I(className="bi bi-database me-1 text-info"), "🗄️ Data Collection"], className="mb-3"),
        dbc.Card([
            dbc.CardBody([
                html.Div(id="data-collection-controls")
            ])
        ])
    ], className="mb-4"),
    
    # Advanced Trading Features 
    html.Div([
        html.H4([html.I(className="bi bi-gear me-1 text-secondary"), "🔧 Advanced Features"], className="mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🔧 Feature Controls"),
                    dbc.CardBody([
                        html.Div(id="show-fi-btn-output"),
                        html.Div(id="prune-trades-btn-output", className="mt-1"),
                        html.Div(id="tune-models-btn-output", className="mt-1"),
                        html.Div(id="online-learn-btn-output", className="mt-1"),
                        html.Div(id="refresh-model-versions-btn-output", className="mt-1")
                    ])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📊 Analytics"),
                    dbc.CardBody([
                        html.Div(id="futures-analytics-display"),
                        html.Div(id="pnl-analytics-display", className="mt-2"),
                        html.Div(id="check-auto-alerts-result", className="mt-2")
                    ])
                ])
            ], width=6),
        ]),
    ], className="mb-4"),

    

    

    
])

# Performance Monitoring Dashboard tab content
performance_dashboard_tab = html.Div([
    html.H2([html.I(className="bi bi-graph-up me-2 text-success"), "📊 Performance Monitoring Dashboard"], className="mb-4"),
    
    # Key metrics row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4([html.I(className="bi bi-trophy me-1 text-warning"), "Win Rate"], className="mb-2"),
                    html.H2(id="perf-win-rate", className="text-success", style={"fontWeight": "bold"}),
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4([html.I(className="bi bi-currency-dollar me-1 text-success"), "Total P&L"], className="mb-2"),
                    html.H2(id="perf-total-pnl", className="text-info", style={"fontWeight": "bold"}),
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4([html.I(className="bi bi-graph-up me-1 text-primary"), "Sharpe Ratio"], className="mb-2"),
                    html.H2(id="perf-sharpe-ratio", className="text-primary", style={"fontWeight": "bold"}),
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4([html.I(className="bi bi-graph-down me-1 text-danger"), "Max Drawdown"], className="mb-2"),
                    html.H2(id="perf-max-drawdown", className="text-danger", style={"fontWeight": "bold"}),
                ])
            ])
        ], width=3),
    ], className="mb-4"),
    
    # Performance charts row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([html.I(className="bi bi-graph-up me-1"), "P&L Over Time"], className="mb-0"),
                ]),
                dbc.CardBody([
                    html.Div([
                        safe_graph("pnl-chart", figure={})
                    ], className="chart-container"),
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([html.I(className="bi bi-pie-chart me-1"), "Trade Distribution"], className="mb-0"),
                ]),
                dbc.CardBody([
                    html.Div([
                        safe_graph("trade-distribution-chart", figure={})
                    ], className="chart-container"),
                ])
            ])
        ], width=6),
    ], className="mb-4"),
    
    # Advanced metrics row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([html.I(className="bi bi-speedometer me-1"), "Risk Metrics"], className="mb-0"),
                ]),
                dbc.CardBody([
                    html.Div(id="risk-metrics-display"),
                ])
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([html.I(className="bi bi-clock me-1"), "Time Analysis"], className="mb-0"),
                ]),
                dbc.CardBody([
                    html.Div(id="time-analysis-display"),
                ])
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([html.I(className="bi bi-list me-1"), "Recent Performance"], className="mb-0"),
                ]),
                dbc.CardBody([
                    html.Div(id="recent-performance-display", style={"maxHeight": "300px", "overflowY": "auto"}),
                ])
            ])
        ], width=4),
    ], className="mb-4"),
    
    # Control panel
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([html.I(className="bi bi-gear me-1"), "Dashboard Controls"], className="mb-0"),
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Timeframe"),
                            dcc.Dropdown(
                                id="perf-timeframe-dropdown",
                                options=[
                                    {"label": "1 Hour", "value": "1h"},
                                    {"label": "1 Day", "value": "1d"},
                                    {"label": "1 Week", "value": "1w"},
                                    {"label": "1 Month", "value": "1m"},
                                    {"label": "All Time", "value": "all"}
                                ],
                                value="1d",
                                clearable=False
                            )
                        ], width=3),
                        dbc.Col([
                            dbc.Label("Update Frequency"),
                            dcc.Dropdown(
                                id="perf-update-frequency",
                                options=[
                                    {"label": "Real-time", "value": "1s"},
                                    {"label": "Every 5 seconds", "value": "5s"},
                                    {"label": "Every 30 seconds", "value": "30s"},
                                    {"label": "Every minute", "value": "1m"}
                                ],
                                value="30s",
                                clearable=False
                            )
                        ], width=3),
                        dbc.Col([
                            dbc.Label(" ", style={"visibility": "hidden"}),
                            dbc.Button([html.I(className="bi bi-download me-1"), "Export Report"], 
                                      id="export-performance-btn", color="primary", className="w-100")
                        ], width=3),
                        dbc.Col([
                            dbc.Label(" ", style={"visibility": "hidden"}),
                            dbc.Button([html.I(className="bi bi-refresh me-1"), "Refresh Now"], 
                                      id="refresh-performance-btn", color="info", className="w-100")
                        ], width=3),
                    ]),
                ])
            ])
        ], width=12),
    ]),
])

# Auto Trading tab content - Use the full layout
auto_trading_tab = create_auto_trading_layout()

# Futures Trading tab content - Use the full layout
futures_trading_tab = create_futures_trading_layout()

# Binance Exact tab content - Use the full layout
binance_exact_tab = create_binance_exact_layout()

# Email Config tab content - Use the full layout
email_config_tab = create_email_config_layout()

# Hybrid Learning tab content - Use the full layout
hybrid_learning_tab = create_hybrid_learning_layout()

# ADVANCED FEATURES TAB - NEW ENDPOINTS
advanced_features_tab = html.Div([
    html.H2([html.I(className="bi bi-gear me-2 text-info"), "⚙️ Advanced Features"], className="mb-4"),
    
    # Chart Controls Section
    dbc.Card([
        dbc.CardHeader("📊 Chart Controls"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button("🔄 Refresh Charts", id="chart-refresh-btn", color="primary", size="sm"),
                    html.Div(id="chart-refresh-status", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("📈 Bollinger Bands", id="chart-bollinger-btn", color="info", size="sm"),
                    html.Div(id="chart-bollinger-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("⚡ Momentum", id="chart-momentum-btn", color="warning", size="sm"),
                    html.Div(id="chart-momentum-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("📊 Volume", id="chart-volume-btn", color="success", size="sm"),
                    html.Div(id="chart-volume-data", className="mt-2")
                ], width=3)
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Button("📈 Show Indicators", id="chart-show-indicators-btn", color="secondary", size="sm"),
                    html.Div(id="chart-indicators-status", className="mt-2")
                ], width=6),
                dbc.Col([
                    dbc.Button("💹 Show Price", id="chart-show-price-btn", color="secondary", size="sm"),
                    html.Div(id="chart-price-status", className="mt-2")
                ], width=6)
            ])
        ])
    ], className="mb-4"),
    
    # HFT Analytics Section
    dbc.Card([
        dbc.CardHeader("⚡ High Frequency Trading Analytics"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button("📊 HFT Analytics", id="hft-analytics-btn", color="primary", size="sm"),
                    html.Div(id="hft-analytics-data", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Button("⚙️ HFT Config", id="hft-config-btn", color="info", size="sm"),
                    html.Div(id="hft-config-status", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Button("🎯 Opportunities", id="hft-opportunities-btn", color="warning", size="sm"),
                    html.Div(id="hft-opportunities-data", className="mt-2")
                ], width=4)
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Button("▶️ Start HFT", id="hft-start-btn", color="success", size="sm"),
                    html.Div(id="hft-start-status", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Button("⏹️ Stop HFT", id="hft-stop-btn", color="danger", size="sm"),
                    html.Div(id="hft-stop-status", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Button("📊 Status", id="hft-status-btn", color="secondary", size="sm"),
                    html.Div(id="hft-status-display", className="mt-2")
                ], width=4)
            ])
        ])
    ], className="mb-4"),
    
    # Performance & Portfolio Section
    dbc.Card([
        dbc.CardHeader("📈 Performance & Portfolio Analytics"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button("📊 Performance Dashboard", id="performance-dashboard-btn", color="primary", size="sm"),
                    html.Div(id="performance-dashboard-data", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Button("📊 Performance Metrics", id="performance-metrics-btn", color="info", size="sm"),
                    html.Div(id="performance-metrics-data", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Button("💼 Portfolio", id="portfolio-btn", color="warning", size="sm"),
                    html.Div(id="portfolio-data", className="mt-2")
                ], width=4)
            ])
        ])
    ], className="mb-4"),
    
    # Advanced ML Section
    dbc.Card([
        dbc.CardHeader("🧠 Advanced Machine Learning"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button("🔍 ML Compatibility", id="ml-compatibility-check-btn", color="primary", size="sm"),
                    html.Div(id="ml-compatibility-check-data", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Button("🔧 Fix ML Issues", id="ml-compatibility-fix-btn", color="danger", size="sm"),
                    html.Div(id="ml-compatibility-fix-status", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Button("💡 ML Recommendations", id="ml-recommendations-btn", color="info", size="sm"),
                    html.Div(id="ml-recommendations-data", className="mt-2")
                ], width=4)
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Button("⚙️ Online ML Config", id="ml-online-config-btn", color="secondary", size="sm"),
                    html.Div(id="ml-online-config-data", className="mt-2")
                ], width=6),
                dbc.Col([
                    dbc.Button("📊 Online ML Performance", id="ml-online-performance-btn", color="success", size="sm"),
                    html.Div(id="ml-online-performance-data", className="mt-2")
                ], width=6)
            ])
        ])
    ], className="mb-4"),
    
    # Risk Management Section
    dbc.Card([
        dbc.CardHeader("⚠️ Advanced Risk Management"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Input(id="risk-amount-input", type="number", placeholder="Amount", value=1000),
                    dbc.Button("📏 Calculate Position Size", id="risk-position-size-btn", color="primary", size="sm", className="mt-2"),
                    html.Div(id="risk-position-size-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("🔍 Check Trade Risk", id="risk-trade-check-btn", color="warning", size="sm"),
                    html.Div(id="risk-trade-check-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("📊 Portfolio Risk", id="risk-portfolio-metrics-btn", color="info", size="sm"),
                    html.Div(id="risk-portfolio-metrics-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("🛑 Stop Loss Strategies", id="risk-stop-loss-btn", color="danger", size="sm"),
                    html.Div(id="risk-stop-loss-data", className="mt-2")
                ], width=3)
            ])
        ])
    ], className="mb-4"),
    
    # Auto Trading Controls Section
    dbc.Card([
        dbc.CardHeader("🤖 Auto Trading Controls"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button("🔄 Toggle Auto Trading", id="auto-trading-toggle-btn", color="primary", size="sm"),
                    html.Div(id="auto-trading-toggle-status", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("⚙️ Trading Settings", id="auto-trading-settings-btn", color="info", size="sm"),
                    html.Div(id="auto-trading-settings-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("📊 Trading Signals", id="auto-trading-signals-btn", color="warning", size="sm"),
                    html.Div(id="auto-trading-signals-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("📈 Trading Status", id="auto-trading-status-refresh-btn", color="success", size="sm"),
                    html.Div(id="auto-trading-status-display", className="mt-2")
                ], width=3)
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Button("⚡ Execute Futures Signal", id="futures-execute-signal-btn", color="danger", size="sm"),
                    html.Div(id="futures-execute-signal-status", className="mt-2")
                ], width=6),
                dbc.Col([
                    dbc.Button("🔥 Binance Auto Execute", id="binance-auto-execute-btn", color="warning", size="sm"),
                    html.Div(id="binance-auto-execute-status", className="mt-2")
                ], width=6)
            ])
        ])
    ], className="mb-4"),
    
    # Email & Notifications Section
    dbc.Card([
        dbc.CardHeader("📧 Email & Notifications"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button("⚙️ Email Config", id="email-config-btn", color="primary", size="sm"),
                    html.Div(id="email-config-status", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("✉️ Test Email", id="email-test-btn", color="info", size="sm"),
                    html.Div(id="email-test-status", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("🔔 Toggle Notifications", id="email-notifications-toggle-btn", color="warning", size="sm"),
                    html.Div(id="email-notifications-status", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Input(id="email-address-input", type="email", placeholder="Email Address"),
                    dbc.Button("📧 Update Email", id="email-address-update-btn", color="success", size="sm", className="mt-2"),
                    html.Div(id="email-address-status", className="mt-2")
                ], width=3)
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Button("🗑️ Clear Notifications", id="notifications-clear-btn", color="danger", size="sm"),
                    html.Div(id="notifications-clear-status", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Button("✅ Mark All Read", id="notifications-mark-read-btn", color="success", size="sm"),
                    html.Div(id="notifications-mark-read-status", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Input(id="manual-alert-message", type="text", placeholder="Alert message"),
                    dbc.Button("📢 Send Alert", id="manual-alert-btn", color="warning", size="sm", className="mt-2"),
                    html.Div(id="manual-alert-status", className="mt-2")
                ], width=4)
            ])
        ])
    ], className="mb-4"),
    
    # Trading Controls Section
    dbc.Card([
        dbc.CardHeader("💰 Trading Controls"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Input(id="trade-symbol-input", type="text", placeholder="Symbol", value="BTCUSDT"),
                    dbc.Select(id="trade-side-dropdown", options=[
                        {"label": "BUY", "value": "BUY"},
                        {"label": "SELL", "value": "SELL"}
                    ], value="BUY"),
                    dbc.Button("💰 Execute Trade", id="trade-execute-btn", color="success", size="sm", className="mt-2"),
                    html.Div(id="trade-execute-status", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("📊 All Trades", id="trades-list-btn", color="info", size="sm"),
                    html.Div(id="trades-list-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("📈 Futures History", id="futures-history-btn", color="warning", size="sm"),
                    html.Div(id="futures-history-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("🔓 Open Futures", id="futures-open-btn", color="primary", size="sm"),
                    html.Div(id="futures-open-data", className="mt-2")
                ], width=3)
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Button("🔄 Reset Virtual Balance", id="virtual-balance-reset-btn", color="danger", size="sm"),
                    html.Div(id="virtual-balance-reset-status", className="mt-2")
                ], width=6),
                dbc.Col([
                    dbc.Button("📊 Test Email Alert", id="test-email-alert-btn", color="info", size="sm"),
                    html.Div(id="test-email-alert-status", className="mt-2")
                ], width=6)
            ])
        ])
    ], className="mb-4"),
    
    # Quick Amount Selection
    dbc.Card([
        dbc.CardHeader("💰 Quick Amount Selection"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button("$50", id="amount-50-btn", color="outline-primary", size="sm"),
                    html.Div(id="amount-50-status", className="mt-2")
                ], width=2),
                dbc.Col([
                    dbc.Button("$100", id="amount-100-btn", color="outline-primary", size="sm"),
                    html.Div(id="amount-100-status", className="mt-2")
                ], width=2),
                dbc.Col([
                    dbc.Button("$250", id="amount-250-btn", color="outline-primary", size="sm"),
                    html.Div(id="amount-250-status", className="mt-2")
                ], width=2),
                dbc.Col([
                    dbc.Button("$500", id="amount-500-btn", color="outline-primary", size="sm"),
                    html.Div(id="amount-500-status", className="mt-2")
                ], width=2),
                dbc.Col([
                    dbc.Button("$1000", id="amount-1000-btn", color="outline-primary", size="sm"),
                    html.Div(id="amount-1000-status", className="mt-2")
                ], width=2),
                dbc.Col([
                    dbc.Button("MAX", id="amount-max-btn", color="outline-warning", size="sm"),
                    html.Div(id="amount-max-status", className="mt-2")
                ], width=2)
            ])
        ])
    ])
])

# Tabs component
tabs = dcc.Tabs([
    dcc.Tab(label="📊 Dashboard", children=[dashboard_tab], value="dashboard"),
    dcc.Tab(label="🤖 Auto Trading", children=[auto_trading_tab], value="auto-trading"),
    dcc.Tab(label="📈 Futures Trading", children=[futures_trading_tab], value="futures-trading"),
    dcc.Tab(label="🔗 Binance-Exact API", children=[binance_exact_tab], value="binance-exact"),
    dcc.Tab(label="✉️ Email Config", children=[email_config_tab], value="email-config"),
    dcc.Tab(label="🧠 Hybrid Learning", children=[hybrid_learning_tab], value="hybrid-learning"),
    dcc.Tab(label="📊 Performance Monitor", children=[performance_dashboard_tab], value="performance-monitor"),
    dcc.Tab(label="⚙️ Advanced Features", children=[advanced_features_tab], value="advanced-features"),
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

    # Missing callback output components (auto-generated)
    html.Div(id="auto-balance-display", style={"display": "none"}),
    html.Div(id="auto-pnl-display", style={"display": "none"}),
    html.Div(id="auto-trade-log", style={"display": "none"}),
    html.Div(id="auto-trades-display", style={"display": "none"}),
    html.Div(id="auto-trading-toggle-output", style={"display": "none"}),
    html.Div(id="auto-winrate-display", style={"display": "none"}),
    html.Div(id="auto-wl-display", style={"display": "none"}),
    html.Div(id="calculated-amount-display", style={"display": "none"}),
    html.Div(id="chart-candles-data", style={"display": "none"}),
    html.Div(id="current-signal-display", style={"display": "none"}),
    html.Div(id="execute-signal-btn", style={"display": "none"}),
    html.Div(id="fapi-account-data", style={"display": "none"}),
    html.Div(id="fapi-balance-data", style={"display": "none"}),
    html.Div(id="fapi-exchange-info-data", style={"display": "none"}),
    html.Div(id="fapi-position-risk-data", style={"display": "none"}),
    html.Div(id="fapi-ticker-data", style={"display": "none"}),
    html.Div(id="fixed-amount-section", style={"display": "none"}),
    html.Div(id="futures-available-balance", style={"display": "none"}),    html.Div(id="futures-margin-ratio", style={"display": "none"}),
    html.Div(id="futures-margin-used", style={"display": "none"}),
    html.Div(id="futures-open-positions", style={"display": "none"}),
    html.Div(id="futures-pnl-display", style={"display": "none"}),    html.Div(id="futures-reset-balance-btn", style={"display": "none"}),
    html.Div(id="futures-settings-result", style={"display": "none"}),    html.Div(id="futures-trading-status", style={"display": "none"}),
    html.Div(id="futures-unrealized-pnl", style={"display": "none"}),    html.Div(id="futures-virtual-total-balance", style={"display": "none"}),
    html.Div(id="indicators-config-data", style={"display": "none"}),
    html.Div(id="indicators-refresh-status", style={"display": "none"}),
    html.Div(id="model-analytics-data", style={"display": "none"}),
    html.Div(id="model-upload-status-data", style={"display": "none"}),
    html.Div(id="open-positions-table", style={"display": "none"}),
    html.Div(id="optimize-gala-btn", style={"display": "none"}),
    html.Div(id="optimize-jasmy-btn", style={"display": "none"}),
    html.Div(id="optimize-kaia-btn", style={"display": "none"}),
    html.Div(id="percentage-amount-section", style={"display": "none"}),
    html.Div(id="percentage-amount-slider", style={"display": "none"}),
    html.Div(id="price-chart-hidden", style={"display": "none"}),
    html.Div(id="price-general-data", style={"display": "none"}),
    html.Div(id="reset-auto-trading-btn", style={"display": "none"}),
    html.Div(id="retrain-model-status", style={"display": "none"}),
    html.Div(id="system-health-data", style={"display": "none"}),
    html.Div(id="test-output", style={"display": "none"}),
    html.Div(id="backtest-result", style={"display": "none"}),
    
    # Hidden futures callback outputs
    html.Div(id="futures-reset-balance-output", style={"display": "none"}),
    html.Div(id="futures-sync-balance-output", style={"display": "none"}),
    
    # Hidden HFT analysis outputs (moved to sidebar)
    html.Div(id="hft-analysis-chart", style={"display": "none"}),
    html.Div(id="hft-stats", style={"display": "none"}),
    
    # Hidden tab content divs for dynamic loading
    html.Div(id="hybrid-learning-tab-content", style={"display": "none"}),
    html.Div(id="email-config-tab-content", style={"display": "none"}),
    html.Div(id="auto-trading-tab-content", style={"display": "none"}),
    html.Div(id="futures-trading-tab-content", style={"display": "none"}),
    html.Div(id="binance-exact-tab-content", style={"display": "none"}),
    
    # Hidden futures trading components    html.Div(id="futures-rsi-indicator", style={"display": "none"}),
    html.Div(id="futures-macd-indicator", style={"display": "none"}),
    html.Div(id="futures-bollinger-indicator", style={"display": "none"}),
    html.Div(id="futures-stochastic-indicator", style={"display": "none"}),
    html.Div(id="futures-atr-indicator", style={"display": "none"}),
    html.Div(id="futures-volume-indicator", style={"display": "none"}),
    html.Div(id="futures-technical-chart", style={"display": "none"}),
    
    # Hidden AI/ML model management outputs
    html.Div(id="model-metrics-display", style={"display": "none"}),
    html.Div(id="hybrid-status-display", style={"display": "none"}),
    html.Div(id="refresh-hft-btn", style={"display": "none"}),
    html.Div(id="save-hft-config-btn", style={"display": "none"}),
    html.Div(id="hft-interval-input", style={"display": "none"}),
    html.Div(id="hft-threshold-input", style={"display": "none"}),
    html.Div(id="hft-max-orders-input", style={"display": "none"}),
    
    # Hidden data collection outputs (moved to sidebar)
    html.Div(id="data-collection-stats", style={"display": "none"}),
    html.Div(id="refresh-data-collection-btn", style={"display": "none"}),
    html.Div(id="save-collection-config-btn", style={"display": "none"}),
    html.Div(id="collection-interval-input", style={"display": "none"}),
    html.Div(id="collection-symbols-input", style={"display": "none"}),
    
    # Hidden online learning outputs (moved to sidebar)
    html.Div(id="update-online-models-btn", style={"display": "none"}),
    html.Div(id="save-learning-config-btn", style={"display": "none"}),
    html.Div(id="learning-rate-input", style={"display": "none"}),
    html.Div(id="batch-size-input", style={"display": "none"}),
    html.Div(id="update-frequency-input", style={"display": "none"}),
    html.Div(id="model-performance-display", style={"display": "none"}),
    html.Div(id="model-performance-chart", style={"display": "none"}),
    html.Div(id="learning-buffer-status", style={"display": "none"}),
    html.Div(id="online-learning-stats", style={"display": "none"}),
    
    # Hidden advanced risk management outputs (moved to sidebar)
    html.Div(id="refresh-risk-btn", style={"display": "none"}),
    html.Div(id="portfolio-risk-percent", style={"display": "none"}),
    html.Div(id="current-drawdown-percent", style={"display": "none"}),
    html.Div(id="risk-score-value", style={"display": "none"}),
    html.Div(id="open-positions-count", style={"display": "none"}),
    html.Div(id="risk-tabs", style={"display": "none"}),
    html.Div(id="risk-tab-content", style={"display": "none"}),
    html.Div(id="risk-alerts-display", style={"display": "none"}),
    html.Div(id="stop-loss-strategy-output", style={"display": "none"}),
    
    # Hidden notification outputs (moved to sidebar)
    html.Div(id="test-notification-btn", style={"display": "none"}),
    dbc.Collapse(id="manual-notification-collapse", is_open=False, children=[]),
    html.Div(id="manual-notification-type", style={"display": "none"}),
    html.Div(id="manual-notification-message", style={"display": "none"}),
    html.Div(id="send-manual-notification-btn", style={"display": "none"}),
    html.Div(id="notifications-display", style={"display": "none"}),
    html.Div(id="show-unread-only", style={"display": "none"}),
    html.Div(id="notification-stats", style={"display": "none"}),
    
    # Hidden email/alert outputs (moved to sidebar)
    html.Div(id="smtp-server-input", style={"display": "none"}),
    html.Div(id="smtp-port-input", style={"display": "none"}),
    html.Div(id="email-address-input", style={"display": "none"}),
    html.Div(id="email-password-input", style={"display": "none"}),
    html.Div(id="save-email-config-btn", style={"display": "none"}),
    html.Div(id="email-test-result", style={"display": "none"}),
    html.Div(id="profit-threshold-input", style={"display": "none"}),
    html.Div(id="loss-threshold-input", style={"display": "none"}),
    html.Div(id="check-auto-alerts-btn", style={"display": "none"}),
    html.Div(id="alert-test-result", style={"display": "none"}),
    html.Div(id="clear-alert-history-btn", style={"display": "none"}),
    html.Div(id="alert-history-display", style={"display": "none"}),
    html.Div(id="alert-stats", style={"display": "none"}),
    
    # Original hidden outputs
    html.Div(id="notification-action-output", style={"display": "none"}),
    html.Div(id="manual-notification-output", style={"display": "none"}),
    html.Div(id="email-config-output", style={"display": "none"}),
    html.Div(id="email-test-output", style={"display": "none"}),
    html.Div(id="alert-send-output", style={"display": "none"}),
    html.Div(id="alert-history-action-output", style={"display": "none"}),
    html.Div(id="hft-action-output", style={"display": "none"}),
    html.Div(id="hft-config-output", style={"display": "none"}),
    html.Div(id="data-collection-action-output", style={"display": "none"}),
    html.Div(id="collection-config-output", style={"display": "none"}),
    html.Div(id="online-learning-action-output", style={"display": "none"}),
    html.Div(id="learning-config-output", style={"display": "none"}),
    html.Div(id="risk-management-output", style={"display": "none"}),
    html.Div(id="position-sizing-output", style={"display": "none"}),
    html.Div(id="trade-risk-check-output", style={"display": "none"}),
    html.Div(id="performance-dashboard-output", style={"display": "none"}),
    html.Div(id="export-performance-output", style={"display": "none"}),
    
    # Hidden inputs wrapped in divs to avoid style prop issues
    html.Div([
        dcc.Dropdown(id="auto-symbol-dropdown"),
        dcc.Input(id="fixed-amount-input", type="number", value=100),
        dcc.Input(id="percentage-amount-input", type="number", value=10),
    ], style={"display": "none"}),
], style={"display": "none"})

# --- FIX: Use correct Dash components for callback compatibility ---
hidden_callback_components = [
    dcc.Checklist(id="show-unread-only", options=[{"label": "Show Unread Only", "value": "unread"}], value=[], style={"display": "none"}),
    dcc.Input(id="email-password-input", type="password", style={"display": "none"}),
    dcc.Input(id="email-address-input", type="email", style={"display": "none"}),
    dcc.Input(id="smtp-port-input", type="number", style={"display": "none"}),
    dcc.Input(id="smtp-server-input", type="text", style={"display": "none"}),
    dcc.Textarea(id="manual-notification-message", style={"display": "none"}),
    dcc.Input(id="manual-notification-type", type="text", style={"display": "none"}),
    dcc.Graph(id="futures-technical-chart", style={"display": "none"}),
]
# --- END FIX ---

# CSS for chart dimension constraints - Add to app external stylesheets
chart_constraints_css = """
/* Chart Container Constraints */
.chart-container {
    max-height: 400px !important;
    overflow: hidden;
}

/* Graph components should not exceed container height */
.js-plotly-plot .plotly .main-svg {
    max-height: 400px !important;
}

/* Prevent chart expansion beyond container */
.dash-graph {
    max-height: 400px !important;
    height: 400px !important;
}

/* Ensure responsive behavior without expansion */
.plotly-graph-div {
    max-height: 400px !important;
    height: 400px !important;
}
"""

# Main layout
layout = html.Div([
    stores_and_intervals,
    
    # Navigation bar
    dbc.Navbar(
        dbc.Container([

            html.Span([

                html.I(className="bi bi-robot me-2 text-success"), 
                "🚀 Crypto Trading Bot Dashboard"
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
        *hidden_callback_components,
    ], style={
        "marginLeft": "350px", 
        "padding": "1em", 
        "minHeight": "100vh", 
        "backgroundColor": "#2a2a2a"
    }, className="main-content"),
    
    # Hidden callback output divs
    html.Div([
        html.Div(id='sidebar-amount-50-output', style={'display': 'none'}),
        html.Div(id='sidebar-amount-100-output', style={'display': 'none'}),
        html.Div(id='sidebar-amount-250-output', style={'display': 'none'}),
        html.Div(id='sidebar-amount-500-output', style={'display': 'none'}),
        html.Div(id='sidebar-amount-1000-output', style={'display': 'none'}),
        html.Div(id='sidebar-amount-max-output', style={'display': 'none'}),
        html.Div(id='sidebar-amount-50-btn-output', style={'display': 'none'}),
        html.Div(id='sidebar-amount-100-btn-output', style={'display': 'none'}),
        html.Div(id='sidebar-amount-250-btn-output', style={'display': 'none'}),
        html.Div(id='sidebar-amount-500-btn-output', style={'display': 'none'}),
        html.Div(id='sidebar-amount-1000-btn-output', style={'display': 'none'}),
        html.Div(id='sidebar-amount-max-btn-output', style={'display': 'none'}),
        html.Div(id='amount-50-btn-output', style={'display': 'none'}),
        html.Div(id='amount-100-btn-output', style={'display': 'none'}),
        html.Div(id='amount-250-btn-output', style={'display': 'none'}),
        html.Div(id='amount-500-btn-output', style={'display': 'none'}),
        html.Div(id='amount-1000-btn-output', style={'display': 'none'}),
        html.Div(id='amount-max-btn-output', style={'display': 'none'}),
        html.Div(id='sidebar-predict-output', style={'display': 'none'}),
        html.Div(id='sidebar-analytics-output', style={'display': 'none'}),
        html.Div(id='test-ml-output', style={'display': 'none'}),
        html.Div(id='reset-balance-output', style={'display': 'none'}),
        html.Div(id='enable-online-learning-output', style={'display': 'none'}),
        html.Div(id='get-prediction-btn-output', style={'display': 'none'}),
        html.Div(id='quick-prediction-btn-output', style={'display': 'none'}),
        html.Div(id='buy-btn-output', style={'display': 'none'}),
        html.Div(id='sell-btn-output', style={'display': 'none'}),
        html.Div(id='trade-execute-btn-output', style={'display': 'none'}),
        html.Div(id='trades-list-btn-output', style={'display': 'none'}),
        html.Div(id='auto-trading-toggle-btn-output', style={'display': 'none'}),
        html.Div(id='auto-trading-settings-btn-output', style={'display': 'none'}),
        html.Div(id='auto-trading-signals-btn-output', style={'display': 'none'}),
        html.Div(id='auto-trading-status-refresh-btn-output', style={'display': 'none'}),
        html.Div(id='futures-execute-signal-btn-output', style={'display': 'none'}),
        html.Div(id='futures-history-btn-output', style={'display': 'none'}),
        html.Div(id='futures-open-btn-output', style={'display': 'none'}),
        html.Div(id='binance-auto-execute-btn-output', style={'display': 'none'}),
        html.Div(id='show-price-chart-btn-output', style={'display': 'none'}),
        html.Div(id='show-indicators-chart-btn-output', style={'display': 'none'}),
        html.Div(id='refresh-charts-btn-output', style={'display': 'none'}),
        html.Div(id='chart-refresh-btn-output', style={'display': 'none'}),
        html.Div(id='chart-bollinger-btn-output', style={'display': 'none'}),
        html.Div(id='chart-momentum-btn-output', style={'display': 'none'}),
        html.Div(id='chart-volume-btn-output', style={'display': 'none'}),
        html.Div(id='chart-show-indicators-btn-output', style={'display': 'none'}),
        html.Div(id='chart-show-price-btn-output', style={'display': 'none'}),
        html.Div(id='show-bollinger-btn-output', style={'display': 'none'}),
        html.Div(id='show-momentum-btn-output', style={'display': 'none'}),
        html.Div(id='show-volume-btn-output', style={'display': 'none'}),
        html.Div(id='sidebar-ml-predict-btn-output', style={'display': 'none'}),
        html.Div(id='sidebar-ml-status-btn-output', style={'display': 'none'}),
        html.Div(id='sidebar-feature-importance-btn-output', style={'display': 'none'}),
        html.Div(id='sidebar-volume-chart-btn-output', style={'display': 'none'}),
        html.Div(id='sidebar-momentum-chart-btn-output', style={'display': 'none'}),
        html.Div(id='sidebar-bollinger-btn-output', style={'display': 'none'}),
        html.Div(id='toggle-hft-tools-output', style={'display': 'none'}),
        html.Div(id='toggle-data-collection-output', style={'display': 'none'}),
        html.Div(id='toggle-online-learning-output', style={'display': 'none'}),
        html.Div(id='toggle-risk-management-output', style={'display': 'none'}),
        html.Div(id='toggle-notifications-output', style={'display': 'none'}),
        html.Div(id='toggle-email-alerts-output', style={'display': 'none'}),
        html.Div(id='toggle-analytics-output', style={'display': 'none'}),
        html.Div(id='toggle-ml-tools-output', style={'display': 'none'}),
        html.Div(id='toggle-charts-output', style={'display': 'none'}),
        html.Div(id='toggle-dev-tools-output', style={'display': 'none'}),
        html.Div(id='start-hft-analysis-btn-output', style={'display': 'none'}),
        html.Div(id='stop-hft-analysis-btn-output', style={'display': 'none'}),
        html.Div(id='hft-analytics-btn-output', style={'display': 'none'}),
        html.Div(id='hft-config-btn-output', style={'display': 'none'}),
        html.Div(id='hft-opportunities-btn-output', style={'display': 'none'}),
        html.Div(id='hft-start-btn-output', style={'display': 'none'}),
        html.Div(id='hft-stop-btn-output', style={'display': 'none'}),
        html.Div(id='hft-status-btn-output', style={'display': 'none'}),
        html.Div(id='hft-analytics-refresh-btn-output', style={'display': 'none'}),
        html.Div(id='start-data-collection-btn-duplicate-output', style={'display': 'none'}),
        html.Div(id='stop-data-collection-btn-duplicate-output', style={'display': 'none'}),
        html.Div(id='enable-online-learning-btn-output', style={'display': 'none'}),
        html.Div(id='disable-online-learning-btn-output', style={'display': 'none'}),
        html.Div(id='optimize-learning-rates-btn-output', style={'display': 'none'}),
        html.Div(id='reset-learning-rates-btn-output', style={'display': 'none'}),
        html.Div(id='ml-online-config-btn-output', style={'display': 'none'}),
        html.Div(id='ml-online-performance-btn-output', style={'display': 'none'}),
        html.Div(id='calculate-position-size-btn-output', style={'display': 'none'}),
        html.Div(id='check-trade-risk-btn-output', style={'display': 'none'}),
        html.Div(id='update-risk-settings-btn-output', style={'display': 'none'}),
        html.Div(id='risk-position-size-btn-output', style={'display': 'none'}),
        html.Div(id='risk-trade-check-btn-output', style={'display': 'none'}),
        html.Div(id='risk-portfolio-metrics-btn-output', style={'display': 'none'}),
        html.Div(id='risk-stop-loss-btn-output', style={'display': 'none'}),
        html.Div(id='refresh-notifications-btn-output', style={'display': 'none'}),
        html.Div(id='clear-notifications-btn-output', style={'display': 'none'}),
        html.Div(id='notifications-clear-btn-output', style={'display': 'none'}),
        html.Div(id='notifications-mark-read-btn-output', style={'display': 'none'}),
        html.Div(id='clear-all-notifications-btn-output', style={'display': 'none'}),
        html.Div(id='mark-all-read-btn-output', style={'display': 'none'}),
        html.Div(id='manual-alert-btn-output', style={'display': 'none'}),
        html.Div(id='send-manual-alert-btn-output', style={'display': 'none'}),
        html.Div(id='test-email-btn-output', style={'display': 'none'}),
        html.Div(id='send-test-alert-btn-output', style={'display': 'none'}),
        html.Div(id='email-config-btn-output', style={'display': 'none'}),
        html.Div(id='email-test-btn-output', style={'display': 'none'}),
        html.Div(id='email-notifications-toggle-btn-output', style={'display': 'none'}),
        html.Div(id='email-address-update-btn-output', style={'display': 'none'}),
        html.Div(id='test-email-alert-btn-output', style={'display': 'none'}),
        html.Div(id='test-email-system-btn-output', style={'display': 'none'}),
        html.Div(id='ml-compatibility-check-btn-output', style={'display': 'none'}),
        html.Div(id='ml-compatibility-fix-btn-output', style={'display': 'none'}),
        html.Div(id='ml-recommendations-btn-output', style={'display': 'none'}),
        html.Div(id='force-model-update-btn-output', style={'display': 'none'}),
        html.Div(id='performance-dashboard-btn-output', style={'display': 'none'}),
        html.Div(id='performance-metrics-btn-output', style={'display': 'none'}),
        html.Div(id='portfolio-btn-output', style={'display': 'none'}),
        html.Div(id='load-auto-settings-btn-output', style={'display': 'none'}),
        html.Div(id='save-auto-settings-btn-output', style={'display': 'none'}),
        html.Div(id='enable-trade-integration-btn-output', style={'display': 'none'}),
        html.Div(id='disable-trade-integration-btn-output', style={'display': 'none'}),
        html.Div(id='virtual-balance-reset-btn-output', style={'display': 'none'}),
        html.Div(id='start-advanced-auto-trading-btn-output', style={'display': 'none'}),
        html.Div(id='stop-advanced-auto-trading-btn-output', style={'display': 'none'}),
        html.Div(id='check-advanced-auto-trading-btn-output', style={'display': 'none'}),
    ], style={'display': 'none'})
])

if __name__ == "__main__":
    print("Layout module loaded successfully")

# ========================================
# ENHANCED LAYOUT COMPONENTS - UNUSED ENDPOINTS
# ========================================

def create_advanced_auto_trading_section():
    """Advanced auto trading controls section"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5("🤖 Advanced Auto Trading System", className="mb-0"),
            dbc.Badge("Enhanced", color="primary", className="ms-2")
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Div(id="advanced-auto-trading-status"),
                    html.Div(id="advanced-auto-trading-controls"),
                ], width=6),
                dbc.Col([
                    html.Div(id="ai-signals-display"),
                    dcc.Interval(id="ai-signals-refresh-interval", interval=30000, n_intervals=0)
                ], width=6)
            ])
        ])
    ])

def create_market_data_section():
    """Market data dashboard section"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5("📊 Real-Time Market Data", className="mb-0"),
            dbc.Badge("Live", color="success", className="ms-2")
        ]),
        dbc.CardBody([
            html.Div(id="market-data-display"),
            dcc.Interval(id="market-data-refresh-interval", interval=15000, n_intervals=0)
        ])
    ])

def create_hft_analytics_section():
    """HFT analytics controls section"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5("⚡ High-Frequency Trading", className="mb-0"),
            dbc.Badge("Pro", color="warning", className="ms-2")
        ]),
        dbc.CardBody([
            dbc.ButtonGroup([
                dbc.Button("📊 Refresh", id="hft-analytics-refresh-btn", color="info", size="sm"),
                dbc.Button("▶️ Start HFT", id="hft-start-btn", color="success", size="sm"),
                dbc.Button("⏹️ Stop HFT", id="hft-stop-btn", color="danger", size="sm")
            ], className="mb-3"),
            html.Div(id="hft-analytics-display")
        ])
    ])

def create_enhanced_charts_section():
    """Enhanced chart controls section"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5("📈 Enhanced Charts", className="mb-0"),
            dbc.Badge("Advanced", color="info", className="ms-2")
        ]),
        dbc.CardBody([
            dbc.ButtonGroup([
                dbc.Button("📊 Bollinger", id="show-bollinger-btn", color="primary", size="sm"),
                dbc.Button("📈 Momentum", id="show-momentum-btn", color="success", size="sm"),
                dbc.Button("📊 Volume", id="show-volume-btn", color="warning", size="sm"),
                dbc.Button("🔄 Refresh", id="refresh-charts-btn", color="info", size="sm")
            ], className="mb-3"),
            html.Div(id="enhanced-chart-display")
        ])
    ])

def create_risk_management_section():
    """Advanced risk management section"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5("⚠️ Risk Management", className="mb-0"),
            dbc.Badge("Safety", color="danger", className="ms-2")
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Amount ($)"),
                    dbc.Input(id="risk-amount-input", type="number", value=1000, step=50),
                    dbc.Label("Risk % of Portfolio"),
                    dbc.Input(id="risk-percentage-input", type="number", value=2, step=0.5, min=0.1, max=10)
                ], width=4),
                dbc.Col([
                    dbc.ButtonGroup([
                        dbc.Button("💰 Calculate Position", id="calculate-position-size-btn", color="primary", size="sm"),
                        dbc.Button("⚠️ Check Risk", id="check-trade-risk-btn", color="warning", size="sm"),
                        dbc.Button("💾 Update Settings", id="update-risk-settings-btn", color="success", size="sm")
                    ], vertical=True, className="mb-2")
                ], width=4),
                dbc.Col([
                    html.Div(id="risk-management-display"),
                    html.Div(id="risk-recommendations")
                ], width=4)
            ])
        ])
    ])

def create_auto_trading_settings_section():
    """Auto trading settings section"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5("⚙️ Auto Trading Settings", className="mb-0"),
            dbc.Badge("Config", color="secondary", className="ms-2")
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Trading Symbol"),
                    dbc.Select(
                        id="auto-symbol-setting",
                        options=[
                            {"label": "BTC/USDT", "value": "BTCUSDT"},
                            {"label": "ETH/USDT", "value": "ETHUSDT"},
                            {"label": "ADA/USDT", "value": "ADAUSDT"},
                            {"label": "SOL/USDT", "value": "SOLUSDT"}
                        ],
                        value="BTCUSDT"
                    ),
                    dbc.Label("Trade Amount ($)"),
                    dbc.Input(id="auto-amount-setting", type="number", value=100, step=10)
                ], width=4),
                dbc.Col([
                    dbc.ButtonGroup([
                        dbc.Button("📥 Load Settings", id="load-auto-settings-btn", color="info", size="sm"),
                        dbc.Button("💾 Save Settings", id="save-auto-settings-btn", color="success", size="sm")
                    ], vertical=True)
                ], width=4),
                dbc.Col([
                    html.Div(id="auto-trading-settings-display")
                ], width=4)
            ])
        ])
    ])

def create_notifications_management_section():
    """Enhanced notifications management"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5("🔔 Notifications Management", className="mb-0"),
            dbc.Badge("Enhanced", color="info", className="ms-2")
        ]),
        dbc.CardBody([
            dbc.ButtonGroup([
                dbc.Button("📧 Send Manual Alert", id="send-manual-alert-btn", color="primary", size="sm"),
                dbc.Button("✉️ Test Email", id="test-email-system-btn", color="info", size="sm"),
                dbc.Button("🗑️ Clear All", id="clear-all-notifications-btn", color="danger", size="sm"),
                dbc.Button("✅ Mark All Read", id="mark-all-read-btn", color="success", size="sm")
            ], className="mb-3"),
            html.Div(id="notifications-management-display")
        ])
    ])

def create_sidebar_amount_buttons():
    """Enhanced sidebar amount selection buttons"""
    return dbc.Card([
        dbc.CardHeader("💰 Quick Amount Selection"),
        dbc.CardBody([
            dbc.ButtonGroup([
                dbc.Button("$50", id="sidebar-amount-50-btn", color="outline-primary", size="sm"),
                dbc.Button("$100", id="sidebar-amount-100-btn", color="outline-primary", size="sm"),
                dbc.Button("$250", id="sidebar-amount-250-btn", color="outline-primary", size="sm"),
                dbc.Button("$500", id="sidebar-amount-500-btn", color="outline-primary", size="sm"),
                dbc.Button("$1K", id="sidebar-amount-1000-btn", color="outline-primary", size="sm"),
                dbc.Button("Max", id="sidebar-amount-max-btn", color="outline-warning", size="sm")
            ], vertical=True)
        ])
    ])

