#!/usr/bin/env python3
"""
Quick bot startup test with shorter timeouts
"""
import sys
import os

# Change to bot directory
bot_dir = r"c:\Users\Hari\Desktop\Crypto bot"
if os.path.exists(bot_dir):
    os.chdir(bot_dir)

# Import and run launcher with testing parameters
import launch_bot

# Override timeouts for testing
def quick_launch():
    """Quick launch for testing"""
    print("🚀 Quick Launch Test...")
    
    # Test backend
    backend = launch_bot.launch_backend()
    if backend:
        print("✅ Backend started successfully")
        
        # Test dashboard  
        dashboard = launch_bot.launch_dashboard()
        if dashboard:
            print("✅ Dashboard started successfully")
            print("🎉 Both services are running!")
            
            # Quick health check
            health = launch_bot.run_system_health_check()
            print(f"📊 Health check: {'✅ Passed' if health else '❌ Failed'}")
            
            return True
        else:
            print("❌ Dashboard failed to start")
            return False
    else:
        print("❌ Backend failed to start")
        return False

if __name__ == "__main__":
    quick_launch()
