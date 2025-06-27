import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add dashboard directory to path
dashboard_dir = os.path.dirname(os.path.abspath(__file__))
if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)

# Import dash app first
from dash_app import app

# Import layout
from layout import layout

# Assign layout to app
app.layout = layout

if __name__ == '__main__':
    print("🚀 Starting Crypto Bot Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:8050")
    
    try:
        app.run(
            debug=False,
            host='localhost',
            port=8050,
            dev_tools_ui=False,
            dev_tools_props_check=False
        )
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        print("Please check if port 8050 is already in use.")
