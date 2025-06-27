#!/usr/bin/env python3
"""
CRYPTO TRADING BOT LAUNCHER - WINDOWS COMPATIBLE
Enhanced launcher with proper Windows emoji support
"""

import subprocess
import time
import sys
import os
import io
import requests
import webbrowser

# Windows-specific encoding setup
if os.name == 'nt':
    # Set UTF-8 environment
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # Try to enable Windows Terminal UTF-8 support
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleOutputCP(65001)  # UTF-8
        kernel32.SetConsoleCP(65001)  # UTF-8
    except:
        pass
    
    # Wrap stdout/stderr for proper emoji handling
    try:
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'buffer'):
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass

def safe_print(message):
    """Safely print messages with emoji support on Windows"""
    try:
        # Try to print with emojis
        print(f"[INFO] {message}")
        sys.stdout.flush()
    except UnicodeEncodeError:
        # Fallback: Replace emojis with text equivalents
        fallback_msg = message
        emoji_map = {
            "🚀": "[START]",
            "✅": "[OK]",
            "❌": "[ERROR]",
            "⏳": "[WAIT]",
            "🔧": "[CONFIG]",
            "📁": "[FOLDER]",
            "🔍": "[CHECK]",
            "📦": "[INSTALL]",
            "🧪": "[TEST]",
            "🌐": "[WEB]",
            "💎": "[SUCCESS]",
            "🎉": "[READY]",
            "⚡": "[FAST]",
            "🔥": "[HOT]",
            "👋": "[BYE]",
            "🛑": "[STOP]",
            "⚠️": "[WARN]",
            "📊": "[CHART]",
            "💰": "[MONEY]",
            "🎯": "[TARGET]"
        }
        
        for emoji, text in emoji_map.items():
            fallback_msg = fallback_msg.replace(emoji, text)
        
        print(f"[INFO] {fallback_msg}")
        sys.stdout.flush()

def print_banner():
    """Print startup banner with Windows-safe emojis"""
    banner = """
==============================================================
    🚀 CRYPTO TRADING BOT - WINDOWS LAUNCHER 🚀
    📊 Backend + Dashboard + Data Collection 📊
    💎 Full Emoji Support + Windows Compatibility 💎
==============================================================
"""
    safe_print(banner)

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

def start_backend():
    """Start the backend server with Windows compatibility"""
    safe_print("🔧 Starting backend server...")
    
    backend_path = os.path.join(os.getcwd(), "backend")
    if not os.path.exists(backend_path):
        safe_print("❌ ERROR: Backend directory not found")
        return None
    
    # Check if already running
    if check_port(8001):
        safe_print("✅ Backend already running")
        return "RUNNING"
    
    try:
        # Start backend with Windows-compatible encoding
        cmd = [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8001"]
        
        # Windows-specific process creation
        startup_info = None
        creation_flags = 0
        
        if os.name == 'nt':
            startup_info = subprocess.STARTUPINFO()
            startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startup_info.wShowWindow = 1  # SW_NORMAL
            # Use CREATE_NEW_CONSOLE to avoid encoding issues
            creation_flags = subprocess.CREATE_NEW_CONSOLE
        
        safe_print(f"⚡ Running backend command: {' '.join(cmd)}")
        
        # Set environment for UTF-8 support
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONLEGACYWINDOWSFSENCODING'] = '0'
        
        process = subprocess.Popen(
            cmd, 
            cwd=backend_path, 
            startupinfo=startup_info,
            creationflags=creation_flags,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        # Wait for startup
        safe_print("⏳ Waiting for backend to start...")
        for i in range(30):
            time.sleep(2)
            if check_port(8001):
                safe_print("✅ Backend started successfully!")
                return process
            safe_print(f"⏳ Waiting... ({i+1}/30)")
        
        safe_print("❌ ERROR: Backend failed to start")
        return None
        
    except Exception as e:
        safe_print(f"❌ ERROR starting backend: {e}")
        return None

def start_dashboard():
    """Start the dashboard with Windows emoji support"""
    safe_print("🎨 Starting beautiful dashboard...")
    
    dashboard_path = os.path.join(os.getcwd(), "dashboard")
    if not os.path.exists(dashboard_path):
        safe_print("❌ ERROR: Dashboard directory not found")
        return None
    
    # Check if already running
    if check_port(8050):
        safe_print("✅ Dashboard already running")
        return "RUNNING"
    
    try:
        # Use the full-featured dashboard with all tabs and features
        dashboard_files = ['app.py', 'start_dashboard.py', 'start_safe.py', 'start_beautiful.py']
        dashboard_file = None
        
        for file in dashboard_files:
            file_path = os.path.join(dashboard_path, file)
            if os.path.exists(file_path):
                dashboard_file = file
                safe_print(f"💎 Found full-featured dashboard: {file}")
                break
        
        if not dashboard_file:
            safe_print("❌ ERROR: No dashboard file found")
            return None
        
        safe_print(f"💎 Using full-featured dashboard: {dashboard_file}")
        
        # Windows-specific process creation with UTF-8 support
        startup_info = None
        creation_flags = 0
        
        if os.name == 'nt':
            startup_info = subprocess.STARTUPINFO()
            startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startup_info.wShowWindow = 1  # SW_NORMAL
            # Use CREATE_NEW_CONSOLE for emoji support
            creation_flags = subprocess.CREATE_NEW_CONSOLE
        
        # Set environment for full UTF-8 support
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONLEGACYWINDOWSFSENCODING'] = '0'
        
        cmd = [sys.executable, "-u", dashboard_file]
        safe_print(f"⚡ Running command: {' '.join(cmd)}")
        
        process = subprocess.Popen(
            cmd, 
            cwd=dashboard_path, 
            startupinfo=startup_info,
            creationflags=creation_flags,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace',
            bufsize=1,
            universal_newlines=True
        )
        
        # Wait for startup
        safe_print("⏳ Waiting for beautiful dashboard to start...")
        for i in range(45):
            time.sleep(2)
            if check_port(8050):
                safe_print("🎉 Beautiful dashboard started successfully!")
                return process
            
            # Check if process crashed
            if process.poll() is not None:
                stdout, _ = process.communicate()
                safe_print("❌ Dashboard process crashed!")
                safe_print(f"📝 OUTPUT: {stdout}")
                return None
                
            safe_print(f"⏳ Waiting... ({i+1}/45)")
        
        # Timeout
        process.terminate()
        safe_print("❌ ERROR: Dashboard startup timeout")
        return None
        
    except Exception as e:
        safe_print(f"❌ ERROR starting dashboard: {e}")
        return None

def check_data_collection():
    """Check if data collection is running"""
    try:
        response = requests.get("http://localhost:8001/ml/data_collection/stats", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            if stats.get("status") == "success":
                safe_print("🎯 Data collection is running automatically!")
                return True
    except:
        pass
    return False

def open_browser():
    """Open browser to dashboard"""
    time.sleep(3)
    try:
        webbrowser.open("http://localhost:8050")
        safe_print("🌐 Browser opened to beautiful dashboard")
    except:
        safe_print("🌐 Please open http://localhost:8050 manually")

def main():
    """Main launcher function with Windows emoji support"""
    print_banner()
    
    # Change to bot directory
    bot_dir = r"c:\Users\Hari\Desktop\Crypto bot"
    if os.path.exists(bot_dir):
        os.chdir(bot_dir)
        safe_print(f"📁 Working in: {bot_dir}")
    
    # Start backend
    backend = start_backend()
    if not backend:
        safe_print("❌ FAILED: Cannot start without backend")
        return False
    
    # Start dashboard
    dashboard = start_dashboard()
    if not dashboard:
        safe_print("❌ FAILED: Cannot start without dashboard")
        return False
    
    # Check data collection
    time.sleep(3)
    if check_data_collection():
        safe_print("🎯 SUCCESS: Automatic data collection verified!")
    else:
        safe_print("⚠️ WARNING: Data collection status unknown")
    
    # Final verification
    safe_print("🔍 Verifying all services...")
    backend_ok = check_port(8001)
    dashboard_ok = check_port(8050)
    
    if backend_ok and dashboard_ok:
        safe_print("🎉 SUCCESS: All systems operational!")
        
        success_banner = """
==============================================================
    🚀 CRYPTO TRADING BOT READY! 🚀
    
    🌐 Dashboard:  http://localhost:8050
    🔧 Backend:    http://localhost:8001  
    📚 API Docs:   http://localhost:8001/docs
    
    ✨ Features: AI/ML Trading + Auto Data Collection
    💎 Beautiful Emoji-Rich Interface
    🎯 Windows Compatible UTF-8 Support
==============================================================
"""
        safe_print(success_banner)
        
        # Open browser
        open_browser()
        
        # Keep running
        try:
            safe_print("🚀 Bot is running! Press Ctrl+C to exit launcher")
            while True:
                time.sleep(60)
                # Quick health check
                if not check_port(8001) or not check_port(8050):
                    safe_print("⚠️ WARNING: Service health check failed")
        except KeyboardInterrupt:
            safe_print("👋 Launcher stopped. Services continue running.")
        
        return True
    else:
        safe_print("❌ FAILED: System health check failed")
        return False

if __name__ == "__main__":
    main()
