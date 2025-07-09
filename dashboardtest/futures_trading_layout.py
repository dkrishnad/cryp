"""
Binance Futures-Style Trading Dashboard Layout
"""

import dash
from dash import html, dcc, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
from datetime import datetime

def create_futures_trading_layout():
    """Create the futures trading dashboard layout"""
    
    layout = html.Div([
        # Header
        dbc.Row([
            dbc.Col([
                html.H2([
                    html.I(className="bi bi-graph-up-arrow me-2"),
                    "Futures Trading - Binance Style"
                ], className="text-primary mb-3"),
                html.P("Advanced leverage trading with margin management, stop loss, take profit, and liquidation protection", 
                       className="text-muted")
            ])
        ], className="mb-4"),
        
        # Account Summary Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Account Balance", className="card-title"),
                        html.H3(id="futures-total-balance", children="$0.00", className="text-success"),
                        html.P([
                            html.Small("Available: "),
                            html.Span(id="futures-available-balance", children="$0.00", className="text-muted")
                        ])
                    ])
                ], className="h-100")
            ], md=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Margin Used", className="card-title"),
                        html.H3(id="futures-margin-used", children="$0.00", className="text-warning"),
                        html.P([
                            html.Small("Ratio: "),
                            html.Span(id="futures-margin-ratio", children="0.00%", className="text-muted")
                        ])
                    ])
                ], className="h-100")
            ], md=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Unrealized P&L", className="card-title"),
                        html.H3(id="futures-unrealized-pnl", children="$0.00", className="text-info"),
                        html.P([
                            html.Small("Open Positions: "),
                            html.Span(id="futures-open-positions", children="0", className="text-muted")
                        ])
                    ])
                ], className="h-100")
            ], md=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Trading Status", className="card-title"),
                        html.H3(id="futures-trading-status", children="🟢 Active", className="text-success"),
                        html.P([
                            html.Small("Can Trade: "),
                            html.Span(id="futures-can-trade", children="Yes", className="text-muted")
                        ])
                    ])
                ], className="h-100")
            ], md=3),
            
            # Add Virtual Balance card for synchronization
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5([
                            html.I(className="bi bi-wallet2 me-1"),
                            "Virtual Balance"
                        ], className="card-title text-info"),
                        html.H3(id="futures-virtual-balance", children="$10,000.00", className="text-info"),
                        html.P([
                            html.Small("P&L: "),
                            html.Span(id="futures-pnl-display", children="$0.00", className="text-muted")
                        ]),
                        html.P([
                            html.Small("Total: "),
                            html.Span(id="futures-virtual-total-balance", children="$10,000.00", className="text-success")
                        ]),
                        html.P([
                            html.Small("Available: "),
                            html.Span(id="futures-available-balance-virtual", children="$10,000.00", className="text-primary")
                        ]),
                        dbc.ButtonGroup([
                            dbc.Button("Reset", id="futures-reset-balance-btn", color="secondary", size="sm"),
                            dbc.Button("Sync", id="futures-sync-balance-btn", color="info", size="sm", outline=True)
                        ], size="sm", className="mt-1")
                    ])
                ], className="h-100 border-info")
            ], md=3)
        ], className="mb-4"),
        
        # Trading Controls
        dbc.Row([
            # Manual Trading Panel
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="bi bi-joystick me-2"),
                            "Manual Trading"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        # Symbol Selection
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Symbol"),
                                dcc.Dropdown(
                                    id="futures-symbol-dropdown",
                                    options=[
                                        {"label": "BTC/USDT", "value": "BTCUSDT"},
                                        {"label": "ETH/USDT", "value": "ETHUSDT"},
                                        {"label": "KAIA/USDT", "value": "KAIAUSDT"},
                                        {"label": "BNB/USDT", "value": "BNBUSDT"},
                                    ],
                                    value="BTCUSDT",
                                    clearable=False
                                )
                            ], md=6),
                            dbc.Col([
                                dbc.Label("Position Side"),
                                dcc.Dropdown(
                                    id="futures-side-dropdown",
                                    options=[
                                        {"label": "🟢 LONG", "value": "LONG"},
                                        {"label": "🔴 SHORT", "value": "SHORT"}
                                    ],
                                    value="LONG",
                                    clearable=False
                                )
                            ], md=6)
                        ], className="mb-3"),
                        
                        # Leverage and Margin
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Leverage"),
                                dcc.Slider(
                                    id="futures-leverage-slider",
                                    min=1,
                                    max=125,
                                    step=1,
                                    value=10,
                                    marks={1: "1x", 10: "10x", 25: "25x", 50: "50x", 75: "75x", 100: "100x", 125: "125x"},
                                    tooltip={"placement": "bottom", "always_visible": True}
                                )
                            ], md=6),
                            dbc.Col([
                                dbc.Label("Margin (USDT)"),
                                dbc.Input(
                                    id="futures-margin-input",
                                    type="number",
                                    value=100,
                                    min=10,
                                    max=10000,
                                    step=10
                                )
                            ], md=6)
                        ], className="mb-3"),
                        
                        # Stop Loss and Take Profit
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Stop Loss %"),
                                dbc.Input(
                                    id="futures-sl-input",
                                    type="number",
                                    value=2.0,
                                    min=0.1,
                                    max=50,
                                    step=0.1
                                )
                            ], md=6),
                            dbc.Col([
                                dbc.Label("Take Profit %"),
                                dbc.Input(
                                    id="futures-tp-input",
                                    type="number",
                                    value=5.0,
                                    min=0.1,
                                    max=100,
                                    step=0.1
                                )
                            ], md=6)
                        ], className="mb-3"),
                        
                        # Action Buttons
                        dbc.Row([
                            dbc.Col([
                                dbc.Button(
                                    [html.I(className="bi bi-arrow-up me-1"), "LONG"],
                                    id="futures-long-btn",
                                    color="success",
                                    size="lg",
                                    className="w-100"
                                )
                            ], md=6),
                            dbc.Col([
                                dbc.Button(
                                    [html.I(className="bi bi-arrow-down me-1"), "SHORT"],
                                    id="futures-short-btn",
                                    color="danger",
                                    size="lg",
                                    className="w-100"
                                )
                            ], md=6)
                        ]),
                        
                        # Result Display
                        html.Div(id="futures-trade-result", className="mt-3")
                    ])
                ])
            ], md=6),
            
            # Auto Trading Settings
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="bi bi-robot me-2"),
                            "Auto Trading Settings"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        # Auto Trading Toggle
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Auto Trading"),
                                dbc.Switch(
                                    id="futures-auto-trading-switch",
                                    value=False,
                                    label="Enable Futures Auto Trading"
                                )
                            ])
                        ], className="mb-3"),
                        
                        # Default Settings
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Default Leverage"),
                                dcc.Dropdown(
                                    id="futures-auto-leverage-dropdown",
                                    options=[
                                        {"label": f"{i}x", "value": i}
                                        for i in [1, 2, 3, 5, 10, 20, 25, 50, 75, 100, 125]
                                    ],
                                    value=10,
                                    clearable=False
                                )
                            ], md=6),
                            dbc.Col([
                                dbc.Label("Default Margin"),
                                dbc.Input(
                                    id="futures-auto-margin-input",
                                    type="number",
                                    value=100,
                                    min=10,
                                    max=1000
                                )
                            ], md=6)
                        ], className="mb-3"),
                        
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Auto Stop Loss %"),
                                dbc.Input(
                                    id="futures-auto-sl-input",
                                    type="number",
                                    value=2.0,
                                    min=0.1,
                                    max=10,
                                    step=0.1
                                )
                            ], md=6),
                            dbc.Col([
                                dbc.Label("Auto Take Profit %"),
                                dbc.Input(
                                    id="futures-auto-tp-input",
                                    type="number",
                                    value=5.0,
                                    min=0.1,
                                    max=20,
                                    step=0.1
                                )
                            ], md=6)
                        ], className="mb-3"),
                        
                        # Risk Management
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Max Margin Ratio %"),
                                dbc.Input(
                                    id="futures-max-margin-ratio",
                                    type="number",
                                    value=80,
                                    min=10,
                                    max=95,
                                    step=5
                                )
                            ], md=6),
                            dbc.Col([
                                dbc.Label("Risk Per Trade %"),
                                dbc.Input(
                                    id="futures-risk-per-trade",
                                    type="number",
                                    value=1.0,
                                    min=0.1,
                                    max=10,
                                    step=0.1
                                )
                            ], md=6)
                        ], className="mb-3"),
                        
                        # Save Settings Button
                        dbc.Button(
                            [html.I(className="bi bi-save me-1"), "Save Settings"],
                            id="futures-save-settings-btn",
                            color="primary",
                            className="w-100"
                        ),
                        
                        # Settings Result
                        html.Div(id="futures-settings-result", className="mt-2")
                    ])
                ])
            ], md=6)
        ], className="mb-4"),         
        # Advanced Technical Analysis Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="bi bi-graph-up me-2"),
                            "📈 Advanced Technical Analysis"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        # Price Chart with Indicators
                        dbc.Row([
                            dbc.Col([
                                html.H6("📊 Price Chart with Bollinger Bands", className="mb-2"),
                                dcc.Graph(id="futures-price-chart", figure={})
                            ], md=12)
                        ], className="mb-3"),
                        
                        # Technical Indicators Row
                        dbc.Row([
                            dbc.Col([
                                html.H6("📈 RSI & MACD Indicators", className="mb-2"),
                                dcc.Graph(id="futures-indicators-chart", figure={})
                            ], md=12)
                        ], className="mb-3"),
                        
                        # Advanced Indicators Cards
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardHeader("🎯 RSI Signal"),
                                    dbc.CardBody([
                                        html.H4(id="futures-rsi-value", className="text-center mb-1"),
                                        html.P(id="futures-rsi-signal", className="text-center mb-0")
                                    ])
                                ])
                            ], md=3),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardHeader("⚡ MACD Signal"),
                                    dbc.CardBody([
                                        html.H4(id="futures-macd-value", className="text-center mb-1"),
                                        html.P(id="futures-macd-signal", className="text-center mb-0")
                                    ])
                                ])
                            ], md=3),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardHeader("🔵 Stochastic"),
                                    dbc.CardBody([
                                        html.H4(id="futures-stoch-value", className="text-center mb-1"),
                                        html.P(id="futures-stoch-signal", className="text-center mb-0")
                                    ])
                                ])
                            ], md=3),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardHeader("📊 ATR"),
                                    dbc.CardBody([
                                        html.H4(id="futures-atr-value", className="text-center mb-1"),
                                        html.P("Volatility", className="text-center mb-0")
                                    ])
                                ])
                            ], md=3)
                        ], className="mb-3"),
                        
                        # Volume and Momentum Indicators
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardHeader("📈 Volume Ratio"),
                                    dbc.CardBody([
                                        html.H4(id="futures-volume-ratio", className="text-center mb-1"),
                                        html.P(id="futures-volume-signal", className="text-center mb-0")
                                    ])
                                ])
                            ], md=4),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardHeader("🎯 Momentum"),
                                    dbc.CardBody([
                                        html.H4(id="futures-momentum-value", className="text-center mb-1"),
                                        html.P(id="futures-momentum-signal", className="text-center mb-0")
                                    ])
                                ])
                            ], md=4),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardHeader("🤖 AI Signal"),
                                    dbc.CardBody([
                                        html.H4(id="futures-ai-signal", className="text-center mb-1"),
                                        html.P(id="futures-ai-confidence", className="text-center mb-0")
                                    ])
                                ])
                            ], md=4)
                        ], className="mb-3"),
                        
                        # Refresh Button for Indicators
                        dbc.Row([
                            dbc.Col([
                                dbc.Button(
                                    [html.I(className="bi bi-arrow-clockwise me-1"), "🔄 Refresh Technical Analysis"],
                                    id="futures-refresh-indicators-btn",
                                    color="primary",
                                    size="sm",
                                    className="w-100"
                                )
                            ])
                        ])
                    ])
                ])
            ])
        ], className="mb-4"),
        
        # Positions Table
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="bi bi-list-task me-2"),
                            "Open Positions"
                        ], className="mb-0"),
                        dbc.Button(
                            [html.I(className="bi bi-arrow-clockwise me-1"), "Refresh"],
                            id="futures-refresh-positions-btn",
                            color="outline-primary",
                            size="sm",
                            className="float-end"
                        )
                    ]),
                    dbc.CardBody([
                        html.Div(id="futures-positions-table")
                    ])
                ])
            ])
        ], className="mb-4"),
        
        # Trade History
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="bi bi-clock-history me-2"),
                            "Trade History"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        html.Div(id="futures-history-table")
                    ])
                ])
            ])
        ]),
        
        # Auto-refresh interval
        dcc.Interval(
            id="futures-refresh-interval",
            interval=5000,  # 5 seconds
            n_intervals=0
        ),
        
        # Store components
        dcc.Store(id="futures-data-store", data={}),
        
        # Hidden components for missing futures callbacks
        html.Div([
            html.Div(id="futures-trading-controls", style={"display": "none"}),
            html.Div(id="futures-trading-tab-content", style={"display": "none"}),
            html.Div(id="futures-rsi-indicator", style={"display": "none"}),
            html.Div(id="futures-macd-indicator", style={"display": "none"}),
            html.Div(id="futures-bollinger-indicator", style={"display": "none"}),
            html.Div(id="futures-stochastic-indicator", style={"display": "none"}),
            html.Div(id="futures-atr-indicator", style={"display": "none"}),
            html.Div(id="futures-volume-indicator", style={"display": "none"}),
            html.Div(id="futures-technical-chart", style={"display": "none"}),
        ], style={"display": "none"}),
    ], className="p-3")
    
    return layout

def create_futures_positions_table(positions):
    """Create positions table"""
    if not positions:
        return html.Div([
            html.P("No open positions", className="text-muted text-center p-3")
        ])
    
    columns = [
        {"name": "Symbol", "id": "symbol"},
        {"name": "Side", "id": "side"},
        {"name": "Size", "id": "size", "type": "numeric", "format": {"specifier": ",.4f"}},
        {"name": "Entry Price", "id": "entry_price", "type": "numeric", "format": {"specifier": ",.4f"}},
        {"name": "Current Price", "id": "current_price", "type": "numeric", "format": {"specifier": ",.4f"}},
        {"name": "Leverage", "id": "leverage"},
        {"name": "Margin", "id": "margin_used", "type": "numeric", "format": {"specifier": ",.2f"}},
        {"name": "Unrealized P&L", "id": "unrealized_pnl", "type": "numeric", "format": {"specifier": ",.2f"}},
        {"name": "P&L %", "id": "unrealized_pnl_percent", "type": "numeric", "format": {"specifier": ",.2f"}},
        {"name": "Liquidation", "id": "liquidation_price", "type": "numeric", "format": {"specifier": ",.4f"}},
        {"name": "Actions", "id": "actions"}
    ]
    
    # Format data for table
    table_data = []
    for pos in positions:
        row = {
            "symbol": pos["symbol"],
            "side": "🟢 LONG" if pos["side"] == "LONG" else "🔴 SHORT",
            "size": pos["size"],
            "entry_price": pos["entry_price"],
            "current_price": pos["current_price"],
            "leverage": f"{pos['leverage']}x",
            "margin_used": pos["margin_used"],
            "unrealized_pnl": pos["unrealized_pnl"],
            "unrealized_pnl_percent": pos["unrealized_pnl_percent"],
            "liquidation_price": pos["liquidation_price"],
            "actions": "Close"
        }
        table_data.append(row)
    
    return dash_table.DataTable(
        columns=columns,
        data=table_data,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "center", "padding": "10px"},
        style_data_conditional=[  # type: ignore
            {
                "if": {"filter_query": "{unrealized_pnl} > 0"},
                "backgroundColor": "#d4edda",
                "color": "black"
            },
            {
                "if": {"filter_query": "{unrealized_pnl} < 0"},
                "backgroundColor": "#f8d7da",
                "color": "black"
            }
        ],
        style_header={"backgroundColor": "#f8f9fa", "fontWeight": "bold"}
    )

def create_futures_history_table(trades):
    """Create trade history table"""
    if not trades:
        return html.Div([
            html.P("No trade history", className="text-muted text-center p-3")
        ])
    
    columns = [
        {"name": "Symbol", "id": "symbol"},
        {"name": "Side", "id": "side"},
        {"name": "Entry", "id": "entry_price", "type": "numeric", "format": {"specifier": ",.4f"}},
        {"name": "Exit", "id": "exit_price", "type": "numeric", "format": {"specifier": ",.4f"}},
        {"name": "Size", "id": "size", "type": "numeric", "format": {"specifier": ",.4f"}},
        {"name": "Leverage", "id": "leverage"},
        {"name": "P&L", "id": "pnl", "type": "numeric", "format": {"specifier": ",.2f"}},
        {"name": "P&L %", "id": "pnl_percent", "type": "numeric", "format": {"specifier": ",.2f"}},
        {"name": "Reason", "id": "reason"},
        {"name": "Closed At", "id": "closed_at"}
    ]
    
    # Format data for table
    table_data = []
    for trade in trades:
        row = {
            "symbol": trade["symbol"],
            "side": "🟢 LONG" if trade["side"] == "LONG" else "🔴 SHORT",
            "entry_price": trade["entry_price"],
            "exit_price": trade["exit_price"],
            "size": trade["size"],
            "leverage": f"{trade['leverage']}x",
            "pnl": trade["pnl"],
            "pnl_percent": trade["pnl_percent"],
            "reason": trade["reason"].replace("_", " ").title(),
            "closed_at": trade["closed_at"][:19] if trade["closed_at"] else ""
        }
        table_data.append(row)
    
    return dash_table.DataTable(
        columns=columns,
        data=table_data,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "center", "padding": "8px"},
        style_data_conditional=[  # type: ignore
            {
                "if": {"filter_query": "{pnl} > 0"},
                "backgroundColor": "#d4edda",
                "color": "black"
            },
            {
                "if": {"filter_query": "{pnl} < 0"},
                "backgroundColor": "#f8d7da",
                "color": "black"
            }
        ],
        style_header={"backgroundColor": "#f8f9fa", "fontWeight": "bold"},
        page_size=10
    )

def register_futures_trading_callbacks(app):
    """Register callbacks for futures trading tab"""
    @app.callback(
        Output("futures-trading-status", "children"),
        Input("futures-auto-trading-switch", "value")
    )
    def update_futures_trading_status(toggle):
        return "✅ Auto Trading Enabled" if toggle else "📝 Manual Trading Only"
    
    @app.callback(
        Output("futures-position-display", "children"),
        Input("refresh-futures-positions", "n_clicks")
    )
    def update_futures_positions(n_clicks):
        return "No open positions"
    
    print("[OK] Futures trading callbacks registered")
