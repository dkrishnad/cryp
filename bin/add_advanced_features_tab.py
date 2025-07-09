#!/usr/bin/env python3
"""
Add advanced features tab to the dashboard layout to expose all new endpoint connections
"""

import os
import re

def create_advanced_features_tab():
    """Create a comprehensive advanced features tab"""
    advanced_tab = '''

# ADVANCED FEATURES TAB - NEW ENDPOINTS
advanced_features_tab = html.Div([
    html.H2([html.I(className="bi bi-gear me-2 text-info"), "⚙️ Advanced Features"], className="mb-4"),
    
    # Chart Controls Section
    dbc.Card([
        dbc.CardHeader("📊 Chart Controls"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button("🔄 Refresh Charts", id="chart-refresh-btn", color="primary", size="sm"),
                    html.Div(id="chart-refresh-status", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("📈 Bollinger Bands", id="chart-bollinger-btn", color="info", size="sm"),
                    html.Div(id="chart-bollinger-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("⚡ Momentum", id="chart-momentum-btn", color="warning", size="sm"),
                    html.Div(id="chart-momentum-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("📊 Volume", id="chart-volume-btn", color="success", size="sm"),
                    html.Div(id="chart-volume-data", className="mt-2")
                ], width=3)
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Button("📈 Show Indicators", id="chart-show-indicators-btn", color="secondary", size="sm"),
                    html.Div(id="chart-indicators-status", className="mt-2")
                ], width=6),
                dbc.Col([
                    dbc.Button("💹 Show Price", id="chart-show-price-btn", color="secondary", size="sm"),
                    html.Div(id="chart-price-status", className="mt-2")
                ], width=6)
            ])
        ])
    ], className="mb-4"),
    
    # HFT Analytics Section
    dbc.Card([
        dbc.CardHeader("⚡ High Frequency Trading Analytics"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button("📊 HFT Analytics", id="hft-analytics-btn", color="primary", size="sm"),
                    html.Div(id="hft-analytics-data", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Button("⚙️ HFT Config", id="hft-config-btn", color="info", size="sm"),
                    html.Div(id="hft-config-status", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Button("🎯 Opportunities", id="hft-opportunities-btn", color="warning", size="sm"),
                    html.Div(id="hft-opportunities-data", className="mt-2")
                ], width=4)
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Button("▶️ Start HFT", id="hft-start-btn", color="success", size="sm"),
                    html.Div(id="hft-start-status", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Button("⏹️ Stop HFT", id="hft-stop-btn", color="danger", size="sm"),
                    html.Div(id="hft-stop-status", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Button("📊 Status", id="hft-status-btn", color="secondary", size="sm"),
                    html.Div(id="hft-status-display", className="mt-2")
                ], width=4)
            ])
        ])
    ], className="mb-4"),
    
    # Performance & Portfolio Section
    dbc.Card([
        dbc.CardHeader("📈 Performance & Portfolio Analytics"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button("📊 Performance Dashboard", id="performance-dashboard-btn", color="primary", size="sm"),
                    html.Div(id="performance-dashboard-data", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Button("📊 Performance Metrics", id="performance-metrics-btn", color="info", size="sm"),
                    html.Div(id="performance-metrics-data", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Button("💼 Portfolio", id="portfolio-btn", color="warning", size="sm"),
                    html.Div(id="portfolio-data", className="mt-2")
                ], width=4)
            ])
        ])
    ], className="mb-4"),
    
    # Advanced ML Section
    dbc.Card([
        dbc.CardHeader("🧠 Advanced Machine Learning"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button("🔍 ML Compatibility", id="ml-compatibility-check-btn", color="primary", size="sm"),
                    html.Div(id="ml-compatibility-check-data", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Button("🔧 Fix ML Issues", id="ml-compatibility-fix-btn", color="danger", size="sm"),
                    html.Div(id="ml-compatibility-fix-status", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Button("💡 ML Recommendations", id="ml-recommendations-btn", color="info", size="sm"),
                    html.Div(id="ml-recommendations-data", className="mt-2")
                ], width=4)
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Button("⚙️ Online ML Config", id="ml-online-config-btn", color="secondary", size="sm"),
                    html.Div(id="ml-online-config-data", className="mt-2")
                ], width=6),
                dbc.Col([
                    dbc.Button("📊 Online ML Performance", id="ml-online-performance-btn", color="success", size="sm"),
                    html.Div(id="ml-online-performance-data", className="mt-2")
                ], width=6)
            ])
        ])
    ], className="mb-4"),
    
    # Risk Management Section
    dbc.Card([
        dbc.CardHeader("⚠️ Advanced Risk Management"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Input(id="risk-amount-input", type="number", placeholder="Amount", value=1000),
                    dbc.Button("📏 Calculate Position Size", id="risk-position-size-btn", color="primary", size="sm", className="mt-2"),
                    html.Div(id="risk-position-size-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("🔍 Check Trade Risk", id="risk-trade-check-btn", color="warning", size="sm"),
                    html.Div(id="risk-trade-check-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("📊 Portfolio Risk", id="risk-portfolio-metrics-btn", color="info", size="sm"),
                    html.Div(id="risk-portfolio-metrics-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("🛑 Stop Loss Strategies", id="risk-stop-loss-btn", color="danger", size="sm"),
                    html.Div(id="risk-stop-loss-data", className="mt-2")
                ], width=3)
            ])
        ])
    ], className="mb-4"),
    
    # Auto Trading Controls Section
    dbc.Card([
        dbc.CardHeader("🤖 Auto Trading Controls"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button("🔄 Toggle Auto Trading", id="auto-trading-toggle-btn", color="primary", size="sm"),
                    html.Div(id="auto-trading-toggle-status", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("⚙️ Trading Settings", id="auto-trading-settings-btn", color="info", size="sm"),
                    html.Div(id="auto-trading-settings-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("📊 Trading Signals", id="auto-trading-signals-btn", color="warning", size="sm"),
                    html.Div(id="auto-trading-signals-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("📈 Trading Status", id="auto-trading-status-refresh-btn", color="success", size="sm"),
                    html.Div(id="auto-trading-status-display", className="mt-2")
                ], width=3)
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Button("⚡ Execute Futures Signal", id="futures-execute-signal-btn", color="danger", size="sm"),
                    html.Div(id="futures-execute-signal-status", className="mt-2")
                ], width=6),
                dbc.Col([
                    dbc.Button("🔥 Binance Auto Execute", id="binance-auto-execute-btn", color="warning", size="sm"),
                    html.Div(id="binance-auto-execute-status", className="mt-2")
                ], width=6)
            ])
        ])
    ], className="mb-4"),
    
    # Email & Notifications Section
    dbc.Card([
        dbc.CardHeader("📧 Email & Notifications"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button("⚙️ Email Config", id="email-config-btn", color="primary", size="sm"),
                    html.Div(id="email-config-status", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("✉️ Test Email", id="email-test-btn", color="info", size="sm"),
                    html.Div(id="email-test-status", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("🔔 Toggle Notifications", id="email-notifications-toggle-btn", color="warning", size="sm"),
                    html.Div(id="email-notifications-status", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Input(id="email-address-input", type="email", placeholder="Email Address"),
                    dbc.Button("📧 Update Email", id="email-address-update-btn", color="success", size="sm", className="mt-2"),
                    html.Div(id="email-address-status", className="mt-2")
                ], width=3)
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Button("🗑️ Clear Notifications", id="notifications-clear-btn", color="danger", size="sm"),
                    html.Div(id="notifications-clear-status", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Button("✅ Mark All Read", id="notifications-mark-read-btn", color="success", size="sm"),
                    html.Div(id="notifications-mark-read-status", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Input(id="manual-alert-message", type="text", placeholder="Alert message"),
                    dbc.Button("📢 Send Alert", id="manual-alert-btn", color="warning", size="sm", className="mt-2"),
                    html.Div(id="manual-alert-status", className="mt-2")
                ], width=4)
            ])
        ])
    ], className="mb-4"),
    
    # Trading Controls Section
    dbc.Card([
        dbc.CardHeader("💰 Trading Controls"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Input(id="trade-symbol-input", type="text", placeholder="Symbol", value="BTCUSDT"),
                    dbc.Select(id="trade-side-dropdown", options=[
                        {"label": "BUY", "value": "BUY"},
                        {"label": "SELL", "value": "SELL"}
                    ], value="BUY"),
                    dbc.Button("💰 Execute Trade", id="trade-execute-btn", color="success", size="sm", className="mt-2"),
                    html.Div(id="trade-execute-status", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("📊 All Trades", id="trades-list-btn", color="info", size="sm"),
                    html.Div(id="trades-list-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("📈 Futures History", id="futures-history-btn", color="warning", size="sm"),
                    html.Div(id="futures-history-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("🔓 Open Futures", id="futures-open-btn", color="primary", size="sm"),
                    html.Div(id="futures-open-data", className="mt-2")
                ], width=3)
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Button("🔄 Reset Virtual Balance", id="virtual-balance-reset-btn", color="danger", size="sm"),
                    html.Div(id="virtual-balance-reset-status", className="mt-2")
                ], width=6),
                dbc.Col([
                    dbc.Button("📊 Test Email Alert", id="test-email-alert-btn", color="info", size="sm"),
                    html.Div(id="test-email-alert-status", className="mt-2")
                ], width=6)
            ])
        ])
    ], className="mb-4"),
    
    # Futures API Section
    dbc.Card([
        dbc.CardHeader("🔗 Futures API Endpoints"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button("ℹ️ Exchange Info", id="fapi-exchange-info-btn", color="primary", size="sm"),
                    html.Div(id="fapi-exchange-info-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("📊 24hr Ticker", id="fapi-ticker-btn", color="info", size="sm"),
                    html.Div(id="fapi-ticker-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("👤 Account", id="fapi-account-btn", color="warning", size="sm"),
                    html.Div(id="fapi-account-data", className="mt-2")
                ], width=3),
                dbc.Col([
                    dbc.Button("💰 Balance", id="fapi-balance-btn", color="success", size="sm"),
                    html.Div(id="fapi-balance-data", className="mt-2")
                ], width=3)
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Button("⚠️ Position Risk", id="fapi-position-risk-btn", color="danger", size="sm"),
                    html.Div(id="fapi-position-risk-data", className="mt-2")
                ], width=6),
                dbc.Col([
                    dbc.Button("🏥 System Health", id="system-health-btn", color="secondary", size="sm"),
                    html.Div(id="system-health-data", className="mt-2")
                ], width=6)
            ])
        ])
    ], className="mb-4"),
    
    # Model Management Section
    dbc.Card([
        dbc.CardHeader("🤖 Model Management"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button("📊 Model Analytics", id="model-analytics-btn", color="primary", size="sm"),
                    html.Div(id="model-analytics-data", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Button("📤 Upload Status", id="model-upload-status-btn", color="info", size="sm"),
                    html.Div(id="model-upload-status-data", className="mt-2")
                ], width=4),
                dbc.Col([
                    dbc.Button("🔄 Retrain Model", id="retrain-model-btn", color="warning", size="sm"),
                    html.Div(id="retrain-model-status", className="mt-2")
                ], width=4)
            ])
        ])
    ], className="mb-4"),
    
    # Chart Data Section
    dbc.Card([
        dbc.CardHeader("📊 Chart Data"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Input(id="chart-symbol-input", type="text", placeholder="Symbol", value="BTCUSDT"),
                    dbc.Button("🕯️ Get Candles", id="chart-candles-btn", color="primary", size="sm", className="mt-2"),
                    html.Div(id="chart-candles-data", className="mt-2")
                ], width=6),
                dbc.Col([
                    dbc.Button("💹 General Price", id="price-general-btn", color="success", size="sm"),
                    html.Div(id="price-general-data", className="mt-2")
                ], width=6)
            ])
        ])
    ], className="mb-4"),
    
    # Indicators Section
    dbc.Card([
        dbc.CardHeader("📈 Indicators Management"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button("⚙️ Indicators Config", id="indicators-config-btn", color="primary", size="sm"),
                    html.Div(id="indicators-config-data", className="mt-2")
                ], width=6),
                dbc.Col([
                    dbc.Button("🔄 Refresh Indicators", id="indicators-refresh-btn", color="info", size="sm"),
                    html.Div(id="indicators-refresh-status", className="mt-2")
                ], width=6)
            ])
        ])
    ], className="mb-4"),
    
    # Quick Amount Selection
    dbc.Card([
        dbc.CardHeader("💰 Quick Amount Selection"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button("$50", id="amount-50-btn", color="outline-primary", size="sm"),
                    html.Div(id="amount-50-status", className="mt-2")
                ], width=2),
                dbc.Col([
                    dbc.Button("$100", id="amount-100-btn", color="outline-primary", size="sm"),
                    html.Div(id="amount-100-status", className="mt-2")
                ], width=2),
                dbc.Col([
                    dbc.Button("$250", id="amount-250-btn", color="outline-primary", size="sm"),
                    html.Div(id="amount-250-status", className="mt-2")
                ], width=2),
                dbc.Col([
                    dbc.Button("$500", id="amount-500-btn", color="outline-primary", size="sm"),
                    html.Div(id="amount-500-status", className="mt-2")
                ], width=2),
                dbc.Col([
                    dbc.Button("$1000", id="amount-1000-btn", color="outline-primary", size="sm"),
                    html.Div(id="amount-1000-status", className="mt-2")
                ], width=2),
                dbc.Col([
                    dbc.Button("MAX", id="amount-max-btn", color="outline-warning", size="sm"),
                    html.Div(id="amount-max-status", className="mt-2")
                ], width=2)
            ])
        ])
    ])
])

'''
    return advanced_tab

def add_advanced_tab_to_tabs():
    """Add the advanced features tab to the existing tabs structure"""
    tabs_file = r"c:\Users\Hari\Desktop\Testin dub\dashboardtest\layout.py"
    
    # Read current file
    with open(tabs_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the tabs definition and add the new tab
    if "dbc.Tab(label=" in content and "advanced_features_tab" not in content:
        # Add the advanced features tab component first
        advanced_tab_code = create_advanced_features_tab()
        
        # Insert before the main layout
        layout_marker = "# Main layout\nlayout = html.Div(["
        if layout_marker in content:
            content = content.replace(layout_marker, advanced_tab_code + "\n\n" + layout_marker)
        
        # Find where tabs are defined and add our new tab
        import re
        
        # Look for the tabs structure
        tabs_pattern = r'(dbc\.Tab\(label="[^"]*",.*?children=.*?\),?\s*)\]'
        matches = list(re.finditer(tabs_pattern, content, re.DOTALL))
        
        if matches:
            # Find the last tab and add our new tab after it
            last_match = matches[-1]
            new_tab = '            dbc.Tab(label="⚙️ Advanced Features", tab_id="advanced-features-tab", children=advanced_features_tab),\n        ]'
            content = content[:last_match.end()-8] + ',\n            dbc.Tab(label="⚙️ Advanced Features", tab_id="advanced-features-tab", children=advanced_features_tab)\n        ]' + content[last_match.end():]
        
        # Write back
        with open(tabs_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Added Advanced Features tab to dashboard layout")
        return True
    else:
        print("❌ Could not find tabs structure or advanced tab already exists")
        return False

if __name__ == "__main__":
    success = add_advanced_tab_to_tabs()
    if success:
        print("🎯 Advanced features tab integration complete!")
        print("📊 Dashboard now exposes 60+ new endpoint connections through UI")
    else:
        print("❌ Failed to integrate advanced features tab")
