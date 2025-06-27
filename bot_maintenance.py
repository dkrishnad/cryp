#!/usr/bin/env python3
"""
🔧 Crypto Trading Bot Maintenance Script
Comprehensive maintenance and health monitoring for your crypto trading bot
"""

import os
import sys
import json
import sqlite3
import requests
import subprocess
import time
import psutil
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import logging

class BotMaintenanceManager:
    def __init__(self):
        self.bot_dir = Path(__file__).parent
        self.db_path = self.bot_dir / "trades.db"
        self.logs_dir = self.bot_dir / "logs"
        self.backups_dir = self.bot_dir / "backups"
        self.reports_dir = self.bot_dir / "maintenance_reports"
        
        # Create directories if they don't exist
        self.logs_dir.mkdir(exist_ok=True)
        self.backups_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # API endpoints
        self.backend_url = "http://localhost:8000"
        self.dashboard_url = "http://localhost:8050"
        
        # Maintenance report
        self.maintenance_report = {
            'timestamp': datetime.now().isoformat(),
            'checks_performed': [],
            'issues_found': [],
            'fixes_applied': [],
            'recommendations': []
        }

    def setup_logging(self):
        """Setup logging for maintenance operations"""
        log_file = self.logs_dir / f"maintenance_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def print_header(self, title):
        """Print formatted header"""
        print("\n" + "=" * 60)
        print(f"🔧 {title}")
        print("=" * 60)

    def print_section(self, title):
        """Print formatted section"""
        print(f"\n📋 {title}")
        print("-" * 40)

    def check_system_resources(self):
        """Check system resources (CPU, Memory, Disk)"""
        self.print_section("SYSTEM RESOURCES CHECK")
        
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            print(f"💻 CPU Usage: {cpu_percent:.1f}%")
            
            # Memory usage
            memory = psutil.virtual_memory()
            print(f"🧠 Memory Usage: {memory.percent:.1f}% ({memory.used / (1024**3):.1f}GB / {memory.total / (1024**3):.1f}GB)")
            
            # Disk usage
            disk = psutil.disk_usage(str(self.bot_dir))
            disk_percent = (disk.used / disk.total) * 100
            print(f"💾 Disk Usage: {disk_percent:.1f}% ({disk.used / (1024**3):.1f}GB / {disk.total / (1024**3):.1f}GB)")
            
            # Check for issues
            issues = []
            if cpu_percent > 80:
                issues.append(f"High CPU usage: {cpu_percent:.1f}%")
            if memory.percent > 85:
                issues.append(f"High memory usage: {memory.percent:.1f}%")
            if disk_percent > 90:
                issues.append(f"Low disk space: {disk_percent:.1f}% used")
            
            if issues:
                self.maintenance_report['issues_found'].extend(issues)
                print("⚠️  Resource Issues Found:")
                for issue in issues:
                    print(f"   • {issue}")
            else:
                print("✅ System resources are healthy")
            
            self.maintenance_report['checks_performed'].append("System Resources")
            
        except Exception as e:
            error_msg = f"Error checking system resources: {str(e)}"
            self.logger.error(error_msg)
            self.maintenance_report['issues_found'].append(error_msg)

    def check_database_health(self):
        """Check database health and perform optimization"""
        self.print_section("DATABASE HEALTH CHECK")
        
        try:
            if not self.db_path.exists():
                print("❌ Database not found - creating new database")
                self.maintenance_report['issues_found'].append("Database file missing")
                return
            
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Check database integrity
            cursor.execute("PRAGMA integrity_check")
            integrity_result = cursor.fetchone()[0]
            
            if integrity_result == "ok":
                print("✅ Database integrity: OK")
            else:
                print(f"❌ Database integrity issues: {integrity_result}")
                self.maintenance_report['issues_found'].append(f"Database integrity: {integrity_result}")
            
            # Get database size
            db_size = self.db_path.stat().st_size / (1024 * 1024)  # MB
            print(f"📊 Database size: {db_size:.2f} MB")
            
            # Check table statistics
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            print(f"📋 Tables found: {len(tables)}")
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"   • {table_name}: {count} records")
            
            # Vacuum database for optimization
            print("🔧 Optimizing database...")
            cursor.execute("VACUUM")
            print("✅ Database optimization complete")
            self.maintenance_report['fixes_applied'].append("Database vacuum optimization")
            
            conn.close()
            self.maintenance_report['checks_performed'].append("Database Health")
            
        except Exception as e:
            error_msg = f"Error checking database: {str(e)}"
            self.logger.error(error_msg)
            self.maintenance_report['issues_found'].append(error_msg)

    def check_api_endpoints(self):
        """Check if API endpoints are responding"""
        self.print_section("API ENDPOINTS CHECK")
        
        endpoints_to_check = [
            (f"{self.backend_url}/health", "Backend Health"),
            (f"{self.backend_url}/model/predict", "ML Prediction"),
            (f"{self.backend_url}/model/crypto_transfer/status", "Transfer Learning"),
            (f"{self.dashboard_url}", "Dashboard")
        ]
        
        for url, name in endpoints_to_check:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ {name}: Responding (Status: {response.status_code})")
                else:
                    print(f"⚠️  {name}: Status {response.status_code}")
                    self.maintenance_report['issues_found'].append(f"{name} returned status {response.status_code}")
            except requests.exceptions.ConnectionError:
                print(f"❌ {name}: Not responding (Connection refused)")
                self.maintenance_report['issues_found'].append(f"{name} not responding")
            except requests.exceptions.Timeout:
                print(f"❌ {name}: Timeout")
                self.maintenance_report['issues_found'].append(f"{name} timeout")
            except Exception as e:
                print(f"❌ {name}: Error - {str(e)}")
                self.maintenance_report['issues_found'].append(f"{name} error: {str(e)}")
        
        self.maintenance_report['checks_performed'].append("API Endpoints")

    def check_model_files(self):
        """Check ML model files and their integrity"""
        self.print_section("ML MODEL FILES CHECK")
        
        model_files = [
            "kaia_rf_model.joblib",
            "model_analytics.json"
        ]
        
        for model_file in model_files:
            file_path = self.bot_dir / model_file
            if file_path.exists():
                size_mb = file_path.stat().st_size / (1024 * 1024)
                print(f"✅ {model_file}: Found ({size_mb:.2f} MB)")
            else:
                print(f"❌ {model_file}: Missing")
                self.maintenance_report['issues_found'].append(f"Missing model file: {model_file}")
        
        # Check for Python dependencies
        try:
            import joblib
            import pandas as pd
            import numpy as np
            import sklearn
            print("✅ Core ML dependencies: Available")
        except ImportError as e:
            error_msg = f"Missing ML dependency: {str(e)}"
            print(f"❌ {error_msg}")
            self.maintenance_report['issues_found'].append(error_msg)
        
        self.maintenance_report['checks_performed'].append("ML Model Files")

    def cleanup_old_files(self, days_old=30):
        """Clean up old log files and temporary files"""
        self.print_section("FILE CLEANUP")
        
        try:
            cutoff_date = datetime.now() - timedelta(days=days_old)
            cleaned_files = 0
            cleaned_size = 0
            
            # Clean log files
            if self.logs_dir.exists():
                for log_file in self.logs_dir.glob("*.log"):
                    if datetime.fromtimestamp(log_file.stat().st_mtime) < cutoff_date:
                        file_size = log_file.stat().st_size
                        log_file.unlink()
                        cleaned_files += 1
                        cleaned_size += file_size
            
            # Clean temporary files
            temp_patterns = ["*.tmp", "*.temp", "__pycache__", "*.pyc"]
            for pattern in temp_patterns:
                for temp_file in self.bot_dir.rglob(pattern):
                    if temp_file.is_file() and datetime.fromtimestamp(temp_file.stat().st_mtime) < cutoff_date:
                        file_size = temp_file.stat().st_size
                        temp_file.unlink()
                        cleaned_files += 1
                        cleaned_size += file_size
                    elif temp_file.is_dir() and pattern == "__pycache__":
                        shutil.rmtree(temp_file, ignore_errors=True)
                        cleaned_files += 1
            
            print(f"🧹 Cleaned {cleaned_files} files ({cleaned_size / (1024*1024):.2f} MB freed)")
            self.maintenance_report['fixes_applied'].append(f"Cleaned {cleaned_files} old files")
            self.maintenance_report['checks_performed'].append("File Cleanup")
            
        except Exception as e:
            error_msg = f"Error during cleanup: {str(e)}"
            self.logger.error(error_msg)
            self.maintenance_report['issues_found'].append(error_msg)

    def backup_database(self):
        """Create database backup"""
        self.print_section("DATABASE BACKUP")
        
        try:
            if not self.db_path.exists():
                print("❌ No database to backup")
                return
            
            backup_name = f"trades_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            backup_path = self.backups_dir / backup_name
            
            shutil.copy2(self.db_path, backup_path)
            backup_size = backup_path.stat().st_size / (1024 * 1024)
            
            print(f"✅ Database backed up: {backup_name} ({backup_size:.2f} MB)")
            
            # Keep only last 10 backups
            backups = sorted(self.backups_dir.glob("trades_backup_*.db"), key=lambda x: x.stat().st_mtime, reverse=True)
            for old_backup in backups[10:]:
                old_backup.unlink()
                print(f"🗑️  Removed old backup: {old_backup.name}")
            
            self.maintenance_report['fixes_applied'].append(f"Created database backup: {backup_name}")
            self.maintenance_report['checks_performed'].append("Database Backup")
            
        except Exception as e:
            error_msg = f"Error creating backup: {str(e)}"
            self.logger.error(error_msg)
            self.maintenance_report['issues_found'].append(error_msg)

    def check_trading_performance(self):
        """Check recent trading performance metrics"""
        self.print_section("TRADING PERFORMANCE CHECK")
        
        try:
            if not self.db_path.exists():
                print("❌ No database found for performance analysis")
                return
            
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Check if trades table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='trades'")
            if not cursor.fetchone():
                print("❌ No trades table found")
                conn.close()
                return
            
            # Get recent trades (last 7 days)
            week_ago = (datetime.now() - timedelta(days=7)).isoformat()
            cursor.execute("""
                SELECT COUNT(*), AVG(profit_percentage), SUM(profit_percentage)
                FROM trades 
                WHERE timestamp > ?
            """, (week_ago,))
            
            result = cursor.fetchone()
            if result and result[0] > 0:
                trade_count, avg_profit, total_profit = result
                print(f"📊 Trades (last 7 days): {trade_count}")
                print(f"📈 Average profit: {avg_profit:.2f}%")
                print(f"💰 Total profit: {total_profit:.2f}%")
                
                if avg_profit < 0:
                    self.maintenance_report['issues_found'].append(f"Negative average profit: {avg_profit:.2f}%")
                    self.maintenance_report['recommendations'].append("Review trading strategy - negative performance detected")
            else:
                print("📊 No trades found in the last 7 days")
                self.maintenance_report['recommendations'].append("No recent trading activity - consider checking auto-trading settings")
            
            conn.close()
            self.maintenance_report['checks_performed'].append("Trading Performance")
            
        except Exception as e:
            error_msg = f"Error checking trading performance: {str(e)}"
            self.logger.error(error_msg)
            self.maintenance_report['issues_found'].append(error_msg)

    def generate_recommendations(self):
        """Generate maintenance recommendations"""
        self.print_section("MAINTENANCE RECOMMENDATIONS")
        
        # Add general recommendations based on issues found
        if len(self.maintenance_report['issues_found']) == 0:
            self.maintenance_report['recommendations'].append("System is running optimally - no issues detected")
            print("✅ System is running optimally")
        else:
            print(f"⚠️  Found {len(self.maintenance_report['issues_found'])} issues")
            
        # Specific recommendations
        recommendations = [
            "🔄 Run this maintenance script weekly for optimal performance",
            "📊 Monitor trading performance regularly through the dashboard",
            "💾 Ensure adequate disk space (>10GB free recommended)",
            "🔒 Keep database backups in a secure location",
            "📱 Set up alerts for critical system issues",
            "🔧 Update dependencies monthly using pip install -r requirements.txt --upgrade"
        ]
        
        for rec in recommendations:
            if rec not in self.maintenance_report['recommendations']:
                self.maintenance_report['recommendations'].append(rec)
                print(rec)

    def save_maintenance_report(self):
        """Save maintenance report to file"""
        report_file = self.reports_dir / f"maintenance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w') as f:
            json.dump(self.maintenance_report, f, indent=2)
        
        print(f"\n📋 Maintenance report saved: {report_file.name}")

    def run_full_maintenance(self):
        """Run complete maintenance routine"""
        self.print_header("CRYPTO BOT MAINTENANCE - FULL SYSTEM CHECK")
        
        print(f"🕒 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Bot Directory: {self.bot_dir}")
        
        # Run all maintenance checks
        self.check_system_resources()
        self.check_database_health()
        self.check_api_endpoints()
        self.check_model_files()
        self.check_trading_performance()
        self.cleanup_old_files()
        self.backup_database()
        self.generate_recommendations()
        
        # Summary
        self.print_section("MAINTENANCE SUMMARY")
        print(f"✅ Checks performed: {len(self.maintenance_report['checks_performed'])}")
        print(f"⚠️  Issues found: {len(self.maintenance_report['issues_found'])}")
        print(f"🔧 Fixes applied: {len(self.maintenance_report['fixes_applied'])}")
        print(f"💡 Recommendations: {len(self.maintenance_report['recommendations'])}")
        
        if self.maintenance_report['issues_found']:
            print("\n❗ ISSUES FOUND:")
            for i, issue in enumerate(self.maintenance_report['issues_found'], 1):
                print(f"   {i}. {issue}")
        
        if self.maintenance_report['fixes_applied']:
            print("\n🔧 FIXES APPLIED:")
            for i, fix in enumerate(self.maintenance_report['fixes_applied'], 1):
                print(f"   {i}. {fix}")
        
        self.save_maintenance_report()
        
        print(f"\n🏁 Maintenance completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

    def run_quick_health_check(self):
        """Run quick health check"""
        self.print_header("QUICK HEALTH CHECK")
        
        self.check_system_resources()
        self.check_api_endpoints()
        
        if len(self.maintenance_report['issues_found']) == 0:
            print("\n✅ Quick health check: ALL SYSTEMS HEALTHY")
        else:
            print(f"\n⚠️  Quick health check: {len(self.maintenance_report['issues_found'])} issues found")
            for issue in self.maintenance_report['issues_found']:
                print(f"   • {issue}")

def main():
    """Main function with maintenance options"""
    print("🔧 Crypto Trading Bot Maintenance Script")
    print("=" * 50)
    print("1. Full Maintenance (recommended weekly)")
    print("2. Quick Health Check")
    print("3. Database Backup Only")
    print("4. File Cleanup Only")
    print("5. Exit")
    
    try:
        choice = input("\nSelect option (1-5): ").strip()
        
        maintenance_manager = BotMaintenanceManager()
        
        if choice == "1":
            maintenance_manager.run_full_maintenance()
        elif choice == "2":
            maintenance_manager.run_quick_health_check()
        elif choice == "3":
            maintenance_manager.backup_database()
        elif choice == "4":
            maintenance_manager.cleanup_old_files()
        elif choice == "5":
            print("👋 Exiting maintenance script")
            return
        else:
            print("❌ Invalid option selected")
    
    except KeyboardInterrupt:
        print("\n\n🛑 Maintenance interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during maintenance: {str(e)}")

if __name__ == "__main__":
    main()
