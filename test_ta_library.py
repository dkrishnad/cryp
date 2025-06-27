#!/usr/bin/env python3
"""
Quick test to check the ta library API
"""
import sys
import os

print("🔧 Testing TA library API...")

try:
    import ta
    print("✅ TA library imported successfully!")
    
    # Check what's available in ta library
    print("\n📋 Available in ta library:")
    for attr in dir(ta):
        if not attr.startswith('_'):
            print(f"  - {attr}")
    
    # Try to access momentum
    if hasattr(ta, 'momentum'):
        print("\n✅ ta.momentum available")
        momentum_attrs = [attr for attr in dir(ta.momentum) if not attr.startswith('_')]
        print(f"  Available: {momentum_attrs[:5]}...")  # Show first 5
    else:
        print("\n❌ ta.momentum not available")
    
    # Check main functions
    main_functions = [func for func in dir(ta) if callable(getattr(ta, func)) and not func.startswith('_')]
    print(f"\n📋 Main functions: {main_functions[:10]}...")
    
except ImportError as e:
    print(f"❌ TA library not available: {e}")
except Exception as e:
    print(f"❌ Error testing TA library: {e}")

print("\n🎯 Test complete!")
