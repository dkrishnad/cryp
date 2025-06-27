"""
Binance-exact dashboard callbacks
Handles all interactions for the Binance-exact API dashboard
"""

import dash
from dash import Input, Output, State, html, callback_context
import dash_bootstrap_components as dbc
import json
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from binance_exact_layout import (
        check_api_status, get_account_info, get_balance_info, get_positions,
        place_order, get_open_orders, set_leverage, set_margin_type,
        get_24hr_tickers, get_exchange_info, execute_auto_signal
    )
except ImportError:
    from dashboard.binance_exact_layout import (
        check_api_status, get_account_info, get_balance_info, get_positions,
        place_order, get_open_orders, set_leverage, set_margin_type,
        get_24hr_tickers, get_exchange_info, execute_auto_signal
    )

def register_binance_exact_callbacks(app):
    """Register all callbacks for Binance-exact dashboard"""
    
    @app.callback(
        Output('binance-api-status', 'children'),
        Input('refresh-api-status', 'n_clicks'),
        prevent_initial_call=False
    )
    def update_api_status(n_clicks):
        """Update API status display"""
        success, message = check_api_status()
        
        if success:
            return dbc.Alert([
                html.I(className="fas fa-check-circle me-2"),
                f"✅ Connected - {message}"
            ], color="success")
        else:
            return dbc.Alert([
                html.I(className="fas fa-exclamation-triangle me-2"),
                f"❌ Disconnected - {message}"
            ], color="danger")
    
    @app.callback(
        Output('binance-account-info', 'children'),
        [Input('load-account-btn', 'n_clicks'),
         Input('load-balance-btn', 'n_clicks')],
        prevent_initial_call=True
    )
    def load_account_data(account_clicks, balance_clicks):
        """Load account or balance information"""
        ctx = callback_context
        
        if not ctx.triggered:
            return html.P("Click a button to load account data")
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'load-account-btn':
            success, data = get_account_info()
            if success:
                return dbc.Card([
                    dbc.CardHeader("Account Information"),
                    dbc.CardBody([
                        html.P(f"Total Wallet Balance: {data.get('totalWalletBalance', 'N/A')} USDT"),
                        html.P(f"Available Balance: {data.get('availableBalance', 'N/A')} USDT"),
                        html.P(f"Total Unrealized PnL: {data.get('totalUnrealizedProfit', 'N/A')} USDT"),
                        html.P(f"Total Margin Balance: {data.get('totalMarginBalance', 'N/A')} USDT"),
                        html.P(f"Max Withdraw Amount: {data.get('maxWithdrawAmount', 'N/A')} USDT"),
                        html.Hr(),
                        html.Pre(json.dumps(data, indent=2), 
                                style={'fontSize': '10px', 'maxHeight': '200px', 'overflow': 'auto'})
                    ])
                ], color="light")
            else:
                return dbc.Alert(f"Failed to load account: {data}", color="danger")
                
        elif button_id == 'load-balance-btn':
            success, data = get_balance_info()
            if success:
                balance_cards = []
                for asset in data:
                    if float(asset.get('balance', 0)) > 0:
                        balance_cards.append(
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6(asset.get('asset', 'Unknown'), className="card-title"),
                                    html.P(f"Balance: {asset.get('balance', 'N/A')}"),
                                    html.P(f"Available: {asset.get('availableBalance', 'N/A')}"),
                                    html.P(f"Unrealized PnL: {asset.get('unrealizedProfit', 'N/A')}")
                                ])
                            ], className="mb-2")
                        )
                
                if balance_cards:
                    return html.Div(balance_cards)
                else:
                    return dbc.Alert("No assets with positive balance found", color="info")
            else:
                return dbc.Alert(f"Failed to load balance: {data}", color="danger")
        
        return html.P("No action taken")
    
    @app.callback(
        Output('binance-positions-info', 'children'),
        Input('get-positions-btn', 'n_clicks'),
        State('position-symbol', 'value'),
        prevent_initial_call=True
    )
    def load_positions(n_clicks, symbol):
        """Load position information"""
        if not n_clicks:
            return html.P("Click to load positions")
        
        success, data = get_positions(symbol if symbol else None)
        
        if success:
            if not data:
                return dbc.Alert("No positions found", color="info")
            
            position_cards = []
            for pos in data:
                if float(pos.get('positionAmt', 0)) != 0:
                    pnl = float(pos.get('unrealizedProfit', 0))
                    pnl_color = "success" if pnl >= 0 else "danger"
                    
                    position_cards.append(
                        dbc.Card([
                            dbc.CardHeader(f"{pos.get('symbol', 'Unknown')} - {pos.get('positionSide', 'Unknown')}"),
                            dbc.CardBody([
                                html.P(f"Position Amount: {pos.get('positionAmt', 'N/A')}"),
                                html.P(f"Entry Price: {pos.get('entryPrice', 'N/A')}"),
                                html.P(f"Mark Price: {pos.get('markPrice', 'N/A')}"),
                                html.P(f"Unrealized PnL: ", className="d-inline"),
                                html.Span(f"{pos.get('unrealizedProfit', 'N/A')}", 
                                         className=f"text-{pnl_color} fw-bold"),
                                html.P(f"Percentage: {pos.get('percentage', 'N/A')}%"),
                                html.P(f"Leverage: {pos.get('leverage', 'N/A')}x"),
                                html.P(f"Margin Type: {pos.get('marginType', 'N/A')}")
                            ])
                        ], className="mb-2")
                    )
            
            if position_cards:
                return html.Div(position_cards)
            else:
                return dbc.Alert("No open positions found", color="info")
        else:
            return dbc.Alert(f"Failed to load positions: {data}", color="danger")
    
    @app.callback(
        Output('order-result', 'children'),
        [Input('place-order-btn', 'n_clicks'),
         Input('get-orders-btn', 'n_clicks')],
        [State('order-symbol', 'value'),
         State('order-side', 'value'),
         State('order-type', 'value'),
         State('order-quantity', 'value'),
         State('order-price', 'value')],
        prevent_initial_call=True
    )
    def handle_orders(place_clicks, get_clicks, symbol, side, order_type, quantity, price):
        """Handle order placement and retrieval"""
        ctx = callback_context
        
        if not ctx.triggered:
            return html.P("No action taken")
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'place-order-btn':
            if not all([symbol, side, order_type, quantity]):
                return dbc.Alert("Please fill all required fields", color="warning")
            
            success, data = place_order(symbol, side, order_type, quantity, price)
            
            if success:
                return dbc.Card([
                    dbc.CardHeader("Order Placed Successfully"),
                    dbc.CardBody([
                        html.P(f"Order ID: {data.get('orderId', 'N/A')}"),
                        html.P(f"Symbol: {data.get('symbol', 'N/A')}"),
                        html.P(f"Side: {data.get('side', 'N/A')}"),
                        html.P(f"Type: {data.get('type', 'N/A')}"),
                        html.P(f"Quantity: {data.get('origQty', 'N/A')}"),
                        html.P(f"Status: {data.get('status', 'N/A')}"),
                        html.Hr(),
                        html.Pre(json.dumps(data, indent=2), 
                                style={'fontSize': '10px', 'maxHeight': '200px', 'overflow': 'auto'})
                    ])
                ], color="success")
            else:
                return dbc.Alert(f"Order failed: {data}", color="danger")
                
        elif button_id == 'get-orders-btn':
            success, data = get_open_orders()
            
            if success:
                if not data:
                    return dbc.Alert("No open orders found", color="info")
                
                order_cards = []
                for order in data:
                    order_cards.append(
                        dbc.Card([
                            dbc.CardHeader(f"Order {order.get('orderId', 'Unknown')}"),
                            dbc.CardBody([
                                html.P(f"Symbol: {order.get('symbol', 'N/A')}"),
                                html.P(f"Side: {order.get('side', 'N/A')}"),
                                html.P(f"Type: {order.get('type', 'N/A')}"),
                                html.P(f"Quantity: {order.get('origQty', 'N/A')}"),
                                html.P(f"Price: {order.get('price', 'N/A')}"),
                                html.P(f"Status: {order.get('status', 'N/A')}")
                            ])
                        ], className="mb-2")
                    )
                
                return html.Div(order_cards)
            else:
                return dbc.Alert(f"Failed to get orders: {data}", color="danger")
        
        return html.P("No action taken")
    
    @app.callback(
        Output('leverage-result', 'children'),
        [Input('set-leverage-btn', 'n_clicks'),
         Input('set-margin-btn', 'n_clicks')],
        [State('leverage-symbol', 'value'),
         State('leverage-value', 'value'),
         State('margin-type', 'value')],
        prevent_initial_call=True
    )
    def handle_leverage_margin(leverage_clicks, margin_clicks, symbol, leverage, margin_type):
        """Handle leverage and margin type changes"""
        ctx = callback_context
        
        if not ctx.triggered:
            return html.P("No action taken")
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'set-leverage-btn':
            if not symbol or not leverage:
                return dbc.Alert("Please fill symbol and leverage", color="warning")
            
            success, data = set_leverage(symbol, leverage)
            
            if success:
                return dbc.Card([
                    dbc.CardHeader("Leverage Updated"),
                    dbc.CardBody([
                        html.P(f"Symbol: {data.get('symbol', 'N/A')}"),
                        html.P(f"Leverage: {data.get('leverage', 'N/A')}x"),
                        html.P(f"Max Notional Value: {data.get('maxNotionalValue', 'N/A')}")
                    ])
                ], color="success")
            else:
                return dbc.Alert(f"Failed to set leverage: {data}", color="danger")
                
        elif button_id == 'set-margin-btn':
            if not symbol or not margin_type:
                return dbc.Alert("Please fill symbol and margin type", color="warning")
            
            success, data = set_margin_type(symbol, margin_type)
            
            if success:
                return dbc.Card([
                    dbc.CardHeader("Margin Type Updated"),
                    dbc.CardBody([
                        html.P(f"Symbol: {symbol}"),
                        html.P(f"Margin Type: {margin_type}"),
                        html.P("✅ Successfully updated")
                    ])
                ], color="success")
            else:
                return dbc.Alert(f"Failed to set margin type: {data}", color="danger")
        
        return html.P("No action taken")
    
    @app.callback(
        Output('market-data-result', 'children'),
        [Input('get-tickers-btn', 'n_clicks'),
         Input('get-exchange-btn', 'n_clicks')],
        prevent_initial_call=True
    )
    def handle_market_data(tickers_clicks, exchange_clicks):
        """Handle market data requests"""
        ctx = callback_context
        
        if not ctx.triggered:
            return html.P("No action taken")
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'get-tickers-btn':
            success, data = get_24hr_tickers()
            
            if success:
                ticker_cards = []
                for ticker in data[:5]:  # Show first 5 tickers
                    price_change = float(ticker.get('priceChangePercent', 0))
                    color = "success" if price_change >= 0 else "danger"
                    
                    ticker_cards.append(
                        dbc.Card([
                            dbc.CardHeader(ticker.get('symbol', 'Unknown')),
                            dbc.CardBody([
                                html.P(f"Last Price: {ticker.get('lastPrice', 'N/A')}"),
                                html.P([
                                    "24h Change: ",
                                    html.Span(f"{ticker.get('priceChangePercent', 'N/A')}%", 
                                             className=f"text-{color} fw-bold")
                                ]),
                                html.P(f"Volume: {ticker.get('volume', 'N/A')}"),
                                html.P(f"High: {ticker.get('highPrice', 'N/A')}"),
                                html.P(f"Low: {ticker.get('lowPrice', 'N/A')}")
                            ])
                        ], className="mb-2")
                    )
                
                return html.Div(ticker_cards)
            else:
                return dbc.Alert(f"Failed to get tickers: {data}", color="danger")
                
        elif button_id == 'get-exchange-btn':
            success, data = get_exchange_info()
            
            if success:
                return dbc.Card([
                    dbc.CardHeader("Exchange Information"),
                    dbc.CardBody([
                        html.P(f"Timezone: {data.get('timezone', 'N/A')}"),
                        html.P(f"Server Time: {datetime.fromtimestamp(data.get('serverTime', 0)/1000).strftime('%Y-%m-%d %H:%M:%S')}"),
                        html.P(f"Futures Type: {data.get('futuresType', 'N/A')}"),
                        html.P(f"Available Symbols: {len(data.get('symbols', []))}"),
                        html.Hr(),
                        html.H6("Rate Limits:"),
                        html.Ul([
                            html.Li(f"{limit.get('rateLimitType', 'Unknown')}: {limit.get('limit', 'N/A')} per {limit.get('interval', 'N/A')}")
                            for limit in data.get('rateLimits', [])
                        ])
                    ])
                ], color="info")
            else:
                return dbc.Alert(f"Failed to get exchange info: {data}", color="danger")
        
        return html.P("No action taken")
    
    @app.callback(
        Output('auto-trading-result', 'children'),
        Input('execute-auto-btn', 'n_clicks'),
        [State('auto-symbol', 'value'),
         State('auto-direction', 'value'),
         State('auto-confidence', 'value'),
         State('auto-price', 'value')],
        prevent_initial_call=True
    )
    def handle_auto_trading(n_clicks, symbol, direction, confidence, price):
        """Handle auto trading signal execution"""
        if not n_clicks:
            return html.P("Click to execute auto signal")
        
        if not all([symbol, direction, confidence, price]):
            return dbc.Alert("Please fill all fields", color="warning")
        
        success, data = execute_auto_signal(symbol, direction, confidence, price)
        
        if success:
            if data.get('status') == 'success':
                return dbc.Card([
                    dbc.CardHeader("Auto Signal Executed Successfully"),
                    dbc.CardBody([
                        html.P(f"✅ {data.get('message', 'Signal executed')}"),
                        html.P(f"Symbol: {symbol}"),
                        html.P(f"Direction: {direction}"),
                        html.P(f"Confidence: {confidence * 100:.1f}%"),
                        html.P(f"Price: {price}"),
                        html.P(f"Leverage: {data.get('leverage', 'N/A')}x"),
                        html.P(f"Quantity: {data.get('quantity', 'N/A')}"),
                        html.P(f"Margin Used: {data.get('margin_used', 'N/A')} USDT"),
                        html.Hr(),
                        html.H6("Order Details:"),
                        html.Pre(json.dumps(data.get('order', {}), indent=2), 
                                style={'fontSize': '10px', 'maxHeight': '200px', 'overflow': 'auto'})
                    ])
                ], color="success")
            else:
                return dbc.Alert(f"Auto trading failed: {data.get('message', 'Unknown error')}", color="danger")
        else:
            return dbc.Alert(f"Failed to execute auto signal: {data}", color="danger")
