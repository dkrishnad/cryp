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
