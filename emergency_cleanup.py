#!/usr/bin/env python3
"""
EMERGENCY CALLBACK CLEANUP
Remove all duplicate callbacks that are causing conflicts
"""

import re

def clean_duplicate_callbacks():
    """Remove duplicate callbacks from callbacks.py"""
    print("🚨 EMERGENCY CLEANUP: Removing duplicate callbacks...")
    
    with open('dashboard/callbacks.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Track callback signatures we've seen
    seen_callbacks = set()
    clean_lines = []
    skip_until = None
    removed_count = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this line starts a callback
        if line.strip().startswith('@app.callback'):
            # Get the output pattern from this callback
            callback_block = []
            j = i
            
            # Collect the callback signature
            while j < len(lines):
                callback_block.append(lines[j])
                if lines[j].strip().startswith('def '):
                    break
                j += 1
            
            # Extract outputs to create a signature
            callback_text = '\n'.join(callback_block)
            output_matches = re.findall(r'Output\([\'\"](.*?)[\'\"]', callback_text)
            
            if output_matches:
                # Create signature from outputs
                signature = tuple(sorted(output_matches))
                
                # Check if we've seen this signature before
                if signature in seen_callbacks:
                    # Skip this duplicate callback
                    print(f"Removing duplicate callback for: {output_matches}")
                    removed_count += 1
                    
                    # Skip until we find the next callback or end
                    while i < len(lines):
                        if i + 1 < len(lines) and (lines[i + 1].strip().startswith('@app.callback') or 
                                                  lines[i + 1].strip().startswith('# ---')):
                            break
                        i += 1
                    continue
                else:
                    # First time seeing this signature
                    seen_callbacks.add(signature)
        
        clean_lines.append(line)
        i += 1
    
    # Write the cleaned content
    cleaned_content = '\n'.join(clean_lines)
    with open('dashboard/callbacks.py', 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    print(f"✅ Removed {removed_count} duplicate callbacks")
    return removed_count

def main():
    print("🚨 EMERGENCY DASHBOARD CLEANUP")
    print("=" * 50)
    
    removed = clean_duplicate_callbacks()
    
    print(f"\n✅ Cleanup complete! Removed {removed} duplicates")
    print("\nNow testing dashboard...")
    
    # Test if dashboard can start
    import subprocess
    import time
    
    try:
        # Try to import callbacks to check for syntax errors
        import sys
        sys.path.append('dashboard')
        
        print("Testing callback imports...")
        # This will fail if there are syntax errors
        result = subprocess.run(['python', '-c', 'import dashboard.callbacks'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Callbacks import successfully!")
        else:
            print(f"❌ Import error: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    main()
