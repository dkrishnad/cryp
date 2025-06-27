#!/usr/bin/env python3
"""
Diagnostic script to test the dashboard hybrid learning functionality
"""

import requests
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

def test_browser_interaction():
    """Test the dashboard in a real browser"""
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("http://localhost:8050")
        
        print("🌐 Dashboard loaded in browser")
        
        # Wait for the page to load
        wait = WebDriverWait(driver, 10)
        
        # Click on the Hybrid Learning tab
        hybrid_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Hybrid Learning')]")))
        hybrid_tab.click()
        print("✅ Clicked on Hybrid Learning tab")
        
        # Wait for the content to load
        time.sleep(2)
        
        # Check if the hybrid prediction display element exists
        try:
            prediction_display = driver.find_element(By.ID, "hybrid-prediction-display")
            print("✅ Found hybrid-prediction-display element")
            print(f"📄 Current content: {prediction_display.text[:200]}...")
        except Exception as e:
            print(f"❌ Could not find hybrid-prediction-display element: {e}")
        
        # Check if the symbol dropdown exists
        try:
            symbol_dropdown = driver.find_element(By.ID, "hybrid-symbol-selector")
            print("✅ Found hybrid-symbol-selector dropdown")
        except Exception as e:
            print(f"❌ Could not find hybrid-symbol-selector dropdown: {e}")
        
        # Check if the update button exists
        try:
            update_button = driver.find_element(By.ID, "hybrid-predict-btn")
            print("✅ Found hybrid-predict-btn button")
            
            # Try clicking the button
            update_button.click()
            print("✅ Clicked update prediction button")
            
            # Wait and check for changes
            time.sleep(3)
            prediction_display = driver.find_element(By.ID, "hybrid-prediction-display")
            print(f"📄 Content after button click: {prediction_display.text[:200]}...")
            
        except Exception as e:
            print(f"❌ Could not find or click hybrid-predict-btn button: {e}")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ Browser test failed: {e}")
        return False

def test_dashboard_without_browser():
    """Test dashboard accessibility without browser automation"""
    
    print("🌐 Testing Dashboard Accessibility")
    print("-" * 40)
    
    try:
        resp = requests.get("http://localhost:8050", timeout=10)
        if resp.status_code == 200:
            print("✅ Dashboard is accessible")
            
            # Check if the response contains hybrid learning elements
            content = resp.text
            
            if "hybrid-learning-tab-content" in content:
                print("✅ Hybrid learning tab content found in HTML")
            else:
                print("❌ Hybrid learning tab content NOT found in HTML")
            
            if "hybrid-prediction-display" in content:
                print("✅ Hybrid prediction display element found in HTML")
            else:
                print("❌ Hybrid prediction display element NOT found in HTML")
            
            if "hybrid-symbol-selector" in content:
                print("✅ Hybrid symbol selector found in HTML")
            else:
                print("❌ Hybrid symbol selector NOT found in HTML")
                
            return True
        else:
            print(f"❌ Dashboard returned status: {resp.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Could not access dashboard: {e}")
        return False

def test_callback_triggers():
    """Test various trigger scenarios"""
    
    print("🔄 Testing Callback Trigger Scenarios")
    print("-" * 40)
    
    scenarios = [
        {"symbol": "btcusdt", "n_clicks": None, "n_intervals": 0, "desc": "Page load"},
        {"symbol": "btcusdt", "n_clicks": 1, "n_intervals": 0, "desc": "Button click"},
        {"symbol": "kaiausdt", "n_clicks": None, "n_intervals": 1, "desc": "Symbol change"},
        {"symbol": "ethusdt", "n_clicks": 1, "n_intervals": 2, "desc": "Both triggers"},
    ]
    
    for scenario in scenarios:
        print(f"\n📋 Scenario: {scenario['desc']}")
        url = f"http://localhost:8001/ml/hybrid/predict?symbol={scenario['symbol']}"
        
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                result = resp.json()
                prediction = result.get("prediction", {})
                ensemble_pred = prediction.get("ensemble_prediction", 0)
                ensemble_conf = prediction.get("ensemble_confidence", 0)
                
                print(f"   ✅ API Response: {'BUY' if ensemble_pred == 1 else 'SELL'} ({ensemble_conf:.2%})")
            else:
                print(f"   ❌ API Error: {resp.status_code}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")

def main():
    print("🚀 Hybrid Learning Dashboard Diagnostic")
    print("=" * 60)
    
    # Test 1: Dashboard accessibility
    dashboard_ok = test_dashboard_without_browser()
    
    # Test 2: API endpoints
    test_callback_triggers()
    
    # Test 3: Browser automation (optional, requires ChromeDriver)
    try:
        print("\n🤖 Attempting browser automation test...")
        browser_ok = test_browser_interaction()
    except Exception as e:
        print(f"⚠ Browser test skipped (ChromeDriver not available): {e}")
        browser_ok = None
    
    # Summary
    print("\n📋 Diagnostic Summary")
    print("=" * 30)
    print(f"Dashboard accessible: {'✅' if dashboard_ok else '❌'}")
    print(f"Browser test: {'✅' if browser_ok else '❌' if browser_ok is False else '⚠ Skipped'}")
    
    if dashboard_ok:
        print("\n💡 Recommendations:")
        print("1. Check browser console for JavaScript errors")
        print("2. Verify the Dash callback is properly registered")
        print("3. Try manually refreshing the Hybrid Learning tab")
        print("4. Check if other tabs work correctly for comparison")

if __name__ == "__main__":
    main()
