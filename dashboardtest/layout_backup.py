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

def safe_slider(id, min=0, max=100, value=50, **kwargs):
    """Slider with fallback for loading errors"""
    try:
        return dcc.Slider(id=id, min=min, max=max, value=value, **kwargs)
    except Exception as e:
        print(f"[LAYOUT FIX] Slider {id} fallback: {e}")
        return dcc.Input(id=id, type='range', min=min, max=max, value=value, **kwargs)

def safe_upload(id, **kwargs):
    """Upload with fallback for loading errors"""
    try:
        return dcc.Upload(id=id, **kwargs)
    except Exception as e:
        print(f"[LAYOUT FIX] Upload {id} fallback: {e}")
        return html.Div([
            dcc.Upload(id=f"{id}-input", style={"display": "none"}),
            html.Button("Choose File", id=f"{id}-button", className="btn btn-outline-primary"),
            html.Div(id=id, **kwargs)
        ])

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

# Add dummy div for clientside callback
dummy_div = html.Div(id='dummy-div', style={'display': 'none'})


sidebar = html.Div([
    dcc.Store(id="selected-symbol-store", storage_type="memory"),
    dcc.Store(id="live-price-cache", storage_type="memory"),
    dcc.Store(id="upload-tracking-store", storage_type="memory", data={"active": False}),
    # Live price updates via interval (replacing WebSocket)
    dcc.Interval(id="live-price-interval", interval=2000, n_intervals=0),
    
    html.H4([html.I(className="bi bi-gear-fill me-2 text-primary"), "Settings & Controls"], className="mb-3 mt-2"),
    # --- Trading Configuration Section ---
    dbc.Collapse([
        dbc.Row([
            dbc.Col([
                dbc.Label([html.I(className="bi bi-currency-bitcoin me-1 text-warning"), "Symbol"], id="label-symbol"),                dcc.Dropdown(
                    id="sidebar-symbol",
                    options=[{"label": s.upper(), "value": s} for s in [
                        'btcusdt', 'ethusdt', 'solusdt', 'avaxusdt', 'dogeusdt', 'bnbusdt', 'maticusdt', 'pepeusdt',
                        # Low-cap gems with good potential
                        'kaiausdt', 'jasmyusdt', 'galausdt', 'roseusdt', 'chrusdt', 'celrusdt', 'ckbusdt', 'ognusdt',
                        'fetusdt', 'bandusdt', 'oceanusdt', 'tlmusdt', 'aliceusdt', 'slpusdt', 'mtlusdt', 'sunusdt',
                        'winsusdt', 'dentusdt', 'hotusdt', 'vtousdt', 'stmxusdt', 'keyusdt', 'storjusdt', 'ampusdt',
                        # Traditional alts
                        'adausdt', 'xrpusdt', 'ltcusdt', 'linkusdt', 'dotusdt', 'uniusdt', 'bchusdt', 'filusdt',
                        'trxusdt', 'etcusdt', 'aptusdt', 'arbusdt', 'nearusdt', 'atomusdt', 'sandusdt', 'manausdt',
                        'chzusdt', 'egldusdt', 'ftmusdt', 'icpusdt', 'runeusdt', 'sushiusdt', 'aaveusdt', 'snxusdt',
                        'crvusdt', 'compusdt', 'enjusdt', '1inchusdt', 'xmrusdt', 'zecusdt', 'dashusdt', 'omgusdt',
                        'yfiusdt', 'balusdt', 'ctkusdt', 'ankrusdt', 'batusdt', 'cvcusdt', 'dgbusdt'
                    ]],
                    value='kaiausdt',  # Set KAIA as default
                    multi=False,
                    clearable=False,
                    style={"backgroundColor": "#ffffff", "color": "#2f3542"},
                    disabled=False  # Ensure dropdown is enabled
                ),
                dbc.Tooltip("Select trading pair", target="label-symbol", placement="top"),
            ]),
            dbc.Col([
                dbc.Label([html.I(className="bi bi-wallet2 me-1 text-success"), "Virtual Balance"], id="label-vbal"),
                html.Div(id="virtual-balance", style={"fontWeight": "bold", "fontSize": 18, "color": "#00ff88"}),
                dbc.Tooltip("Your simulated trading balance", target="label-vbal", placement="top"),
            ])
        ], className="mb-2"),
    ], id="collapse-trading-config", is_open=True),
    html.Hr(),
    # --- Streamlit-style Expanders (now with real controls) ---
    dbc.Collapse([
        dbc.Label([html.I(className="bi bi-sliders me-1"), "Signal Filters"]),
        dcc.Checklist(
            options=[
                {"label": "Enable RSI Filter", "value": "rsi"},
                {"label": "Enable MACD Filter", "value": "macd"},
                {"label": "Enable Bollinger Bands Filter", "value": "bbands"},
            ],
            value=[],
            id="signal-filters-checklist",
            style={"color": "#00ff88"}
        ),
    ], id="collapse-signal-filters", is_open=True),
    dbc.Collapse([
        dbc.Label([html.I(className="bi bi-cpu me-1"), "AI Prediction Settings"]),
        dcc.Dropdown(
            id="ai-model-dropdown",
            options=[{"label": "XGBoost", "value": "xgboost"}, {"label": "LightGBM", "value": "lightgbm"}, {"label": "Neural Net", "value": "nn"}],
            value="xgboost",
            clearable=False,
            style={"backgroundColor": "#404040", "color": "#e0e0e0"}
        ),
        html.Div("Select the AI model for predictions.", style={"color": "#aaa", "marginTop": "0.5em"}),
    ], id="collapse-ai-prediction", is_open=True),
    dbc.Collapse([
        dbc.Label([html.I(className="bi bi-star-fill me-1"), "Ultra-High Confidence Filter"]),
        dcc.Slider(
            id="ultra-confidence-slider",
            min=0, max=1, step=0.01, value=0.95,
            marks={0.9: "0.9", 0.95: "0.95", 1: "1.0"},
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        html.Div("Set the minimum confidence threshold for signals.", style={"color": "#aaa", "marginTop": "0.5em"}),
    ], id="collapse-ultra-confidence", is_open=True),
    dbc.Collapse([
        dbc.Label([html.I(className="bi bi-cash-coin me-1"), "Quick Profit Settings"]),
        dcc.Input(id="quick-profit-target", type="number", value=1.0, step=0.1, style={"width": "100%"}),
        html.Div("Set the quick profit target %.", style={"color": "#aaa", "marginTop": "0.5em"}),
    ], id="collapse-quick-profit", is_open=True),
    dbc.Collapse([
        dbc.Label([html.I(className="bi bi-arrow-repeat me-1"), "Real-time Settings"]),
        dcc.Checklist(
            options=[{"label": "Enable Real-time Mode", "value": "realtime"}],
            value=[],
            id="realtime-mode-checklist",
            style={"color": "#00ff88"}
        ),
    ], id="collapse-realtime", is_open=True),
    # --- Model Version Selection ---
    html.Div([
        dbc.Label([html.I(className="bi bi-layers me-1 text-info"), "Model Version"]),
        dcc.Dropdown(id="model-version-dropdown", options=[], value=None, clearable=True, style={"backgroundColor": "#404040", "color": "#e0e0e0"}),
        dbc.Button("Refresh Model Versions", id="refresh-model-versions-btn", color="secondary", className="mb-2 w-100"),
    ], style={"marginBottom": "1em"}),

    # --- Model Metrics Dashboard ---
    dbc.Collapse([
        html.H4([html.I(className="bi bi-graph-up-arrow me-2 text-primary"), "Model Metrics"], className="mb-3 mt-2"),
        dbc.Button("Show Model Metrics", id="show-model-metrics-btn", color="info", className="mb-2 w-100"),
        html.Div(id="model-metrics-dashboard"),
    ], id="collapse-model-metrics", is_open=True, className="content-section"),
    html.Hr(),    # --- Universal Reset All Button ---
    dbc.Button("🧹 Reset ALL (Balance, Trades, Notifications)", id="reset-all-btn", color="danger", className="mb-2 w-100"),
    html.Div(id="reset-all-btn-output"),
    # --- Advanced/Dev Tools Section (collapsible) ---
    dbc.Collapse([
        html.H4([html.I(className="bi bi-tools me-2 text-warning"), "Advanced / Dev Tools"], className="mb-3 mt-2"),
        dbc.Button([html.I(className="bi bi-database-check me-1"), "Test DB Write"], id="test-db-btn", color="info", className="mb-2 w-100"),
        html.Div(id="test-db-btn-output"),
        dbc.Button([html.I(className="bi bi-cpu me-1"), "Test ML"], id="test-ml-btn", color="info", className="mb-2 w-100"),
        html.Div(id="test-ml-btn-output"),
        dbc.Button([html.I(className="bi bi-bar-chart-fill me-1"), "Show Feature Importance"], id="show-fi-btn", color="primary", className="mb-2 w-100"),
        html.Div(id="show-fi-btn-output"),
        dbc.Button([html.I(className="bi bi-graph-up-arrow me-1"), "Run Backtest (Sample)"], id="run-backtest-sample-btn", color="primary", className="mb-2 w-100"),
        html.Div(id="run-backtest-sample-btn-output"),
        dbc.Button([html.I(className="bi bi-trash3-fill me-1"), "Prune Old Trades"], id="prune-trades-btn", color="danger", className="mb-2 w-100"),
        html.Div(id="prune-trades-btn-output"),
        dbc.Button([html.I(className="bi bi-sliders me-1"), "Tune Models"], id="tune-models-btn", color="primary", className="mb-2 w-100"),
        html.Div(id="tune-models-btn-output"),
        dbc.Button([html.I(className="bi bi-activity me-1"), "Check Drift"], id="check-drift-btn", color="warning", className="mb-2 w-100"),
        html.Div(id="check-drift-btn-output"),
        dbc.Button([html.I(className="bi bi-arrow-repeat me-1"), "Reset Virtual Balance"], id="reset-balance-btn", color="secondary", className="mb-2 w-100"),
        html.Div(id="reset-balance-btn-output"),
        html.Hr(),        dbc.Button([html.I(className="bi bi-lightning-charge me-1"), "Online Learn"], id="online-learn-btn", color="info", className="mb-2 w-100"),
        html.Div(id="online-learn-btn-output"),
    ], id="collapse-advanced-dev-tools", is_open=True, className="content-section"),

    # --- Model Logs/Errors Section ---
    dbc.Collapse([
        html.H4([html.I(className="bi bi-journal-text me-2 text-info"), "Model Logs & Errors"], className="mb-3 mt-2"),
        dbc.Button("Refresh Logs", id="refresh-logs-btn", color="secondary", className="mb-2 w-100"),
        html.Div(id="refresh-logs-btn-output"),
        html.Div(id="model-logs-table"),
        html.Div(id="model-errors-table"),
    ], id="collapse-model-logs", is_open=True, className="content-section"),

    # --- Feature Importance Section ---
    dbc.Collapse([
        html.H4([html.I(className="bi bi-bar-chart-fill me-2 text-warning"), "Feature Importance"], className="mb-3 mt-2"),
        dbc.Button("Show Feature Importance", id="show-fi-btn-2", color="primary", className="mb-2 w-100"),
        dcc.Graph(id="feature-importance-graph"),
        html.Div(id="feature-importance-metrics"),
    ], id="collapse-feature-importance", is_open=True, className="content-section"),    # --- Backtest Section ---
    dbc.Collapse([
        html.H4([html.I(className="bi bi-graph-up-arrow me-2 text-primary"), "Backtest"], className="mb-3 mt-2"),        dbc.Button("Run Backtest", id="run-backtest-btn", color="primary", className="mb-2 w-100"),
        html.Div(id="run-backtest-btn-output"),
        dbc.Button("🏆 Run Both Systems", id="run-comprehensive-backtest-btn", color="success", className="mb-2 w-100"),
        html.Div(id="run-comprehensive-backtest-btn-output"),
        html.Small("↑ Runs both Original + Transfer Learning systems", className="text-muted d-block mb-2"),
        html.Div(id="backtest-result"),
    ], id="collapse-backtest", is_open=True, className="content-section"),

    # --- Analytics Section ---
    dbc.Collapse([
        html.H4([html.I(className="bi bi-bar-chart-line-fill me-2 text-success"), "Analytics"], className="mb-3 mt-2"),
        dbc.Button("Show Analytics", id="show-analytics-btn", color="secondary", className="mb-2 w-100"),
        html.Div(id="show-analytics-btn-output"),
        dcc.Graph(id="advanced-analytics-graph"),
        html.Div(id="advanced-analytics-metrics"),
    ], id="collapse-analytics", is_open=True, className="content-section"),

    # --- Batch Prediction Section ---
    dbc.Collapse([
        html.H4([html.I(className="bi bi-upload me-2 text-info"), "Batch Prediction"], className="mb-3 mt-2"),
        dcc.Upload(
            id="batch-predict-upload",
            children=dbc.Button("Upload CSV for Batch Prediction", color="primary", className="mb-2 w-100"),
            multiple=False
        ),
        dbc.Button("Run Batch Prediction", id="run-batch-predict-btn", color="success", className="mb-2 w-100"),
        html.Div(id="batch-predict-result"),
    ], id="collapse-batch-predict", is_open=True, className="content-section"),

    # --- Risk Management Controls ---
    html.Div([
        dbc.Label([html.I(className="bi bi-shield-lock me-1 text-danger"), "Risk Management"], style={"marginTop": "1em"}),
        dbc.Row([
            dbc.Col([
                dbc.Label("Max Drawdown"),
                dcc.Input(id="risk-max-drawdown", type="number", value=1000, min=0, step=1, style={"width": "100%"}),
            ]),
            dbc.Col([
                dbc.Label("Stop-Loss %"),
                dcc.Input(id="risk-stoploss", type="number", value=1.0, min=0, step=0.1, style={"width": "100%"}),
            ]),
            dbc.Col([
                dbc.Label("Position Size"),
                dcc.Input(id="risk-position-size", type="number", value=100, min=1, step=1, style={"width": "100%"}),
            ]),
        ], className="mb-2"),                html.Small("Configure risk controls for all trades. Max drawdown is the maximum loss before trading stops.", style={"color": "#95a5a6"}),
    ], className="content-section"),

    # --- Email Notification Toggle & Address ---
    html.Div([
        dbc.Checkbox(id="email-notify-toggle", value=False, style={"marginRight": "0.5em"}),
        dbc.Label([html.I(className="bi bi-envelope-at me-1 text-info"), "Enable Email Notifications"], html_for="email-notify-toggle"),
        dbc.Input(id="email-notify-address", type="email", placeholder="Notification email address", style={"marginTop": "0.5em"}),
    ], style={"marginBottom": "1em", "marginTop": "1em"}),
], id="sidebar-fixed", style={"width": "350px", "backgroundColor": "#2a2a2a", "color": "#e0e0e0", "zIndex": 2001, "position": "fixed", "top": 0, "left": 0, "height": "100vh", "overflowY": "auto", "boxShadow": "2px 0 8px rgba(0,0,0,0.3)", "borderRight": "1px solid #404040"}, className="sidebar")

# Tabs for all major features
tabs = dcc.Tabs([
    dcc.Tab(label="Dashboard", children=[
        html.Div([
            html.H2([html.I(className="bi bi-speedometer2 me-2 text-info"), "Real-Time Trading Dashboard"], className="mb-3 mt-2"),
            dbc.Row([
                dbc.Col([
                    html.H4([html.I(className="bi bi-currency-exchange me-1 text-warning"), "Live Price"]),
                    html.Div(id="live-price", style={"fontSize": 32, "fontWeight": "bold", "marginBottom": 20, "color": "#00ff88"}),
                ], width=3),
                dbc.Col([
                    html.H4([html.I(className="bi bi-graph-up-arrow me-1 text-success"), "Portfolio Status"]),
                    html.Div(id="portfolio-status", style={"fontSize": 18, "marginBottom": 10}),
                ], width=3),
                dbc.Col([
                    html.H4([html.I(className="bi bi-bar-chart-line-fill me-1 text-primary"), "Performance Monitor"]),
                    html.Div(id="performance-monitor", style={"fontSize": 18, "marginBottom": 10}),
                ], width=3),
                dbc.Col([
                    html.H4([html.I(className="bi bi-bell-fill me-1 text-danger"), "Notifications"]),
                    html.Div(id="notifications-list"),
                ], width=3),
            ], className="mb-3"),

            # --- Open Positions Table ---
            html.H4([html.I(className="bi bi-table me-1 text-info"), "Open Positions"]),
            dash_table.DataTable(
                id="open-positions-table",
                columns=[
                    {"name": "ID", "id": "ID"},
                    {"name": "Symbol", "id": "Symbol"},
                    {"name": "Action", "id": "Action"},
                    {"name": "Amount", "id": "Amount"},
                    {"name": "Entry Price", "id": "Entry Price"},
                    {"name": "Current Price", "id": "Current Price"},
                    {"name": "Stop Loss", "id": "Stop Loss"},
                    {"name": "Take Profit", "id": "Take Profit"},
                    {"name": "Live P&L", "id": "Live P&L"},
                    {"name": "Confidence", "id": "Confidence"}
                ],
                data=[],
                style_cell={
                    'backgroundColor': '#1a1a1a',
                    'color': 'white',
                    'border': '1px solid #444',
                    'fontSize': '12px',
                    'textAlign': 'center'
                },
                style_header={
                    'backgroundColor': '#333',
                    'fontWeight': 'bold'
                },
                style_data_conditional=[
                    {
                        'if': {'filter_query': '{Action} = BUY'},
                        'backgroundColor': '#1a3d2e',
                        'color': '#4ade80'
                    },
                    {
                        'if': {'filter_query': '{Action} = SELL'},
                        'backgroundColor': '#3d1a1a',
                        'color': '#f87171'
                    },
                    {
                        'if': {'filter_query': '{Live P&L} contains 🟢'},
                        'backgroundColor': '#1a3d2e',
                        'color': '#4ade80'
                    },
                    {
                        'if': {'filter_query': '{Live P&L} contains 🔴'},
                        'backgroundColor': '#3d1a1a',
                        'color': '#f87171'
                    }
                ],
                style_table={'overflowX': 'auto'},
            ),
            # --- Technical Indicators & Regime Section ---
            html.Div([
                html.H4([
                    html.I(className="bi bi-bar-chart-steps me-1 text-info"),
                    "Technical Indicators & Regime"
                ]),
                dbc.Row([
                    dbc.Col([
                        html.Div("Current Regime:", style={"fontWeight": "bold", "color": "#00ff88"}),
                        html.Div(id="current-regime", style={"fontSize": 20, "marginBottom": 10}),
                    ], width=3),
                    dbc.Col([
                        html.Div("RSI:", style={"fontWeight": "bold", "color": "#00ff88"}),
                        html.Div(id="rsi-value", style={"fontSize": 20, "marginBottom": 10}),
                    ], width=2),
                    dbc.Col([
                        html.Div("MACD:", style={"fontWeight": "bold", "color": "#00ff88"}),
                        html.Div(id="macd-value", style={"fontSize": 20, "marginBottom": 10}),
                    ], width=2),
                    dbc.Col([
                        html.Div("Bollinger Bands:", style={"fontWeight": "bold", "color": "#00ff88"}),
                        html.Div(id="bbands-value", style={"fontSize": 20, "marginBottom": 10}),
                    ], width=3),                ], className="mb-2"),
            ], className="content-section tech-indicators"),

            html.Hr(),
            html.H4([html.I(className="bi bi-lightning-fill me-1 text-warning"), "Active Trades"]),            dash_table.DataTable(
                id="active-trades-table",
                columns=[
                    {"name": "ID", "id": "id"},
                    {"name": "Symbol", "id": "symbol"},
                    {"name": "Direction", "id": "direction"},
                    {"name": "Amount", "id": "amount"},
                    {"name": "Entry Price", "id": "entry_price"},
                    {"name": "PnL", "id": "pnl"},
                    {"name": "Status", "id": "status"},
                ],
                data=[],
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left'},
                style_header={'backgroundColor': '#f8f9fa', 'color': '#2f3542', 'fontWeight': 'bold'},
            ),
            # --- Trade Management Controls ---
            html.Div([
                html.H5("Manage Selected Trade", style={"marginTop": "1em"}),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Close Trade", id="close-trade-btn", color="danger", className="me-2 w-100"),
                    ], width=2),
                    dbc.Col([
                        dbc.Button("Cancel Trade", id="cancel-trade-btn", color="warning", className="me-2 w-100"),
                    ], width=2),
                    dbc.Col([
                        dbc.Button("Activate Trade", id="activate-trade-btn", color="success", className="w-100"),
                    ], width=2),
                    dbc.Col([
                        html.Div(id="trade-action-result", style={"fontWeight": "bold", "fontSize": 16, "color": "#00ff88"}),
                    ], width=6),
                ], className="mb-2"),                html.Small("Select a row in the Active Trades table above, then choose an action.", style={"color": "#95a5a6"}),
            ], className="content-section"),

            # --- Safety Check Controls ---
            html.Div([
                html.H5("Safety Check", style={"marginTop": "1em"}),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Run Safety Check", id="safety-check-btn", color="info", className="me-2 w-100"),
                    ], width=2),
                    dbc.Col([
                        html.Div(id="safety-check-result", style={"fontWeight": "bold", "fontSize": 16, "color": "#00bfff"}),
                    ], width=10),
                ], className="mb-2"),                html.Small("Checks for risk, margin, and trade safety before opening a trade.", style={"color": "#aaa"}),
            ], style={"backgroundColor": "#333333", "borderRadius": "8px", "padding": "1em", "marginBottom": "1em", "border": "1px solid #404040"}),

            # --- Advanced Analytics Controls ---
            html.Div([
                html.H5("Advanced Analytics", style={"marginTop": "1em"}),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Show Analytics", id="show-analytics-btn", color="secondary", className="me-2 w-100"),
                    ], width=2),
                    dbc.Col([
                        dcc.Graph(id="advanced-analytics-graph", style={"height": "300px"}),
                    ], width=10),
                ], className="mb-2"),                html.Div(id="advanced-analytics-metrics", style={"color": "#e0e0e0", "marginTop": "0.5em"}),
            ], style={"backgroundColor": "#333333", "borderRadius": "8px", "padding": "1em", "marginBottom": "1em", "border": "1px solid #404040"}),

            # --- Notification Management Controls ---
            html.Div([
                html.H5("Manage Notifications", style={"marginTop": "1em"}),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Mark as Read", id="mark-notification-read-btn", color="info", className="me-2 w-100"),
                    ], width=2),
                    dbc.Col([
                        dbc.Button("Delete Notification", id="delete-notification-btn", color="danger", className="w-100"),
                    ], width=2),
                    dbc.Col([
                        html.Div(id="notification-action-result", style={"fontWeight": "bold", "fontSize": 16, "color": "#00ff88"}),
                    ], width=8),
                ], className="mb-2"),                html.Small("Select a notification in the list above, then choose an action.", style={"color": "#aaa"}),
            ], style={"backgroundColor": "#333333", "borderRadius": "8px", "padding": "1em", "marginBottom": "1em", "border": "1px solid #404040"}),

            # --- Trade History Section ---
            html.H4([html.I(className="bi bi-clock-history me-1 text-info"), "Trade History"]),
            dash_table.DataTable(
                id="trades-table",
                columns=[
                    {"name": "ID", "id": "id"},
                    {"name": "Symbol", "id": "symbol"},
                    {"name": "Direction", "id": "direction"},
                    {"name": "Amount", "id": "amount"},
                    {"name": "Entry Price", "id": "entry_price"},
                    {"name": "PnL", "id": "pnl"},
                    {"name": "Status", "id": "status"},
                ],
                data=[],
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left'},                style_header={'backgroundColor': '#404040', 'color': '#ffffff', 'fontWeight': 'bold'},
            ),
            html.Div(id="trades-error", style={"color": "red"}),
        ], style={"backgroundColor": "#333333", "color": "#e0e0e0", "borderRadius": "10px", "padding": "1.5em", "border": "1px solid #404040"})
    ]),
    # Only essential tabs remain
    dcc.Tab(label="ML Prediction", children=[
        html.Div([
            html.H2([html.I(className="bi bi-cpu me-2 text-primary"), "ML Prediction"]),
            dbc.Row([
                dbc.Col(["Amount:", dcc.Input(id="ml-amount", type="number", value=1, step=0.01, style={"width": "100%"})], width=2),
                dbc.Col(["Entry Price:", dcc.Input(id="ml-entry", type="number", value=50000, step=0.01, style={"width": "100%"})], width=2),
                dbc.Col(["TP %:", dcc.Input(id="ml-tp", type="number", value=2, step=0.01, style={"width": "100%"})], width=2),
                dbc.Col(["SL %:", dcc.Input(id="ml-sl", type="number", value=1, step=0.01, style={"width": "100%"})], width=2),
                dbc.Col([html.Button([html.I(className="bi bi-lightning-charge-fill me-1"), "Predict"], id="ml-predict-btn", n_clicks=0, className="btn btn-success w-100")], width=2),
            ], className="mb-2"),
            html.Div(id="ml-prediction-result", style={"fontWeight": "bold", "fontSize": 18, "marginBottom": 20, "color": "#00ff88"}),
            # --- Batch Prediction Section ---
            html.Hr(),            html.H4([html.I(className="bi bi-upload me-1 text-info"), "Batch Prediction"]),
            dcc.Upload(
                id="batch-predict-upload",
                children=dbc.Button("Upload CSV for Batch Prediction", color="primary", className="mb-2"),
                multiple=False
            ),
            
            # --- Upload Progress Tracker ---
            html.Div([
                html.H5([html.I(className="bi bi-clock-history me-1"), "Upload Progress"], className="mb-2"),
                dbc.Progress(
                    id="upload-progress-bar",
                    value=0,
                    striped=True,
                    animated=False,
                    color="info",
                    className="mb-2",
                    style={"height": "20px", "display": "none"}
                ),
                html.Div(id="upload-status-text", className="mb-2", style={"fontSize": "14px", "color": "#aaa"}),
                dbc.Button(
                    [html.I(className="bi bi-arrow-clockwise me-1"), "Check Upload Status"], 
                    id="refresh-upload-status-btn", 
                    color="info", 
                    size="sm",
                    className="mb-2"
                ),            ], className="border rounded p-2 mb-3", style={"backgroundColor": "#333333", "border": "1px solid #404040"}),
            
            dbc.Button("Run Batch Prediction", id="run-batch-predict-btn", color="success", className="mb-2"),
            html.Div(id="batch-predict-result", style={"fontWeight": "bold", "fontSize": 18, "marginBottom": 20, "color": "#4CAF50"}),
        ], style={"backgroundColor": "#333333", "color": "#e0e0e0", "borderRadius": "10px", "padding": "1.5em", "border": "1px solid #404040"})
    ]),
    dcc.Tab(label="Open Trade", children=[
        html.Div([
            html.H2([html.I(className="bi bi-plus-circle-fill me-2 text-success"), "Open Trade"]),
            dbc.Row([
                dbc.Col(["Symbol:", dcc.Input(id="trade-symbol", type="text", value="BTCUSDT", style={"width": "100%"})], width=2),
                dbc.Col(["Amount:", dcc.Input(id="trade-amount", type="number", value=0.1, step=0.01, style={"width": "100%"})], width=2),
                dbc.Col(["Entry Price:", dcc.Input(id="trade-entry", type="number", value=50000, step=0.01, style={"width": "100%"})], width=2),
                dbc.Col(["TP %:", dcc.Input(id="trade-tp", type="number", value=2, step=0.01, style={"width": "100%"})], width=2),
                dbc.Col(["SL %:", dcc.Input(id="trade-sl", type="number", value=1, step=0.01, style={"width": "100%"})], width=2),
                dbc.Col([
                    dbc.Button([html.I(className="bi bi-arrow-up-circle me-1"), "Open Long"], id="open-long-btn", n_clicks=0, color="success", className="w-100 mb-1"),
                    dbc.Button([html.I(className="bi bi-arrow-down-circle me-1"), "Open Short"], id="open-short-btn", n_clicks=0, color="danger", className="w-100"),
                ], width=2),
            ], className="mb-2"),            html.Div(id="trade-result", style={"fontWeight": "bold", "fontSize": 18, "marginBottom": 20, "color": "#4CAF50"}),
        ], style={"backgroundColor": "#333333", "color": "#e0e0e0", "borderRadius": "10px", "padding": "1.5em", "border": "1px solid #404040"})
    ]),
    
    dcc.Tab(label="Model Analytics", children=[
        html.Div([
            html.H2([html.I(className="bi bi-bar-chart-line-fill me-2 text-success"), "Model Analytics"], className="mb-3 mt-2"),
            dbc.Button("Refresh Analytics", id="refresh-model-analytics-btn", color="info", className="mb-2 w-100"),
            html.Div(id="refresh-model-analytics-btn-output"),
            html.Div(id="model-analytics-table"),
            dcc.Graph(id="model-analytics-graph"),
        ], style={"padding": "2em"}),
    ]),
    
    dcc.Tab(label="🤖 Hybrid Learning", children=[
        html.Div(id="hybrid-learning-tab-content", style={"padding": "1em"})
    ]),
    
    dcc.Tab(label="📧 Email Config", children=[
        html.Div(id="email-config-tab-content", style={"padding": "1em"})
    ]),
    
    dcc.Tab(label="🤖 Auto Trading", children=[
        html.Div(id="auto-trading-tab-content", style={"padding": "1em"})
    ]),
    dcc.Tab(label="⚡ Futures Trading", children=[
        html.Div(id="futures-trading-tab-content", style={"padding": "1em"})
    ]),
    dcc.Tab(label="🔗 Binance-Exact API", children=[
        html.Div(id="binance-exact-tab-content", style={"padding": "1em"})
    ]),
])

# Notification Toasts (for real-time feedback)
notification_toast = dbc.Toast(
    id="notification-toast",
    header="Notification",
    # is_open is not needed for sidebar, only for notification_toast
    dismissable=True,
    icon="primary",
    style={"position": "fixed", "top": 70, "right": 30, "minWidth": 350, "zIndex": 2000},
)

 # --- Advanced/Dev Tools Section (collapsible) ---

# Main layout
layout = html.Div([
    dbc.Navbar(
        dbc.Container([
            html.Span([html.I(className="bi bi-robot me-2 text-success"), "Perfectbot V2"], style={"fontWeight": "bold", "fontSize": 24, "color": "#00ff88"}),
        ], fluid=True),        color="dark",
        dark=True,
        style={"marginBottom": "0.5em", "borderRadius": "0 0 10px 10px", "marginLeft": "350px"}
    ),
    sidebar,    html.Div([
        notification_toast,
        dcc.Interval(id="interval-prediction", interval=5*1000, n_intervals=0),
        dcc.Interval(id="interval-indicators", interval=30*1000, n_intervals=0),  # 30 seconds for periodic updates
        dcc.Interval(id="interval-upload-status", interval=2*1000, n_intervals=0, disabled=True),  # 2 seconds for upload tracking
        dcc.Interval(id="auto-trading-interval", interval=5*1000, n_intervals=0),  # Auto trading interval - global so it works on any tab
        tabs,
        html.Div(id="test-output", style={"color": "yellow", "fontWeight": "bold", "fontSize": 18}),
        html.Div(id="backtest-result", style={"display": "none"}),
        
        # Hidden components for callback outputs that don't need visible UI
        html.Div([
            html.Div(id="auto-settings-summary", style={"display": "none"}),
            html.Div(id="auto-trading-start-btn", style={"display": "none"}),
            html.Div(id="auto-trading-stop-btn", style={"display": "none"}),
            html.Div(id="trade-status-display", style={"display": "none"}),
            html.Div(id="dummy-div", style={"display": "none"}),
            html.Div(id="auto-trading-status", style={"display": "none"}),
            html.Div(id="auto-trading-toggle-output", style={"display": "none"}),
            html.Div(id="auto-balance-display", style={"display": "none"}),
            html.Div(id="auto-pnl-display", style={"display": "none"}),
            html.Div(id="auto-winrate-display", style={"display": "none"}),
            html.Div(id="auto-wl-display", style={"display": "none"}),
            html.Div(id="auto-trades-display", style={"display": "none"}),
            html.Div(id="fixed-amount-section", style={"display": "none"}),
            html.Div(id="percentage-amount-section", style={"display": "none"}),
            html.Div(id="calculated-amount-display", style={"display": "none"}),
            html.Div(id="current-signal-display", style={"display": "none"}),
            html.Div(id="save-auto-settings-btn", style={"display": "none"}),
            html.Div(id="analytics-output", style={"display": "none"}),
            html.Div(id="auto-trade-log", style={"display": "none"}),
            html.Div(id="trade-logs-output", style={"display": "none"}),
            html.Div(id="refresh-model-versions-btn-output", style={"display": "none"}),
            html.Div(id="low-cap-settings-display", style={"display": "none"}),
            # Hidden inputs for auto trading - wrapped in divs since sliders don't accept style
            html.Div([
                dcc.Dropdown(id="auto-symbol-dropdown"),
                dcc.Slider(id="auto-confidence-slider", min=0, max=100, value=70),
                dcc.Slider(id="auto-risk-slider", min=1, max=10, value=5),
                dcc.Slider(id="auto-tp-slider", min=0.5, max=10, value=2, step=0.1),
                dcc.Slider(id="auto-sl-slider", min=0.5, max=5, value=1, step=0.1),
                dcc.Input(id="fixed-amount-input", type="number", value=100),
                dcc.Input(id="percentage-amount-input", type="number", value=10),
                dcc.Slider(id="percentage-amount-slider", min=1, max=100, value=10),
                html.Button("Execute Signal", id="execute-signal-btn"),
                html.Button("Reset Auto Trading", id="reset-auto-trading-btn"),
                dbc.Button("💾 Save Settings", id="save-settings-btn"),
            ], style={"display": "none"}),
        ])
    ], style={"marginLeft": "350px", "padding": "1em", "minHeight": "100vh", "backgroundColor": "#2a2a2a"}, className="main-content"),
])
