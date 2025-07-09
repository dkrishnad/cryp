import sys
import os
import io
import logging
from datetime import datetime

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
            "📊": "[DASHBOARD]", "💎": "[SUCCESS]", "🎉": "[READY]", "🐛": "[DEBUG]"
        }
        for emoji, text in emoji_map.items():
            fallback_msg = fallback_msg.replace(emoji, text)
        print(fallback_msg)
        sys.stdout.flush()

# Set up comprehensive logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dashboard_debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Create logger
logger = logging.getLogger(__name__)

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add dashboard directory to path
dashboard_dir = os.path.dirname(os.path.abspath(__file__))
if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)

# Enhanced error handling for imports
try:
    safe_print("🔧 Loading Dash app configuration...")
    logger.info("Loading Dash app configuration...")
    from debug_dash_app import app
    safe_print("✅ Debug Dash app loaded successfully")
    logger.info("Debug Dash app loaded successfully")
    
    safe_print("🔧 Loading callbacks...")
    logger.info("Loading callbacks...")
    import callbacks
    safe_print("✅ Callbacks loaded successfully")
    logger.info("Callbacks loaded successfully")
    
    safe_print("🔧 Loading layout...")
    logger.info("Loading layout...")
    from layout import layout
    safe_print("✅ Layout loaded successfully")
    logger.info("Layout loaded successfully")
    
    # Count callbacks
    callback_count = len(app.callback_map)
    safe_print(f"🐛 Total callbacks registered: {callback_count}")
    logger.info(f"Total callbacks registered: {callback_count}")
    
    # List callback outputs for debugging
    safe_print("🐛 Registered callback outputs:")
    logger.info("Registered callback outputs:")
    for callback_id, callback_obj in app.callback_map.items():
        safe_print(f"  - {callback_id}")
        logger.info(f"  Callback: {callback_id}")
    
except ImportError as e:
    safe_print(f"❌ Import error: {e}")
    logger.error(f"Import error: {e}")
    raise
except Exception as e:
    safe_print(f"❌ Unexpected error during import: {e}")
    logger.error(f"Unexpected error during import: {e}")
    raise

# Assign layout to app
app.layout = layout

# Add callback context logging
from dash import callback_context

def log_callback_context():
    """Log callback context for debugging"""
    if callback_context.triggered:
        for trigger in callback_context.triggered:
            logger.info(f"Callback triggered by: {trigger['prop_id']} = {trigger['value']}")
    else:
        logger.info("No callback triggers found")

if __name__ == '__main__':
    safe_print("🚀 Starting Full-Featured Crypto Bot Dashboard (DEBUG MODE)...")
    safe_print("🐛 Debug mode enabled with comprehensive logging!")
    safe_print("📊 All tabs and features enabled!")
    safe_print("📊 Dashboard will be available at: http://localhost:8050")
    safe_print("🐛 Check dashboard_debug.log for detailed logging")
    
    logger.info("Starting dashboard in debug mode")
    logger.info(f"Dashboard started at: {datetime.now()}")
    
    try:
        app.run(
            debug=True,  # Enable debug mode
            host='localhost',
            port=8050,
            dev_tools_ui=True,  # Enable dev tools
            dev_tools_props_check=True,  # Enable props checking
            dev_tools_serve_dev_bundles=True,  # Serve dev bundles
            dev_tools_hot_reload=True,  # Enable hot reload
            threaded=True  # Enable threading for better performance
        )
    except Exception as e:
        safe_print(f"❌ Error starting dashboard: {e}")
        logger.error(f"Error starting dashboard: {e}")
        safe_print("Please check if port 8050 is already in use.")
