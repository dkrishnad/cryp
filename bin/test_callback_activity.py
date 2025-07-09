#!/usr/bin/env python3
"""
Simple test to check if the auto trading interval callback is working at all.
"""

import requests
import time

def check_callback_activity():
    print("🔍 Checking Auto Trading Callback Activity...")
    print("=" * 50)
    
    # Monitor dashboard logs for auto trading callback activity
    print("⏰ Waiting 15 seconds to see if auto trading callback is triggered...")
    print("   Looking for: '🔄 Auto trading status callback triggered'")
    print("   If you don't see this message, the callback is not running.")
    print()
    
    time.sleep(15)
    
    print("✅ Check complete. If you saw '🔄 Auto trading status callback triggered' messages,")
    print("   the callback is working. If not, there's an issue with the callback registration")
    print("   or the interval component is not active.")

if __name__ == "__main__":
    check_callback_activity()
