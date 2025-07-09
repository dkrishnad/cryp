#!/usr/bin/env python3
"""
Duplicate Functionality Checker
Analyzes each duplicate ID to determine if removal would cause functionality loss
"""

import os
import re
import json
from datetime import datetime

def read_file_content(file_path):
    """Read file content safely"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ""

def extract_component_context(content, component_id, context_lines=5):
    """Extract context around a component ID"""
    lines = content.split('\n')
    contexts = []
    
    for i, line in enumerate(lines):
        if f'id="{component_id}"' in line or f"id='{component_id}'" in line:
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)
            context = {
                'line_number': i + 1,
                'context': '\n'.join(lines[start:end]),
                'component_line': line.strip()
            }
            contexts.append(context)
    
    return contexts

def analyze_component_differences(id_name, contexts):
    """Analyze if the duplicate components have different functionality"""
    if len(contexts) < 2:
        return "No duplicates found"
    
    differences = []
    component_types = set()
    properties = []
    
    for i, context in enumerate(contexts):
        # Extract component type (dcc.Input, html.Button, etc.)
        line = context['component_line']
        if 'dcc.' in line:
            comp_type = re.search(r'dcc\.(\w+)', line)
            if comp_type:
                component_types.add(f"dcc.{comp_type.group(1)}")
        elif 'html.' in line:
            comp_type = re.search(r'html\.(\w+)', line)
            if comp_type:
                component_types.add(f"html.{comp_type.group(1)}")
        elif 'dbc.' in line:
            comp_type = re.search(r'dbc\.(\w+)', line)
            if comp_type:
                component_types.add(f"dbc.{comp_type.group(1)}")
        
        # Extract properties like className, style, children, etc.
        props = re.findall(r'(\w+)=', line)
        properties.extend(props)
        
        # Look for different configurations in context
        context_text = context['context']
        if 'className' in context_text:
            class_matches = re.findall(r'className=["\']([^"\']+)["\']', context_text)
            if class_matches:
                differences.append(f"Context {i+1}: className={class_matches}")
        
        if 'style' in context_text:
            differences.append(f"Context {i+1}: Has custom style")
        
        if 'children' in context_text:
            differences.append(f"Context {i+1}: Has children content")
    
    analysis = {
        'component_types': list(component_types),
        'unique_types': len(component_types) > 1,
        'property_differences': differences,
        'total_contexts': len(contexts),
        'recommendation': 'KEEP_BOTH' if len(component_types) > 1 or len(differences) > 2 else 'SAFE_TO_REMOVE'
    }
    
    return analysis

def check_callback_usage(component_id, callback_files):
    """Check if component is used in callbacks"""
    usage_count = 0
    callback_usage = []
    
    for file_path in callback_files:
        content = read_file_content(file_path)
        if content:
            # Check for Input, Output, State usage
            patterns = [
                rf'Input\(["\']?{re.escape(component_id)}["\']?',
                rf'Output\(["\']?{re.escape(component_id)}["\']?',
                rf'State\(["\']?{re.escape(component_id)}["\']?'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content)
                if matches:
                    usage_count += len(matches)
                    callback_usage.append({
                        'file': os.path.basename(file_path),
                        'pattern': pattern,
                        'count': len(matches)
                    })
    
    return {
        'total_usage': usage_count,
        'callback_files': callback_usage,
        'is_critical': usage_count > 0
    }

def main():
    print("🔍 DUPLICATE FUNCTIONALITY ANALYSIS")
    print("=" * 70)
    print("Checking if duplicate IDs have different functionality...")
    print("=" * 70)
    
    # Files to analyze
    layout_files = [
        'dashboardtest/layout.py',
        'dashboardtest/auto_trading_layout.py',
        'dashboardtest/futures_trading_layout.py',
        'dashboardtest/binance_exact_layout.py',
        'dashboardtest/email_config_layout.py',
        'dashboardtest/hybrid_learning_layout.py'
    ]
    
    callback_files = [
        'dashboardtest/callbacks.py',
        'dashboardtest/futures_callbacks.py'
    ]
    
    # Known duplicates from previous analysis
    duplicate_ids = [
        'auto-rollback-status',
        'email-address-input',
        'notification-action-output',
        'manual-notification-output',
        'email-config-output',
        'alert-send-output',
        'hft-action-output',
        'hft-config-output',
        'data-collection-action-output',
        'collection-config-output',
        'online-learning-action-output',
        'learning-config-output',
        'risk-management-output',
        'position-sizing-output',
        'trade-risk-check-output',
        'show-unread-only',
        'email-password-input',
        'smtp-port-input',
        'smtp-server-input',
        'manual-notification-message',
        'manual-notification-type',
        'futures-technical-chart',
        'hft-start-btn',
        'hft-stop-btn',
        'refresh-charts-btn',
        'risk-amount-input',
        'calculate-position-size-btn',
        'check-trade-risk-btn',
        'auto-trading-toggle-output',
        'auto-symbol-dropdown',
        'fixed-amount-input',
        'fixed-amount-section',
        'percentage-amount-input',
        'percentage-amount-slider',
        'calculated-amount-display',
        'percentage-amount-section',
        'save-auto-settings-btn',
        'current-signal-display',
        'auto-balance-display',
        'auto-pnl-display',
        'auto-winrate-display',
        'auto-trades-display',
        'auto-wl-display',
        'execute-signal-btn',
        'reset-auto-trading-btn',
        'optimize-kaia-btn',
        'optimize-jasmy-btn',
        'optimize-gala-btn',
        'open-positions-table',
        'auto-trade-log',
        'check-auto-alerts-result',
        'auto-trading-tab-content',
        'futures-available-balance',
        'futures-margin-used',
        'futures-margin-ratio',
        'futures-unrealized-pnl',
        'futures-open-positions',
        'futures-trading-status',
        'futures-pnl-display',
        'futures-virtual-total-balance',
        'futures-reset-balance-btn',
        'futures-settings-result',
        'futures-trading-tab-content',
        'futures-rsi-indicator',
        'futures-macd-indicator',
        'futures-bollinger-indicator',
        'futures-stochastic-indicator',
        'futures-atr-indicator',
        'futures-volume-indicator',
        'binance-exact-tab-content',
        'api-status-alert',
        'save-email-config-btn',
        'email-config-status',
        'email-config-tab-content',
        'online-learning-stats',
        'data-collection-stats',
        'comprehensive-backtest-output',
        'backtest-progress',
        'backtest-results-enhanced',
        'hybrid-status-display'
    ]
    
    # Read all layout files
    file_contents = {}
    for file_path in layout_files:
        content = read_file_content(file_path)
        if content:
            file_contents[file_path] = content
    
    analysis_results = {}
    critical_components = []
    safe_to_remove = []
    
    print(f"📋 Analyzing {len(duplicate_ids)} duplicate IDs...")
    print()
    
    for component_id in duplicate_ids:
        print(f"🔍 Analyzing: {component_id}")
        
        # Collect contexts from all files
        all_contexts = []
        file_locations = []
        
        for file_path, content in file_contents.items():
            contexts = extract_component_context(content, component_id)
            if contexts:
                for context in contexts:
                    context['file'] = file_path
                    all_contexts.append(context)
                    file_locations.append(os.path.basename(file_path))
        
        if len(all_contexts) < 2:
            print(f"   ⚠️  Only found in {len(all_contexts)} location(s)")
            continue
        
        # Analyze functionality differences
        func_analysis = analyze_component_differences(component_id, all_contexts)
        
        # Check callback usage
        callback_analysis = check_callback_usage(component_id, callback_files)
        
        analysis_results[component_id] = {
            'file_locations': file_locations,
            'contexts_count': len(all_contexts),
            'functionality_analysis': func_analysis,
            'callback_usage': callback_analysis,
            'all_contexts': all_contexts
        }
        
        # Determine criticality
        is_critical = (
            callback_analysis['is_critical'] or
            (isinstance(func_analysis, dict) and func_analysis.get('unique_types', False)) or
            (isinstance(func_analysis, dict) and func_analysis.get('recommendation') == 'KEEP_BOTH')
        )
        
        if is_critical:
            critical_components.append(component_id)
            print(f"   🚨 CRITICAL: Used in callbacks or has different functionality")
        else:
            safe_to_remove.append(component_id)
            print(f"   ✅ SAFE: Appears to be redundant duplicate")
        
        print(f"   📍 Found in: {', '.join(file_locations)}")
        if callback_analysis['is_critical']:
            print(f"   🔗 Callback usage: {callback_analysis['total_usage']} references")
        print()
    
    print("=" * 70)
    print("📊 ANALYSIS SUMMARY")
    print("=" * 70)
    print(f"🚨 CRITICAL components (keep both): {len(critical_components)}")
    for comp in critical_components:
        print(f"   - {comp}")
    
    print(f"\n✅ SAFE TO REMOVE duplicates: {len(safe_to_remove)}")
    for comp in safe_to_remove[:10]:  # Show first 10
        print(f"   - {comp}")
    if len(safe_to_remove) > 10:
        print(f"   ... and {len(safe_to_remove) - 10} more")
    
    print(f"\n📊 Total analyzed: {len(analysis_results)}")
    print(f"📊 Critical (preserve): {len(critical_components)}")
    print(f"📊 Safe to remove: {len(safe_to_remove)}")
    print(f"📊 Functionality preserved: {(len(critical_components) / len(analysis_results)) * 100:.1f}%")
    
    # Save detailed analysis
    with open('duplicate_functionality_analysis.json', 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_analyzed': len(analysis_results),
                'critical_components': len(critical_components),
                'safe_to_remove': len(safe_to_remove)
            },
            'critical_components': critical_components,
            'safe_to_remove': safe_to_remove,
            'detailed_analysis': analysis_results
        }, f, indent=2)
    
    print(f"\n💾 Detailed analysis saved to: duplicate_functionality_analysis.json")
    
    return analysis_results, critical_components, safe_to_remove

if __name__ == "__main__":
    main()
