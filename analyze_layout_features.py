#!/usr/bin/env python3
"""
COMPREHENSIVE LAYOUT FEATURE ANALYSIS
This script analyzes ALL features in the current layout to ensure 100% preservation
"""

import re
import json
from datetime import datetime

def analyze_layout_features():
    """Analyze all features in the current layout.py file"""
    
    print("🔍 COMPREHENSIVE LAYOUT FEATURE ANALYSIS")
    print("=" * 70)
    
    try:
        with open('dashboardtest/layout.py', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ layout.py not found")
        return
    
    features = {}
    
    # 1. Analyze Stores and Intervals
    stores = re.findall(r'dcc\.Store\([^)]*id=["\']([^"\']+)["\']', content)
    intervals = re.findall(r'dcc\.Interval\([^)]*id=["\']([^"\']+)["\']', content)
    
    features['stores'] = stores
    features['intervals'] = intervals
    
    print(f"📦 STORES ({len(stores)}):")
    for store in stores:
        print(f"   - {store}")
    
    print(f"\n⏰ INTERVALS ({len(intervals)}):")
    for interval in intervals:
        print(f"   - {interval}")
    
    # 2. Analyze Tabs
    tabs = re.findall(r'dcc\.Tab\([^)]*label=["\']([^"\']+)["\'].*?value=["\']([^"\']+)["\']', content)
    features['tabs'] = tabs
    
    print(f"\n🗂️ TABS ({len(tabs)}):")
    for label, value in tabs:
        print(f"   - {label} → {value}")
    
    # 3. Analyze Major Sections/Variables
    sections = []
    section_patterns = [
        r'(\w+_tab)\s*=\s*html\.Div',
        r'(\w+_section)\s*=\s*html\.Div',
        r'(\w+_component)\s*=\s*html\.Div',
        r'(sidebar)\s*=\s*html\.Div',
    ]
    
    for pattern in section_patterns:
        matches = re.findall(pattern, content)
        sections.extend(matches)
    
    features['sections'] = list(set(sections))
    
    print(f"\n🏗️ MAJOR SECTIONS ({len(features['sections'])}):")
    for section in sorted(features['sections']):
        print(f"   - {section}")
    
    # 4. Analyze Buttons
    buttons = re.findall(r'dbc\.Button\([^)]*id=["\']([^"\']+)["\']', content)
    features['buttons'] = buttons
    
    print(f"\n🔘 BUTTONS ({len(buttons)}):")
    for button in sorted(set(buttons)):
        print(f"   - {button}")
    
    # 5. Analyze Graphs/Charts
    graphs = re.findall(r'safe_graph\(["\']([^"\']+)["\']', content)
    dcc_graphs = re.findall(r'dcc\.Graph\([^)]*id=["\']([^"\']+)["\']', content)
    all_graphs = list(set(graphs + dcc_graphs))
    features['graphs'] = all_graphs
    
    print(f"\n📊 CHARTS/GRAPHS ({len(all_graphs)}):")
    for graph in sorted(all_graphs):
        print(f"   - {graph}")
    
    # 6. Analyze Dropdowns
    dropdowns = re.findall(r'dcc\.Dropdown\([^)]*id=["\']([^"\']+)["\']', content)
    features['dropdowns'] = dropdowns
    
    print(f"\n📋 DROPDOWNS ({len(dropdowns)}):")
    for dropdown in sorted(set(dropdowns)):
        print(f"   - {dropdown}")
    
    # 7. Analyze Input Components
    inputs = re.findall(r'dbc\.Input\([^)]*id=["\']([^"\']+)["\']', content)
    features['inputs'] = inputs
    
    print(f"\n📝 INPUT FIELDS ({len(inputs)}):")
    for input_field in sorted(set(inputs)):
        print(f"   - {input_field}")
    
    # 8. Analyze Tables
    tables = re.findall(r'dash_table\.DataTable\([^)]*id=["\']([^"\']+)["\']', content)
    features['tables'] = tables
    
    print(f"\n📋 DATA TABLES ({len(tables)}):")
    for table in sorted(set(tables)):
        print(f"   - {table}")
    
    # 9. Count total unique IDs
    all_ids = re.findall(r'id=["\']([^"\']+)["\']', content)
    unique_ids = list(set(all_ids))
    features['unique_ids'] = unique_ids
    
    print(f"\n🆔 TOTAL UNIQUE IDs: {len(unique_ids)}")
    
    # 10. Analyze JavaScript imports
    js_files = re.findall(r'assets/([^"\']+\.js)', content)
    css_files = re.findall(r'assets/([^"\']+\.css)', content)
    
    features['js_files'] = js_files
    features['css_files'] = css_files
    
    print(f"\n📜 JAVASCRIPT FILES ({len(js_files)}):")
    for js in sorted(set(js_files)):
        print(f"   - {js}")
    
    print(f"\n🎨 CSS FILES ({len(css_files)}):")
    for css in sorted(set(css_files)):
        print(f"   - {css}")
    
    # 11. Analyze Special Features
    special_features = []
    
    # Check for WebSocket
    if 'ws://' in content or 'websocket' in content.lower():
        special_features.append("WebSocket Integration")
    
    # Check for Real-time features
    if 'realtime' in content.lower() or 'live-price' in content:
        special_features.append("Real-time Data")
    
    # Check for ML features
    if 'prediction' in content.lower() or 'model' in content.lower():
        special_features.append("ML/AI Features")
    
    # Check for Trading features
    if 'auto-trading' in content or 'futures' in content:
        special_features.append("Advanced Trading")
    
    # Check for Email features
    if 'email' in content.lower() or 'smtp' in content.lower():
        special_features.append("Email/Notifications")
    
    # Check for Risk Management
    if 'risk' in content.lower():
        special_features.append("Risk Management")
    
    features['special_features'] = special_features
    
    print(f"\n🚀 SPECIAL FEATURES ({len(special_features)}):")
    for feature in special_features:
        print(f"   - {feature}")
    
    # 12. Summary Report
    print("\n" + "=" * 70)
    print("📋 FEATURE PRESERVATION CHECKLIST")
    print("=" * 70)
    
    total_components = (len(features['stores']) + len(features['intervals']) + 
                       len(features['buttons']) + len(features['graphs']) + 
                       len(features['dropdowns']) + len(features['inputs']) + 
                       len(features['tables']))
    
    print(f"✅ Total Stores: {len(features['stores'])}")
    print(f"✅ Total Intervals: {len(features['intervals'])}")
    print(f"✅ Total Tabs: {len(features['tabs'])}")
    print(f"✅ Total Sections: {len(features['sections'])}")
    print(f"✅ Total Buttons: {len(features['buttons'])}")
    print(f"✅ Total Charts: {len(features['graphs'])}")
    print(f"✅ Total Dropdowns: {len(features['dropdowns'])}")
    print(f"✅ Total Inputs: {len(features['inputs'])}")
    print(f"✅ Total Tables: {len(features['tables'])}")
    print(f"✅ Total Components: {total_components}")
    print(f"✅ Total Unique IDs: {len(features['unique_ids'])}")
    print(f"✅ Special Features: {len(features['special_features'])}")
    
    # Save to JSON for reference
    with open('layout_features_analysis.json', 'w') as f:
        json.dump(features, f, indent=2)
    
    print(f"\n💾 Analysis saved to: layout_features_analysis.json")
    print(f"🕒 Timestamp: {datetime.now().isoformat()}")
    
    return features

if __name__ == "__main__":
    analyze_layout_features()
