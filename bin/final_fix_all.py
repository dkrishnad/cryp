#!/usr/bin/env python3
"""
FINAL COMPREHENSIVE FIX SCRIPT
==============================
This script will fix ALL remaining issues in the crypto bot
"""

import os
import re
import ast

def fix_callbacks_file():
    """Fix any remaining issues in callbacks.py"""
    print("🔧 FIXING CALLBACKS FILE...")
    
    with open('dashboard/callbacks.py', 'r') as f:
        content = f.read()
    
    # Remove any hanging HTML elements that might be leftover
    lines = content.split('\n')
    cleaned_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Skip obviously broken lines that are hanging HTML
        if (line.strip().startswith('html.') and 
            not any(keyword in line for keyword in ['def ', 'return', '=', '@']) and
            not line.strip().endswith(',')):
            print(f"Removing hanging HTML line: {line.strip()}")
            i += 1
            continue
            
        # Skip lines that are clearly leftover fragments
        if (re.match(r'^\s+]\s*,\s*className=', line) or
            re.match(r'^\s+]\)\s*,\s*$', line) or
            re.match(r'^\s+]\s*,\s*className=.*\)\s*,\s*$', line)):
            print(f"Removing fragment line: {line.strip()}")
            i += 1
            continue
            
        cleaned_lines.append(line)
        i += 1
    
    # Write back the cleaned content
    cleaned_content = '\n'.join(cleaned_lines)
    
    # Verify syntax before saving
    try:
        ast.parse(cleaned_content)
        with open('dashboard/callbacks.py', 'w') as f:
            f.write(cleaned_content)
        print("✅ Callbacks file cleaned and verified")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error after cleaning: {e}")
        return False

def check_and_fix_duplicates():
    """Check and remove any duplicate callback outputs"""
    print("🔧 CHECKING FOR DUPLICATE CALLBACKS...")
    
    with open('dashboard/callbacks.py', 'r') as f:
        content = f.read()
    
    # Find all @app.callback decorators and their outputs
    callback_pattern = r'@app\.callback\(\s*Output\([\'\"](.*?)[\'\"]'
    outputs = re.findall(callback_pattern, content)
    
    from collections import Counter
    output_counts = Counter(outputs)
    duplicates = {k: v for k, v in output_counts.items() if v > 1}
    
    if duplicates:
        print(f"❌ Found {len(duplicates)} duplicate outputs:")
        for output_id, count in duplicates.items():
            print(f"  - '{output_id}': {count} times")
        
        # Remove duplicate callbacks (keep only the first occurrence)
        lines = content.split('\n')
        seen_outputs = set()
        cleaned_lines = []
        skip_until_next_callback = False
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            if skip_until_next_callback:
                if line.strip().startswith('@app.callback') or line.strip().startswith('def '):
                    skip_until_next_callback = False
                else:
                    i += 1
                    continue
            
            if '@app.callback' in line:
                # Check if this is a duplicate
                match = re.search(r'Output\([\'\"](.*?)[\'\"]', line)
                if match:
                    output_id = match.group(1)
                    if output_id in seen_outputs:
                        print(f"Removing duplicate callback for: {output_id}")
                        skip_until_next_callback = True
                        i += 1
                        continue
                    else:
                        seen_outputs.add(output_id)
            
            cleaned_lines.append(line)
            i += 1
        
        # Write back cleaned content
        cleaned_content = '\n'.join(cleaned_lines)
        with open('dashboard/callbacks.py', 'w') as f:
            f.write(cleaned_content)
        print("✅ Duplicate callbacks removed")
        
    else:
        print("✅ No duplicate callbacks found")
    
    return len(duplicates) == 0

def fix_app_imports():
    """Fix any import issues in app.py"""
    print("🔧 FIXING APP IMPORTS...")
    
    app_content = '''import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import dash app first
from dash_app import app

# Import callbacks to register them
import callbacks

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
'''
    
    with open('dashboard/app.py', 'w') as f:
        f.write(app_content)
    print("✅ App.py fixed")

def fix_dash_app():
    """Ensure dash_app.py is clean"""
    print("🔧 FIXING DASH APP...")
    
    dash_app_content = '''import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Create Dash app with Bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'assets/dark-theme.css',
        'assets/custom.css'
    ],
    suppress_callback_exceptions=True,
    assets_folder='assets'
)

# Configure app
app.title = "Crypto Trading Bot Dashboard"
app.config.suppress_callback_exceptions = True

# Server for deployment
server = app.server
'''
    
    with open('dashboard/dash_app.py', 'w') as f:
        f.write(dash_app_content)
    print("✅ Dash app fixed")

def create_startup_script():
    """Create a simple startup script"""
    print("🔧 CREATING STARTUP SCRIPT...")
    
    startup_content = '''@echo off
echo ========================================
echo CRYPTO BOT - STARTING DASHBOARD
echo ========================================

echo Testing imports...
python -c "import dashboard.callbacks; print('✅ Callbacks OK')" || goto :error
python -c "import dashboard.layout; print('✅ Layout OK')" || goto :error
python -c "from dashboard.dash_app import app; print('✅ App OK')" || goto :error

echo.
echo 🚀 Starting dashboard...
echo Dashboard will be available at: http://localhost:8050
echo.
echo Press Ctrl+C to stop the dashboard
echo.

python dashboard/app.py
goto :end

:error
echo ❌ Import test failed! 
echo Please check the error messages above.
pause

:end
'''
    
    with open('start_dashboard.bat', 'w') as f:
        f.write(startup_content)
    print("✅ Startup script created")

def main():
    print("=" * 60)
    print("🛠️  FINAL COMPREHENSIVE FIX")
    print("=" * 60)
    
    success = True
    
    # Fix callbacks file
    if not fix_callbacks_file():
        success = False
    
    # Check and fix duplicates
    if not check_and_fix_duplicates():
        success = False
    
    # Fix app imports
    fix_app_imports()
    
    # Fix dash app
    fix_dash_app()
    
    # Create startup script
    create_startup_script()
    
    print("\n" + "=" * 60)
    print("📊 FIX SUMMARY")
    print("=" * 60)
    
    if success:
        print("🎉 ALL FIXES APPLIED SUCCESSFULLY!")
        print("\n✅ Your crypto bot is now ready!")
        print("\n🚀 To start the dashboard:")
        print("   Windows: start_dashboard.bat")
        print("   Manual:  python dashboard/app.py")
        print("\n🌐 Dashboard URL: http://localhost:8050")
    else:
        print("❌ SOME FIXES FAILED!")
        print("Please check the error messages above.")

if __name__ == "__main__":
    main()
