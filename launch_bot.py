#!/usr/bin/env python3
"""
CRYPTO TRADING BOT LAUNCHER - SIMPLIFIED
Automatic startup for backend and dashboard with data collection
"""

import subprocess
import time
import sys
import os
import requests
import webbrowser

def print_status(message):
    """Simple status printing"""
    print(f"[INFO] {message}")

def print_banner():
    """Print startup banner"""
    print("\n" + "="*60)
    print("    CRYPTO TRADING BOT - AUTO LAUNCHER")
    print("    Backend + Dashboard + Data Collection")
    print("="*60 + "\n")

def check_port(port):
    """Check if port is responding"""
    try:
        # Try multiple addresses for better compatibility
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

def start_backend():
    """Start the backend server"""
    print_status("Starting backend server...")
    
    backend_path = os.path.join(os.getcwd(), "backend")
    if not os.path.exists(backend_path):
        print_status("ERROR: Backend directory not found")
        return None
    
    # Check if already running
    if check_port(8001):
        print_status("Backend already running")
        return "RUNNING"
    
    try:
        # Start backend
        cmd = [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8001"]
        
        # Show console window on Windows for debugging
        startup_info = None
        if os.name == 'nt':
            startup_info = subprocess.STARTUPINFO()
            startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startup_info.wShowWindow = 1  # SW_NORMAL = 1
        
        print_status(f"Running backend command: {' '.join(cmd)}")
        process = subprocess.Popen(
            cmd, 
            cwd=backend_path, 
            startupinfo=startup_info,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Wait for startup
        print_status("Waiting for backend to start...")
        for i in range(30):
            time.sleep(2)
            if check_port(8001):
                print_status("Backend started successfully!")
                return process
            print_status(f"Waiting... ({i+1}/30)")
        
        print_status("ERROR: Backend failed to start")
        return None
        
    except Exception as e:
        print_status(f"ERROR starting backend: {e}")
        return None

def start_dashboard():
    """Start the dashboard"""
    print_status("Starting dashboard...")
    
    dashboard_path = os.path.join(os.getcwd(), "dashboard")
    if not os.path.exists(dashboard_path):
        print_status("ERROR: Dashboard directory not found")
        return None
    
    # Check if already running
    if check_port(8050):
        print_status("Dashboard already running")
        return "RUNNING"
    
    try:
        # Find dashboard file - prioritize beautiful emoji-rich version
        dashboard_files = ['start_beautiful.py', 'start_safe.py', 'start_minimal.py', 'start_dashboard.py', 'dash_app.py', 'app.py']
        dashboard_file = None
        
        for file in dashboard_files:
            file_path = os.path.join(dashboard_path, file)
            if os.path.exists(file_path):
                dashboard_file = file
                print_status(f"Found dashboard file: {file}")
                break
        
        if not dashboard_file:
            print_status("ERROR: No dashboard file found")
            return None
        
        # Start dashboard with visible output for debugging
        startup_info = None
        if os.name == 'nt':
            startup_info = subprocess.STARTUPINFO()
            # Don't hide window to see errors
            startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startup_info.wShowWindow = 1  # SW_NORMAL = 1
        
        # Use python -u for unbuffered output to see errors immediately
        cmd = [sys.executable, "-u", dashboard_file]
        print_status(f"Running command: {' '.join(cmd)}")
        process = subprocess.Popen(
            cmd, 
            cwd=dashboard_path, 
            startupinfo=startup_info,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Combine stderr with stdout
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Wait for startup with better feedback
        print_status("Waiting for dashboard to start...")
        for i in range(45):  # Increased timeout
            time.sleep(2)
            if check_port(8050):
                print_status("Dashboard started successfully!")
                return process
            
            # Check if process crashed
            if process.poll() is not None:
                # Process has terminated, get output
                stdout, _ = process.communicate()
                print_status(f"Dashboard process crashed!")
                print_status(f"OUTPUT: {stdout}")
                return None
                
            # Show real-time output if available
            if process.stdout and process.stdout.readable():
                import select
                if hasattr(select, 'select'):  # Unix-like systems
                    ready, _, _ = select.select([process.stdout], [], [], 0)
                    if ready:
                        line = process.stdout.readline()
                        if line:
                            print_status(f"Dashboard: {line.strip()}")
                
            print_status(f"Waiting... ({i+1}/45)")
        
        # Timeout - kill process and report
        process.terminate()
        stdout, _ = process.communicate(timeout=5)
        print_status("ERROR: Dashboard startup timeout")
        print_status(f"Final OUTPUT: {stdout}")
        return None
        
    except Exception as e:
        print_status(f"ERROR starting dashboard: {e}")
        return None

def check_data_collection():
    """Check if data collection is running"""
    try:
        response = requests.get("http://localhost:8001/ml/data_collection/stats", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            if stats.get("status") == "success":
                print_status("Data collection is running automatically!")
                return True
    except:
        pass
    return False

def open_browser():
    """Open browser to dashboard"""
    time.sleep(3)
    try:
        webbrowser.open("http://localhost:8050")
        print_status("Browser opened to dashboard")
    except:
        print_status("Please open http://localhost:8050 manually")

def main():
    """Main launcher function"""
    print_banner()
    
    # Change to bot directory
    bot_dir = r"c:\Users\Hari\Desktop\Crypto bot"
    if os.path.exists(bot_dir):
        os.chdir(bot_dir)
        print_status(f"Working in: {bot_dir}")
    
    # Start backend
    backend = start_backend()
    if not backend:
        print_status("FAILED: Cannot start without backend")
        return False
    
    # Start dashboard
    dashboard = start_dashboard()
    if not dashboard:
        print_status("FAILED: Cannot start without dashboard")
        return False
    
    # Check data collection
    time.sleep(3)
    if check_data_collection():
        print_status("SUCCESS: Automatic data collection verified!")
    else:
        print_status("WARNING: Data collection status unknown")
    
    # Final verification
    print_status("Verifying all services...")
    backend_ok = check_port(8001)
    dashboard_ok = check_port(8050)
    
    if backend_ok and dashboard_ok:
        print_status("SUCCESS: All systems operational!")
        print("\n" + "="*60)
        print("    CRYPTO TRADING BOT READY!")
        print("")
        print("    Dashboard:  http://localhost:8050")
        print("    Backend:    http://localhost:8001")
        print("    API Docs:   http://localhost:8001/docs")
        print("")
        print("    Features: AI/ML Trading + Auto Data Collection")
        print("="*60)
        
        # Open browser
        open_browser()
        
        # Keep running
        try:
            print_status("Bot is running! Press Ctrl+C to exit launcher")
            while True:
                time.sleep(60)
                # Quick health check
                if not check_port(8001) or not check_port(8050):
                    print_status("WARNING: Service health check failed")
        except KeyboardInterrupt:
            print_status("Launcher stopped. Services continue running.")
        
        return True
    else:
        print_status("FAILED: System health check failed")
        return False

if __name__ == "__main__":
    main()
