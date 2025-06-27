import requests
import time

# Simulate dashboard interactions and check terminal output
print("🔧 TESTING DASHBOARD FRONTEND CALLBACKS")
print("=" * 50)

print("\n📋 INSTRUCTIONS:")
print("1. Keep this terminal open")
print("2. Open the dashboard: http://127.0.0.1:8050")
print("3. Try these actions and watch for debug output:")
print("")
print("   🔹 Change symbol in sidebar dropdown (select BTC)")
print("   🔹 Click 'Open Long' button")
print("   🔹 Click 'Open Short' button")
print("")
print("4. Check the dashboard terminal for debug messages like:")
print("   [DASH DEBUG] sync_selected_symbol called...")
print("   [DASH DEBUG] update_live_price_cache called...")
print("   [DASH DEBUG] Trade action button clicked...")
print("")
print("If you see NO debug messages, then callbacks aren't triggering.")
print("If you see debug messages but no changes, then there's a display issue.")
print("")
print("🔍 WHAT TO REPORT:")
print("- Do you see debug messages in the dashboard terminal?")
print("- What happens when you click buttons? Any error messages?") 
print("- Does the symbol dropdown have options?")
print("- Does the live price show '--' or a number?")
print("- Does the symbol selection change anything on screen?")
print("")
print("💡 The backend is working perfectly, so the issue is frontend-specific.")

# Test if dashboard is accessible
try:
    import requests
    resp = requests.get("http://127.0.0.1:8050")
    print(f"\n✅ Dashboard is accessible: {resp.status_code}")
except:
    print(f"\n❌ Dashboard is not accessible")

print("\n" + "=" * 50)
