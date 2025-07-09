import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import os
import logging

# Set up logger
logger = logging.getLogger(__name__)

# Create Dash app with enhanced debugging configuration
app = dash.Dash(
    __name__, 
    suppress_callback_exceptions=False,  # Show callback exceptions
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css"
    ],
    # Load Plotly from CDN to fix 500 errors
    external_scripts=[
        "https://cdn.plot.ly/plotly-2.27.0.min.js"
    ],
    assets_folder='assets',
    serve_locally=False,
    compress=False,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": "Crypto Trading Bot Dashboard"}
    ]
)

# Enable client-side callback debugging
app.clientside_callback_manager.callback_context_id = True

# Server configuration
server = app.server
server.config['SECRET_KEY'] = os.urandom(12)

# Add request logging
@server.before_request
def log_request_info():
    from flask import request
    logger.info(f"Request: {request.method} {request.url}")

@server.after_request
def log_response_info(response):
    logger.info(f"Response: {response.status_code}")
    return response

# Add callback debugging
original_callback = app.callback

def debug_callback(*args, **kwargs):
    """Wrapper to add debugging to callbacks"""
    def decorator(func):
        logger.info(f"Registering callback for function: {func.__name__}")
        if 'outputs' in kwargs:
            outputs = kwargs['outputs']
            if isinstance(outputs, list):
                logger.info(f"Callback outputs: {[str(output) for output in outputs]}")
            else:
                logger.info(f"Callback output: {str(outputs)}")
        
        def wrapper(*callback_args, **callback_kwargs):
            from dash import callback_context
            logger.info(f"Executing callback: {func.__name__}")
            if callback_context.triggered:
                for trigger in callback_context.triggered:
                    logger.info(f"Triggered by: {trigger['prop_id']} = {trigger['value']}")
            
            try:
                result = func(*callback_args, **callback_kwargs)
                logger.info(f"Callback {func.__name__} executed successfully")
                return result
            except Exception as e:
                logger.error(f"Callback {func.__name__} failed: {str(e)}")
                raise
        
        return original_callback(*args, **kwargs)(wrapper)
    return decorator

# Replace the callback decorator with debug version
app.callback = debug_callback

logger.info("Debug Dash app initialized with enhanced logging")
