#!/usr/bin/env python3
"""
Simplified dashboard app for testing
"""

import sys
import os
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# Simple app without complex imports
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# Simple layout for testing
app.layout = html.Div([
    html.H1("🚀 Crypto Bot Dashboard - Test Mode", className="text-center mb-4"),
    html.P("This is a test version to verify basic functionality.", className="text-center"),
    
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("✅ Dashboard Status"),
                        html.P("Dashboard is running successfully!"),
                        html.P("Backend should be accessible at: http://localhost:8000"),
                        html.P("Dashboard is accessible at: http://localhost:8050"),
                    ])
                ])
            ], width=12)
        ])
    ])
])

if __name__ == '__main__':
    print("🚀 Starting Test Dashboard...")
    print("📊 Test dashboard will be available at: http://localhost:8050")
    
    try:
        app.run_server(
            debug=False,
            host='localhost',
            port=8050
        )
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
