#!/usr/bin/env python3
"""
Minimal Button Test Dashboard - Test one button at a time to identify issues
"""

import sys
import os
import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import requests
import json
from datetime import datetime

# Add dashboard directory to path
dashboard_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, dashboard_dir)

# Import debug logger
from debug_logger import debugger, debug_callback

# Create minimal Dash app
app = dash.Dash(
    __name__, 
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# Simple layout with one button to test
def create_test_layout(button_name="health_check"):
    """Create a test layout with one specific button"""
    
    if button_name == "health_check":
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("🔧 Single Button Test: Health Check", className="text-center mb-4"),
                    html.Hr(),
                    
                    # Health Check Button
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("System Health Check"),
                            dbc.Button(
                                "Check Health",
                                id="health-check-btn",
                                color="primary",
                                size="lg",
                                className="mb-3"
                            ),
                            html.Div(id="health-status", className="mt-3")
                        ])
                    ], className="mb-4"),
                    
                    # Debug Info
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Debug Information"),
                            html.Pre(id="debug-info", style={"fontSize": "12px"})
                        ])
                    ])
                ])
            ])
        ], fluid=True)
    
    elif button_name == "price_fetch":
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("💰 Single Button Test: Price Fetch", className="text-center mb-4"),
                    html.Hr(),
                    
                    # Price Fetch Button
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Fetch Current Price"),
                            dbc.InputGroup([
                                dbc.Input(
                                    id="symbol-input",
                                    placeholder="Enter symbol (e.g., BTCUSDT)",
                                    value="BTCUSDT"
                                ),
                                dbc.Button(
                                    "Get Price",
                                    id="price-fetch-btn",
                                    color="success"
                                )
                            ], className="mb-3"),
                            html.Div(id="price-result", className="mt-3")
                        ])
                    ], className="mb-4"),
                    
                    # Debug Info
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Debug Information"),
                            html.Pre(id="debug-info", style={"fontSize": "12px"})
                        ])
                    ])
                ])
            ])
        ], fluid=True)
    
    elif button_name == "auto_trading":
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("🤖 Single Button Test: Auto Trading", className="text-center mb-4"),
                    html.Hr(),
                    
                    # Auto Trading Controls
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Auto Trading Controls"),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button(
                                        "Start Auto Trading",
                                        id="start-auto-trading-btn",
                                        color="success",
                                        className="me-2"
                                    ),
                                    dbc.Button(
                                        "Stop Auto Trading",
                                        id="stop-auto-trading-btn",
                                        color="danger",
                                        className="me-2"
                                    ),
                                    dbc.Button(
                                        "Check Status",
                                        id="auto-trading-status-btn",
                                        color="info"
                                    )
                                ])
                            ], className="mb-3"),
                            html.Div(id="auto-trading-result", className="mt-3")
                        ])
                    ], className="mb-4"),
                    
                    # Debug Info
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Debug Information"),
                            html.Pre(id="debug-info", style={"fontSize": "12px"})
                        ])
                    ])
                ])
            ])
        ], fluid=True)
    
    # Default: show all available tests
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("🧪 Button Test Selection", className="text-center mb-4"),
                html.Hr(),
                
                html.P("Select which button test to run:", className="lead"),
                
                dbc.ListGroup([
                    dbc.ListGroupItem([
                        dbc.Button("Test Health Check Button", href="?test=health_check", color="primary", className="w-100")
                    ]),
                    dbc.ListGroupItem([
                        dbc.Button("Test Price Fetch Button", href="?test=price_fetch", color="success", className="w-100")
                    ]),
                    dbc.ListGroupItem([
                        dbc.Button("Test Auto Trading Buttons", href="?test=auto_trading", color="warning", className="w-100")
                    ])
                ])
            ])
        ])
    ], fluid=True)

# Get test type from URL parameter (simulation)
test_type = "health_check"  # Default test

# Set the layout
app.layout = create_test_layout(test_type)

# Health Check Button Callback
@app.callback(
    [Output("health-status", "children"),
     Output("debug-info", "children")],
    [Input("health-check-btn", "n_clicks")],
    prevent_initial_call=True
)
@debug_callback("health_check_callback")
def test_health_check(n_clicks):
    """Test the health check functionality"""
    if not n_clicks:
        return "", ""
    
    debugger.log_button_click("health-check-btn", n_clicks, {"test": "health_check"})
    
    try:
        # Test backend connection
        response = requests.get("http://localhost:5000/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            # Format the health data nicely
            health_display = dbc.Alert([
                html.H5("✅ Backend is Healthy!", className="alert-heading"),
                html.P(f"Status: {data.get('status', 'unknown')}"),
                html.P(f"Message: {data.get('message', 'No message')}"),
                html.P(f"Timestamp: {data.get('timestamp', 'No timestamp')}"),
                html.Hr(),
                html.P("Components Status:", className="mb-1"),
                html.Pre(json.dumps(data.get('components', {}), indent=2))
            ], color="success")
            
            debug_info = f"""Health Check Test Results:
✅ Backend connection: SUCCESS
✅ Response status: {response.status_code}
✅ Response time: {response.elapsed.total_seconds():.3f}s
✅ Data received: {len(str(data))} characters

Raw Response:
{json.dumps(data, indent=2)}"""
            
        else:
            health_display = dbc.Alert([
                html.H5("⚠️ Backend Response Error", className="alert-heading"),
                html.P(f"Status Code: {response.status_code}"),
                html.P(f"Response: {response.text[:200]}...")
            ], color="warning")
            
            debug_info = f"""Health Check Test Results:
❌ Backend error: HTTP {response.status_code}
⚠️ Response: {response.text[:200]}..."""
    
    except requests.exceptions.ConnectionError:
        health_display = dbc.Alert([
            html.H5("❌ Backend Connection Failed", className="alert-heading"),
            html.P("Cannot connect to backend at http://localhost:5000"),
            html.P("Make sure the backend is running!")
        ], color="danger")
        
        debug_info = """Health Check Test Results:
❌ Backend connection: FAILED
❌ Error: Connection refused
❌ Backend may not be running on port 5000"""
    
    except Exception as e:
        health_display = dbc.Alert([
            html.H5("❌ Unexpected Error", className="alert-heading"),
            html.P(f"Error: {str(e)}")
        ], color="danger")
        
        debug_info = f"""Health Check Test Results:
❌ Unexpected error: {str(e)}
❌ Error type: {type(e).__name__}"""
    
    return health_display, debug_info

if __name__ == "__main__":
    print("🧪 Starting Minimal Button Test Dashboard...")
    print("📊 Testing individual buttons to identify issues")
    print("🌐 Dashboard available at: http://localhost:8051")
    
    try:
        app.run(
            debug=True,
            host='localhost',
            port=8051,  # Different port to avoid conflicts
            dev_tools_ui=True,
            dev_tools_props_check=True
        )
    except Exception as e:
        print(f"❌ Error starting test dashboard: {e}")
