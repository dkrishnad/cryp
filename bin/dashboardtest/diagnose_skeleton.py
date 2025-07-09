#!/usr/bin/env python3
"""
Comprehensive dashboard skeleton diagnosis
"""
import sys
import os
import traceback
import json

# Add paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dashboard_dir = os.path.dirname(os.path.abspath(__file__))
if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)

def diagnose_skeleton_issue():
    """Diagnose why dashboard appears as skeleton"""
    print("=" * 80)
    print("🔍 DASHBOARD SKELETON DIAGNOSIS")
    print("=" * 80)
    
    issues_found = []
    
    # Test 1: Import verification
    print("\n1️⃣ Testing Imports...")
    try:
        from dash_app import app
        print("✅ dash_app imported")
        
        import callbacks
        print("✅ callbacks imported")
        
        from layout import layout
        print("✅ layout imported")
        
        app.layout = layout
        print("✅ layout assigned")
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        issues_found.append(f"Import error: {e}")
        traceback.print_exc()
    
    # Test 2: Check callback registration
    print("\n2️⃣ Testing Callback Registration...")
    try:
        callback_count = len(app.callback_map)
        print(f"📊 Callbacks registered: {callback_count}")
        
        if callback_count == 0:
            issues_found.append("No callbacks registered")
        else:
            print("✅ Callbacks are registered")
            
        # List first few callbacks
        for i, (callback_id, callback) in enumerate(list(app.callback_map.items())[:5]):
            print(f"   {i+1}. {callback_id}")
            
    except Exception as e:
        print(f"❌ Callback error: {e}")
        issues_found.append(f"Callback error: {e}")
    
    # Test 3: Check for critical layout components
    print("\n3️⃣ Testing Layout Components...")
    try:
        layout_str = str(layout)
        
        critical_components = [
            'price-chart',
            'indicators-chart',
            'virtual-balance', 
            'performance-monitor',
            'tabs-content'
        ]
        
        missing_components = []
        for component in critical_components:
            if component not in layout_str:
                missing_components.append(component)
                print(f"❌ Missing: {component}")
            else:
                print(f"✅ Found: {component}")
        
        if missing_components:
            issues_found.append(f"Missing components: {missing_components}")
            
    except Exception as e:
        print(f"❌ Layout error: {e}")
        issues_found.append(f"Layout error: {e}")
    
    # Test 4: Check for data loading functions
    print("\n4️⃣ Testing Data Loading Functions...")
    try:
        # Search for data loading patterns in callbacks
        with open('callbacks.py', 'r', encoding='utf-8') as f:
            callback_content = f.read()
            
        data_patterns = [
            'requests.get',
            'fetch_data',
            'get_price_data',
            'get_indicators',
            'backend'
        ]
        
        found_patterns = []
        for pattern in data_patterns:
            if pattern in callback_content:
                found_patterns.append(pattern)
                print(f"✅ Found data pattern: {pattern}")
        
        if not found_patterns:
            issues_found.append("No data loading patterns found in callbacks")
            print("❌ No data loading patterns found")
        
    except Exception as e:
        print(f"❌ Data loading check error: {e}")
        issues_found.append(f"Data loading check error: {e}")
    
    # Test 5: Check for proper interval setup
    print("\n5️⃣ Testing Interval Components...")
    try:
        import re
        
        # Check layout for intervals
        interval_pattern = r'dcc\.Interval\([^)]*id=[\'"]([^\'"]*)[\'"]'
        intervals_in_layout = re.findall(interval_pattern, layout_str)
        print(f"📊 Intervals in layout: {intervals_in_layout}")
        
        # Check callbacks for interval inputs
        interval_input_pattern = r'Input\([\'"]([^\'"]*)[\'"],\s*[\'"]n_intervals[\'"]'
        intervals_in_callbacks = re.findall(interval_input_pattern, callback_content)
        print(f"📊 Intervals in callbacks: {set(intervals_in_callbacks)}")
        
        # Find mismatches
        layout_set = set(intervals_in_layout)
        callback_set = set(intervals_in_callbacks)
        
        missing_in_layout = callback_set - layout_set
        missing_in_callbacks = layout_set - callback_set
        
        if missing_in_layout:
            issues_found.append(f"Intervals referenced in callbacks but missing in layout: {missing_in_layout}")
            print(f"❌ Missing in layout: {missing_in_layout}")
        
        if missing_in_callbacks:
            print(f"⚠️ Intervals in layout but not used in callbacks: {missing_in_callbacks}")
        
        if not missing_in_layout and not missing_in_callbacks:
            print("✅ All intervals properly matched")
            
    except Exception as e:
        print(f"❌ Interval check error: {e}")
        issues_found.append(f"Interval check error: {e}")
    
    # Test 6: Look for dummy/placeholder content
    print("\n6️⃣ Checking for Skeleton/Placeholder Content...")
    try:
        skeleton_indicators = [
            'placeholder',
            'coming soon',
            'under construction', 
            'todo',
            'dummy data',
            'sample data',
            'html.Div("No data")',
            'return "Loading..."',
            'return []'
        ]
        
        found_skeleton = []
        for indicator in skeleton_indicators:
            if indicator.lower() in callback_content.lower():
                found_skeleton.append(indicator)
        
        if found_skeleton:
            issues_found.append(f"Skeleton content found: {found_skeleton}")
            print(f"❌ Skeleton content: {found_skeleton}")
        else:
            print("✅ No obvious skeleton content found")
            
    except Exception as e:
        print(f"❌ Skeleton check error: {e}")
    
    # Generate summary
    print("\n" + "=" * 80)
    print("📋 DIAGNOSIS SUMMARY")
    print("=" * 80)
    
    if issues_found:
        print(f"❌ {len(issues_found)} ISSUES FOUND:")
        for i, issue in enumerate(issues_found, 1):
            print(f"   {i}. {issue}")
        
        print("\n🔧 RECOMMENDED ACTIONS:")
        
        if any("import" in issue.lower() for issue in issues_found):
            print("   - Fix import errors first")
        
        if any("callback" in issue.lower() for issue in issues_found):
            print("   - Fix callback registration issues")
            
        if any("component" in issue.lower() for issue in issues_found):
            print("   - Add missing layout components")
            
        if any("data" in issue.lower() for issue in issues_found):
            print("   - Implement proper data loading in callbacks")
            
        if any("skeleton" in issue.lower() for issue in issues_found):
            print("   - Replace placeholder content with real functionality")
            
    else:
        print("✅ NO MAJOR ISSUES FOUND")
        print("💡 The skeleton issue might be due to:")
        print("   - Backend not running (start backend first)")
        print("   - Network connectivity issues")
        print("   - Browser caching (try Ctrl+F5)")
        print("   - Missing CSS/assets files")
    
    print("=" * 80)
    return issues_found

if __name__ == "__main__":
    diagnose_skeleton_issue()
