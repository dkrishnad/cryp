#!/usr/bin/env python3
"""
Final Comprehensive Validation Script
Runs detailed checks from correct directories with proper path handling
"""

import os
import sys
import json
import importlib.util
import ast
from datetime import datetime
import subprocess
import traceback

class ComprehensiveValidator:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.backend_dir = os.path.join(self.base_dir, "backendtest")
        self.dashboard_dir = os.path.join(self.base_dir, "dashboardtest")
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "backend_tests": {},
            "dashboard_tests": {},
            "integration_tests": {},
            "summary": {}
        }
        
    def log(self, message, level="INFO"):
        print(f"[{level}] {message}")
        
    def check_file_syntax(self, file_path):
        """Check Python file syntax"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            ast.parse(source)
            return {"status": "success", "message": "Syntax OK"}
        except SyntaxError as e:
            return {"status": "error", "message": f"Syntax error at line {e.lineno}: {e.msg}"}
        except Exception as e:
            return {"status": "error", "message": f"Error reading file: {str(e)}"}
    
    def check_module_import(self, module_path, working_dir):
        """Check if a module can be imported from a specific directory"""
        try:
            # Change to working directory
            original_dir = os.getcwd()
            original_path = sys.path.copy()
            
            os.chdir(working_dir)
            if working_dir not in sys.path:
                sys.path.insert(0, working_dir)
            
            # Get module name
            module_name = os.path.splitext(os.path.basename(module_path))[0]
            
            # Try to import
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Restore
            os.chdir(original_dir)
            sys.path = original_path
            
            return {"status": "success", "message": "Import successful"}
            
        except Exception as e:
            # Restore
            os.chdir(original_dir)
            sys.path = original_path
            return {"status": "error", "message": str(e)}
    
    def check_compilation(self, file_path, working_dir):
        """Check if file compiles using py_compile"""
        try:
            original_dir = os.getcwd()
            os.chdir(working_dir)
            
            result = subprocess.run([
                sys.executable, "-m", "py_compile", os.path.basename(file_path)
            ], capture_output=True, text=True, timeout=30)
            
            os.chdir(original_dir)
            
            if result.returncode == 0:
                return {"status": "success", "message": "Compilation successful"}
            else:
                return {"status": "error", "message": result.stderr}
                
        except Exception as e:
            os.chdir(original_dir)
            return {"status": "error", "message": str(e)}
    
    def analyze_endpoints(self, file_path):
        """Extract API endpoints from FastAPI file"""
        endpoints = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for @app.{method} decorators
            import re
            pattern = r'@app\.(get|post|put|delete|patch)\("([^"]+)"\)'
            matches = re.findall(pattern, content, re.IGNORECASE)
            
            for method, path in matches:
                endpoints.append(f"{method.upper()} {path}")
                
        except Exception as e:
            self.log(f"Error analyzing endpoints in {file_path}: {e}", "ERROR")
            
        return endpoints
    
    def validate_backend(self):
        """Comprehensive backend validation"""
        self.log("🔍 VALIDATING BACKEND COMPONENTS")
        
        backend_files = []
        if os.path.exists(self.backend_dir):
            for file in os.listdir(self.backend_dir):
                if file.endswith('.py') and not file.startswith('__'):
                    backend_files.append(os.path.join(self.backend_dir, file))
        
        backend_results = {}
        
        for file_path in backend_files:
            file_name = os.path.basename(file_path)
            self.log(f"   Checking {file_name}...")
            
            result = {
                "syntax": self.check_file_syntax(file_path),
                "compilation": self.check_compilation(file_path, self.backend_dir),
                "import": self.check_module_import(file_path, self.backend_dir)
            }
            
            # Special handling for main.py
            if file_name == "main.py":
                result["endpoints"] = self.analyze_endpoints(file_path)
            
            backend_results[file_name] = result
            
            # Status summary
            status_emoji = "✅" if all(
                r["status"] == "success" for r in [result["syntax"], result["compilation"]]
            ) else "❌"
            self.log(f"   {status_emoji} {file_name}")
        
        self.results["backend_tests"] = backend_results
        return backend_results
    
    def validate_dashboard(self):
        """Comprehensive dashboard validation"""
        self.log("\n🎨 VALIDATING DASHBOARD COMPONENTS")
        
        dashboard_files = []
        if os.path.exists(self.dashboard_dir):
            for file in os.listdir(self.dashboard_dir):
                if file.endswith('.py') and file in ['app.py', 'layout.py', 'callbacks.py', 'utils.py']:
                    dashboard_files.append(os.path.join(self.dashboard_dir, file))
        
        dashboard_results = {}
        
        for file_path in dashboard_files:
            file_name = os.path.basename(file_path)
            self.log(f"   Checking {file_name}...")
            
            result = {
                "syntax": self.check_file_syntax(file_path),
                "compilation": self.check_compilation(file_path, self.dashboard_dir)
            }
            
            dashboard_results[file_name] = result
            
            # Status summary
            status_emoji = "✅" if all(
                r["status"] == "success" for r in result.values()
            ) else "❌"
            self.log(f"   {status_emoji} {file_name}")
        
        self.results["dashboard_tests"] = dashboard_results
        return dashboard_results
    
    def test_api_server_startup(self):
        """Test if the API server can start"""
        self.log("\n🚀 TESTING API SERVER STARTUP")
        
        try:
            original_dir = os.getcwd()
            os.chdir(self.backend_dir)
            
            # Test basic import of main.py
            result = subprocess.run([
                sys.executable, "-c", 
                "import main; print('✅ FastAPI app imported successfully')"
            ], capture_output=True, text=True, timeout=15)
            
            os.chdir(original_dir)
            
            if result.returncode == 0:
                self.log("   ✅ API server startup test passed")
                return {"status": "success", "message": "Server can start"}
            else:
                self.log(f"   ❌ API server startup failed: {result.stderr}")
                return {"status": "error", "message": result.stderr}
                
        except Exception as e:
            os.chdir(original_dir)
            self.log(f"   ❌ Server startup test error: {e}")
            return {"status": "error", "message": str(e)}
    
    def check_missing_dependencies(self):
        """Check for missing Python packages"""
        self.log("\n📦 CHECKING DEPENDENCIES")
        
        required_packages = [
            'fastapi', 'uvicorn', 'pydantic', 'requests', 'numpy', 
            'dash', 'plotly', 'pandas', 'sqlite3'
        ]
        
        missing = []
        available = []
        
        for package in required_packages:
            try:
                __import__(package)
                available.append(package)
                self.log(f"   ✅ {package}")
            except ImportError:
                missing.append(package)
                self.log(f"   ❌ {package}")
        
        return {"missing": missing, "available": available}
    
    def run_full_validation(self):
        """Run complete validation suite"""
        print("=" * 80)
        print("🔍 FINAL COMPREHENSIVE CODEBASE VALIDATION")
        print("=" * 80)
        
        # Dependencies check
        deps = self.check_missing_dependencies()
        self.results["dependencies"] = deps
        
        # Backend validation
        backend_results = self.validate_backend()
        
        # Dashboard validation  
        dashboard_results = self.validate_dashboard()
        
        # Integration tests
        server_test = self.test_api_server_startup()
        self.results["integration_tests"]["server_startup"] = server_test
        
        # Generate summary
        self.generate_summary()
        
        # Save results
        self.save_results()
        
        return self.results
    
    def generate_summary(self):
        """Generate validation summary"""
        self.log("\n" + "=" * 80)
        self.log("📊 VALIDATION SUMMARY")
        self.log("=" * 80)
        
        backend_files = len(self.results["backend_tests"])
        backend_success = sum(1 for result in self.results["backend_tests"].values() 
                            if result["syntax"]["status"] == "success" and 
                               result["compilation"]["status"] == "success")
        
        dashboard_files = len(self.results["dashboard_tests"])
        dashboard_success = sum(1 for result in self.results["dashboard_tests"].values()
                              if all(r["status"] == "success" for r in result.values()))
        
        missing_deps = len(self.results["dependencies"]["missing"])
        
        self.log(f"📁 Backend Files: {backend_success}/{backend_files} ✅")
        self.log(f"🎨 Dashboard Files: {dashboard_success}/{dashboard_files} ✅")
        self.log(f"📦 Missing Dependencies: {missing_deps}")
        
        if "server_startup" in self.results["integration_tests"]:
            server_status = self.results["integration_tests"]["server_startup"]["status"]
            self.log(f"🚀 Server Startup: {'✅' if server_status == 'success' else '❌'}")
        
        # Endpoints count
        main_result = self.results["backend_tests"].get("main.py", {})
        if "endpoints" in main_result:
            endpoint_count = len(main_result["endpoints"])
            self.log(f"🌐 API Endpoints Found: {endpoint_count}")
        
        # Overall status
        overall_success = (
            backend_success == backend_files and 
            dashboard_success == dashboard_files and
            missing_deps == 0
        )
        
        status = "🟢 EXCELLENT" if overall_success else "🟡 NEEDS ATTENTION"
        self.log(f"\n🎯 OVERALL STATUS: {status}")
        
        self.results["summary"] = {
            "backend_success_rate": f"{backend_success}/{backend_files}",
            "dashboard_success_rate": f"{dashboard_success}/{dashboard_files}",
            "missing_dependencies": missing_deps,
            "overall_status": "success" if overall_success else "needs_attention"
        }
    
    def save_results(self):
        """Save detailed results to file"""
        output_file = os.path.join(self.base_dir, "final_validation_results.json")
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            self.log(f"\n📄 Detailed results saved to: {output_file}")
        except Exception as e:
            self.log(f"❌ Error saving results: {e}", "ERROR")

def main():
    validator = ComprehensiveValidator()
    results = validator.run_full_validation()
    
    # Return appropriate exit code
    if results["summary"]["overall_status"] == "success":
        print("\n✅ All validations passed successfully!")
        return 0
    else:
        print("\n⚠️ Some issues found - check results above")
        return 1

if __name__ == "__main__":
    exit(main())
