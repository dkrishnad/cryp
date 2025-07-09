#!/usr/bin/env python3
"""
Simple test to verify .dict() calls have been replaced in the codebase.
"""

import os
import re
from pathlib import Path

def check_dict_calls():
    """Check for remaining .dict() calls in Python files."""
    
    project_root = Path(__file__).parent
    print(f"🔍 Scanning Python files in: {project_root}")
    
    python_files = list(project_root.rglob("*.py"))
    print(f"📁 Found {len(python_files)} Python files")
    
    dict_calls = []
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find .dict() calls (not in comments)
            lines = content.split('\n')
            for line_num, line in enumerate(lines, 1):
                stripped = line.strip()
                if '.dict()' in line and not stripped.startswith('#'):
                    dict_calls.append({
                        'file': str(file_path.relative_to(project_root)),
                        'line': line_num,
                        'content': stripped
                    })
                    
        except Exception as e:
            print(f"⚠️  Could not read {file_path}: {e}")
    
    if dict_calls:
        print(f"\n❌ Found {len(dict_calls)} .dict() calls:")
        for call in dict_calls:
            print(f"  📄 {call['file']}:{call['line']}")
            print(f"     {call['content']}")
        return False
    else:
        print("\n✅ No .dict() calls found in codebase!")
        return True

def check_model_dump_usage():
    """Check that .model_dump() is being used instead."""
    
    project_root = Path(__file__).parent
    python_files = list(project_root.rglob("*.py"))
    
    model_dump_count = 0
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            model_dump_count += content.count('.model_dump()')
                    
        except Exception:
            pass
    
    print(f"✅ Found {model_dump_count} .model_dump() calls in codebase")
    return model_dump_count > 0

def main():
    """Main function."""
    
    print("=" * 60)
    print("🔧 PYDANTIC .dict() REPLACEMENT VERIFICATION")
    print("=" * 60)
    
    # Check for .dict() calls
    no_dict_calls = check_dict_calls()
    
    # Check for .model_dump() usage
    has_model_dump = check_model_dump_usage()
    
    print("\n" + "=" * 60)
    if no_dict_calls and has_model_dump:
        print("🎉 SUCCESS! All .dict() calls have been replaced with .model_dump()")
    elif no_dict_calls:
        print("✅ No .dict() calls found, but no .model_dump() calls either")
    else:
        print("❌ FAILED! Some .dict() calls still remain")
    print("=" * 60)
    
    return no_dict_calls

if __name__ == "__main__":
    main()
