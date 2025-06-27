#!/usr/bin/env python3
"""
Clean Dashboard App - Fixed for Windows and proper startup
"""
import sys
import os
import io

# Windows-specific encoding setup
if os.name == 'nt':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleOutputCP(65001)
        kernel32.SetConsoleCP(65001)
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
            "🔧": "[CONFIG]", "✅": "[OK]", "❌": "[ERROR]", 
            "🚀": "[START]", "📊": "[DASHBOARD]", "💎": "[SUCCESS]"
        }
        for emoji, text in emoji_map.items():
            fallback_msg = fallback_msg.replace(emoji, text)
        print(fallback_msg)
        sys.stdout.flush()

# Setup paths
dashboard_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(dashboard_dir)

if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import components
try:
    safe_print("🔧 Loading Dash app configuration...")
    from dash_app import app
    safe_print("✅ Dash app loaded successfully")
    
    safe_print("🔧 Loading layout...")
    from layout import layout
    safe_print("✅ Layout loaded successfully")
    
    safe_print("🔧 Loading callbacks...")
    import callbacks
    safe_print("✅ Callbacks loaded successfully")
    
    # Register Binance-exact callbacks if available
    try:
        from binance_exact_callbacks import register_binance_exact_callbacks
        register_binance_exact_callbacks(app)
        safe_print("✅ Binance-exact callbacks registered")
    except ImportError:
        safe_print("ℹ️ Binance-exact callbacks not available")
    except Exception as e:
        safe_print(f"⚠️ Failed to register Binance-exact callbacks: {e}")
        
except ImportError as e:
    safe_print(f"❌ Import error: {e}")
    raise
except Exception as e:
    safe_print(f"❌ Unexpected error during import: {e}")
    raise

# Assign layout to app
app.layout = layout

if __name__ == '__main__':
    safe_print("🚀 Starting Crypto Bot Dashboard...")
    safe_print("📊 Dashboard will be available at: http://localhost:8050")
    
    try:
        app.run(
            debug=False,
            host='127.0.0.1',
            port=8050,
            dev_tools_ui=False,
            dev_tools_props_check=False,
            dev_tools_hot_reload=False,
            dev_tools_serve_dev_bundles=False
        )
    except Exception as e:
        safe_print(f"❌ Error starting dashboard: {e}")
        safe_print("🔧 Trying fallback configuration...")
        try:
            app.run(debug=False, port=8050, host='127.0.0.1')
        except Exception as e2:
            safe_print(f"❌ Fallback failed: {e2}")
            safe_print("Please check if port 8050 is already in use.")
