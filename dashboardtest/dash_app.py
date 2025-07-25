import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import os

# Create Dash app with enhanced configuration
app = dash.Dash(
    __name__, 
    suppress_callback_exceptions=False,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css"
    ],
    assets_folder='assets',
    serve_locally=True,
    compress=False,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": "Crypto Trading Bot Dashboard"}
    ]
)

# Server configuration
server = app.server
server.config['SECRET_KEY'] = os.urandom(12)
