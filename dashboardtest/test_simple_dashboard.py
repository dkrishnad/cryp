#!/usr/bin/env python3
"""
Simple dashboard test to check if the basic layout can render without errors
"""
import sys
import os
import io

# Windows-specific encoding setup
if os.name == 'nt':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleOutputCP(65001)
        kernel32.SetConsoleCP(65001)
    except:
        pass

# Add current directory to path
dashboard_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(dashboard_dir)
sys.path.insert(0, dashboard_dir)
sys.path.insert(0, parent_dir)

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# Create a simple app with minimal configuration
app = dash.Dash(
    __name__, 
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# Simple test layout
app.layout = html.Div([
    html.H1("🚀 Crypto Bot Dashboard", className="text-center mb-4"),
    html.Div([
        html.H3("Dashboard Status", className="text-info"),
        html.P("✅ Dashboard is running successfully!", className="text-success"),
        html.P("🔧 Backend connection: Testing...", id="backend-status"),
        html.P("📊 WebSocket connection: Testing...", id="websocket-status"),
    ], className="text-center p-4"),
    
    # Simple interval component for updates
    dcc.Interval(
        id='status-interval',
        interval=5000,  # 5 seconds
        n_intervals=0
    )
])

# Simple callback to test if callbacks work
@app.callback(
    [dash.dependencies.Output('backend-status', 'children'),
     dash.dependencies.Output('websocket-status', 'children')],
    [dash.dependencies.Input('status-interval', 'n_intervals')]
)
def update_status(n_intervals):
    """Simple status update callback"""
    try:
        import requests
        
        # Test backend connection
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                backend_status = "🟢 Backend connection: Connected"
            else:
                backend_status = f"🟡 Backend connection: Status {response.status_code}"
        except:
            backend_status = "🔴 Backend connection: Disconnected"
        
        # Test WebSocket (just show configured endpoint)
        websocket_status = "📡 WebSocket: ws://localhost:8000/ws/price"
        
        return backend_status, websocket_status
    except Exception as e:
        return f"🔴 Backend connection: Error - {str(e)}", "🔴 WebSocket: Error"

if __name__ == '__main__':
    print("🧪 Starting Simple Dashboard Test...")
    print("📊 Test dashboard will be available at: http://localhost:8051")
    print("🔍 This will help identify if the issue is with the basic app or specific callbacks")
    
    try:
        app.run(
            debug=True,
            port=8051,
            host='127.0.0.1'
        )
    except Exception as e:
        print(f"❌ Error starting test dashboard: {e}")
