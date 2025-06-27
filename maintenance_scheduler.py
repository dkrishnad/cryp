#!/usr/bin/env python3
"""
🕐 Crypto Bot Maintenance Scheduler
Automated scheduler for regular bot maintenance
"""

import schedule
import time
import subprocess
import sys
from datetime import datetime
from pathlib import Path

class MaintenanceScheduler:
    def __init__(self):
        self.bot_dir = Path(__file__).parent
        self.maintenance_script = self.bot_dir / "bot_maintenance.py"
        self.log_file = self.bot_dir / "logs" / "scheduler.log"
        
        # Create logs directory if it doesn't exist
        self.log_file.parent.mkdir(exist_ok=True)

    def log_message(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Print to console
        print(log_entry.strip())
        
        # Write to log file
        with open(self.log_file, 'a') as f:
            f.write(log_entry)

    def run_maintenance(self, maintenance_type="full"):
        """Run maintenance script"""
        self.log_message(f"🔧 Starting {maintenance_type} maintenance...")
        
        try:
            if maintenance_type == "full":
                # Simulate selecting option 1 (Full Maintenance)
                process = subprocess.Popen(
                    [sys.executable, str(self.maintenance_script)],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate(input="1\n")
                
            elif maintenance_type == "quick":
                # Simulate selecting option 2 (Quick Health Check)
                process = subprocess.Popen(
                    [sys.executable, str(self.maintenance_script)],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate(input="2\n")
                
            elif maintenance_type == "backup":
                # Simulate selecting option 3 (Database Backup Only)
                process = subprocess.Popen(
                    [sys.executable, str(self.maintenance_script)],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate(input="3\n")
            
            if process.returncode == 0:
                self.log_message(f"✅ {maintenance_type} maintenance completed successfully")
            else:
                self.log_message(f"❌ {maintenance_type} maintenance failed with return code {process.returncode}")
                if stderr:
                    self.log_message(f"Error output: {stderr}")
                    
        except Exception as e:
            self.log_message(f"❌ Error running {maintenance_type} maintenance: {str(e)}")

    def run_full_maintenance(self):
        """Scheduled full maintenance"""
        self.run_maintenance("full")

    def run_quick_check(self):
        """Scheduled quick health check"""
        self.run_maintenance("quick")

    def run_backup(self):
        """Scheduled database backup"""
        self.run_maintenance("backup")

    def start_scheduler(self):
        """Start the maintenance scheduler"""
        self.log_message("🚀 Starting Crypto Bot Maintenance Scheduler")
        
        # Schedule maintenance tasks
        schedule.every().sunday.at("02:00").do(self.run_full_maintenance)  # Weekly full maintenance
        schedule.every().day.at("06:00").do(self.run_quick_check)          # Daily quick check
        schedule.every().day.at("12:00").do(self.run_backup)               # Daily backup
        schedule.every().day.at("18:00").do(self.run_quick_check)          # Evening quick check
        
        self.log_message("📅 Maintenance schedule configured:")
        self.log_message("   • Full maintenance: Every Sunday at 02:00")
        self.log_message("   • Quick health check: Daily at 06:00 and 18:00")
        self.log_message("   • Database backup: Daily at 12:00")
        
        print("\n🔧 Crypto Bot Maintenance Scheduler Running")
        print("=" * 50)
        print("📅 SCHEDULE:")
        print("   • Full maintenance: Every Sunday at 02:00")
        print("   • Quick health check: Daily at 06:00 and 18:00")
        print("   • Database backup: Daily at 12:00")
        print("\n🛑 Press Ctrl+C to stop the scheduler")
        print("=" * 50)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            self.log_message("🛑 Maintenance scheduler stopped by user")
            print("\n🛑 Maintenance scheduler stopped")

def main():
    """Main function"""
    print("🕐 Crypto Bot Maintenance Scheduler")
    print("=" * 40)
    print("1. Start Automated Scheduler")
    print("2. Run One-Time Full Maintenance")
    print("3. Run One-Time Quick Check")
    print("4. Run One-Time Backup")
    print("5. Exit")
    
    try:
        choice = input("\nSelect option (1-5): ").strip()
        
        scheduler = MaintenanceScheduler()
        
        if choice == "1":
            scheduler.start_scheduler()
        elif choice == "2":
            scheduler.run_full_maintenance()
        elif choice == "3":
            scheduler.run_quick_check()
        elif choice == "4":
            scheduler.run_backup()
        elif choice == "5":
            print("👋 Exiting scheduler")
            return
        else:
            print("❌ Invalid option selected")
    
    except KeyboardInterrupt:
        print("\n\n🛑 Scheduler interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
