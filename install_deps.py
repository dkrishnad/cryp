#!/usr/bin/env python3
"""
Check and install missing dependencies
"""
import subprocess
import sys

required_packages = [
    'uvicorn',
    'fastapi',
    'dash',
    'dash-bootstrap-components',
    'plotly',
    'pandas',
    'numpy',
    'requests',
    'python-binance',
    'ccxt',
    'ta',
    'scikit-learn'
]

def check_and_install():
    print("🔍 Checking required packages...")
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n📦 Found {len(missing)} missing packages")
        print("Installing missing packages...")
        
        for package in missing:
            try:
                print(f"Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} installed")
            except Exception as e:
                print(f"❌ Failed to install {package}: {e}")
    else:
        print("\n🎉 All required packages are installed!")

if __name__ == "__main__":
    check_and_install()
