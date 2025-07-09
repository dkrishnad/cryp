#!/usr/bin/env python3
"""
Dashboard Configuration Quick Fix
Fixes Dash app configuration for proper callback functionality
"""

import os
import sys

def safe_print(message):
    """Print with emoji fallback"""
    try:
        print(message)
    except UnicodeEncodeError:
        fallback_msg = message.replace("🔧", "[FIX]").replace("✅", "[OK]").replace("❌", "[ERROR]")
        print(fallback_msg)

def create_fixed_dash_app():
    """Create a fixed dash_app.py with proper callback configuration"""
    
    fixed_content = '''import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import os

# Create Dash app with FIXED configuration for callback functionality
app = dash.Dash(
    __name__, 
    suppress_callback_exceptions=False,  # CHANGED: Enable callback validation
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css"
    ],
    # Serve locally for better debugging
    serve_locally=True,  # CHANGED: Serve locally for debugging
    compress=False,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": "Crypto Trading Bot Dashboard"}
    ]
)

# Server configuration
server = app.server
server.config['SECRET_KEY'] = os.urandom(12)
'''
    
    dash_app_path = r"c:\Users\Hari\Desktop\Test.binnew\Testin dub\dashboardtest\dash_app.py"
    
    # Backup original
    backup_path = dash_app_path + ".backup"
    if os.path.exists(dash_app_path):
        with open(dash_app_path, 'r') as f:
            original_content = f.read()
        with open(backup_path, 'w') as f:
            f.write(original_content)
        safe_print(f"✅ Backed up original to: {backup_path}")
    
    # Write fixed version
    with open(dash_app_path, 'w') as f:
        f.write(fixed_content)
    
    safe_print("✅ Created fixed dash_app.py")
    return True

def create_fixed_app_py():
    """Create a fixed app.py with debug mode enabled"""
    
    fixed_content = '''import sys
import os
import io

# Windows-specific encoding setup for emojis
if os.name == 'nt':
    # Set UTF-8 environment
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # Try to enable Windows Terminal UTF-8 support
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleOutputCP(65001)  # UTF-8
        kernel32.SetConsoleCP(65001)  # UTF-8
    except:
        pass
    
    # Wrap stdout/stderr for proper emoji handling
    try:
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'buffer'):
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass

def safe_print(message):
    """Safely print messages with emoji support on Windows"""
    try:
        print(message)
        sys.stdout.flush()
    except UnicodeEncodeError:
        # Fallback: Replace emojis with text equivalents
        fallback_msg = message
        emoji_map = {
            "🔧": "[CONFIG]", "✅": "[OK]", "❌": "[ERROR]", "🚀": "[START]",
            "📊": "[DASHBOARD]", "💎": "[SUCCESS]", "🎉": "[READY]"
        }
        for emoji, text in emoji_map.items():
            fallback_msg = fallback_msg.replace(emoji, text)
        print(fallback_msg)
        sys.stdout.flush()

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add dashboard directory to path
dashboard_dir = os.path.dirname(os.path.abspath(__file__))
if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)

# Enhanced error handling for imports
try:
    safe_print("🔧 Loading Dash app configuration...")
    from dash_app import app
    safe_print("✅ Dash app loaded successfully")
    
    safe_print("🔧 Loading callbacks...")
    import callbacks
    safe_print("✅ Callbacks loaded successfully")
    
    safe_print("🔧 Loading layout...")
    from layout import layout
    safe_print("✅ Layout loaded successfully")
    
except ImportError as e:
    safe_print(f"❌ Import error: {e}")
    raise
except Exception as e:
    safe_print(f"❌ Unexpected error during import: {e}")
    raise

# Assign layout to app
app.layout = layout

if __name__ == '__main__':
    safe_print("🚀 Starting Full-Featured Crypto Bot Dashboard...")
    safe_print("📊 All tabs and features enabled!")
    safe_print("📊 Dashboard will be available at: http://localhost:8050")
    
    try:
        app.run(
            debug=True,  # CHANGED: Enable debug mode for better error reporting
            host='localhost',
            port=8050,
            dev_tools_ui=True,  # CHANGED: Enable dev tools for debugging
            dev_tools_props_check=True  # CHANGED: Enable props checking
        )
    except Exception as e:
        safe_print(f"❌ Error starting dashboard: {e}")
        safe_print("Please check if port 8050 is already in use.")
'''
    
    app_py_path = r"c:\Users\Hari\Desktop\Test.binnew\Testin dub\dashboardtest\app.py"
    
    # Backup original
    backup_path = app_py_path + ".backup"
    if os.path.exists(app_py_path):
        with open(app_py_path, 'r', encoding='utf-8', errors='replace') as f:
            original_content = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        safe_print(f"✅ Backed up original to: {backup_path}")
    
    # Write fixed version
    with open(app_py_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    safe_print("✅ Created fixed app.py with debug mode enabled")
    return True

def main():
    safe_print("🔧 DASHBOARD CONFIGURATION QUICK FIX")
    safe_print("=" * 50)
    safe_print("📋 Fixing Dash app configuration for callback functionality")
    safe_print("")
    
    # Fix dash_app.py
    safe_print("🔧 Step 1: Fixing dash_app.py configuration...")
    create_fixed_dash_app()
    
    # Fix app.py 
    safe_print("🔧 Step 2: Fixing app.py debug configuration...")
    create_fixed_app_py()
    
    safe_print("")
    safe_print("✅ CONFIGURATION FIXES APPLIED!")
    safe_print("=" * 50)
    safe_print("")
    safe_print("🚀 NOW RESTART THE DASHBOARD:")
    safe_print("1. Stop current dashboard (Ctrl+C)")
    safe_print("2. cd dashboardtest")
    safe_print("3. python app.py")
    safe_print("")
    safe_print("🔧 CHANGES MADE:")
    safe_print("- suppress_callback_exceptions: True → False")
    safe_print("- serve_locally: False → True") 
    safe_print("- debug: False → True")
    safe_print("- dev_tools_ui: False → True")
    safe_print("- dev_tools_props_check: False → True")
    safe_print("")
    safe_print("📋 These changes should enable proper callback functionality!")

if __name__ == "__main__":
    main()
