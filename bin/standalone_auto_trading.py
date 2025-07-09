#!/usr/bin/env python3
"""
Standalone Auto Trading Executor
Runs independently and executes auto trading via backend API
"""
import requests
import time
import json
from datetime import datetime

API_URL = "http://localhost:8001"

def check_and_execute_auto_trading():
    """Check auto trading status and execute if conditions are met"""
    try:
        # 1. Check if auto trading is enabled
        status_resp = requests.get(f"{API_URL}/auto_trading/status")
        if status_resp.status_code != 200:
            print(f"❌ Could not get auto trading status: {status_resp.status_code}")
            return
        
        status_data = status_resp.json()
        if not status_data.get("status") == "success":
            print(f"❌ Auto trading status error: {status_data}")
            return
            
        auto_trading_state = status_data.get("auto_trading", {})
        enabled = auto_trading_state.get("enabled", False)
        
        if not enabled:
            print("⏸️ Auto trading is disabled")
            return
            
        print("✅ Auto trading is enabled")
        
        # 2. Get current signal
        signal_resp = requests.get(f"{API_URL}/auto_trading/current_signal")
        if signal_resp.status_code != 200:
            print(f"❌ Could not get current signal: {signal_resp.status_code}")
            return
            
        signal_data = signal_resp.json()
        if not signal_data.get("status") == "success":
            print(f"❌ Signal error: {signal_data}")
            return
            
        signal_info = signal_data.get("signal", {})
        signal_type = signal_info.get("signal")
        confidence = signal_info.get("confidence", 0)
        
        print(f"📊 Current signal: {signal_type}, confidence: {confidence:.2f}")
        
        # 3. Check if confidence meets threshold (same logic as dashboard)
        confidence_threshold = auto_trading_state.get("confidence_threshold", 0.7)
        
        if confidence >= confidence_threshold and signal_type in ["BUY", "SELL"]:
            print(f"🎯 High confidence {signal_type} signal detected! Executing trade...")
            
            # 4. Execute the trade
            execute_resp = requests.post(f"{API_URL}/auto_trading/execute_signal")
            if execute_resp.status_code == 200:
                execute_data = execute_resp.json()
                if execute_data.get("status") == "success":
                    trade = execute_data.get("trade", {})
                    print(f"✅ Trade executed successfully: {trade}")
                else:
                    print(f"❌ Trade execution failed: {execute_data}")
            else:
                print(f"❌ Trade execution request failed: {execute_resp.status_code}")
        else:
            print(f"⏳ Signal confidence {confidence:.2f} below threshold {confidence_threshold}")
            
    except Exception as e:
        print(f"❌ Error in auto trading check: {e}")

def main():
    """Main auto trading loop"""
    print("🚀 Starting standalone auto trading executor...")
    print(f"   Backend: {API_URL}")
    print(f"   Check interval: 5 seconds")
    print(f"   Time: {datetime.now()}")
    print()
    
    # Test backend connectivity
    try:
        health_resp = requests.get(f"{API_URL}/health", timeout=5)
        if health_resp.status_code == 200:
            print("✅ Backend is accessible")
        else:
            print(f"❌ Backend health check failed: {health_resp.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return
    
    print("🔄 Starting auto trading monitoring loop...")
    print("   Press Ctrl+C to stop")
    print()
    
    try:
        iteration = 0
        while True:
            iteration += 1
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Auto trading check #{iteration}")
            
            check_and_execute_auto_trading()
            print()
            
            time.sleep(5)  # Check every 5 seconds
            
    except KeyboardInterrupt:
        print("\n🛑 Auto trading executor stopped by user")

if __name__ == "__main__":
    main()
