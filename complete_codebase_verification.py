#!/usr/bin/env python3
"""
Complete Codebase Verification Script
Checks for missing imports, wrong names, non-existent modules, and other issues
"""

import os
import sys
import ast
import importlib.util
import traceback
from datetime import datetime
import subprocess
import json

class CodebaseVerifier:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.backend_dir = os.path.join(self.base_dir, "backendtest")
        self.dashboard_dir = os.path.join(self.base_dir, "dashboardtest")
        self.issues = {
            "missing_imports": [],
            "missing_functions": [],
            "missing_classes": [],
            "wrong_names": [],
            "syntax_errors": [],
            "import_errors": [],
            "missing_files": [],
            "undefined_variables": [],
            "type_errors": []
        }
        
    def log(self, message, level="INFO"):
        print(f"[{level}] {message}")
        
    def check_file_exists(self, file_path):
        """Check if a file exists"""
        return os.path.exists(file_path)
    
    def extract_imports_from_file(self, file_path):
        """Extract all imports from a Python file"""
        imports = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append({
                            "type": "import",
                            "module": alias.name,
                            "alias": alias.asname,
                            "line": node.lineno
                        })
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        imports.append({
                            "type": "from_import",
                            "module": module,
                            "name": alias.name,
                            "alias": alias.asname,
                            "line": node.lineno
                        })
        except Exception as e:
            self.issues["syntax_errors"].append({
                "file": file_path,
                "error": str(e),
                "line": getattr(e, 'lineno', 'unknown')
            })
        
        return imports
    
    def extract_function_calls(self, file_path):
        """Extract function calls from a Python file"""
        function_calls = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        function_calls.append({
                            "name": node.func.id,
                            "line": node.lineno
                        })
                    elif isinstance(node.func, ast.Attribute):
                        # Handle method calls like obj.method()
                        if isinstance(node.func.value, ast.Name):
                            function_calls.append({
                                "name": f"{node.func.value.id}.{node.func.attr}",
                                "line": node.lineno
                            })
        except Exception as e:
            pass  # Already handled in extract_imports_from_file
        
        return function_calls
    
    def check_import_availability(self, import_info, working_dir):
        """Check if an import is available"""
        try:
            original_dir = os.getcwd()
            original_path = sys.path.copy()
            
            os.chdir(working_dir)
            if working_dir not in sys.path:
                sys.path.insert(0, working_dir)
            
            if import_info["type"] == "import":
                module_name = import_info["module"]
                try:
                    __import__(module_name)
                    return True
                except ImportError:
                    return False
            elif import_info["type"] == "from_import":
                module_name = import_info["module"]
                item_name = import_info["name"]
                try:
                    module = __import__(module_name, fromlist=[item_name])
                    if hasattr(module, item_name):
                        return True
                    return False
                except ImportError:
                    return False
                    
        except Exception:
            return False
        finally:
            os.chdir(original_dir)
            sys.path = original_path
    
    def verify_backend_files(self):
        """Verify all backend files"""
        self.log("🔍 VERIFYING BACKEND FILES")
        
        backend_files = []
        if os.path.exists(self.backend_dir):
            for file in os.listdir(self.backend_dir):
                if file.endswith('.py'):
                    backend_files.append(os.path.join(self.backend_dir, file))
        
        for file_path in backend_files:
            file_name = os.path.basename(file_path)
            self.log(f"   Checking {file_name}...")
            
            # Check imports
            imports = self.extract_imports_from_file(file_path)
            for imp in imports:
                if not self.check_import_availability(imp, self.backend_dir):
                    self.issues["import_errors"].append({
                        "file": file_path,
                        "import": imp,
                        "line": imp["line"]
                    })
            
            # Check function calls
            function_calls = self.extract_function_calls(file_path)
            # We'll cross-reference these later
    
    def verify_dashboard_files(self):
        """Verify all dashboard files"""
        self.log("\n🎨 VERIFYING DASHBOARD FILES")
        
        dashboard_files = []
        if os.path.exists(self.dashboard_dir):
            for file in os.listdir(self.dashboard_dir):
                if file.endswith('.py') and file in ['app.py', 'layout.py', 'callbacks.py', 'utils.py']:
                    dashboard_files.append(os.path.join(self.dashboard_dir, file))
        
        for file_path in dashboard_files:
            file_name = os.path.basename(file_path)
            self.log(f"   Checking {file_name}...")
            
            # Check imports
            imports = self.extract_imports_from_file(file_path)
            for imp in imports:
                if not self.check_import_availability(imp, self.dashboard_dir):
                    self.issues["import_errors"].append({
                        "file": file_path,
                        "import": imp,
                        "line": imp["line"]
                    })
    
    def check_main_py_issues(self):
        """Specific checks for main.py"""
        self.log("\n🔧 CHECKING MAIN.PY SPECIFIC ISSUES")
        
        main_path = os.path.join(self.backend_dir, "main.py")
        if not os.path.exists(main_path):
            self.issues["missing_files"].append("main.py")
            return
        
        # Check for specific patterns in main.py
        try:
            with open(main_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for missing uvicorn import
            if "import uvicorn" not in content:
                self.issues["missing_imports"].append({
                    "file": main_path,
                    "missing": "uvicorn",
                    "note": "Required for FastAPI server"
                })
            
            # Check for incomplete function implementations
            incomplete_functions = []
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith('def ') and i + 1 < len(lines):
                    # Check if next few lines are empty or just pass/...
                    next_lines = lines[i+1:i+5]
                    content_lines = [l.strip() for l in next_lines if l.strip() and not l.strip().startswith('#')]
                    if not content_lines or all(l in ['pass', '...', 'return', 'return None'] for l in content_lines):
                        func_name = line.strip().split('(')[0].replace('def ', '')
                        incomplete_functions.append({
                            "function": func_name,
                            "line": i + 1
                        })
            
            if incomplete_functions:
                self.issues["missing_functions"].extend(incomplete_functions)
                
        except Exception as e:
            self.log(f"Error analyzing main.py: {e}", "ERROR")
    
    def check_cross_references(self):
        """Check cross-references between files"""
        self.log("\n🔗 CHECKING CROSS-REFERENCES")
        
        # Check if imported modules exist in the expected locations
        expected_modules = [
            "db.py", "trading.py", "ml.py", "ws.py", "hybrid_learning.py",
            "online_learning.py", "data_collection.py", "email_utils.py",
            "price_feed.py", "futures_trading.py", "binance_futures_exact.py",
            "advanced_auto_trading.py", "minimal_transfer_endpoints.py",
            "ml_compatibility_manager.py", "missing_endpoints.py"
        ]
        
        for module in expected_modules:
            module_path = os.path.join(self.backend_dir, module)
            if not os.path.exists(module_path):
                self.issues["missing_files"].append({
                    "file": module,
                    "expected_path": module_path,
                    "note": "Referenced in main.py but file missing"
                })
    
    def check_specific_issues(self):
        """Check for specific known issues"""
        self.log("\n🎯 CHECKING SPECIFIC KNOWN ISSUES")
        
        # Check for duplicate imports in main.py
        main_path = os.path.join(self.backend_dir, "main.py")
        if os.path.exists(main_path):
            with open(main_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for duplicate minimal_transfer_endpoints imports
            if content.count("from minimal_transfer_endpoints import") > 1:
                self.issues["wrong_names"].append({
                    "file": main_path,
                    "issue": "Duplicate minimal_transfer_endpoints import",
                    "suggestion": "Remove duplicate import statement"
                })
            
            # Check for duplicate ML_COMPATIBILITY_AVAILABLE assignments
            if content.count("ML_COMPATIBILITY_AVAILABLE = True") > 1:
                self.issues["wrong_names"].append({
                    "file": main_path,
                    "issue": "Duplicate ML_COMPATIBILITY_AVAILABLE assignment",
                    "suggestion": "Remove duplicate assignment"
                })
    
    def run_verification(self):
        """Run complete verification"""
        print("=" * 80)
        print("🔍 COMPLETE CODEBASE VERIFICATION")
        print("=" * 80)
        
        # Verify backend
        self.verify_backend_files()
        
        # Verify dashboard
        self.verify_dashboard_files()
        
        # Check main.py specifics
        self.check_main_py_issues()
        
        # Check cross-references
        self.check_cross_references()
        
        # Check specific issues
        self.check_specific_issues()
        
        # Generate report
        self.generate_report()
        
        return self.issues
    
    def generate_report(self):
        """Generate comprehensive report"""
        print("\n" + "=" * 80)
        print("📊 VERIFICATION REPORT")
        print("=" * 80)
        
        total_issues = sum(len(issues) for issues in self.issues.values())
        
        if total_issues == 0:
            print("🎉 NO ISSUES FOUND! Your codebase is clean.")
            return
        
        print(f"⚠️  Total Issues Found: {total_issues}")
        
        # Import errors
        if self.issues["import_errors"]:
            print(f"\n❌ IMPORT ERRORS ({len(self.issues['import_errors'])}):")
            for error in self.issues["import_errors"][:10]:  # Show first 10
                file_name = os.path.basename(error["file"])
                if error["import"]["type"] == "import":
                    print(f"   {file_name}:{error['line']} - Cannot import '{error['import']['module']}'")
                else:
                    print(f"   {file_name}:{error['line']} - Cannot import '{error['import']['name']}' from '{error['import']['module']}'")
        
        # Missing files
        if self.issues["missing_files"]:
            print(f"\n📁 MISSING FILES ({len(self.issues['missing_files'])}):")
            for missing in self.issues["missing_files"]:
                if isinstance(missing, dict):
                    print(f"   {missing['file']} - {missing['note']}")
                else:
                    print(f"   {missing}")
        
        # Syntax errors
        if self.issues["syntax_errors"]:
            print(f"\n🚨 SYNTAX ERRORS ({len(self.issues['syntax_errors'])}):")
            for error in self.issues["syntax_errors"]:
                file_name = os.path.basename(error["file"])
                print(f"   {file_name}:{error['line']} - {error['error']}")
        
        # Wrong names/duplicates
        if self.issues["wrong_names"]:
            print(f"\n🔄 WRONG NAMES/DUPLICATES ({len(self.issues['wrong_names'])}):")
            for issue in self.issues["wrong_names"]:
                file_name = os.path.basename(issue["file"])
                print(f"   {file_name} - {issue['issue']}")
                if "suggestion" in issue:
                    print(f"      💡 {issue['suggestion']}")
        
        # Missing functions
        if self.issues["missing_functions"]:
            print(f"\n🔧 INCOMPLETE FUNCTIONS ({len(self.issues['missing_functions'])}):")
            for func in self.issues["missing_functions"][:10]:
                if isinstance(func, dict):
                    print(f"   Line {func['line']}: {func['function']}() - Implementation missing")
        
        # Save detailed report
        output_file = os.path.join(self.base_dir, "codebase_verification_report.json")
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "summary": {
                        "total_issues": total_issues,
                        "import_errors": len(self.issues["import_errors"]),
                        "missing_files": len(self.issues["missing_files"]),
                        "syntax_errors": len(self.issues["syntax_errors"]),
                        "wrong_names": len(self.issues["wrong_names"]),
                        "missing_functions": len(self.issues["missing_functions"])
                    },
                    "issues": self.issues
                }, f, indent=2, ensure_ascii=False)
            print(f"\n📄 Detailed report saved to: {output_file}")
        except Exception as e:
            print(f"❌ Error saving report: {e}")

def main():
    verifier = CodebaseVerifier()
    issues = verifier.run_verification()
    
    total_issues = sum(len(issue_list) for issue_list in issues.values())
    if total_issues == 0:
        print("\n✅ VERIFICATION COMPLETE: NO ISSUES FOUND!")
        return 0
    else:
        print(f"\n⚠️  VERIFICATION COMPLETE: {total_issues} ISSUES FOUND")
        return 1

if __name__ == "__main__":
    exit(main())
