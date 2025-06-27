#!/usr/bin/env python3
"""
Fix Unicode Emoji Encoding Issues in Dashboard Callbacks
Replaces Unicode emojis with ASCII equivalents to prevent Windows encoding errors
"""

import re

def fix_unicode_emojis():
    file_path = r"c:\Users\Hari\Desktop\Crypto bot\dashboard\callbacks.py"
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define replacements for Unicode emojis
    emoji_replacements = {
        '✅': '[OK]',
        '❌': '[ERROR]',
        '⚡': '[FAST]', 
        '🎯': '[TARGET]',
        '📧': '[EMAIL]',
        '🚀': '[ROCKET]',
        '📊': '[CHART]',
        '🔧': '[TOOL]',
        '🔍': '[SEARCH]',
        '💡': '[IDEA]',
        '⭐': '[STAR]',
        '🎉': '[PARTY]',
        '🔥': '[FIRE]',
        '💰': '[MONEY]',
        '📈': '[UP]',
        '📉': '[DOWN]',
        '⚠️': '[WARNING]',
        '🔴': '[RED]',
        '🟢': '[GREEN]',
        '🟡': '[YELLOW]',
        '🔵': '[BLUE]',
        '⭕': '[CIRCLE]',
        '❗': '[EXCLAMATION]',
        '❓': '[QUESTION]',
        '💭': '[THOUGHT]',
        '💻': '[COMPUTER]',
        '🎮': '[GAME]',
        '📱': '[PHONE]',
        '🧠': '[BRAIN]',  # Brain emoji causing the current error
        '🔒': '[LOCK]',   # Lock emoji
        '🔄': '[REFRESH]', # Refresh emoji
        '🔮': '[CRYSTAL]', # Crystal ball emoji
        'ℹ️': '[INFO]',    # Info emoji with modifier
        'ℹ': '[INFO]',     # Info emoji without modifier
        '✕': '[X]',       # X mark
        '✓': '[CHECK]',   # Check mark
        '🛑': '[STOP]',   # Stop sign
        '🧪': '[TEST]',   # Test tube
        '🤖': '[ROBOT]',  # Robot
        '⏸️': '[PAUSE]',   # Pause button with modifier
        '⏸': '[PAUSE]',    # Pause button without modifier
    }
    
    # Apply replacements
    original_content = content
    for emoji, replacement in emoji_replacements.items():
        content = content.replace(emoji, replacement)
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Count changes
    changes = sum(1 for emoji in emoji_replacements.keys() if emoji in original_content)
    
    print(f"[SUCCESS] Fixed {changes} types of Unicode emojis in dashboard/callbacks.py")
    print("[INFO] Replaced with ASCII equivalents to prevent encoding errors")
    print("[READY] Dashboard should now start without Unicode encoding issues")

if __name__ == "__main__":
    fix_unicode_emojis()
