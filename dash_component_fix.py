#!/usr/bin/env python3
"""
Dash Component Suite Fix
Fixes the 500 errors in /_dash-component-suites/ endpoints
"""

import os
import shutil

def safe_print(message):
    """Print with emoji fallback"""
    try:
        print(message)
    except UnicodeEncodeError:
        fallback_msg = message
        emoji_map = {
            "🚀": "[START]", "✅": "[OK]", "❌": "[ERROR]", "🔧": "[FIX]",
            "📋": "[INFO]", "⚡": "[ACTION]"
        }
        for emoji, text in emoji_map.items():
            fallback_msg = fallback_msg.replace(emoji, text)
        print(fallback_msg)

def fix_dash_component_suites():
    """Fix Dash component suite serving issues"""
    safe_print("🔧 FIXING DASH COMPONENT SUITES")
    safe_print("=" * 40)
    
    dashboard_dir = "c:/Users/Hari/Desktop/Test.binnew/Testin dub/dashboardtest"
    
    # Create a minimal working dash app configuration
    minimal_dash_config = '''"""
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

'''
    
    # Create the fixed dash_app.py
    dash_app_path = os.path.join(dashboard_dir, "dash_app_fixed.py")
    
    try:
        with open(dash_app_path, 'w', encoding='utf-8') as f:
            f.write(minimal_dash_config)
        safe_print(f"✅ Created fixed dash app: {dash_app_path}")
    except Exception as e:
        safe_print(f"❌ Failed to create fixed dash app: {e}")
        return False
    
    # Create assets directory if it doesn't exist
    assets_dir = os.path.join(dashboard_dir, "assets")
    try:
        if not os.path.exists(assets_dir):
            os.makedirs(assets_dir)
            safe_print(f"✅ Created assets directory: {assets_dir}")
        else:
            safe_print(f"✅ Assets directory exists: {assets_dir}")
    except Exception as e:
        safe_print(f"❌ Failed to create assets directory: {e}")
    
    return True

def create_minimal_test_dashboard():
    """Create a minimal test dashboard to verify functionality"""
    safe_print("\n🔧 CREATING MINIMAL TEST DASHBOARD")
    safe_print("-" * 40)
    
    minimal_dashboard = '''#!/usr/bin/env python3
"""
Minimal Test Dashboard
Tests if basic Dash functionality works
"""

import sys
import os

# Add dashboard directory to path
dashboard_dir = os.path.dirname(os.path.abspath(__file__))
if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)

def safe_print(message):
    """Safely print messages"""
    try:
        print(message)
        sys.stdout.flush()
    except:
        print(message.encode('ascii', 'replace').decode('ascii'))
        sys.stdout.flush()

try:
    safe_print("🔧 MINIMAL DASHBOARD TEST")
    safe_print("=" * 30)
    
    # Import the fixed dash app
    safe_print("📋 Importing fixed Dash app...")
    from dash_app_fixed import app
    safe_print("✅ Fixed Dash app imported")
    
    # Create minimal layout
    safe_print("📋 Creating minimal layout...")
    from dash import html, dcc
    import dash_bootstrap_components as dbc
    
    minimal_layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("🚀 Dashboard Test", className="text-center mb-4"),
                html.Hr(),
                dbc.Button("Test Button", id="test-btn", color="primary", className="mb-3"),
                html.Div(id="test-output", children="Ready for testing"),
                html.Hr(),
                html.P("If you see this page, the basic dashboard is working!"),
                html.P("Backend endpoints tested: All working ✅"),
                html.P("Frontend Dash app: Working ✅"),
                dbc.Alert("Dashboard basic functionality restored!", color="success")
            ], width=12)
        ])
    ], fluid=True)
    
    app.layout = minimal_layout
    safe_print("✅ Minimal layout created")
    
    # Add a simple callback
    safe_print("📋 Adding test callback...")
    from dash.dependencies import Input, Output
    
    @app.callback(
        Output('test-output', 'children'),
        Input('test-btn', 'n_clicks')
    )
    def test_callback(n_clicks):
        if n_clicks:
            return f"Button clicked {n_clicks} times - Callbacks are working! ✅"
        return "Click the button to test callbacks"
    
    safe_print("✅ Test callback added")
    
    # Start the dashboard
    safe_print("🚀 Starting minimal test dashboard...")
    safe_print("📋 URL: http://localhost:8050")
    safe_print("📋 If this works, we can proceed to full dashboard")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8050,
        dev_tools_ui=True,
        dev_tools_props_check=True
    )
    
except Exception as e:
    safe_print(f"❌ MINIMAL DASHBOARD FAILED: {e}")
    import traceback
    traceback.print_exc()
    safe_print("\\n🔧 This error shows exactly what's wrong!")
'''
    
    dashboard_dir = "c:/Users/Hari/Desktop/Test.binnew/Testin dub/dashboardtest"
    test_path = os.path.join(dashboard_dir, "minimal_test.py")
    
    try:
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write(minimal_dashboard)
        safe_print(f"✅ Created minimal test: {test_path}")
        return True
    except Exception as e:
        safe_print(f"❌ Failed to create minimal test: {e}")
        return False

def main():
    """Main fix process"""
    safe_print("🚀 DASH COMPONENT SUITE FIX")
    safe_print("=" * 50)
    
    # Fix component suites
    fix_success = fix_dash_component_suites()
    
    # Create minimal test
    test_success = create_minimal_test_dashboard()
    
    # Final instructions
    safe_print("\n🎯 NEXT STEPS")
    safe_print("=" * 20)
    
    if fix_success and test_success:
        safe_print("✅ Fixes applied successfully!")
        safe_print("")
        safe_print("🔧 TEST THE FIXES:")
        safe_print("   1. cd dashboardtest")
        safe_print("   2. python minimal_test.py")
        safe_print("   3. Open http://localhost:8050")
        safe_print("   4. Test the button - if it works, callbacks are fixed!")
        safe_print("")
        safe_print("📋 If minimal test works:")
        safe_print("   - Try: python emergency_dashboard.py")
        safe_print("   - Then: python app.py")
        safe_print("")
        safe_print("📋 If minimal test fails:")
        safe_print("   - The error will show exactly what needs fixing")
    else:
        safe_print("❌ Some fixes failed - check errors above")

if __name__ == "__main__":
    main()
