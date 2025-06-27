import sys
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
    safe_print("� All tabs and features enabled!")
    safe_print("�📊 Dashboard will be available at: http://localhost:8050")
    
    try:
        app.run(
            debug=False,
            host='localhost',
            port=8050,
            dev_tools_ui=False,
            dev_tools_props_check=False
        )
    except Exception as e:
        safe_print(f"❌ Error starting dashboard: {e}")
        safe_print("Please check if port 8050 is already in use.")
dashboard_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(dashboard_dir)

# Add both dashboard and parent directories to path
if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the app first, then callbacks, then layout
from dash_app import app, server

# Now import callbacks (this will register all callbacks)
try:
    import callbacks
    print("[SUCCESS] Callbacks imported successfully")
except Exception as e:
    print(f"[ERROR] Failed to import callbacks: {e}")
    print("[WARNING] Dashboard will run with limited functionality")

# Import layout after callbacks are registered
from layout import layout

# Register Binance-exact callbacks if available
try:
    from binance_exact_callbacks import register_binance_exact_callbacks
    register_binance_exact_callbacks(app)
    print("[SUCCESS] Binance-exact callbacks registered")
except ImportError:
    print("[INFO] Binance-exact callbacks not available")
except Exception as e:
    print(f"[WARNING] Failed to register Binance-exact callbacks: {e}")

# User-friendly: Add meta tags, title, favicon, and loading spinner

app.layout = layout

if __name__ == "__main__":
    print("🚀 Starting Crypto Bot Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:8050")
    
    # Enhanced server configuration for better component loading
    try:
        app.run(
            debug=False,  # Disable debug to reduce overhead
            port=8050,
            host='127.0.0.1',
            dev_tools_hot_reload=False,  # Disable hot reload to prevent conflicts
            dev_tools_ui=False,  # Disable dev tools UI
            dev_tools_serve_dev_bundles=False  # Use production bundles
        )
    except Exception as e:
        print(f"❌ Failed to start dashboard: {e}")
        print("🔧 Trying fallback configuration...")
        app.run(debug=False, port=8050, host='127.0.0.1')
