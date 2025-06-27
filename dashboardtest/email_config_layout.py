#!/usr/bin/env python3
"""
Email Configuration Layout for Dashboard
"""
import dash
from dash import dcc, html, Input, Output, State
import requests

API_URL = "http://localhost:8000"

def create_email_config_layout():
    """Create email configuration layout"""
    
    return html.Div([
        html.H4("📧 Email Configuration", className="mb-3"),
        
        # Email Settings Form
        html.Div([
            # SMTP Server Settings
            html.Div([
                html.H5("SMTP Server Settings", className="mb-3"),
                
                html.Div([
                    html.Div([
                        html.Label("SMTP Server:", className="form-label"),
                        dcc.Input(
                            id="smtp-server-input",
                            type="text",
                            placeholder="smtp.gmail.com",
                            className="form-control"
                        )
                    ], className="col-md-6"),
                    
                    html.Div([
                        html.Label("SMTP Port:", className="form-label"),
                        dcc.Input(
                            id="smtp-port-input",
                            type="number",
                            value=587,
                            className="form-control"
                        )
                    ], className="col-md-6")
                ], className="row mb-3"),
                
                html.Div([
                    html.Div([
                        html.Label("Email Address:", className="form-label"),
                        dcc.Input(
                            id="smtp-user-input",
                            type="email",
                            placeholder="your.email@gmail.com",
                            className="form-control"
                        )
                    ], className="col-md-6"),
                    
                    html.Div([
                        html.Label("Password/App Password:", className="form-label"),
                        dcc.Input(
                            id="smtp-pass-input",
                            type="password",
                            placeholder="Enter password or app password",
                            className="form-control"
                        )
                    ], className="col-md-6")
                ], className="row mb-3")
            ], className="card-body"),
            
            # Notification Settings
            html.Div([
                html.H5("Notification Settings", className="mb-3"),
                
                html.Div([
                    html.Div([
                        html.Label("Notification Email:", className="form-label"),
                        dcc.Input(
                            id="notify-email-input",
                            type="email",
                            placeholder="notifications@example.com",
                            className="form-control"
                        )
                    ], className="col-md-8"),
                    
                    html.Div([
                        html.Label("Enable Notifications:", className="form-label"),
                        html.Div([
                            dcc.Checklist(
                                id="email-enabled-checkbox",
                                options=[{"label": " Enable", "value": "enabled"}],
                                value=[],
                                className="form-check"
                            )
                        ])
                    ], className="col-md-4")
                ], className="row mb-3")
            ], className="card-body"),
            
            # Action Buttons
            html.Div([
                html.Button(
                    "💾 Save Configuration",
                    id="save-email-config-btn",
                    className="btn btn-primary me-2"
                ),
                html.Button(
                    "🔧 Test Connection",
                    id="test-email-config-btn",
                    className="btn btn-info me-2"
                ),
                html.Button(
                    "📧 Send Test Email",
                    id="send-test-email-btn",
                    className="btn btn-success me-2"
                ),
                html.Button(
                    "🔄 Load Current Config",
                    id="load-email-config-btn",
                    className="btn btn-secondary"
                )
            ], className="mb-3"),
            
            # Status Messages
            html.Div(id="email-config-status", className="mt-3"),
            
            # Email Preview
            html.Div([
                html.H5("Test Email Preview", className="mb-3"),
                html.Div([
                    html.Div([
                        html.Label("Subject:", className="form-label"),
                        dcc.Input(
                            id="test-email-subject",
                            type="text",
                            value="Test Email from Crypto Bot",
                            className="form-control"
                        )
                    ], className="col-md-12 mb-2"),
                    
                    html.Div([
                        html.Label("Message:", className="form-label"),
                        dcc.Textarea(
                            id="test-email-body",
                            value="This is a test email to verify your email configuration is working correctly.",
                            className="form-control",
                            style={"height": "100px"}
                        )
                    ], className="col-md-12")
                ], className="row")
            ], className="card-body border-top")
            
        ], className="card"),
        
        # Hidden components for missing email config callbacks
        html.Div([
            html.Div(id="email-config-tab-content", style={"display": "none"}),
        ], style={"display": "none"}),
    ])

def register_email_config_callbacks(app):
    """Register callbacks for email configuration"""
    
    @app.callback(
        [Output("smtp-server-input", "value"),
         Output("smtp-port-input", "value"),
         Output("smtp-user-input", "value"),
         Output("notify-email-input", "value"),
         Output("email-enabled-checkbox", "value"),
         Output("email-config-status", "children")],
        Input("load-email-config-btn", "n_clicks"),
        prevent_initial_call=False
    )
    def load_email_config(n_clicks):
        """Load current email configuration"""
        try:
            resp = requests.get(f"{API_URL}/email/config", timeout=5)
            if resp.status_code == 200:
                result = resp.json()
                config = result.get("config", {})
                
                return (
                    config.get("smtp_server", ""),
                    config.get("smtp_port", 587),
                    config.get("smtp_user", ""),
                    config.get("to_email", ""),
                    ["enabled"] if config.get("enabled", False) else [],
                    html.Div("✅ Configuration loaded", className="alert alert-success")
                )
            else:
                return ("", 587, "", "", [], 
                       html.Div("❌ Failed to load configuration", className="alert alert-danger"))
                
        except Exception as e:
            return ("", 587, "", "", [],
                   html.Div(f"❌ Error: {str(e)}", className="alert alert-danger"))
    
    @app.callback(
        Output("email-config-status", "children", allow_duplicate=True),
        [Input("save-email-config-btn", "n_clicks")],
        [State("smtp-server-input", "value"),
         State("smtp-port-input", "value"),
         State("smtp-user-input", "value"),
         State("smtp-pass-input", "value"),
         State("notify-email-input", "value"),
         State("email-enabled-checkbox", "value")],
        prevent_initial_call=True
    )
    def save_email_config(n_clicks, smtp_server, smtp_port, smtp_user, 
                         smtp_pass, notify_email, enabled):
        """Save email configuration"""
        if not n_clicks:
            return dash.no_update
            
        try:
            config = {
                "smtp_server": smtp_server or "smtp.gmail.com",
                "smtp_port": smtp_port or 587,
                "smtp_user": smtp_user or "",
                "smtp_pass": smtp_pass or "",
                "from_email": smtp_user or "",
                "to_email": notify_email or smtp_user or "",
                "enabled": "enabled" in (enabled or [])
            }
            
            resp = requests.post(f"{API_URL}/email/config", json=config, timeout=5)
            if resp.status_code == 200:
                return html.Div("✅ Configuration saved successfully", className="alert alert-success")
            else:
                return html.Div("❌ Failed to save configuration", className="alert alert-danger")
                
        except Exception as e:
            return html.Div(f"❌ Error: {str(e)}", className="alert alert-danger")
    
    @app.callback(
        Output("email-config-status", "children", allow_duplicate=True),
        Input("test-email-config-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def test_email_config(n_clicks):
        """Test email configuration"""
        if not n_clicks:
            return dash.no_update
            
        try:
            resp = requests.post(f"{API_URL}/email/test", timeout=10)
            if resp.status_code == 200:
                result = resp.json()
                if result.get("status") == "success":
                    return html.Div("✅ Email connection successful", className="alert alert-success")
                else:
                    message = result.get("result", {}).get("message", "Unknown error")
                    return html.Div(f"❌ Email test failed: {message}", className="alert alert-danger")
            else:
                return html.Div("❌ Failed to test email", className="alert alert-danger")
                
        except Exception as e:
            return html.Div(f"❌ Error: {str(e)}", className="alert alert-danger")
    
    @app.callback(
        Output("email-config-status", "children", allow_duplicate=True),
        [Input("send-test-email-btn", "n_clicks")],
        [State("test-email-subject", "value"),
         State("test-email-body", "value")],
        prevent_initial_call=True
    )
    def send_test_email(n_clicks, subject, body):
        """Send test email"""
        if not n_clicks:
            return dash.no_update
            
        try:
            data = {
                "subject": subject or "Test Email from Crypto Bot",
                "body": body or "This is a test email."
            }
            
            resp = requests.post(f"{API_URL}/email/send_test", json=data, timeout=10)
            if resp.status_code == 200:
                result = resp.json()
                if result.get("status") == "success":
                    return html.Div("✅ Test email sent successfully", className="alert alert-success")
                else:
                    message = result.get("result", {}).get("message", "Unknown error")
                    return html.Div(f"❌ Failed to send test email: {message}", className="alert alert-danger")
            else:
                return html.Div("❌ Failed to send test email", className="alert alert-danger")
                
        except Exception as e:
            return html.Div(f"❌ Error: {str(e)}", className="alert alert-danger")

if __name__ == "__main__":
    print("This module should be imported and used with the main dashboard app")
