#!/usr/bin/env python3
"""
🚀 Crypto Bot Service Manager
Manages bot services (backend, dashboard) and runs maintenance
"""

import subprocess
import sys
import time
import requests
from pathlib import Path
import signal
import atexit

class BotServiceManager:
    def __init__(self):
        self.bot_dir = Path(__file__).parent
        self.backend_process = None
        self.dashboard_process = None
        
        # Register cleanup handlers
        atexit.register(self.cleanup)
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signum, frame):
        """Handle system signals"""
        print(f"\n🛑 Received signal {signum}, shutting down...")
        self.cleanup()
        sys.exit(0)

    def cleanup(self):
        """Clean up processes"""
        if self.backend_process:
            print("🔄 Stopping backend...")
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
        
        if self.dashboard_process:
            print("🔄 Stopping dashboard...")
            self.dashboard_process.terminate()
            try:
                self.dashboard_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.dashboard_process.kill()

    def check_service(self, url, name, timeout=5):
        """Check if a service is responding"""
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                print(f"✅ {name}: Running and responding")
                return True
            else:
                print(f"⚠️  {name}: Running but status {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print(f"❌ {name}: Not responding")
            return False
        except Exception as e:
            print(f"❌ {name}: Error - {str(e)}")
            return False

    def start_backend(self):
        """Start the backend service"""
        print("🚀 Starting backend service...")
        
        backend_path = self.bot_dir / "backend" / "main.py"
        if not backend_path.exists():
            print(f"❌ Backend file not found: {backend_path}")
            return False
        
        try:
            self.backend_process = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"],
                cwd=str(self.bot_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait a moment for startup
            time.sleep(3)
            
            # Check if it's running
            if self.check_service("http://localhost:8000/health", "Backend"):
                return True
            else:
                print("⚠️  Backend started but not responding yet...")
                return True  # May need more time to start
                
        except Exception as e:
            print(f"❌ Error starting backend: {str(e)}")
            return False

    def start_dashboard(self):
        """Start the dashboard service"""
        print("🚀 Starting dashboard service...")
        
        dashboard_path = self.bot_dir / "dashboard" / "app.py"
        if not dashboard_path.exists():
            print(f"❌ Dashboard file not found: {dashboard_path}")
            return False
        
        try:
            self.dashboard_process = subprocess.Popen(
                [sys.executable, str(dashboard_path)],
                cwd=str(self.bot_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait a moment for startup
            time.sleep(5)
            
            # Check if it's running
            if self.check_service("http://localhost:8050", "Dashboard"):
                return True
            else:
                print("⚠️  Dashboard started but not responding yet...")
                return True  # May need more time to start
                
        except Exception as e:
            print(f"❌ Error starting dashboard: {str(e)}")
            return False

    def check_all_services(self):
        """Check status of all services"""
        print("🔍 Checking service status...")
        print("-" * 40)
        
        services = [
            ("http://localhost:8000/health", "Backend"),
            ("http://localhost:8050", "Dashboard"),
            ("http://localhost:8000/model/predict", "ML Prediction"),
            ("http://localhost:8000/model/crypto_transfer/status", "Transfer Learning")
        ]
        
        running_services = 0
        for url, name in services:
            if self.check_service(url, name):
                running_services += 1
        
        print(f"\n📊 Services running: {running_services}/{len(services)}")
        return running_services == len(services)

    def run_maintenance(self):
        """Run maintenance check"""
        print("🔧 Running maintenance check...")
        
        try:
            result = subprocess.run(
                [sys.executable, "bot_maintenance.py"],
                input="2\n",  # Quick health check
                text=True,
                capture_output=True,
                cwd=str(self.bot_dir)
            )
            
            if result.returncode == 0:
                print("✅ Maintenance check completed")
            else:
                print("⚠️  Maintenance check had issues")
                
        except Exception as e:
            print(f"❌ Error running maintenance: {str(e)}")

    def start_all_services(self):
        """Start all bot services"""
        print("🚀 CRYPTO BOT SERVICE MANAGER")
        print("=" * 50)
        print("🔄 Starting all services...\n")
        
        # Start backend
        backend_ok = self.start_backend()
        
        # Start dashboard
        dashboard_ok = self.start_dashboard()
        
        if backend_ok and dashboard_ok:
            print("\n✅ All services started!")
            print("🌐 Backend: http://localhost:8000")
            print("📊 Dashboard: http://localhost:8050")
        else:
            print("\n⚠️  Some services may not have started correctly")
        
        # Wait for services to fully initialize
        print("\n⏳ Waiting for services to initialize...")
        time.sleep(10)
        
        # Check service status
        print("\n" + "=" * 50)
        all_running = self.check_all_services()
        
        if all_running:
            print("\n🎉 ALL SERVICES ARE RUNNING PERFECTLY!")
        else:
            print("\n⚠️  Some services need attention")
        
        return all_running

    def monitor_services(self):
        """Monitor services and keep them running"""
        print("\n🔍 MONITORING MODE")
        print("=" * 50)
        print("📊 Monitoring services every 60 seconds...")
        print("🛑 Press Ctrl+C to stop monitoring\n")
        
        try:
            while True:
                print(f"⏰ {time.strftime('%H:%M:%S')} - Checking services...")
                
                # Check if processes are still running
                if self.backend_process and self.backend_process.poll() is not None:
                    print("❌ Backend process died, restarting...")
                    self.start_backend()
                
                if self.dashboard_process and self.dashboard_process.poll() is not None:
                    print("❌ Dashboard process died, restarting...")
                    self.start_dashboard()
                
                # Check service health
                self.check_all_services()
                
                print("💤 Sleeping for 60 seconds...\n")
                time.sleep(60)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")

def main():
    """Main function"""
    print("🚀 Crypto Bot Service Manager")
    print("=" * 40)
    print("1. Start All Services")
    print("2. Check Service Status")
    print("3. Start Services + Monitor")
    print("4. Run Maintenance Only")
    print("5. Exit")
    
    try:
        choice = input("\nSelect option (1-5): ").strip()
        
        manager = BotServiceManager()
        
        if choice == "1":
            manager.start_all_services()
            input("\n📌 Press Enter to stop services...")
            
        elif choice == "2":
            manager.check_all_services()
            
        elif choice == "3":
            if manager.start_all_services():
                manager.monitor_services()
            
        elif choice == "4":
            manager.run_maintenance()
            
        elif choice == "5":
            print("👋 Exiting service manager")
            return
              else:
            print("❌ Invalid option selected")
    
    except KeyboardInterrupt:
        print("\n\n🛑 Service manager interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    finally:
        # Cleanup will be called automatically
        pass

if __name__ == "__main__":
    main()
