#!/usr/bin/env python3
"""
Comprehensive Codebase Check Script
Performs line-by-line analysis of the crypto trading bot application
"""

import os
import sys
import ast
import json
import traceback
import importlib.util
from pathlib import Path
from datetime import datetime

class CodebaseChecker:
    def __init__(self, workspace_path):
        self.workspace_path = Path(workspace_path)
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "summary": {},
            "files_checked": [],
            "syntax_errors": [],
            "import_errors": [],
            "missing_files": [],
            "function_analysis": {},
            "endpoint_analysis": {},
            "critical_issues": [],
            "recommendations": []
        }
        
    def check_file_syntax(self, file_path):
        """Check Python file for syntax errors"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try to parse the AST
            ast.parse(content)
            return True, None
        except SyntaxError as e:
            return False, f"Syntax error at line {e.lineno}: {e.msg}"
        except Exception as e:
            return False, f"Parse error: {str(e)}"
    
    def check_imports(self, file_path):
        """Check if all imports can be resolved"""
        import_errors = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        try:
                            __import__(alias.name)
                        except ImportError as e:
                            import_errors.append(f"Import '{alias.name}' failed: {str(e)}")
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        try:
                            if node.level == 0:  # Absolute import
                                __import__(node.module)
                            else:  # Relative import - check locally
                                pass  # Skip relative imports for now
                        except ImportError as e:
                            import_errors.append(f"Import from '{node.module}' failed: {str(e)}")
        except Exception as e:
            import_errors.append(f"Could not analyze imports: {str(e)}")
        
        return import_errors
    
    def analyze_functions(self, file_path):
        """Analyze function definitions and calls"""
        functions = {"defined": [], "called": [], "async": [], "missing_params": []}
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = {
                        "name": node.name,
                        "line": node.lineno,
                        "args": [arg.arg for arg in node.args.args],
                        "is_async": False
                    }
                    functions["defined"].append(func_info)
                elif isinstance(node, ast.AsyncFunctionDef):
                    func_info = {
                        "name": node.name,
                        "line": node.lineno,
                        "args": [arg.arg for arg in node.args.args],
                        "is_async": True
                    }
                    functions["defined"].append(func_info)
                    functions["async"].append(node.name)
                elif isinstance(node, ast.Call):
                    if hasattr(node.func, 'id'):
                        functions["called"].append(node.func.id)
                    elif hasattr(node.func, 'attr'):
                        functions["called"].append(node.func.attr)
        except Exception as e:
            functions["error"] = str(e)
        
        return functions
    
    def check_backend_main(self):
        """Specifically check the main backend file"""
        main_path = self.workspace_path / "backendtest" / "main.py"
        if not main_path.exists():
            self.results["critical_issues"].append("Main backend file (backendtest/main.py) not found!")
            return
        
        print(f"[INFO] Checking main backend file: {main_path}")
        
        # Check syntax
        syntax_ok, syntax_error = self.check_file_syntax(main_path)
        if not syntax_ok:
            self.results["syntax_errors"].append({
                "file": str(main_path),
                "error": syntax_error
            })
        
        # Check imports
        import_errors = self.check_imports(main_path)
        if import_errors:
            self.results["import_errors"].extend([{
                "file": str(main_path),
                "error": err
            } for err in import_errors])
        
        # Analyze functions
        functions = self.analyze_functions(main_path)
        self.results["function_analysis"]["main.py"] = functions
        
        # Check for FastAPI endpoints
        endpoints = []
        try:
            with open(main_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for @app.get, @app.post, etc.
            import re
            endpoint_patterns = [
                r'@app\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']',
                r'@app\.(get|post|put|delete|patch)\("([^"]+)"',
                r"@app\.(get|post|put|delete|patch)\('([^']+)'"
            ]
            
            for pattern in endpoint_patterns:
                matches = re.findall(pattern, content)
                for method, path in matches:
                    endpoints.append(f"{method.upper()} {path}")
            
            self.results["endpoint_analysis"]["main.py"] = {
                "total_endpoints": len(endpoints),
                "endpoints": sorted(list(set(endpoints)))
            }
            
        except Exception as e:
            self.results["endpoint_analysis"]["main.py"] = {"error": str(e)}
    
    def check_dashboard_files(self):
        """Check dashboard files"""
        dashboard_path = self.workspace_path / "dashboardtest"
        if not dashboard_path.exists():
            self.results["critical_issues"].append("Dashboard directory (dashboardtest/) not found!")
            return
        
        key_files = ["app.py", "callbacks.py", "layout.py", "utils.py"]
        for file_name in key_files:
            file_path = dashboard_path / file_name
            if file_path.exists():
                print(f"[INFO] Checking dashboard file: {file_path}")
                syntax_ok, syntax_error = self.check_file_syntax(file_path)
                if not syntax_ok:
                    self.results["syntax_errors"].append({
                        "file": str(file_path),
                        "error": syntax_error
                    })
                
                # Check imports
                import_errors = self.check_imports(file_path)
                if import_errors:
                    self.results["import_errors"].extend([{
                        "file": str(file_path),
                        "error": err
                    } for err in import_errors])
            else:
                self.results["missing_files"].append(str(file_path))
    
    def check_backend_modules(self):
        """Check all backend module files"""
        backend_path = self.workspace_path / "backendtest"
        if not backend_path.exists():
            return
        
        python_files = list(backend_path.glob("*.py"))
        for file_path in python_files:
            if file_path.name == "main.py":
                continue  # Already checked
            
            print(f"[INFO] Checking backend module: {file_path}")
            self.results["files_checked"].append(str(file_path))
            
            syntax_ok, syntax_error = self.check_file_syntax(file_path)
            if not syntax_ok:
                self.results["syntax_errors"].append({
                    "file": str(file_path),
                    "error": syntax_error
                })
            
            functions = self.analyze_functions(file_path)
            self.results["function_analysis"][file_path.name] = functions
    
    def check_critical_dependencies(self):
        """Check if critical dependencies exist"""
        critical_files = [
            "backendtest/main.py",
            "backendtest/db.py", 
            "backendtest/trading.py",
            "backendtest/ml.py",
            "backendtest/online_learning.py",
            "backendtest/data_collection.py",
            "backendtest/missing_endpoints.py",
            "dashboardtest/app.py",
            "dashboardtest/callbacks.py"
        ]
        
        for file_path in critical_files:
            full_path = self.workspace_path / file_path
            if not full_path.exists():
                self.results["missing_files"].append(file_path)
                self.results["critical_issues"].append(f"Critical file missing: {file_path}")
    
    def test_compilation(self):
        """Test if main files can be imported/compiled"""
        print("[INFO] Testing compilation of main backend file...")
        
        # Add backend path to sys.path temporarily
        backend_path = str(self.workspace_path / "backendtest")
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        
        try:
            # Try to compile main.py
            main_path = self.workspace_path / "backendtest" / "main.py"
            if main_path.exists():
                with open(main_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                compile(content, str(main_path), 'exec')
                self.results["summary"]["main_compilation"] = "SUCCESS"
        except Exception as e:
            self.results["summary"]["main_compilation"] = f"FAILED: {str(e)}"
            self.results["critical_issues"].append(f"Main backend compilation failed: {str(e)}")
    
    def generate_recommendations(self):
        """Generate recommendations based on findings"""
        recommendations = []
        
        if self.results["syntax_errors"]:
            recommendations.append("Fix syntax errors in Python files before proceeding")
        
        if self.results["missing_files"]:
            recommendations.append(f"Create missing critical files: {', '.join(self.results['missing_files'])}")
        
        if len(self.results["import_errors"]) > 5:
            recommendations.append("Many import errors detected - check Python environment and install missing packages")
        
        # Check endpoint coverage
        main_endpoints = self.results.get("endpoint_analysis", {}).get("main.py", {}).get("total_endpoints", 0)
        if main_endpoints < 20:
            recommendations.append(f"Only {main_endpoints} API endpoints found - expected 30+ for full functionality")
        
        self.results["recommendations"] = recommendations
    
    def run_comprehensive_check(self):
        """Run all checks"""
        print("=" * 80)
        print("COMPREHENSIVE CODEBASE CHECK - LINE BY LINE ANALYSIS")
        print("=" * 80)
        
        self.check_critical_dependencies()
        self.check_backend_main()
        self.check_backend_modules() 
        self.check_dashboard_files()
        self.test_compilation()
        self.generate_recommendations()
        
        # Generate summary
        self.results["summary"].update({
            "total_files_checked": len(self.results["files_checked"]) + 1,  # +1 for main.py
            "syntax_errors_count": len(self.results["syntax_errors"]),
            "import_errors_count": len(self.results["import_errors"]),
            "missing_files_count": len(self.results["missing_files"]),
            "critical_issues_count": len(self.results["critical_issues"])
        })
        
        return self.results
    
    def print_results(self):
        """Print detailed results"""
        results = self.results
        
        print("\n" + "=" * 80)
        print("CODEBASE CHECK RESULTS")
        print("=" * 80)
        
        print(f"\n📊 SUMMARY:")
        print(f"   Files Checked: {results['summary'].get('total_files_checked', 0)}")
        print(f"   Syntax Errors: {results['summary'].get('syntax_errors_count', 0)}")
        print(f"   Import Errors: {results['summary'].get('import_errors_count', 0)}")
        print(f"   Missing Files: {results['summary'].get('missing_files_count', 0)}")
        print(f"   Critical Issues: {results['summary'].get('critical_issues_count', 0)}")
        
        if results['syntax_errors']:
            print(f"\n❌ SYNTAX ERRORS ({len(results['syntax_errors'])}):")
            for error in results['syntax_errors']:
                print(f"   {error['file']}: {error['error']}")
        
        if results['critical_issues']:
            print(f"\n🚨 CRITICAL ISSUES ({len(results['critical_issues'])}):")
            for issue in results['critical_issues']:
                print(f"   • {issue}")
        
        if results['missing_files']:
            print(f"\n📁 MISSING FILES ({len(results['missing_files'])}):")
            for file in results['missing_files']:
                print(f"   • {file}")
        
        # Show endpoint analysis
        if 'main.py' in results['endpoint_analysis']:
            endpoints = results['endpoint_analysis']['main.py']
            if 'total_endpoints' in endpoints:
                print(f"\n🌐 API ENDPOINTS FOUND: {endpoints['total_endpoints']}")
                if endpoints['total_endpoints'] > 0:
                    print("   Sample endpoints:")
                    for endpoint in endpoints['endpoints'][:10]:  # Show first 10
                        print(f"      {endpoint}")
                    if len(endpoints['endpoints']) > 10:
                        print(f"      ... and {len(endpoints['endpoints']) - 10} more")
        
        # Show function analysis summary
        total_functions = 0
        total_async = 0
        for file, funcs in results['function_analysis'].items():
            if 'defined' in funcs:
                total_functions += len(funcs['defined'])
                total_async += len(funcs.get('async', []))
        
        if total_functions > 0:
            print(f"\n⚙️  FUNCTIONS ANALYSIS:")
            print(f"   Total Functions: {total_functions}")
            print(f"   Async Functions: {total_async}")
        
        if results['recommendations']:
            print(f"\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(results['recommendations'], 1):
                print(f"   {i}. {rec}")
        
        # Overall status
        if (results['summary'].get('syntax_errors_count', 0) == 0 and 
            results['summary'].get('critical_issues_count', 0) == 0):
            print(f"\n✅ OVERALL STATUS: PASSED")
            print("   Your codebase appears to be syntactically correct and ready to run!")
        else:
            print(f"\n⚠️  OVERALL STATUS: ISSUES FOUND")
            print("   Please address the issues above before running the application.")
        
        print("\n" + "=" * 80)


if __name__ == "__main__":
    workspace_path = r"c:\Users\Hari\Desktop\Testin dub"
    checker = CodebaseChecker(workspace_path)
    
    try:
        results = checker.run_comprehensive_check()
        checker.print_results()
        
        # Save detailed results to file
        results_file = os.path.join(workspace_path, "codebase_check_results.json")
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n📄 Detailed results saved to: {results_file}")
        
    except Exception as e:
        print(f"❌ Error during codebase check: {e}")
        traceback.print_exc()
