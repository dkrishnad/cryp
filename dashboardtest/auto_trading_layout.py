"""
Auto Trading Layout for Crypto Bot Dashboard
Real-time automated trading interface with controls and monitoring
"""

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

def create_auto_trading_layout():
    """Create the auto trading tab layout"""
    
    layout = dbc.Container([
        # Header Section
        dbc.Row([
            dbc.Col([
                html.H2("🤖 Auto Trading", className="text-white mb-3"),
                html.P(
                    "Automated trading system with real-time signal generation and risk management. "
                    "All trades are executed using virtual balance for safety.",
                    className="text-muted mb-4"
                )
            ])
        ]),
        
        # Status and Controls Row
        dbc.Row([
            # Auto Trading Controls
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4("🎛️ Auto Trading Controls", className="mb-0 text-white")
                    ]),
                    dbc.CardBody([
                        # Enable/Disable Toggle
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Auto Trading Status", className="text-white"),                                dbc.Switch(
                                    id="auto-trading-toggle",
                                    value=False,
                                    className="mb-3"
                                ),
                                html.Div(id="auto-trading-toggle-output", className="mb-2"),  # Status output for toggle
                                html.Div(id="auto-trading-status", className="mb-3")
                            ])
                        ]),
                        
                        # Settings Form
                        html.Hr(className="border-secondary"),
                        html.H5("⚙️ Trading Settings", className="text-white mb-3"),                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Symbol", className="text-white fw-bold mb-2"),                                dcc.Dropdown(
                                    id="auto-symbol-dropdown",
                                    options=[
                                        # Low-cap gems (highlighted)
                                        {"label": "🌟 KAIA/USDT (Low-cap Gem)", "value": "KAIAUSDT"},
                                        {"label": "🌟 JASMY/USDT (Low-cap Gem)", "value": "JASMYUSDT"},
                                        {"label": "🌟 GALA/USDT (Low-cap Gem)", "value": "GALAUSDT"},
                                        {"label": "🌟 ROSE/USDT (Low-cap Gem)", "value": "ROSEUSDT"},
                                        {"label": "🌟 CHR/USDT (Low-cap Gem)", "value": "CHRUSDT"},
                                        {"label": "🌟 CELR/USDT (Low-cap Gem)", "value": "CELRUSDT"},
                                        {"label": "🌟 CKB/USDT (Low-cap Gem)", "value": "CKBUSDT"},
                                        {"label": "🌟 OGN/USDT (Low-cap Gem)", "value": "OGNUSDT"},
                                        {"label": "🌟 FET/USDT (Low-cap Gem)", "value": "FETUSDT"},
                                        {"label": "🌟 BAND/USDT (Low-cap Gem)", "value": "BANDUSDT"},
                                        # Separator
                                        {"label": "─── Major Coins ───", "value": "", "disabled": True},
                                        # Major coins
                                        {"label": "₿ BTC/USDT", "value": "BTCUSDT"},
                                        {"label": "⧫ ETH/USDT", "value": "ETHUSDT"},
                                        {"label": "🟡 BNB/USDT", "value": "BNBUSDT"},
                                        {"label": "🔵 ADA/USDT", "value": "ADAUSDT"},
                                        {"label": "⚫ DOT/USDT", "value": "DOTUSDT"},
                                        {"label": "🟣 SOL/USDT", "value": "SOLUSDT"}
                                    ],
                                    value="KAIAUSDT",  # Default to KAIA
                                    className="mb-3 auto-trading-dropdown",
                                    style={
                                        "background": "linear-gradient(135deg, #2d3748 0%, #1a202c 100%)",
                                        "border": "2px solid #4a5568",
                                        "borderRadius": "12px",
                                        "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.3)",
                                        "minHeight": "48px"
                                    },
                                    optionHeight=50,
                                    placeholder="🎯 Select Trading Pair",
                                    searchable=True,
                                    clearable=False
                                )
                            ], width=6),                            dbc.Col([
                                dbc.Label("Timeframe", className="text-white fw-bold mb-2"),
                                dcc.Dropdown(
                                    id="auto-timeframe-dropdown",
                                    options=[
                                        {"label": "⚡ 1 Minute (Scalping)", "value": "1m"},
                                        {"label": "🔥 5 Minutes (Quick Trades)", "value": "5m"},
                                        {"label": "📈 15 Minutes (Short Term)", "value": "15m"},
                                        {"label": "⏰ 1 Hour (Recommended)", "value": "1h"},
                                        {"label": "📊 4 Hours (Swing)", "value": "4h"},
                                        {"label": "📅 1 Day (Position)", "value": "1d"}
                                    ],
                                    value="1h",
                                    className="mb-3 auto-trading-dropdown timeframe-dropdown",
                                    style={
                                        "background": "linear-gradient(135deg, #2d3748 0%, #1a202c 100%)",
                                        "border": "2px solid #4a5568",
                                        "borderRadius": "12px",
                                        "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.3)",
                                        "minHeight": "48px"
                                    },
                                    optionHeight=45,
                                    placeholder="📊 Select Timeframe",
                                    searchable=False,
                                    clearable=False
                                )
                            ], width=6)                        ]),
                        
                        # Amount Selection Section
                        html.Hr(className="border-secondary"),
                        html.H5("💰 Trade Amount", className="text-white mb-3"),
                        
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Amount Type", className="text-white fw-bold mb-2"),                                dcc.RadioItems(
                                    id="amount-type-radio",
                                    options=[
                                        {"label": " Fixed Amount (USDT)", "value": "fixed"},
                                        {"label": " Percentage of Balance", "value": "percentage"}
                                    ],
                                    value="fixed",  # Changed default to fixed
                                    className="text-white mb-3",
                                    inputStyle={"margin-right": "8px"},
                                    labelStyle={"margin-right": "20px"}
                                )
                            ], width=12)
                        ]),
                        
                        dbc.Row([
                            dbc.Col([                                # Fixed Amount Input
                                html.Div([
                                    dbc.Label("Trade Amount (USDT)", className="text-white fw-bold mb-2"),
                                    dbc.InputGroup([
                                        dbc.InputGroupText("💵"),
                                        dbc.Input(
                                            id="fixed-amount-input",
                                            type="number",
                                            value=50,  # Changed default to smaller amount
                                            min=1,     # Changed minimum to 1 USD
                                            max=10000,
                                            step=1,    # Changed step to 1 for precise input
                                            placeholder="Enter amount in USDT",
                                            className="bg-dark text-white border-secondary"
                                        ),
                                        dbc.InputGroupText("USDT")
                                    ], className="mb-2"),
                                    # Quick amount buttons
                                    dbc.ButtonGroup([
                                        dbc.Button("$1", id="amount-1", size="sm", color="outline-primary"),
                                        dbc.Button("$10", id="amount-10", size="sm", color="outline-primary"),
                                        dbc.Button("$50", id="amount-50", size="sm", color="outline-primary"),
                                        dbc.Button("$100", id="amount-100", size="sm", color="outline-primary"),
                                        dbc.Button("$500", id="amount-500", size="sm", color="outline-primary")
                                    ], className="mb-3 w-100")
                                ], id="fixed-amount-section")
                            ], width=6),
                            dbc.Col([
                # Percentage Amount
                html.Div([
                    dbc.Label("Percentage of Balance (%)", className="text-white fw-bold mb-2"),
                    dbc.Row([
                        dbc.Col([
                            dbc.InputGroup([
                                dbc.InputGroupText("📈"),
                                dbc.Input(
                                    id="percentage-amount-input",
                                    type="number",
                                    value=10,
                                    min=1,
                                    max=50,
                                    step=1,
                                    className="bg-dark text-white border-secondary"
                                ),
                                dbc.InputGroupText("%")
                            ], className="mb-2")
                        ], width=12)
                    ]),
                    dcc.Slider(
                        id="percentage-amount-slider",
                        min=1,
                        max=50,
                        step=1,
                        value=10,
                        marks={i: f"{i}%" for i in range(0, 51, 10)},
                        className="mb-2"
                    ),
                    html.Div(id="calculated-amount-display", className="text-info mb-3")
                ], id="percentage-amount-section", style={"display": "none"})
                            ], width=6)
                        ]),
                        
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Risk per Trade (%)", className="text-white"),
                                dcc.Slider(
                                    id="auto-risk-slider",
                                    min=0.5,
                                    max=20,
                                    step=0.5,
                                    value=5.0,
                                    marks={i: f"{i}%" for i in range(0, 21, 5)},
                                    className="mb-3"
                                )
                            ], width=6),
                            dbc.Col([
                                dbc.Label("Min Confidence (%)", className="text-white"),
                                dcc.Slider(
                                    id="auto-confidence-slider",
                                    min=50,
                                    max=95,
                                    step=5,
                                    value=70,
                                    marks={i: f"{i}%" for i in range(50, 101, 10)},
                                    className="mb-3"
                                )
                            ], width=6)
                        ]),
                        
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Take Profit (%)", className="text-white"),
                                dcc.Slider(
                                    id="auto-tp-slider",
                                    min=0.5,
                                    max=10,
                                    step=0.1,
                                    value=2.0,
                                    marks={i: f"{i}%" for i in range(0, 11, 2)},
                                    className="mb-3"
                                )
                            ], width=6),
                            dbc.Col([
                                dbc.Label("Stop Loss (%)", className="text-white"),
                                dcc.Slider(
                                    id="auto-sl-slider",
                                    min=0.2,
                                    max=5,
                                    step=0.1,
                                    value=1.0,
                                    marks={i: f"{i}%" for i in range(0, 6, 1)},
                                    className="mb-3"
                                )
                            ], width=6)
                        ]),
                        
                        # Save Settings Button
                        dbc.Button(
                            "💾 Save Settings",
                            id="save-auto-settings-btn",
                            color="success",
                            className="w-100"
                        )
                    ])
                ], className="border-0", style={"backgroundColor": "#23272f"})
            ], width=6),
            
            # Current Signal and Status
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4("📊 Current Signal", className="mb-0 text-white")
                    ]),
                    dbc.CardBody([
                        html.Div(id="current-signal-display", className="text-center"),
                        html.Hr(className="border-secondary"),
                        
                        # Balance and Performance
                        dbc.Row([
                            dbc.Col([
                                html.H6("💰 Virtual Balance", className="text-white"),
                                html.H4(id="auto-balance-display", className="text-success")
                            ], width=6),
                            dbc.Col([
                                html.H6("📈 Total P&L", className="text-white"),
                                html.H4(id="auto-pnl-display", className="text-info")
                            ], width=6)
                        ]),
                        
                        html.Hr(className="border-secondary"),
                        
                        # Performance Stats
                        dbc.Row([
                            dbc.Col([
                                html.Small("Win Rate", className="text-muted"),
                                html.P(id="auto-winrate-display", className="text-white mb-1")
                            ], width=4),
                            dbc.Col([
                                html.Small("Total Trades", className="text-muted"),
                                html.P(id="auto-trades-display", className="text-white mb-1")
                            ], width=4),
                            dbc.Col([
                                html.Small("Winning/Losing", className="text-muted"),
                                html.P(id="auto-wl-display", className="text-white mb-1")
                            ], width=4)
                        ]),
                        
                        # Control Buttons
                        html.Hr(className="border-secondary"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Button(
                                    "🔄 Execute Signal",
                                    id="execute-signal-btn",
                                    color="primary",
                                    className="w-100 mb-2"
                                )
                            ], width=6),
                            dbc.Col([
                                dbc.Button(
                                    "🔄 Reset System",
                                    id="reset-auto-trading-btn",
                                    color="warning",
                                    className="w-100 mb-2"
                                )
                            ], width=6)
                        ])
                    ])
                ], className="border-0", style={"backgroundColor": "#23272f"})
            ], width=6)
        ], className="mb-4"),
        
        # Low-Cap Coin Optimization Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4("🌟 Low-Cap Coin Trading Hub", className="mb-0 text-white")
                    ]),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.H6("🎯 Quick Optimize", className="text-white mb-3"),
                                html.P("Automatically apply optimized settings for low-cap coins", className="text-muted small mb-3"),
                                dbc.Button(
                                    "⚡ Optimize for KAIA",
                                    id="optimize-kaia-btn",
                                    color="success",
                                    size="sm",
                                    className="me-2 mb-2"
                                ),
                                dbc.Button(
                                    "⚡ Optimize for JASMY",
                                    id="optimize-jasmy-btn",
                                    color="success",
                                    size="sm",
                                    className="me-2 mb-2"
                                ),
                                dbc.Button(
                                    "⚡ Optimize for GALA",
                                    id="optimize-gala-btn",
                                    color="success",
                                    size="sm",
                                    className="me-2 mb-2"
                                ),
                            ], width=4),
                            dbc.Col([
                                html.H6("📈 Low-Cap Advantages", className="text-white mb-3"),
                                html.Ul([
                                    html.Li("Higher volatility = More profit opportunities", className="text-muted small"),
                                    html.Li("Lower market cap = Bigger % moves", className="text-muted small"),
                                    html.Li("Less institutional competition", className="text-muted small"),
                                    html.Li("Better technical patterns", className="text-muted small"),
                                ], className="text-muted small")
                            ], width=4),
                            dbc.Col([
                                html.H6("⚙️ Optimized Settings", className="text-white mb-3"),
                                html.Div(id="low-cap-settings-display", children=[
                                    html.P("💡 Lower confidence threshold (55-65%)", className="text-info small mb-1"),
                                    html.P("💰 Reduced risk per trade (3-4%)", className="text-info small mb-1"),
                                    html.P("🎯 Higher take profit (2-2.5x)", className="text-info small mb-1"),
                                    html.P("🛑 Tighter stop loss (1-1.2x)", className="text-info small mb-1"),
                                ])
                            ], width=4)
                        ])
                    ])
                ], className="border-0", style={"backgroundColor": "#23272f"})
            ])
        ], className="mb-4"),
        
        # Open Positions and Trade Log Row
        dbc.Row([
            # Open Positions
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4("📋 Open Positions", className="mb-0 text-white")
                    ]),
                    dbc.CardBody([
                        html.Div(id="open-positions-table")
                    ])
                ], className="border-0", style={"backgroundColor": "#23272f"})
            ], width=7),
            
            # Trade Log
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4("📜 Trade Log", className="mb-0 text-white")
                    ]),
                    dbc.CardBody([
                        html.Div(
                            id="auto-trade-log",
                            style={
                                "height": "300px",
                                "overflowY": "auto",
                                "backgroundColor": "#1a1a1a",
                                "padding": "10px",
                                "borderRadius": "5px",
                                "fontFamily": "monospace",
                                "fontSize": "12px"
                            }
                        )
                    ])
                ], className="border-0", style={"backgroundColor": "#23272f"})            ], width=5)
        ]),
        
        # Store for auto trading state
        dcc.Store(id="auto-trading-store")
        
    ], fluid=True, className="py-4")
    
    # Hidden components for missing auto trading callbacks  
    hidden_auto_components = html.Div([
        html.Div(id="auto-rollback-status", style={"display": "none"}),
        html.Div(id="check-auto-alerts-result", style={"display": "none"}),
        html.Div(id="auto-trading-tab-content", style={"display": "none"}),
    ], style={"display": "none"})
    
    # Add hidden components to layout
    final_layout = html.Div([layout, hidden_auto_components])
    
    return final_layout

def register_auto_trading_callbacks(app):
    """Register callbacks for auto trading tab"""
    @app.callback(
        Output("auto-trading-status", "children"),
        Input("auto-trading-toggle", "value")
    )
    def update_auto_trading_status(toggle):
        return "✅ Enabled" if toggle else "❌ Disabled"
    
    @app.callback(
        Output("auto-signal-display", "children"),
        Input("refresh-auto-signal", "n_clicks")
    )
    def update_auto_signal(n_clicks):
        return "Signal: BUY BTCUSDT (Confidence: 85%)"
    
    print("[OK] Auto trading callbacks registered")
