#!/usr/bin/env python3
"""
FIXED CRYPTO TRADING BOT LAUNCHER
Auto-installs dependencies and provides better error reporting
"""

import subprocess
import time
import sys
import os
import requests
import webbrowser

def print_status(message):
    """Enhanced status printing with emojis"""
    print(f"[INFO] {message}")

def print_error(message):
    """Error printing"""
    print(f"[ERROR] {message}")

def print_success(message):
    """Success printing"""
    print(f"[SUCCESS] {message}")

def print_banner():
    """Print startup banner"""
    print("\n" + "="*60)
    print("    🚀 CRYPTO TRADING BOT - FIXED LAUNCHER")
    print("    🔧 Auto-fix Dependencies + Detailed Diagnostics")
    print("="*60 + "\n")

def install_dependencies():
    """Install missing dependencies"""
    print_status("🔍 Checking and installing dependencies...")
    
    required_packages = [
        'uvicorn[standard]',
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
    
    missing = []
    for package in required_packages:
        try:
            # Test import
            import_name = package.replace('-', '_').replace('[standard]', '')
            __import__(import_name)
            print_status(f"✅ {package}")
        except ImportError:
            print_status(f"❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print_status(f"📦 Installing {len(missing)} missing packages...")
        for package in missing:
            try:
                print_status(f"Installing {package}...")
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package, "--upgrade"
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print_success(f"✅ {package} installed")
            except Exception as e:
                print_error(f"❌ Failed to install {package}: {e}")
                return False
    else:
        print_success("🎉 All dependencies are installed!")
    
    return True

def check_port(port):
    """Check if port is responding"""
    try:
        addresses = ["http://127.0.0.1", "http://localhost"]
        for addr in addresses:
            try:
                url = f"{addr}:{port}/health" if port == 8001 else f"{addr}:{port}"
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    return True
            except:
                continue
        return False
    except:
        return False

def test_imports():
    """Test if critical imports work"""
    print_status("🧪 Testing critical imports...")
    
    try:
        import uvicorn
        print_status("✅ uvicorn")
    except ImportError as e:
        print_error(f"❌ uvicorn: {e}")
        return False
    
    try:
        import dash
        print_status("✅ dash")
    except ImportError as e:
        print_error(f"❌ dash: {e}")
        return False
    
    try:
        import dash_bootstrap_components
        print_status("✅ dash_bootstrap_components")
    except ImportError as e:
        print_error(f"❌ dash_bootstrap_components: {e}")
        return False
    
    return True

def start_backend():
    """Start the backend server with detailed error reporting"""
    print_status("🔧 Starting backend server...")
    
    backend_path = os.path.join(os.getcwd(), "backend")
    if not os.path.exists(backend_path):
        print_error("Backend directory not found!")
        return None
    
    # Check if already running
    if check_port(8001):
        print_success("Backend already running")
        return "RUNNING"
    
    try:
        # Test if we can import the backend first
        sys.path.insert(0, backend_path)
        try:
            import main
            print_status("✅ Backend main.py can be imported")
        except Exception as e:
            print_error(f"❌ Cannot import backend main.py: {e}")
            return None
        finally:
            if backend_path in sys.path:
                sys.path.remove(backend_path)
        
        # Start backend
        cmd = [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8001"]
        print_status(f"Running: {' '.join(cmd)}")
        
        process = subprocess.Popen(
            cmd, 
            cwd=backend_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Wait for startup with real-time output
        print_status("⏳ Waiting for backend to start...")
        for i in range(30):
            time.sleep(2)
            if check_port(8001):
                print_success("🎉 Backend started successfully!")
                return process
            
            # Check if process crashed
            if process.poll() is not None:
                stdout, _ = process.communicate()
                print_error("Backend process crashed!")
                print_error(f"Output: {stdout}")
                return None
                
            print_status(f"⏳ Waiting... ({i+1}/30)")
        
        print_error("Backend startup timeout")
        process.terminate()
        return None
        
    except Exception as e:
        print_error(f"Error starting backend: {e}")
        return None

def start_dashboard():
    """Start the dashboard with detailed error reporting"""
    print_status("🎨 Starting beautiful dashboard...")
    
    dashboard_path = os.path.join(os.getcwd(), "dashboard")
    if not os.path.exists(dashboard_path):
        print_error("Dashboard directory not found!")
        return None
    
    # Check if already running
    if check_port(8050):
        print_success("Dashboard already running")
        return "RUNNING"
    
    try:
        # Test dashboard imports first
        sys.path.insert(0, dashboard_path)
        try:
            import layout
            print_status("✅ Dashboard layout.py can be imported")
            import callbacks
            print_status("✅ Dashboard callbacks.py can be imported")
        except Exception as e:
            print_error(f"❌ Cannot import dashboard modules: {e}")
            return None
        finally:
            if dashboard_path in sys.path:
                sys.path.remove(dashboard_path)
        
        # Find dashboard file
        dashboard_files = ['start_beautiful.py', 'start_safe.py', 'start_minimal.py']
        dashboard_file = None
        
        for file in dashboard_files:
            file_path = os.path.join(dashboard_path, file)
            if os.path.exists(file_path):
                dashboard_file = file
                print_status(f"Found dashboard file: {file}")
                break
        
        if not dashboard_file:
            print_error("No dashboard file found!")
            return None
        
        # Start dashboard
        cmd = [sys.executable, "-u", dashboard_file]
        print_status(f"Running: {' '.join(cmd)}")
        
        process = subprocess.Popen(
            cmd, 
            cwd=dashboard_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Wait for startup
        print_status("⏳ Waiting for dashboard to start...")
        for i in range(45):
            time.sleep(2)
            if check_port(8050):
                print_success("🎉 Dashboard started successfully!")
                return process
            
            # Check if process crashed
            if process.poll() is not None:
                stdout, _ = process.communicate()
                print_error("Dashboard process crashed!")
                print_error(f"Output: {stdout}")
                return None
                
            print_status(f"⏳ Waiting... ({i+1}/45)")
        
        print_error("Dashboard startup timeout")
        process.terminate()
        return None
        
    except Exception as e:
        print_error(f"Error starting dashboard: {e}")
        return None

def main():
    """Main launcher function with fixes"""
    print_banner()
    
    # Change to bot directory
    bot_dir = r"c:\Users\Hari\Desktop\Crypto bot"
    if os.path.exists(bot_dir):
        os.chdir(bot_dir)
        print_status(f"📁 Working in: {bot_dir}")
    
    # Step 1: Install dependencies
    if not install_dependencies():
        print_error("❌ Failed to install dependencies")
        return False
    
    # Step 2: Test imports
    if not test_imports():
        print_error("❌ Import tests failed")
        return False
    
    # Step 3: Start backend
    backend = start_backend()
    if not backend:
        print_error("❌ Cannot start without backend")
        return False
    
    # Step 4: Start dashboard
    dashboard = start_dashboard()
    if not dashboard:
        print_error("❌ Cannot start without dashboard")
        return False
    
    # Final verification
    print_status("🔍 Verifying all services...")
    backend_ok = check_port(8001)
    dashboard_ok = check_port(8050)
    
    if backend_ok and dashboard_ok:
        print_success("🎉 ALL SYSTEMS OPERATIONAL!")
        print("\n" + "="*60)
        print("    🚀 CRYPTO TRADING BOT READY!")
        print("")
        print("    📊 Dashboard:  http://localhost:8050")
        print("    🔧 Backend:    http://localhost:8001")
        print("    📖 API Docs:   http://localhost:8001/docs")
        print("")
        print("    ✨ Features: Beautiful Emoji Dashboard + AI Trading")
        print("="*60)
        
        # Open browser
        time.sleep(3)
        try:
            webbrowser.open("http://localhost:8050")
            print_success("🌐 Browser opened to dashboard")
        except:
            print_status("Please open http://localhost:8050 manually")
        
        return True
    else:
        print_error("❌ System health check failed")
        print_error(f"Backend OK: {backend_ok}, Dashboard OK: {dashboard_ok}")
        return False

if __name__ == "__main__":
    main()
