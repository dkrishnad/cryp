#!/usr/bin/env python3
"""
Beautiful Emoji-Rich Dashboard Starter - Windows Compatible
"""
import os
import sys
import io

# Set UTF-8 encoding for Windows compatibility
if os.name == 'nt':
    # Force UTF-8 encoding
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    # Redirect stdout to handle Unicode properly
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def safe_print(msg):
    """Print safely with emoji support"""
    try:
        print(msg)
    except UnicodeEncodeError:
        # Fallback without emojis for ancient systems
        import re
        clean_msg = re.sub(r'[^\x00-\x7F]+', '', msg)
        print(clean_msg)

def main():
    safe_print("🚀 Starting Beautiful Crypto Trading Bot Dashboard...")
    safe_print("✨ Loading emoji-rich interface...")
    
    try:
        # Import Dash components
        import dash
        import dash_bootstrap_components as dbc
        
        safe_print("📊 Creating dashboard app...")
        app = dash.Dash(
            __name__,
            suppress_callback_exceptions=True,
            external_stylesheets=[
                dbc.themes.BOOTSTRAP,
                "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css"
            ]
        )
        
        safe_print("🎨 Loading beautiful layout...")
        from layout import layout
        app.layout = layout
        
        safe_print("⚡ Loading interactive callbacks...")
        import callbacks
        
        safe_print("🎉 Dashboard ready with full emoji support!")
        safe_print(f"🔥 Callbacks loaded: {len(app.callback_map)}")
        safe_print("")
        safe_print("🌐 Starting server on http://localhost:8050")
        safe_print("💎 Enjoy the beautiful emoji-rich interface!")
        safe_print("🛑 Press Ctrl+C to stop")
        safe_print("")
        
        # Start server
        app.run(debug=False, port=8050, host="127.0.0.1")
        
    except KeyboardInterrupt:
        safe_print("")
        safe_print("👋 Dashboard stopped by user")
    except Exception as e:
        safe_print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
