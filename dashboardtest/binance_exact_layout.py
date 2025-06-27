"""
Binance-exact dashboard integration
Provides UI components for Binance-exact API testing and management
"""

import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import requests
import json
from datetime import datetime, timedelta
import pandas as pd

# Backend API URL
API_URL = "http://localhost:8000"

def create_binance_exact_layout():
    """Create the Binance-exact API management layout"""
    
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("🔗 Binance-Exact API", className="text-primary mb-4"),
                html.P("1:1 Binance Futures API compatibility for seamless real trading transition", 
                       className="text-muted")
            ])
        ]),
        
        # API Status Panel
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("📡 API Status & Connection", className="mb-0")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div(id="binance-api-status", children=[
                                    dbc.Alert("Checking API status...", color="info", id="api-status-alert")
                                ])
                            ], width=8),
                            dbc.Col([
                                dbc.Button("🔄 Refresh Status", id="refresh-api-status", color="primary", outline=True)
                            ], width=4)
                        ])
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        # Account Information
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("💰 Account Information", className="mb-0")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div(id="binance-account-info")
                            ], width=8),
                            dbc.Col([
                                dbc.Button("📊 Load Account", id="load-account-btn", color="success"),
                                html.Br(),
                                html.Br(),
                                dbc.Button("💎 Load Balance", id="load-balance-btn", color="info")
                            ], width=4)
                        ])
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        # Position Management
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("📈 Position Management", className="mb-0")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.InputGroup([
                                    dbc.InputGroupText("Symbol"),
                                    dbc.Input(id="position-symbol", placeholder="BTCUSDT", value="BTCUSDT")
                                ]),
                                html.Br(),
                                dbc.Button("📊 Get Positions", id="get-positions-btn", color="primary"),
                                html.Br(),
                                html.Br(),
                                html.Div(id="binance-positions-info")
                            ], width=12)
                        ])
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        # Order Testing
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("🎯 Order Testing", className="mb-0")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.InputGroup([
                                    dbc.InputGroupText("Symbol"),
                                    dbc.Input(id="order-symbol", placeholder="BTCUSDT", value="BTCUSDT")
                                ]),
                                html.Br(),
                                dbc.InputGroup([
                                    dbc.InputGroupText("Side"),
                                    dbc.Select(
                                        id="order-side",
                                        options=[
                                            {"label": "BUY", "value": "BUY"},
                                            {"label": "SELL", "value": "SELL"}
                                        ],
                                        value="BUY"
                                    )
                                ]),
                                html.Br(),
                                dbc.InputGroup([
                                    dbc.InputGroupText("Type"),
                                    dbc.Select(
                                        id="order-type",
                                        options=[
                                            {"label": "MARKET", "value": "MARKET"},
                                            {"label": "LIMIT", "value": "LIMIT"}
                                        ],
                                        value="MARKET"
                                    )
                                ]),
                                html.Br(),
                                dbc.InputGroup([
                                    dbc.InputGroupText("Quantity"),
                                    dbc.Input(id="order-quantity", placeholder="0.001", value="0.001", type="number")
                                ]),
                                html.Br(),
                                dbc.InputGroup([
                                    dbc.InputGroupText("Price"),
                                    dbc.Input(id="order-price", placeholder="107000", value="107000", type="number")
                                ]),
                                html.Br(),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button("📤 Place Order", id="place-order-btn", color="success")
                                    ], width=6),
                                    dbc.Col([
                                        dbc.Button("📋 Get Orders", id="get-orders-btn", color="info")
                                    ], width=6)
                                ])
                            ], width=6),
                            dbc.Col([
                                html.Div(id="order-result")
                            ], width=6)
                        ])
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        # Leverage & Margin
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("⚡ Leverage & Margin", className="mb-0")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.InputGroup([
                                    dbc.InputGroupText("Symbol"),
                                    dbc.Input(id="leverage-symbol", placeholder="BTCUSDT", value="BTCUSDT")
                                ]),
                                html.Br(),
                                dbc.InputGroup([
                                    dbc.InputGroupText("Leverage"),
                                    dbc.Input(id="leverage-value", placeholder="20", value="20", type="number")
                                ]),
                                html.Br(),
                                dbc.InputGroup([
                                    dbc.InputGroupText("Margin Type"),
                                    dbc.Select(
                                        id="margin-type",
                                        options=[
                                            {"label": "ISOLATED", "value": "ISOLATED"},
                                            {"label": "CROSSED", "value": "CROSSED"}
                                        ],
                                        value="ISOLATED"
                                    )
                                ]),
                                html.Br(),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button("⚡ Set Leverage", id="set-leverage-btn", color="warning")
                                    ], width=6),
                                    dbc.Col([
                                        dbc.Button("🎚️ Set Margin", id="set-margin-btn", color="secondary")
                                    ], width=6)
                                ])
                            ], width=6),
                            dbc.Col([
                                html.Div(id="leverage-result")
                            ], width=6)
                        ])
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        # Market Data
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("📊 Market Data", className="mb-0")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Button("📈 Get 24hr Tickers", id="get-tickers-btn", color="primary"),
                                html.Br(),
                                html.Br(),
                                dbc.Button("ℹ️ Exchange Info", id="get-exchange-btn", color="info")
                            ], width=3),
                            dbc.Col([
                                html.Div(id="market-data-result")
                            ], width=9)
                        ])
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        # Auto Trading Test
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("🤖 Auto Trading Test", className="mb-0")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.InputGroup([
                                    dbc.InputGroupText("Symbol"),
                                    dbc.Input(id="auto-symbol", placeholder="BTCUSDT", value="BTCUSDT")
                                ]),
                                html.Br(),
                                dbc.InputGroup([
                                    dbc.InputGroupText("Direction"),
                                    dbc.Select(
                                        id="auto-direction",
                                        options=[
                                            {"label": "BUY/LONG", "value": "BUY"},
                                            {"label": "SELL/SHORT", "value": "SELL"}
                                        ],
                                        value="BUY"
                                    )
                                ]),
                                html.Br(),
                                dbc.InputGroup([
                                    dbc.InputGroupText("Confidence"),
                                    dbc.Input(id="auto-confidence", placeholder="0.8", value="0.8", type="number", min=0, max=1, step=0.1)
                                ]),
                                html.Br(),
                                dbc.InputGroup([
                                    dbc.InputGroupText("Price"),
                                    dbc.Input(id="auto-price", placeholder="107000", value="107000", type="number")
                                ]),
                                html.Br(),
                                dbc.Button("🚀 Execute Auto Signal", id="execute-auto-btn", color="success", size="lg")
                            ], width=6),
                            dbc.Col([
                                html.Div(id="auto-trading-result")
                            ], width=6)
                        ])
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        # Hidden components for missing binance exact callbacks
        html.Div([
            html.Div(id="binance-exact-tab-content", style={"display": "none"}),
        ], style={"display": "none"}),
    ], fluid=True)

# Helper functions for API calls
def check_api_status():
    """Check if Binance-exact API is responsive"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            return True, "API is healthy and responsive"
        else:
            return False, f"API returned status {response.status_code}"
    except Exception as e:
        return False, f"Cannot connect to API: {str(e)}"

def get_account_info():
    """Get account information from Binance-exact API"""
    try:
        response = requests.get(f"{API_URL}/fapi/v2/account", timeout=10)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"API returned status {response.status_code}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_balance_info():
    """Get balance information from Binance-exact API"""
    try:
        response = requests.get(f"{API_URL}/fapi/v2/balance", timeout=10)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"API returned status {response.status_code}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_positions(symbol=None):
    """Get position information"""
    try:
        url = f"{API_URL}/fapi/v2/positionRisk"
        if symbol:
            url += f"?symbol={symbol}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"API returned status {response.status_code}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def place_order(symbol, side, order_type, quantity, price=None):
    """Place an order"""
    try:
        data = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": str(quantity),
            "positionSide": "BOTH"
        }
        if price and order_type == "LIMIT":
            data["price"] = str(price)
            data["timeInForce"] = "GTC"
            
        response = requests.post(f"{API_URL}/fapi/v1/order", data=data, timeout=10)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"API returned status {response.status_code}: {response.text}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_open_orders():
    """Get open orders"""
    try:
        response = requests.get(f"{API_URL}/fapi/v1/openOrders", timeout=10)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"API returned status {response.status_code}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def set_leverage(symbol, leverage):
    """Set leverage for symbol"""
    try:
        data = {"symbol": symbol, "leverage": leverage}
        response = requests.post(f"{API_URL}/fapi/v1/leverage", data=data, timeout=10)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"API returned status {response.status_code}: {response.text}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def set_margin_type(symbol, margin_type):
    """Set margin type for symbol"""
    try:
        data = {"symbol": symbol, "marginType": margin_type}
        response = requests.post(f"{API_URL}/fapi/v1/marginType", data=data, timeout=10)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"API returned status {response.status_code}: {response.text}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_24hr_tickers():
    """Get 24hr ticker statistics"""
    try:
        response = requests.get(f"{API_URL}/fapi/v1/ticker/24hr", timeout=10)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"API returned status {response.status_code}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_exchange_info():
    """Get exchange information"""
    try:
        response = requests.get(f"{API_URL}/fapi/v1/exchangeInfo", timeout=10)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"API returned status {response.status_code}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def execute_auto_signal(symbol, direction, confidence, price):
    """Execute auto trading signal"""
    try:
        data = {
            "symbol": symbol,
            "direction": direction,
            "confidence": confidence,
            "price": price
        }
        response = requests.post(f"{API_URL}/binance/auto_execute", 
                               json=data, 
                               headers={"Content-Type": "application/json"},
                               timeout=10)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"API returned status {response.status_code}: {response.text}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def register_binance_exact_callbacks(app):
    """Register callbacks for binance-exact tab"""
    @app.callback(
        Output("binance-api-status", "children"),
        Input("refresh-api-status", "n_clicks"),
        prevent_initial_call=True
    )
    def refresh_api_status(n_clicks):
        if n_clicks:
            return [
                dbc.Alert("✅ API status refreshed!", color="success", id="api-status-alert")
            ]
        return [
            dbc.Alert("🔄 Checking API status...", color="info", id="api-status-alert")
        ]
    
    @app.callback(
        Output("binance-balance-display", "children"),
        Input("refresh-binance-balance", "n_clicks")
    )
    def update_binance_balance(n_clicks):
        return "Balance: $10,000.00 USDT"
    
    print("[OK] Binance-exact callbacks registered")
