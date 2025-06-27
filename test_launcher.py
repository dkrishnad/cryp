#!/usr/bin/env python3
"""
Quick launcher test to validate functionality
"""
import subprocess
import sys
import os
import time

def test_launcher():
    """Test the launcher functionality"""
    print("🧪 Testing Crypto Bot Launcher...")
    
    # Change to bot directory
    bot_dir = r"c:\Users\Hari\Desktop\Crypto bot"
    if os.path.exists(bot_dir):
        os.chdir(bot_dir)
        print(f"✅ Working directory: {bot_dir}")
    
    # Test import
    try:
        import launch_bot
        print("✅ Launcher imports successfully")
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test dependency check
    try:
        result = launch_bot.check_dependencies()
        print(f"✅ Dependency check: {'Passed' if result else 'Failed'}")
    except Exception as e:
        print(f"❌ Dependency check error: {e}")
    
    # Test port checking
    try:
        backend_running = launch_bot.check_port(8001, "Backend")
        dashboard_running = launch_bot.check_port(8050, "Dashboard")
        print(f"📊 Backend (8001): {'Running' if backend_running else 'Available'}")
        print(f"📊 Dashboard (8050): {'Running' if dashboard_running else 'Available'}")
    except Exception as e:
        print(f"❌ Port check error: {e}")
    
    print("🎯 Launcher test completed!")
    print("💡 To start the bot, run: python launch_bot.py")
    
    return True

if __name__ == "__main__":
    test_launcher()
