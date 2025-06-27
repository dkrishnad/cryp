#!/usr/bin/env python3
"""
Optimized dashboard startup script
"""
import sys
import traceback
import os

# Fix encoding issues on Windows
if os.name == 'nt':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

def safe_print(message):
    """Print message with encoding safety"""
    try:
        print(message)
    except UnicodeEncodeError:
        # Fallback to ASCII-safe version
        print(message.encode('ascii', 'replace').decode('ascii'))

try:
    safe_print("Starting Crypto Bot Dashboard...")
    safe_print("Loading components...")
    
    from dash_app import app
    from layout import layout
    # Use the new refactored callbacks file
    import refactored_callbacks_step1 as callbacks
    
    app.layout = layout
    
    safe_print(f"Dashboard ready with {len(app.callback_map)} callbacks")
    safe_print("Performance optimizations applied:")
    safe_print("   • Immediate symbol updates")  
    safe_print("   • Fast 2-second timeouts")
    safe_print("   • Optimized 30-second intervals")
    safe_print("   • Styled indicators for visibility")
    
    safe_print("")
    safe_print("Starting server on http://localhost:8050...")
    safe_print("Technical indicators will update INSTANTLY when changing symbols!")
    
    app.run(debug=True, port=8050, host="0.0.0.0")
    
except KeyboardInterrupt:
    safe_print("")
    safe_print("Dashboard stopped by user")
except Exception as e:
    safe_print(f"")
    safe_print(f"Error starting dashboard: {e}")
    safe_print("")
    safe_print("Full traceback:")
    traceback.print_exc()
    safe_print("")
    safe_print("Try running: python app.py")
    sys.exit(1)
