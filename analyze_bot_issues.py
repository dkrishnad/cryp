#!/usr/bin/env python3
"""
Comprehensive Bot Issues Analysis and Fix
Identifies and fixes:
1. Callback duplicate outputs
2. Missing callback-layout component matches
3. Outbound API issues (Binance, external calls)
4. Error handling improvements
5. Rate limiting and connectivity issues
"""

import os
import re
import json
from collections import Counter, defaultdict
from pathlib import Path

class BotIssueAnalyzer:
    def __init__(self):
        self.issues = []
        self.fixes = []
        
    def analyze_callback_issues(self):
        """Analyze dashboard callback issues"""
        print("=== CALLBACK ISSUES ANALYSIS ===")
        
        # Read callbacks file
        callbacks_path = "dashboard/callbacks.py"
        if not os.path.exists(callbacks_path):
            self.issues.append("❌ callbacks.py file not found")
            return
            
        with open(callbacks_path, 'r') as f:
            content = f.read()
        
        # 1. Find duplicate outputs
        output_pattern = r'Output\([\'\"](.*?)[\'\"]'
        outputs = re.findall(output_pattern, content)
        output_counts = Counter(outputs)
        duplicates = {k: v for k, v in output_counts.items() if v > 1}
        
        print(f"Total callback outputs: {len(outputs)}")
        print(f"Duplicate outputs: {len(duplicates)}")
        
        if duplicates:
            print("\n❌ DUPLICATE CALLBACK OUTPUTS:")
            for output_id, count in duplicates.items():
                print(f"  '{output_id}': {count} times")
                self.issues.append(f"Duplicate callback output: {output_id} ({count} times)")
                
                # Find and suggest fixes
                if output_id == 'virtual-balance':
                    self.fixes.append("Merge virtual-balance callbacks into single callback")
                elif output_id == 'backtest-result':
                    self.fixes.append("Consolidate backtest-result callbacks")
                elif 'allow_duplicate=True' in content:
                    self.fixes.append(f"Review if {output_id} needs allow_duplicate=True")
        
        # 2. Check for missing prevent_initial_call
        callbacks_without_prevent = re.findall(r'@app\.callback\((.*?)\)(?!\s*.*prevent_initial_call)', content, re.DOTALL)
        if callbacks_without_prevent:
            print(f"\n⚠️  Callbacks without prevent_initial_call: {len(callbacks_without_prevent)}")
            self.issues.append("Some callbacks missing prevent_initial_call parameter")
        
        # 3. Check for missing error handling
        error_handling_pattern = r'try:\s*.*?except.*?:'
        callbacks_with_try = len(re.findall(error_handling_pattern, content, re.DOTALL))
        total_callbacks = len(re.findall(r'@app\.callback', content))
        
        print(f"\nCallbacks with error handling: {callbacks_with_try}/{total_callbacks}")
        if callbacks_with_try < total_callbacks * 0.8:
            self.issues.append("Insufficient error handling in callbacks")
            self.fixes.append("Add try-except blocks to all API-calling callbacks")
        
        return duplicates
    
    def analyze_layout_callback_mismatch(self):
        """Check for mismatches between layout components and callbacks"""
        print("\n=== LAYOUT-CALLBACK MISMATCH ANALYSIS ===")
        
        # Read layout file
        layout_path = "dashboard/layout.py"
        callbacks_path = "dashboard/callbacks.py"
        
        if not os.path.exists(layout_path) or not os.path.exists(callbacks_path):
            self.issues.append("❌ Layout or callbacks file not found")
            return
        
        with open(layout_path, 'r') as f:
            layout_content = f.read()
        with open(callbacks_path, 'r') as f:
            callbacks_content = f.read()
        
        # Find all component IDs in layout
        layout_ids = set(re.findall(r'id=[\'\"](.*?)[\'\"]', layout_content))
        
        # Find all callback outputs
        callback_outputs = set(re.findall(r'Output\([\'\"](.*?)[\'\"]', callbacks_content))
        
        # Find mismatches
        missing_in_layout = callback_outputs - layout_ids
        missing_callbacks = layout_ids - callback_outputs
        
        print(f"Layout components: {len(layout_ids)}")
        print(f"Callback outputs: {len(callback_outputs)}")
        
        if missing_in_layout:
            print(f"\n❌ CALLBACK OUTPUTS MISSING IN LAYOUT ({len(missing_in_layout)}):")
            for missing in sorted(missing_in_layout):
                print(f"  '{missing}'")
                self.issues.append(f"Callback output '{missing}' has no layout component")
        
        if missing_callbacks:
            print(f"\n⚠️  LAYOUT COMPONENTS WITHOUT CALLBACKS ({len(missing_callbacks)}):")
            # Filter out common components that don't need callbacks
            exclude_patterns = [
                r'.*-btn$', r'.*-button$', r'.*-input$', r'.*-dropdown$',
                r'.*-checklist$', r'.*-slider$', r'.*-upload$', r'.*-store$',
                r'.*-ws$', r'interval-.*', r'.*-interval$'
            ]
            
            real_missing = []
            for missing in sorted(missing_callbacks):
                if not any(re.match(pattern, missing) for pattern in exclude_patterns):
                    real_missing.append(missing)
            
            for missing in real_missing[:10]:  # Show first 10
                print(f"  '{missing}'")
                self.issues.append(f"Layout component '{missing}' has no callback")
        
        return missing_in_layout, missing_callbacks
    
    def analyze_outbound_api_issues(self):
        """Analyze outbound API call issues"""
        print("\n=== OUTBOUND API ISSUES ANALYSIS ===")
        
        api_files = [
            "backend/main.py",
            "backend/data_collection.py", 
            "dashboard/callbacks.py",
            "binance_futures_exact.py",
            "price_feed.py"
        ]
        
        api_issues = []
        
        for file_path in api_files:
            if not os.path.exists(file_path):
                continue
                
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check for rate limiting
            if 'requests.get' in content or 'requests.post' in content:
                if 'timeout=' not in content:
                    api_issues.append(f"Missing timeout in {file_path}")
                if 'retry' not in content.lower() and 'rate' not in content.lower():
                    api_issues.append(f"No rate limiting/retry logic in {file_path}")
            
            # Check for hardcoded URLs
            urls = re.findall(r'https?://[^\s\'"]+', content)
            for url in urls:
                if 'binance.com' in url and 'api.binance.com' in url:
                    if 'testnet' not in content:
                        api_issues.append(f"Using production Binance API in {file_path}")
            
            # Check for missing error handling on API calls
            if 'aiohttp' in content or 'requests' in content:
                if content.count('try:') < content.count('requests.') / 2:
                    api_issues.append(f"Insufficient error handling for API calls in {file_path}")
        
        print(f"API issues found: {len(api_issues)}")
        for issue in api_issues:
            print(f"  ❌ {issue}")
            self.issues.append(issue)
        
        return api_issues
    
    def analyze_websocket_issues(self):
        """Analyze WebSocket connection issues"""
        print("\n=== WEBSOCKET ISSUES ANALYSIS ===")
        
        ws_files = ["backend/ws.py", "dashboard/callbacks.py"]
        ws_issues = []
        
        for file_path in ws_files:
            if not os.path.exists(file_path):
                continue
                
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check for connection handling
            if 'websocket' in content.lower() or 'ws' in content:
                if 'reconnect' not in content.lower():
                    ws_issues.append(f"No reconnection logic in {file_path}")
                if 'ConnectionClosed' not in content and 'disconnect' not in content:
                    ws_issues.append(f"Missing connection error handling in {file_path}")
        
        print(f"WebSocket issues found: {len(ws_issues)}")
        for issue in ws_issues:
            print(f"  ❌ {issue}")
            self.issues.append(issue)
        
        return ws_issues
    
    def generate_fixes(self):
        """Generate comprehensive fixes for all issues"""
        print("\n=== GENERATED FIXES ===")
        
        fixes = {
            "callback_fixes": [
                "Remove duplicate 'virtual-balance' callback by merging logic",
                "Remove duplicate 'backtest-result' callbacks by consolidating", 
                "Add prevent_initial_call=False to all interval-based callbacks",
                "Add comprehensive error handling with try-except to all API callbacks",
                "Fix notifications callback to use interval timer instead of missing button"
            ],
            "api_fixes": [
                "Add timeout=5 to all requests.get/post calls",
                "Implement exponential backoff retry logic for Binance API",
                "Add rate limiting to prevent API key restrictions",
                "Implement connection pooling for better performance",
                "Add fallback mechanisms when APIs are unavailable"
            ],
            "websocket_fixes": [
                "Add automatic reconnection logic for WebSocket connections",
                "Implement connection state management", 
                "Add heartbeat/ping mechanism to maintain connections",
                "Handle connection drops gracefully"
            ],
            "integration_fixes": [
                "Create missing callback for layout components",
                "Remove unused layout components",
                "Standardize component ID naming convention",
                "Add loading states for all async operations"
            ]
        }
        
        for category, fix_list in fixes.items():
            print(f"\n{category.upper()}:")
            for fix in fix_list:
                print(f"  ✅ {fix}")
        
        return fixes
    
    def run_analysis(self):
        """Run complete analysis"""
        print("🔍 CRYPTO BOT - COMPREHENSIVE ISSUE ANALYSIS")
        print("=" * 60)
        
        duplicates = self.analyze_callback_issues()
        mismatches = self.analyze_layout_callback_mismatch()
        api_issues = self.analyze_outbound_api_issues()
        ws_issues = self.analyze_websocket_issues()
        fixes = self.generate_fixes()
        
        print(f"\n📊 SUMMARY")
        print(f"Total issues found: {len(self.issues)}")
        print(f"Total fixes recommended: {len(self.fixes)}")
        
        if self.issues:
            print(f"\n🚨 CRITICAL ISSUES TO FIX:")
            for i, issue in enumerate(self.issues[:10], 1):
                print(f"  {i}. {issue}")
        
        return {
            "duplicates": duplicates,
            "mismatches": mismatches, 
            "api_issues": api_issues,
            "ws_issues": ws_issues,
            "fixes": fixes,
            "total_issues": len(self.issues)
        }

if __name__ == "__main__":
    analyzer = BotIssueAnalyzer()
    results = analyzer.run_analysis()
