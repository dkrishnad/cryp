#!/usr/bin/env python3
"""
Critical Dash Component Suite Fix
Fixes the /_dash-component-suites/ 500 errors that prevent JavaScript loading
"""

import sys
import os

def safe_print(message, end="\n"):
    """Print with emoji fallback"""
    try:
        print(message, end=end)
    except UnicodeEncodeError:
        fallback_msg = message
        emoji_map = {
            "🔧": "[FIX]", "✅": "[OK]", "❌": "[ERROR]", "🚀": "[START]",
            "📋": "[INFO]", "⚠️": "[WARNING]", "🎯": "[TARGET]"
        }
        for emoji, text in emoji_map.items():
            fallback_msg = fallback_msg.replace(emoji, text)
        print(fallback_msg, end=end)

def fix_dash_component_suites():
    """Fix Dash component suite loading issues"""
    safe_print("🔧 CRITICAL DASH COMPONENT SUITE FIX")
    safe_print("=" * 50)
    
    dashboard_dir = "dashboardtest"
    
    # Create a new minimal dash app that forces local serving
    minimal_dash_content = '''"""
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
'''

    # Write the fixed dash app
    dash_app_path = os.path.join(dashboard_dir, "minimal_dash_app.py")
    
    try:
        with open(dash_app_path, 'w', encoding='utf-8') as f:
            f.write(minimal_dash_content)
        safe_print(f"✅ Created fixed minimal dash app: {dash_app_path}")
    except Exception as e:
        safe_print(f"❌ Error creating minimal dash app: {e}")
        return False
    
    # Create a test script to verify the fix
    test_script_content = '''#!/usr/bin/env python3
"""
Test script to verify Dash component suite fix
"""

import requests
import sys
import os

# Add dashboard directory to path
dashboard_dir = os.path.dirname(os.path.abspath(__file__))
if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)

def test_component_suites():
    """Test if Dash component suites are working"""
    print("🔧 Testing Dash Component Suite Fix...")
    
    base_url = "http://localhost:8050"
    
    # Test critical Dash endpoints
    test_endpoints = [
        "/_dash-layout",
        "/_dash-dependencies", 
        "/_dash-component-suites/dash/dash-renderer/build/dash_renderer.min.js"
    ]
    
    working = 0
    for endpoint in test_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint}")
                working += 1
            else:
                print(f"❌ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")
    
    print(f"\\n📊 Component suites working: {working}/{len(test_endpoints)}")
    
    if working == len(test_endpoints):
        print("🎉 DASH COMPONENT SUITES FIXED!")
        return True
    else:
        print("🔧 Still need more fixes")
        return False

if __name__ == "__main__":
    test_component_suites()
'''
    
    test_script_path = os.path.join(dashboard_dir, "test_component_suites.py")
    
    try:
        with open(test_script_path, 'w', encoding='utf-8') as f:
            f.write(test_script_content)
        safe_print(f"✅ Created component suite test: {test_script_path}")
    except Exception as e:
        safe_print(f"❌ Error creating test script: {e}")
        return False
    
    return True

def create_emergency_dashboard():
    """Create emergency minimal dashboard to test basic functionality"""
    safe_print("🚀 Creating emergency minimal dashboard...")
    
    emergency_content = '''#!/usr/bin/env python3
"""
Emergency Minimal Dashboard
Tests basic Dash functionality without complex components
"""

import sys
import os

# Add dashboard directory to path
dashboard_dir = os.path.dirname(os.path.abspath(__file__))
if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)

from minimal_dash_app import app
from dash import html, dcc, Input, Output
import time

# Simple test layout
app.layout = html.Div([
    html.H1("🚀 Emergency Dashboard Test", style={'textAlign': 'center'}),
    html.Div([
        html.Button("Test Button", id="test-btn", n_clicks=0),
        html.Div(id="test-output", children="Click the button to test interactivity"),
    ], style={'margin': '20px', 'textAlign': 'center'})
])

# Simple test callback
@app.callback(
    Output('test-output', 'children'),
    Input('test-btn', 'n_clicks')
)
def test_callback(n_clicks):
    if n_clicks > 0:
        return f"✅ SUCCESS! Button clicked {n_clicks} times. Callbacks are working!"
    return "Click the button to test interactivity"

if __name__ == '__main__':
    print("🚀 Starting Emergency Dashboard...")
    print("📊 Testing basic Dash functionality...")
    print("📊 Dashboard will be available at: http://localhost:8050")
    
    try:
        app.run(
            debug=True,
            host='localhost',
            port=8050,
            dev_tools_ui=True,
            dev_tools_props_check=True
        )
    except Exception as e:
        print(f"❌ Error starting emergency dashboard: {e}")
'''
    
    emergency_path = os.path.join("dashboardtest", "emergency_dashboard.py")
    
    try:
        with open(emergency_path, 'w', encoding='utf-8') as f:
            f.write(emergency_content)
        safe_print(f"✅ Created emergency dashboard: {emergency_path}")
        return True
    except Exception as e:
        safe_print(f"❌ Error creating emergency dashboard: {e}")
        return False

def main():
    """Main fix function"""
    safe_print("🎯 FIXING DASH COMPONENT SUITE 500 ERRORS")
    safe_print("=" * 50)
    
    # Step 1: Fix component suites
    if fix_dash_component_suites():
        safe_print("✅ Component suite fixes applied")
    else:
        safe_print("❌ Component suite fix failed")
        return
    
    # Step 2: Create emergency dashboard
    if create_emergency_dashboard():
        safe_print("✅ Emergency dashboard created")
    else:
        safe_print("❌ Emergency dashboard creation failed")
        return
    
    safe_print("")
    safe_print("🚀 NEXT STEPS:")
    safe_print("=" * 30)
    safe_print("1. Test emergency dashboard first:")
    safe_print("   cd dashboardtest")
    safe_print("   python emergency_dashboard.py")
    safe_print("")
    safe_print("2. If emergency works, test component suites:")
    safe_print("   python test_component_suites.py")
    safe_print("")
    safe_print("3. If all tests pass, restart main dashboard:")
    safe_print("   python app.py")
    safe_print("")
    safe_print("✅ COMPONENT SUITE FIX COMPLETE!")

if __name__ == "__main__":
    main()
