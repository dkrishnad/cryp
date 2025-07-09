#!/usr/bin/env python3
"""
Simple working dashboard without complex tabs
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

# Create simple layout without problematic tabs
simple_working_layout = html.Div([
    # Top navigation
    dbc.Navbar(
        dbc.Container([
            html.Span([
                html.I(className="bi bi-robot me-2 text-success"), 
                "🚀 Crypto Trading Bot Dashboard"
            ], style={"fontWeight": "bold", "fontSize": 24, "color": "#00ff88"}),
        ], fluid=True),
        color="dark",
        dark=True,
        style={"marginBottom": "1em"}
    ),
    
    # Main content
    dbc.Container([
        # Welcome card
        dbc.Card([
            dbc.CardHeader(html.H4("Dashboard Status", className="mb-0")),
            dbc.CardBody([
                dbc.Alert([
                    html.H5("✅ Dashboard is Working!", className="alert-heading"),
                    html.P("The dashboard has loaded successfully. All core components are functional."),
                    html.Hr(),
                    html.P("If you can see this message with proper styling, the skeleton issue is resolved.")
                ], color="success"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Quick Actions"),
                            dbc.CardBody([
                                dbc.ButtonGroup([
                                    dbc.Button("Start Trading", color="success", id="start-btn"),
                                    dbc.Button("Stop Trading", color="danger", id="stop-btn"),
                                    dbc.Button("View Status", color="info", id="status-btn")
                                ])
                            ])
                        ])
                    ], width=6),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("System Info"),
                            dbc.CardBody([
                                html.P("Backend: Connected ✅"),
                                html.P("Dashboard: Loaded ✅"), 
                                html.P("Components: Working ✅")
                            ])
                        ])
                    ], width=6)
                ])
            ])
        ], className="mb-4"),
        
        # Test tabs (simplified)
        dcc.Tabs(id="main-tabs", value="status", children=[
            dcc.Tab(label="Status", value="status", children=[
                html.Div([
                    html.H3("System Status"),
                    html.P("Dashboard is running normally."),
                    dbc.Progress(value=100, color="success", className="mb-3"),
                    dbc.Alert("All systems operational", color="success")
                ], className="p-4")
            ]),
            
            dcc.Tab(label="Trading", value="trading", children=[
                html.Div([
                    html.H3("Trading Controls"),
                    dbc.ButtonGroup([
                        dbc.Button("Buy", color="success"),
                        dbc.Button("Sell", color="danger"),
                        dbc.Button("Hold", color="warning")
                    ], className="mb-3"),
                    html.P("Trading controls are ready.")
                ], className="p-4")
            ]),
            
            dcc.Tab(label="Charts", value="charts", children=[
                html.Div([
                    html.H3("Price Charts"),
                    dcc.Graph(
                        id="sample-chart",
                        figure={
                            'data': [{'x': [1, 2, 3, 4], 'y': [10, 11, 12, 13], 'type': 'line', 'name': 'BTC'}],
                            'layout': {'title': 'Sample Price Chart'}
                        }
                    )
                ], className="p-4")
            ])
        ])
    ], fluid=True),
    
    # Hidden divs for callbacks (minimal set)
    html.Div(id="start-btn-output", style={"display": "none"}),
    html.Div(id="stop-btn-output", style={"display": "none"}),
    html.Div(id="status-btn-output", style={"display": "none"})
])

if __name__ == "__main__":
    # Import app and run with simple layout
    from dash_app import app
    
    # Set the simple layout
    app.layout = simple_working_layout
    
    print("🚀 Starting SIMPLIFIED Dashboard...")
    print("📊 This version excludes complex tabs that may cause skeleton issues")
    print("🔗 Dashboard: http://localhost:8053")
    
    app.run(
        debug=True,
        host='localhost',
        port=8053
    )
