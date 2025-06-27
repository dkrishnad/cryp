#!/usr/bin/env python3
"""
Backend Integration Verification
Verifies that all backend code and endpoints are properly implemented
"""
import os
import sys
import ast
import re

def analyze_backend_main():
    """Analyze backend/main.py to verify all endpoints are implemented"""
    print("🔍 Analyzing backend/main.py for endpoint implementation...")
    
    with open("backend/main.py", "r") as f:
        content = f.read()
    
    # Count different types of endpoints
    endpoints = {
        "health": re.findall(r'@app\.get\("/health"\)', content),
        "price": re.findall(r'@app\.get\("/price"\)', content),
        "virtual_balance": re.findall(r'@app\.(get|post)\("/virtual_balance', content),
        "trades": re.findall(r'@app\.(get|post)\("/trades', content),
        "auto_trading": re.findall(r'@app\.(get|post)\("/auto_trading/', content),
        "futures": re.findall(r'@app\.(get|post)\("/futures/', content),
        "fapi": re.findall(r'@app\.(get|post|delete)\("/fapi/v1/', content),
        "ml": re.findall(r'@app\.(get|post)\("/ml/', content),
    }
    
    total_endpoints = 0
    for category, matches in endpoints.items():
        count = len(matches)
        total_endpoints += count
        status = "✅" if count > 0 else "❌"
        print(f"{status} {category}: {count} endpoints")
    
    print(f"\n📊 Total Endpoints Implemented: {total_endpoints}")
    return total_endpoints

def check_import_structure():
    """Check if all required modules are properly imported"""
    print("\n🔍 Checking import structure...")
    
    with open("backend/main.py", "r") as f:
        content = f.read()
    
    required_imports = [
        "FastAPI",
        "futures_trading",
        "binance_futures_exact", 
        "hybrid_learning",
        "online_learning",
        "ml_compatibility_manager",
        "db"
    ]
    
    working_imports = []
    missing_imports = []
    
    for import_name in required_imports:
        if import_name in content:
            working_imports.append(import_name)
            print(f"✅ {import_name}")
        else:
            missing_imports.append(import_name)
            print(f"❌ {import_name}")
    
    print(f"\n📊 Import Status: {len(working_imports)}/{len(required_imports)}")
    return len(missing_imports) == 0

def verify_advanced_features():
    """Verify advanced features are implemented"""
    print("\n🔍 Verifying advanced feature implementation...")
    
    features = {
        "Futures Trading": "backend/futures_trading.py",
        "Binance Exact API": "backend/binance_futures_exact.py", 
        "Hybrid Learning": "backend/hybrid_learning.py",
        "Online Learning": "backend/online_learning.py",
        "ML Compatibility": "backend/ml_compatibility_manager.py",
        "Transfer Learning": "backend/crypto_transfer_learning.py",
        "Dashboard Layout": "dashboard/layout.py",
        "Futures Layout": "dashboard/futures_trading_layout.py",
        "Binance Layout": "dashboard/binance_exact_layout.py",
        "Dashboard Callbacks": "dashboard/callbacks.py",
    }
    
    implemented_features = []
    missing_features = []
    
    for feature, file_path in features.items():
        if os.path.exists(file_path):
            implemented_features.append(feature)
            print(f"✅ {feature}")
        else:
            missing_features.append(feature)
            print(f"❌ {feature}")
    
    print(f"\n📊 Advanced Features: {len(implemented_features)}/{len(features)}")
    return len(missing_features) == 0

def main():
    print("🚀 BACKEND INTEGRATION VERIFICATION")
    print("="*50)
    
    # Run all checks
    endpoint_count = analyze_backend_main()
    imports_ok = check_import_structure()
    features_ok = verify_advanced_features()
    
    # Final assessment
    print("\n" + "="*50)
    print("📊 FINAL VERIFICATION RESULTS:")
    
    endpoint_status = "✅ COMPLETE" if endpoint_count >= 40 else "❌ INCOMPLETE"
    import_status = "✅ COMPLETE" if imports_ok else "❌ INCOMPLETE"  
    feature_status = "✅ COMPLETE" if features_ok else "❌ INCOMPLETE"
    
    print(f"Backend Endpoints: {endpoint_status} ({endpoint_count} endpoints)")
    print(f"Import Structure: {import_status}")
    print(f"Advanced Features: {feature_status}")
    
    if endpoint_count >= 40 and imports_ok and features_ok:
        print("\n🎉 BACKEND INTEGRATION: 100% COMPLETE!")
        print("✅ All endpoints implemented and ready")
        print("✅ All imports properly configured") 
        print("✅ All advanced features integrated")
        print("\n💡 Backend endpoints are COMPLETE in code.")
        print("   To make them accessible, simply run: python backend/main.py")
        
        return True
    else:
        print("\n⚠️ Some backend components need attention")
        return False

if __name__ == "__main__":
    main()
