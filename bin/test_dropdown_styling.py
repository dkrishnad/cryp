import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# Simple test app to showcase the improved dropdown
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.CYBORG,
        "/assets/auto-trading-dropdown.css"
    ]
)

app.layout = dbc.Container([
    html.H2("🌟 Enhanced Auto Trading Dropdowns", className="text-white mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Label("Symbol Selection", className="text-white fw-bold mb-2"),
            dcc.Dropdown(
                id="test-symbol-dropdown",
                options=[
                    # Low-cap gems (highlighted)
                    {"label": "🌟 KAIA/USDT (Low-cap Gem)", "value": "KAIAUSDT"},
                    {"label": "🌟 JASMY/USDT (Low-cap Gem)", "value": "JASMYUSDT"},
                    {"label": "🌟 GALA/USDT (Low-cap Gem)", "value": "GALAUSDT"},
                    {"label": "🌟 ROSE/USDT (Low-cap Gem)", "value": "ROSEUSDT"},
                    {"label": "🌟 CHR/USDT (Low-cap Gem)", "value": "CHRUSDT"},
                    # Separator
                    {"label": "─── Major Coins ───", "value": "", "disabled": True},
                    # Major coins
                    {"label": "₿ BTC/USDT", "value": "BTCUSDT"},
                    {"label": "⧫ ETH/USDT", "value": "ETHUSDT"},
                    {"label": "🟡 BNB/USDT", "value": "BNBUSDT"},
                ],
                value="KAIAUSDT",
                className="mb-4 auto-trading-dropdown",
                style={
                    "background": "linear-gradient(135deg, #2d3748 0%, #1a202c 100%)",
                    "border": "2px solid #4a5568",
                    "borderRadius": "12px",
                    "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.3)",
                    "minHeight": "48px"
                },
                optionHeight=50,
                placeholder="🎯 Select Trading Pair",
                searchable=True,
                clearable=False
            ),
            
            html.P("✨ Features:", className="text-white fw-bold mb-2"),
            html.Ul([
                html.Li("🌟 Low-cap gems highlighted with special styling", className="text-muted"),
                html.Li("🎨 Gradient backgrounds and smooth animations", className="text-muted"),
                html.Li("🔍 Searchable with beautiful hover effects", className="text-muted"),
                html.Li("📱 Responsive design for all screen sizes", className="text-muted"),
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Label("Timeframe Selection", className="text-white fw-bold mb-2"),
            dcc.Dropdown(
                id="test-timeframe-dropdown",
                options=[
                    {"label": "⚡ 1 Minute (Scalping)", "value": "1m"},
                    {"label": "🔥 5 Minutes (Quick Trades)", "value": "5m"},
                    {"label": "📈 15 Minutes (Short Term)", "value": "15m"},
                    {"label": "⏰ 1 Hour (Recommended)", "value": "1h"},
                    {"label": "📊 4 Hours (Swing)", "value": "4h"},
                    {"label": "📅 1 Day (Position)", "value": "1d"}
                ],
                value="1h",
                className="mb-4 auto-trading-dropdown timeframe-dropdown",
                style={
                    "background": "linear-gradient(135deg, #2d3748 0%, #1a202c 100%)",
                    "border": "2px solid #4a5568",
                    "borderRadius": "12px",
                    "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.3)",
                    "minHeight": "48px"
                },
                optionHeight=45,
                placeholder="📊 Select Timeframe",
                searchable=False,
                clearable=False
            ),
            
            html.P("🎯 Improvements:", className="text-white fw-bold mb-2"),
            html.Ul([
                html.Li("🎨 Professional gradient styling", className="text-muted"),
                html.Li("✨ Smooth hover and focus animations", className="text-muted"),
                html.Li("🌈 Color-coded options with icons", className="text-muted"),
                html.Li("📏 Consistent height and spacing", className="text-muted"),
            ])
        ], width=6)
    ])
], fluid=True, className="py-5", style={"backgroundColor": "#1a202c", "minHeight": "100vh"})

if __name__ == "__main__":
    app.run(debug=True, port=8055)
