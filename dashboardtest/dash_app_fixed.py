"""
Minimal Working Dash App Configuration
Fixes component suite serving issues
"""

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import os

# Create Dash app with minimal, working configuration
app = dash.Dash(
    __name__, 
    suppress_callback_exceptions=False,  # Show callback exceptions for debugging
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css"
    ],
    # Use CDN for Plotly instead of local serving
    external_scripts=[
        "https://cdn.plot.ly/plotly-2.27.0.min.js"
    ],
    # Critical fixes for component suite issues
    serve_locally=True,           # Serve assets locally
    compress=False,               # Disable compression to avoid errors
    assets_folder='assets',       # Ensure assets folder exists
    dev_tools_ui=True,           # Enable dev tools
    dev_tools_props_check=True,  # Enable prop checking
    dev_tools_serve_dev_bundles=True,  # Serve dev bundles
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": "Crypto Trading Bot Dashboard"}
    ]
)

# Server configuration
server = app.server
server.config['SECRET_KEY'] = os.urandom(12)

# Add specific configuration to fix component suite serving
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

