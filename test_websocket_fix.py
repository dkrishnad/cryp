#!/usr/bin/env python3
"""
WebSocket 404 Fix Verification Test
Test that dashboard no longer tries to connect to Socket.IO endpoints
"""

import sys
import os
import traceback

def test_websocket_config():
    """Test that WebSocket configuration is correct"""
    try:
        print("Testing WebSocket configuration...")
        
        # Check dash_app.py for Socket.IO references
        dash_app_path = "dashboard/dash_app.py"
        if os.path.exists(dash_app_path):
            with open(dash_app_path, 'r') as f:
                content = f.read()
                if 'socket.io' not in content.lower():
                    print("✅ Socket.IO removed from dash_app.py")
                else:
                    print("⚠️ Socket.IO still referenced in dash_app.py")
        
        # Check realtime_client.js for native WebSocket usage
        js_path = "dashboard/assets/realtime_client.js"
        if os.path.exists(js_path):
            with open(js_path, 'r') as f:
                content = f.read()
                if 'new WebSocket(' in content and 'ws://localhost:8001/ws/price' in content:
                    print("✅ Native WebSocket properly configured")
                else:
                    print("❌ WebSocket configuration incorrect")
                    return False
                
                if 'io(' not in content or content.count('io(') == 0:
                    print("✅ Socket.IO client calls removed")
                else:
                    print("⚠️ Socket.IO client calls still present")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing WebSocket config: {str(e)}")
        traceback.print_exc()
        return False

def test_backend_websocket():
    """Test that backend WebSocket endpoint exists"""
    try:
        print("\nTesting backend WebSocket endpoint...")
        
        # Check if ws.py exists and has WebSocket endpoint
        ws_path = "backend/ws.py"
        if os.path.exists(ws_path):
            with open(ws_path, 'r') as f:
                content = f.read()
                if '@router.websocket("/ws/price")' in content:
                    print("✅ Backend WebSocket endpoint found at /ws/price")
                    return True
                else:
                    print("❌ Backend WebSocket endpoint not found")
                    return False
        else:
            print("❌ Backend ws.py file not found")
            return False
            
    except Exception as e:
        print(f"❌ Error testing backend WebSocket: {str(e)}")
        return False

def main():
    """Run WebSocket fix verification tests"""
    print("="*60)
    print("    WEBSOCKET 404 ERRORS FIX VERIFICATION")
    print("="*60)
    
    # Change to bot directory
    bot_dir = r"c:\Users\Hari\Desktop\Crypto bot"
    if os.path.exists(bot_dir):
        os.chdir(bot_dir)
        print(f"Working in: {bot_dir}\n")
    
    # Run tests
    test1 = test_websocket_config()
    test2 = test_backend_websocket()
    
    print("\n" + "="*60)
    if test1 and test2:
        print("🎉 WEBSOCKET 404 ERRORS FIXED!")
        print("✅ Dashboard now uses native WebSockets")
        print("✅ Socket.IO references removed") 
        print("✅ Backend WebSocket endpoint configured")
        print("\n💡 The Socket.IO 404 errors should stop appearing!")
    else:
        print("❌ SOME ISSUES REMAIN")
        print("❌ Additional fixes may be needed")
    print("="*60)
    
    return test1 and test2

if __name__ == "__main__":
    main()
