#!/usr/bin/env python3
"""
Dashboard integration for Hybrid Learning System
Adds hybrid learning monitoring to the existing dashboard
"""
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import requests
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime
import pandas as pd

# Backend URL
API_URL = "http://localhost:5000"

def create_hybrid_learning_layout():
    """Create layout for hybrid learning monitoring"""
    
    return html.Div([
        html.H2("🤖 Hybrid Learning System", className="text-center mb-4"),
        
        # System Status Row
        html.Div([
            html.Div([
                html.H4("System Status", className="card-title"),
                html.Div(id="hybrid-system-status", children=[
                    html.Span("Loading...", className="text-muted")
                ])
            ], className="card-body")
        ], className="card mb-4"),
        
        # Performance Metrics Row
        html.Div([
            # Online Learning Stats
            html.Div([
                html.Div([
                    html.H5("🧠 Online Learning", className="card-title"),
                    html.Div(id="online-learning-stats")
                ], className="card-body")
            ], className="card col-md-6"),
            
            # Data Collection Stats  
            html.Div([
                html.Div([
                    html.H5("📡 Data Collection", className="card-title"),
                    html.Div(id="data-collection-stats")
                ], className="card-body")
            ], className="card col-md-6")
        ], className="row mb-4"),
        
        # Predictions Row
        html.Div([
            html.Div([
                html.H4("🎯 Hybrid Predictions", className="card-title"),
                html.Div([
                    # Symbol selector
                    html.Div([
                        html.Label("Select Symbol:", className="form-label"),
                        dcc.Dropdown(
                            id="hybrid-symbol-selector",
                            options=[
                                {"label": "BTC/USDT", "value": "btcusdt"},
                                {"label": "KAIA/USDT", "value": "kaiausdt"},
                                {"label": "ETH/USDT", "value": "ethusdt"},
                                {"label": "SOL/USDT", "value": "solusdt"}
                            ],
                            value="btcusdt",
                            className="mb-3"
                        )
                    ], className="col-md-4"),
                    
                    # Prediction display
                    html.Div([
                        html.Div(id="hybrid-prediction-display")
                    ], className="col-md-8")
                ], className="row"),
                
                # Controls
                html.Div([
                    html.Button(
                        "🔄 Update Prediction", 
                        id="hybrid-predict-btn",
                        className="btn btn-primary me-2"
                    ),
                    html.Button(
                        "🧠 Trigger Learning Update", 
                        id="hybrid-update-btn",
                        className="btn btn-info me-2"
                    ),
                    html.Button(
                        "📊 Add Training Data", 
                        id="hybrid-add-data-btn",
                        className="btn btn-success"
                    )
                ], className="mt-3")
            ], className="card-body")
        ], className="card mb-4"),
        
        # Performance History
        html.Div([
            html.Div([
                html.H4("📈 Performance History", className="card-title"),
                dcc.Graph(id="hybrid-performance-chart")
            ], className="card-body")
        ], className="card mb-4"),
        
        # Configuration
        html.Div([
            html.Div([
                html.H4("⚙️ Configuration", className="card-title"),
                html.Div([
                    html.Div([
                        html.Label("Batch Model Weight:", className="form-label"),
                        dcc.Slider(
                            id="batch-weight-slider",
                            min=0.1, max=0.9, step=0.1, value=0.7,
                            marks={i/10: f"{i/10:.1f}" for i in range(1, 10)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ], className="col-md-6"),
                    
                    html.Div([
                        html.Label("Online Update Interval (minutes):", className="form-label"),
                        dcc.Input(
                            id="update-interval-input",
                            type="number",
                            value=30,
                            min=5, max=120,
                            className="form-control"
                        )
                    ], className="col-md-6")
                ], className="row"),
                
                html.Button(
                    "💾 Save Configuration",
                    id="save-config-btn", 
                    className="btn btn-warning mt-3"
                )
            ], className="card-body")
        ], className="card mb-4"),
        
        # Auto-refresh interval
        dcc.Interval(
            id="hybrid-refresh-interval",
            interval=30*1000,  # 30 seconds
            n_intervals=0
        ),
        
        # Status messages
        html.Div(id="hybrid-status-messages"),
        
        # Additional AI/ML components for comprehensive integration
        html.Div([
            html.H4([html.I(className="bi bi-graph-up me-1 text-success"), "📊 Enhanced Backtest Results"], className="mb-3"),
            dbc.Card([
                dbc.CardBody([
                    html.Div(id="comprehensive-backtest-output"),
                    dbc.Progress(id="backtest-progress", value=0, className="mt-2"),
                    html.Div(id="backtest-results-enhanced", className="mt-3")
                ])
            ])
        ], className="mb-4"),
        
        # Hybrid Status Display
        html.Div([
            html.H4("📊 Hybrid System Status", className="mb-3"),
            dbc.Card([
                dbc.CardBody([
                    html.Div(id="hybrid-status-display")
                ])
            ])
        ], className="mb-4"),
        
    ], className="container-fluid")

def register_hybrid_learning_callbacks(app):
    """Register callbacks for hybrid learning dashboard"""
    
    @app.callback(
        Output("hybrid-system-status", "children"),
        Input("hybrid-refresh-interval", "n_intervals")
    )
    def update_system_status(n_intervals):
        """Update system status display"""
        try:
            resp = requests.get(f"{API_URL}/ml/hybrid/status", timeout=5)
            if resp.status_code == 200:
                data = resp.json().get("data", {})
                
                status_items = [
                    html.Div([
                        html.Strong("System: "),
                        html.Span(
                            "🟢 Running" if data.get("system_running") else "🔴 Stopped",
                            className="text-success" if data.get("system_running") else "text-danger"
                        )
                    ]),
                    html.Div([
                        html.Strong("Batch Model: "),
                        html.Span(
                            "✅ Loaded" if data.get("batch_model_loaded") else "❌ Not Loaded",
                            className="text-success" if data.get("batch_model_loaded") else "text-warning"
                        )
                    ]),
                    html.Div([
                        html.Strong("Data Collection: "),
                        html.Span(
                            "🟢 Active" if data.get("data_collection", {}).get("is_running") else "🔴 Inactive",
                            className="text-success" if data.get("data_collection", {}).get("is_running") else "text-warning"
                        )
                    ]),
                    html.Div([
                        html.Strong("Last Batch Retrain: "),
                        html.Span(data.get("last_batch_retrain", "Never"))
                    ])
                ]
                
                return status_items
            else:
                return [html.Span("❌ Unable to fetch status", className="text-danger")]
                
        except Exception as e:
            return [html.Span(f"❌ Error: {str(e)}", className="text-danger")]
    
    @app.callback(
        Output("online-learning-stats", "children"),
        Input("hybrid-refresh-interval", "n_intervals")
    )
    def update_online_stats(n_intervals):
        """Update online learning statistics"""
        try:
            resp = requests.get(f"{API_URL}/ml/online/stats", timeout=5)
            if resp.status_code == 200:
                stats = resp.json().get("stats", {})
                
                stats_items = [
                    html.Div([
                        html.Strong("Buffer Size: "),
                        html.Span(str(stats.get("buffer_size", 0)))
                    ]),
                    html.Div([
                        html.Strong("Total Models: "),
                        html.Span(str(stats.get("total_models", 0)))
                    ])                ]
                
                # Add individual model stats
                for model_name, model_stats in stats.items():
                    if isinstance(model_stats, dict) and "model_type" in model_stats:
                        accuracy = model_stats.get("recent_accuracy", 0)
                        stats_items.append(
                            html.Div([
                                html.Strong(f"{model_name}: "),
                                html.Span(f"{accuracy:.4f}", 
                                         className="text-success" if accuracy > 0.6 else "text-warning")
                            ])
                        )
                
                return stats_items
            else:
                return [html.Span("❌ Unable to fetch stats", className="text-danger")]
        except Exception as e:
            return [html.Span(f"❌ Error: {str(e)}", className="text-danger")]
    
    @app.callback(
        Output("data-collection-stats", "children"),
        Input("hybrid-refresh-interval", "n_intervals")
    )
    def update_data_collection_stats(n_intervals):
        """Update data collection statistics"""
        try:
            resp = requests.get(f"{API_URL}/ml/data_collection/stats", timeout=5)
            if resp.status_code == 200:
                stats = resp.json().get("stats", {})
                
                stats_items = [
                    html.Div([
                        html.Strong("Status: "),
                        html.Span(
                            "🟢 Active" if stats.get("is_running") else "🔴 Inactive",
                            className="text-success" if stats.get("is_running") else "text-warning"
                        )
                    ]),
                    html.Div([
                        html.Strong("Interval: "),
                        html.Span(f"{stats.get('collection_interval', 0)} seconds")
                    ])
                ]
                
                # Add symbol stats
                symbol_stats = stats.get("symbol_stats", {})
                for symbol, symbol_data in symbol_stats.items():
                    records = symbol_data.get("total_records", 0)
                    stats_items.append(
                        html.Div([
                            html.Strong(f"{symbol}: "),
                            html.Span(f"{records} records")
                        ])
                    )
                
                return stats_items
            else:                return [html.Span("❌ Unable to fetch stats", className="text-danger")]
        except Exception as e:
            return [html.Span(f"❌ Error: {str(e)}", className="text-danger")]
    
    @app.callback(
        Output("hybrid-prediction-display", "children"),
        [Input("hybrid-predict-btn", "n_clicks"),
         Input("hybrid-symbol-selector", "value"),
         Input("hybrid-refresh-interval", "n_intervals")],
        prevent_initial_call=False
    )
    def update_prediction_display(n_clicks, symbol, n_intervals):
        """Update prediction display"""
        print(f"🔍 HYBRID PREDICTION CALLBACK: symbol={symbol}, n_clicks={n_clicks}, n_intervals={n_intervals}")
        try:
            resp = requests.get(f"{API_URL}/ml/hybrid/predict?symbol={symbol}", timeout=5)
            if resp.status_code == 200:
                result = resp.json()
                prediction = result.get("prediction", {})
                
                ensemble_pred = prediction.get("ensemble_prediction", 0)
                ensemble_conf = prediction.get("ensemble_confidence", 0)
                timestamp = prediction.get("timestamp", "Unknown")
                
                # Get individual predictions from nested structure
                online_predictions = prediction.get("online_predictions", {})
                individual_preds = online_predictions.get("individual_predictions", {})
                
                prediction_display = [
                    html.Div([
                        html.H5("Ensemble Prediction", className="text-primary"),
                        html.H3(
                            "📈 BUY" if ensemble_pred == 1 else "📉 SELL",
                            className="text-success" if ensemble_pred == 1 else "text-danger"
                        ),
                        html.P(f"Confidence: {ensemble_conf:.2%}", className="text-muted"),
                        html.Small(f"Updated: {timestamp}", className="text-muted")
                    ], className="text-center mb-3"),
                    
                    html.Hr(),
                    
                    # Individual predictions
                    html.Div([
                        html.H6("Individual Predictions:", className="mb-2"),
                        html.Div([
                            html.Strong("Batch Model: "),
                            html.Span(
                                str(prediction.get("batch_prediction", "N/A")),
                                className="badge bg-primary ms-1"
                            )
                        ] if prediction.get("batch_prediction") is not None else []),
                        
                        html.Div([
                            html.Strong("Online Models: "),
                            html.Div([
                                html.Span(
                                    f"{name}: {'BUY' if pred == 1 else 'SELL' if pred == -1 else 'HOLD'}", 
                                    className="badge bg-info ms-1"
                                ) for name, pred in individual_preds.items()
                            ]) if individual_preds else html.Span("No online models", className="text-muted")
                        ])
                    ])
                ]
                
                return prediction_display
            else:
                return [html.Span("❌ Unable to fetch prediction", className="text-danger")]
                
        except Exception as e:
            return [html.Span(f"❌ Error: {str(e)}", className="text-danger")]
    
    @app.callback(
        Output("hybrid-status-messages", "children"),
        [Input("hybrid-update-btn", "n_clicks"),
         Input("hybrid-add-data-btn", "n_clicks"),
         Input("save-config-btn", "n_clicks")],
        [State("batch-weight-slider", "value"),
         State("update-interval-input", "value")],
        prevent_initial_call=True
    )
    def handle_actions(update_clicks, add_data_clicks, save_config_clicks, batch_weight, update_interval):
        """Handle action button clicks"""
        ctx = dash.callback_context
        if not ctx.triggered:
            return []
            
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        try:
            if button_id == "hybrid-update-btn":
                resp = requests.post(f"{API_URL}/ml/online/update?batch_size=20", timeout=10)
                if resp.status_code == 200:
                    results = resp.json().get("update_results", {})
                    return [html.Div(f"✅ Models updated: {results}", className="alert alert-success")]
                else:
                    return [html.Div("❌ Update failed", className="alert alert-danger")]
                    
            elif button_id == "hybrid-add-data-btn":
                # Add sample training data
                sample_data = {
                    "features": {
                        "open": 45000, "high": 46000, "low": 44500, "close": 45500,
                        "volume": 1000000, "rsi": 65.2, "macd": 1.23
                    },
                    "target": 1,
                    "symbol": "SAMPLE"
                }
                resp = requests.post(f"{API_URL}/ml/online/add_training_data", json=sample_data, timeout=5)
                if resp.status_code == 200:
                    buffer_size = resp.json().get("buffer_size", 0)
                    return [html.Div(f"✅ Training data added. Buffer: {buffer_size}", className="alert alert-success")]
                else:
                    return [html.Div("❌ Failed to add data", className="alert alert-danger")]
                    
            elif button_id == "save-config-btn":
                config = {
                    "ensemble_weight_batch": batch_weight,
                    "ensemble_weight_online": 1 - batch_weight,
                    "online_update_interval_minutes": update_interval
                }
                resp = requests.post(f"{API_URL}/ml/hybrid/config", json=config, timeout=5)
                if resp.status_code == 200:
                    return [html.Div("✅ Configuration saved", className="alert alert-success")]
                else:
                    return [html.Div("❌ Failed to save config", className="alert alert-danger")]
                    
        except Exception as e:
            return [html.Div(f"❌ Error: {str(e)}", className="alert alert-danger")]
        
        return []
    
    @app.callback(
        Output("hybrid-performance-chart", "figure"),
        Input("hybrid-refresh-interval", "n_intervals")
    )
    def update_performance_chart(n_intervals):
        """Update performance history chart"""
        try:
            resp = requests.get(f"{API_URL}/ml/performance/history", timeout=5)
            if resp.status_code == 200:
                history = resp.json().get("performance_history", [])
                
                if history:
                    df = pd.DataFrame(history)
                    df["timestamp"] = pd.to_datetime(df["timestamp"])
                    
                    # Extract accuracy from performance data
                    df["accuracy"] = df["performance"].apply(
                        lambda x: x.get("accuracy", 0) if isinstance(x, dict) else 0
                    )
                    
                    fig = px.line(
                        df, x="timestamp", y="accuracy",
                        title="Model Performance Over Time",
                        labels={"accuracy": "Accuracy", "timestamp": "Time"}
                    )
                    fig.update_layout(
                        height=300,
                        margin=dict(l=20, r=20, t=40, b=20)
                    )
                    return fig
                else:
                    # Empty chart
                    fig = go.Figure()
                    fig.add_annotation(
                        text="No performance history available",
                        xref="paper", yref="paper",
                        x=0.5, y=0.5,
                        showarrow=False
                    )
                    fig.update_layout(height=300)
                    return fig
            else:
                # Error chart
                fig = go.Figure()
                fig.add_annotation(
                    text="Unable to fetch performance data",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    showarrow=False
                )
                fig.update_layout(height=300)
                return fig
                
        except Exception as e:
            # Error chart
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False
            )
            fig.update_layout(height=300)
            return fig

if __name__ == "__main__":
    print("This module should be imported and used with the main dashboard app")
