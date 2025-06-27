#!/usr/bin/env python3
"""
Script to fix Unicode characters in main.py that cause Windows encoding issues
"""

import re

def fix_unicode_chars():
    with open('main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace problematic Unicode characters
    unicode_replacements = {
        '🔧': '[DEBUG]',
        '📁': '[DEBUG]',
        '📦': '[DEBUG]', 
        '✅': '[OK]',
        '🌟': '[INFO]',
        '📍': '[INFO]',
        '❌': '[ERROR]',
        '💡': '[INFO]',
        '💰': '[INFO]',
        '🚀': '[INFO]',
        '📊': '[INFO]',
        '⚡': '[INFO]',
        '🎯': '[INFO]',
        '📈': '[INFO]',
        '🔄': '[INFO]',
        '🤖': '[INFO]',
        '🛠️': '[DEBUG]',
        '📋': '[INFO]',
        '🔍': '[DEBUG]',
        '⚠️': '[WARN]',
        '📜': '[INFO]',
        '🎮': '[INFO]',
        '🌟': '[INFO]',
        '🔔': '[INFO]',
        '🔕': '[INFO]',
        '📢': '[INFO]',
        '📣': '[INFO]',
        '📯': '[INFO]',
        '🔊': '[INFO]',
        '🔇': '[INFO]',
        '🔈': '[INFO]',
        '🔉': '[INFO]',
        # Handle any other remaining Unicode characters
        '💼': '[INFO]',
        '🎨': '[INFO]',
        '🎭': '[INFO]',
        '🎪': '[INFO]',
        '🎵': '[INFO]',
        '🎸': '[INFO]',
        '🎤': '[INFO]',
        '🎹': '[INFO]',
        '🎺': '[INFO]',
        '🎻': '[INFO]',
        '🥁': '[INFO]',
        '🎷': '[INFO]',
    }
    
    # Also handle these specific unicode sequences
    content = re.sub(r'[^\x00-\x7F]+', '', content)  # Remove all non-ASCII
    
    # Now re-add our simple replacements
    for unicode_char, replacement in unicode_replacements.items():
        content = content.replace(unicode_char, replacement)
    
    # Handle any remaining problematic characters in print statements
    content = re.sub(r'print\("([^"]*)[^\x00-\x7F]+([^"]*)"\)', r'print("[INFO] \1\2")', content)
    
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Unicode characters fixed in main.py")

if __name__ == "__main__":
    fix_unicode_chars()
