#!/usr/bin/env python3
"""
CALLBACK TRIGGER TEST
Check if callbacks are actually being triggered when buttons are clicked
"""

import time
import os
from datetime import datetime

def monitor_debug_log():
    """Monitor the debug log for new entries"""
    log_file = "dashboard_debug.log"
    
    if not os.path.exists(log_file):
        print("❌ Debug log file not found")
        return
    
    print("🔍 MONITORING DEBUG LOG FOR BUTTON CLICKS")
    print("="*60)
    print("📝 Instructions:")
    print("   1. Keep this script running")
    print("   2. Go to the dashboard in your browser")
    print("   3. Click any button (e.g., 'Test ML', 'Analytics', etc.)")
    print("   4. Watch for new log entries below")
    print("   5. Press Ctrl+C to stop monitoring")
    print("\n📊 Starting log monitoring...")
    print("="*60)
    
    # Get initial file size
    initial_size = os.path.getsize(log_file)
    print(f"📈 Initial log size: {initial_size} bytes")
    
    try:
        while True:
            current_size = os.path.getsize(log_file)
            
            if current_size > initial_size:
                # Read new content
                with open(log_file, 'r', encoding='utf-8') as f:
                    f.seek(initial_size)
                    new_content = f.read()
                
                if new_content.strip():
                    print(f"\n🔥 NEW LOG ACTIVITY:")
                    print("-" * 40)
                    for line in new_content.strip().split('\n'):
                        if line.strip():
                            print(f"   {line}")
                    print("-" * 40)
                
                initial_size = current_size
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Monitoring stopped")
        print("📊 Final log size:", os.path.getsize(log_file), "bytes")

if __name__ == "__main__":
    monitor_debug_log()
