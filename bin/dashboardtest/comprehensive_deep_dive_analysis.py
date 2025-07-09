#!/usr/bin/env python3
"""
COMPREHENSIVE DEEP DIVE ANALYSIS
Identify ALL errors in frontend and backend preventing dashboard functionality
"""
import os
import re
import sys
import json
import subprocess
from pathlib import Path

class DashboardDiagnostics:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.dashboard_dir = Path(".")
        self.backend_dir = Path("../backendtest")
        
    def log_error(self, category, error):
        self.errors.append(f"[{category}] {error}")
        
    def log_warning(self, category, warning):
        self.warnings.append(f"[{category}] {warning}")
        
    def check_file_exists(self, filepath, category="FILE"):
        if not os.path.exists(filepath):
            self.log_error(category, f"Missing file: {filepath}")
            return False
        return True
        
    def check_import_syntax(self, filepath):
        """Check if a Python file has syntax errors"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            compile(content, filepath, 'exec')
            return True
        except SyntaxError as e:
            self.log_error("SYNTAX", f"{filepath}: Line {e.lineno}: {e.msg}")
            return False
        except Exception as e:
            self.log_error("SYNTAX", f"{filepath}: {e}")
            return False
            
    def analyze_duplicate_callbacks(self):
        """Find duplicate callback output IDs"""
        callbacks_file = "callbacks.py"
        if not self.check_file_exists(callbacks_file, "CALLBACKS"):
            return
            
        try:
            with open(callbacks_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find all Output() declarations
            output_pattern = r'Output\s*\(\s*["\']([^"\']+)["\']'
            outputs = re.findall(output_pattern, content)
            
            # Count occurrences
            output_counts = {}
            for output in outputs:
                output_counts[output] = output_counts.get(output, 0) + 1
                
            # Find duplicates
            duplicates = {k: v for k, v in output_counts.items() if v > 1}
            
            if duplicates:
                for output_id, count in duplicates.items():
                    self.log_error("DUPLICATE_CALLBACK", f"Output '{output_id}' used {count} times")
                    
        except Exception as e:
            self.log_error("CALLBACKS", f"Error analyzing callbacks: {e}")
            
    def analyze_missing_components(self):
        """Check for missing component IDs referenced in callbacks"""
        # Get all output IDs from callbacks
        try:
            with open("callbacks.py", 'r', encoding='utf-8') as f:
                callbacks_content = f.read()
        except:
            return
            
        output_pattern = r'Output\s*\(\s*["\']([^"\']+)["\']'
        callback_outputs = set(re.findall(output_pattern, callbacks_content))
        
        # Get all component IDs from layout files
        layout_ids = set()
        layout_files = ["layout.py", "auto_trading_layout.py", "futures_trading_layout.py", 
                       "binance_exact_layout.py", "email_config_layout.py", "hybrid_learning_layout.py"]
                       
        for layout_file in layout_files:
            if os.path.exists(layout_file):
                try:
                    with open(layout_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    id_pattern = r'id\s*=\s*["\']([^"\']+)["\']'
                    file_ids = re.findall(id_pattern, content)
                    layout_ids.update(file_ids)
                except Exception as e:
                    self.log_error("LAYOUT", f"Error reading {layout_file}: {e}")
                    
        # Find missing components
        missing = callback_outputs - layout_ids
        for missing_id in missing:
            self.log_error("MISSING_COMPONENT", f"Callback output '{missing_id}' has no corresponding component")
            
    def check_backend_endpoints(self):
        """Analyze backend main.py for endpoint issues"""
        main_py = self.backend_dir / "main.py"
        if not self.check_file_exists(main_py, "BACKEND"):
            return
            
        try:
            with open(main_py, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for endpoint definitions
            endpoint_pattern = r'@app\.(get|post|put|delete)\s*\(\s*["\']([^"\']+)["\']'
            endpoints = re.findall(endpoint_pattern, content)
            
            # Check for WebSocket endpoints
            ws_pattern = r'@router\.websocket\s*\(\s*["\']([^"\']+)["\']'
            ws_endpoints = re.findall(ws_pattern, content)
            
            print(f"Found {len(endpoints)} HTTP endpoints and {len(ws_endpoints)} WebSocket endpoints")
            
            # Check for common required endpoints
            required_endpoints = [
                "/health", "/ml/predict", "/notifications", 
                "/advanced_auto_trading/status", "/price"
            ]
            
            found_endpoints = [endpoint[1] for endpoint in endpoints]
            for req_endpoint in required_endpoints:
                if req_endpoint not in found_endpoints:
                    self.log_warning("BACKEND", f"Missing recommended endpoint: {req_endpoint}")
                    
        except Exception as e:
            self.log_error("BACKEND", f"Error analyzing main.py: {e}")
            
    def check_javascript_files(self):
        """Check JavaScript files for errors"""
        assets_dir = Path("assets")
        if assets_dir.exists():
            js_files = list(assets_dir.glob("*.js"))
            for js_file in js_files:
                try:
                    with open(js_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Check for common JS errors
                    if "ws://localhost:8000/ws/price" in content and "ws://localhost:8000/ws/prices" in content:
                        self.log_error("JAVASCRIPT", f"{js_file}: Conflicting WebSocket URLs")
                        
                    # Check for hardcoded ports that might be wrong
                    if "localhost:8001" in content:
                        self.log_warning("JAVASCRIPT", f"{js_file}: References port 8001 instead of 8000")
                        
                except Exception as e:
                    self.log_error("JAVASCRIPT", f"Error reading {js_file}: {e}")
                    
    def check_dependencies(self):
        """Check for missing Python dependencies"""
        try:
            import dash
            import dash_bootstrap_components
            import plotly
            import requests
        except ImportError as e:
            self.log_error("DEPENDENCIES", f"Missing Python package: {e}")
            
    def check_port_conflicts(self):
        """Check for port conflicts"""
        try:
            result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
            netstat_output = result.stdout
            
            # Check if required ports are in use
            if ":8000" in netstat_output:
                self.log_warning("PORTS", "Port 8000 is in use (this is expected for backend)")
            if ":8050" in netstat_output:
                self.log_warning("PORTS", "Port 8050 is in use (this is expected for dashboard)")
                
        except Exception as e:
            self.log_warning("PORTS", f"Could not check port status: {e}")
            
    def analyze_layout_structure(self):
        """Analyze layout.py for structural issues"""
        layout_file = "layout.py"
        if not self.check_file_exists(layout_file, "LAYOUT"):
            return
            
        try:
            with open(layout_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check if layout variable is defined
            if "layout = " not in content:
                self.log_error("LAYOUT", "No 'layout = ' variable found in layout.py")
                
            # Check for proper imports
            required_imports = ["dash", "html", "dcc", "dbc"]
            for imp in required_imports:
                if imp not in content:
                    self.log_warning("LAYOUT", f"Missing import: {imp}")
                    
            # Check for tab layout imports
            tab_imports = [
                "create_auto_trading_layout",
                "create_futures_trading_layout", 
                "create_binance_exact_layout",
                "create_email_config_layout",
                "create_hybrid_learning_layout"
            ]
            
            for tab_import in tab_imports:
                if tab_import not in content:
                    self.log_warning("LAYOUT", f"Missing tab layout import: {tab_import}")
                    
        except Exception as e:
            self.log_error("LAYOUT", f"Error analyzing layout.py: {e}")
            
    def run_full_analysis(self):
        """Run complete analysis"""
        print("=== COMPREHENSIVE DASHBOARD DEEP DIVE ANALYSIS ===")
        print("Checking all possible sources of errors...\n")
        
        # 1. File existence checks
        print("1. CHECKING FILE EXISTENCE...")
        critical_files = [
            "app.py", "dash_app.py", "layout.py", "callbacks.py",
            "../backendtest/main.py", "../backendtest/ws.py"
        ]
        for file in critical_files:
            self.check_file_exists(file, "CRITICAL_FILE")
            
        # 2. Syntax checks
        print("2. CHECKING PYTHON SYNTAX...")
        python_files = ["app.py", "dash_app.py", "layout.py", "callbacks.py"]
        for file in python_files:
            if os.path.exists(file):
                self.check_import_syntax(file)
                
        # 3. Callback analysis
        print("3. ANALYZING CALLBACKS...")
        self.analyze_duplicate_callbacks()
        self.analyze_missing_components()
        
        # 4. Backend analysis
        print("4. ANALYZING BACKEND...")
        self.check_backend_endpoints()
        
        # 5. Frontend analysis
        print("5. ANALYZING FRONTEND...")
        self.check_javascript_files()
        self.analyze_layout_structure()
        
        # 6. System checks
        print("6. CHECKING SYSTEM...")
        self.check_dependencies()
        self.check_port_conflicts()
        
        # 7. Report results
        self.generate_report()
        
    def generate_report(self):
        """Generate comprehensive error report"""
        print("\n" + "="*80)
        print("COMPREHENSIVE ERROR ANALYSIS REPORT")
        print("="*80)
        
        if self.errors:
            print(f"\n🚨 CRITICAL ERRORS ({len(self.errors)}):")
            print("-" * 50)
            for i, error in enumerate(self.errors, 1):
                print(f"{i:2d}. {error}")
                
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            print("-" * 50)
            for i, warning in enumerate(self.warnings, 1):
                print(f"{i:2d}. {warning}")
                
        if not self.errors and not self.warnings:
            print("\n✅ NO CRITICAL ERRORS FOUND!")
            print("The dashboard should be working. Check browser console for runtime errors.")
        else:
            print(f"\n📊 SUMMARY:")
            print(f"   Critical Errors: {len(self.errors)}")
            print(f"   Warnings: {len(self.warnings)}")
            print(f"\n🔧 RECOMMENDATION:")
            if self.errors:
                print("   Fix all critical errors first, then restart both servers.")
            else:
                print("   Address warnings if possible, then test dashboard functionality.")

if __name__ == "__main__":
    diagnostics = DashboardDiagnostics()
    diagnostics.run_full_analysis()
