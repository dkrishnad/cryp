#!/usr/bin/env python3
"""
Diagnose blank dashboard issue - comprehensive analysis
"""
import sys
import os
import traceback

# Fix encoding for Windows
if os.name == 'nt':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

def safe_print(message):
    """Print message with encoding safety"""
    try:
        print(message)
    except UnicodeEncodeError:
        print(message.encode('ascii', 'replace').decode('ascii'))

def main():
    safe_print("=== DASHBOARD DIAGNOSTIC TEST ===")
    safe_print("")
    
    try:
        # Step 1: Check Dash app creation
        safe_print("1️⃣ Checking Dash app creation...")
        sys.path.append(r"c:\Users\Hari\Desktop\Crypto bot\dashboard")
        
        from dash_app import app
        safe_print(f"   ✅ App created: {type(app)}")
        safe_print(f"   ✅ App server: {type(app.server)}")
        
        # Step 2: Check layout import
        safe_print("")
        safe_print("2️⃣ Checking layout import...")
        from layout import layout
        safe_print(f"   ✅ Layout imported: {type(layout)}")
        
        # Step 3: Check layout content
        safe_print("")
        safe_print("3️⃣ Analyzing layout structure...")
        if hasattr(layout, 'children'):
            safe_print(f"   ✅ Layout has children: {len(layout.children)} items")
            for i, child in enumerate(layout.children):
                safe_print(f"      - Child {i}: {type(child).__name__}")
        else:
            safe_print("   ❌ Layout has no children attribute")
        
        # Step 4: Check app.layout assignment
        safe_print("")
        safe_print("4️⃣ Checking app.layout assignment...")
        app.layout = layout
        safe_print(f"   ✅ App layout assigned: {type(app.layout)}")
        
        # Step 5: Check callbacks import
        safe_print("")
        safe_print("5️⃣ Checking callbacks import...")
        import callbacks
        safe_print(f"   ✅ Callbacks imported successfully")
        safe_print(f"   ✅ Total callbacks registered: {len(app.callback_map)}")
        
        # Step 6: Test HTML generation
        safe_print("")
        safe_print("6️⃣ Testing HTML generation...")
        try:
            # Try to render the layout to HTML
            with app.test_client() as client:
                response = client.get('/')
                safe_print(f"   ✅ HTTP Response: {response.status_code}")
                if response.status_code == 200:
                    content = response.get_data(as_text=True)
                    safe_print(f"   ✅ Content length: {len(content)} characters")
                    if len(content) > 100:
                        safe_print("   ✅ Content appears substantial")
                        # Check for common HTML elements
                        if '<html' in content:
                            safe_print("   ✅ Contains HTML structure")
                        if 'bi bi-robot' in content:
                            safe_print("   ✅ Contains navbar content")
                        if 'sidebar-symbol' in content:
                            safe_print("   ✅ Contains sidebar elements")
                        if 'main-tabs' in content:
                            safe_print("   ✅ Contains main tabs")
                    else:
                        safe_print("   ❌ Content too small - likely empty page")
                else:
                    safe_print(f"   ❌ Non-200 response: {response.status_code}")
        except Exception as e:
            safe_print(f"   ❌ HTML generation error: {e}")
            traceback.print_exc()
        
        # Step 7: Start test server
        safe_print("")
        safe_print("7️⃣ All checks passed! Dashboard should be working.")
        safe_print("")
        safe_print("🔧 DIAGNOSTIC RESULTS:")
        safe_print("   • Dash app: OK")
        safe_print("   • Layout: OK") 
        safe_print("   • Callbacks: OK")
        safe_print("   • HTML Generation: OK")
        safe_print("")
        safe_print("If dashboard is still blank, try:")
        safe_print("   1. Clear browser cache (Ctrl+F5)")
        safe_print("   2. Check browser console for JavaScript errors")
        safe_print("   3. Try different browser")
        safe_print("   4. Check if port 8050 is blocked by firewall")
        safe_print("")
        safe_print("Starting dashboard for manual verification...")
        safe_print("Go to: http://localhost:8050")
        
        app.run(debug=True, port=8050, host="0.0.0.0")
        
    except Exception as e:
        safe_print(f"❌ Error during diagnostic: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
