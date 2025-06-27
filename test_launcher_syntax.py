#!/usr/bin/env python3
"""
Quick launcher syntax verification
"""

import ast
import sys
import traceback

def test_launcher_syntax():
    """Test launcher syntax"""
    print("🔍 Testing launcher syntax...")
    
    try:
        # Test basic syntax parsing
        with open('launch_bot.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the AST to check for syntax errors
        ast.parse(content)
        print("✅ PASS Launcher Syntax - No syntax errors found")
        return True
        
    except SyntaxError as e:
        print(f"❌ FAIL Launcher Syntax - Syntax error: {e}")
        print(f"   Line {e.lineno}: {e.text}")
        return False
    except Exception as e:
        print(f"❌ FAIL Launcher Syntax - Error: {e}")
        return False

def test_launcher_imports():
    """Test launcher imports"""
    print("🔍 Testing launcher imports...")
    
    try:
        # Try to import the launcher module
        sys.path.insert(0, '.')
        import launch_bot
        print("✅ PASS Launcher Import - Successfully imported")
        return True
    except Exception as e:
        print(f"❌ FAIL Launcher Import - Import error: {e}")
        traceback.print_exc()
        return False

def test_launcher_functions():
    """Test key launcher functions exist"""
    print("🔍 Testing launcher functions...")
    
    try:
        import launch_bot
        
        required_functions = [
            'print_banner',
            'check_dependencies', 
            'launch_backend',
            'launch_dashboard',
            'main'
        ]
        
        for func_name in required_functions:
            if not hasattr(launch_bot, func_name):
                print(f"❌ FAIL Missing function: {func_name}")
                return False
        
        print("✅ PASS Launcher Functions - All required functions found")
        return True
        
    except Exception as e:
        print(f"❌ FAIL Launcher Functions - Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 LAUNCHER VERIFICATION")
    print("=" * 50)
    
    all_passed = True
    
    all_passed &= test_launcher_syntax()
    all_passed &= test_launcher_imports()
    all_passed &= test_launcher_functions()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL LAUNCHER TESTS PASSED!")
    else:
        print("⚠️ Some launcher tests failed.")
    
    print("=" * 50)
