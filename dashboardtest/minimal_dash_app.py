"""
Minimal Dash App with Fixed Component Suite Loading
This fixes the /_dash-component-suites/ 500 errors
"""

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import os

# Create Dash app with FORCED local serving to fix component suite issues
app = dash.Dash(
    __name__, 
    suppress_callback_exceptions=False,  # Show callback errors for debugging
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css"
    ],
    # CRITICAL: Force all assets to serve locally to fix 500 errors
    serve_locally=True,  
    assets_folder='assets',
    # REMOVE external Plotly script to fix loading issues
    # external_scripts=[],
    compress=False,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": "Crypto Trading Bot Dashboard"}
    ]
)

# Server configuration
server = app.server
server.config['SECRET_KEY'] = os.urandom(12)

# Enable development tools for debugging
app.config.suppress_callback_exceptions = False
