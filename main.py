#!/usr/bin/env python3
"""
Main Application Entry Point
Crypto Trading Bot with Dashboard and Backend Integration
"""

import sys
import os
import threading
import time
import logging
from pathlib import Path

# Add project directories to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "dashboardtest"))
sys.path.insert(0, str(project_root / "backendtest"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def start_backend_server():
    """Start the backend API server"""
    try:
        import uvicorn
        from backendtest.app import app as backend_app
        logger.info("🚀 Starting Backend API Server on http://localhost:5000")
        uvicorn.run(backend_app, host='0.0.0.0', port=5000, log_level="info")
    except ImportError as e:
        logger.error(f"❌ Could not import backend app: {e}")
        logger.info("⚠️  Backend server not available - running in dashboard-only mode")
    except Exception as e:
        logger.error(f"❌ Backend server error: {e}")

def start_dashboard_server():
    """Start the dashboard server"""
    try:
        from dashboardtest.app import app as dashboard_app
        logger.info("🎛️  Starting Dashboard Server on http://localhost:8050")
        dashboard_app.run(host='0.0.0.0', port=8050, debug=False)
    except ImportError as e:
        logger.error(f"❌ Could not import dashboard app: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Dashboard server error: {e}")
        raise

def start_data_collection():
    """Start data collection system"""
    try:
        from backendtest.data_collection import DataCollector
        logger.info("📊 Starting Data Collection System")
        
        collector = DataCollector()
        collector.start_collection()
        
        return collector
    except ImportError as e:
        logger.warning(f"⚠️  Data collection not available: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ Data collection error: {e}")
        return None

def main():
    """Main application entry point"""
    logger.info("🚀 Starting Crypto Trading Bot Application")
    logger.info("=" * 60)
    
    # Start data collection in background
    data_collector = start_data_collection()
    
    # Start backend server in background thread
    backend_thread = threading.Thread(target=start_backend_server, daemon=True)
    backend_thread.start()
    
    # Give backend time to start
    time.sleep(2)
    
    try:
        # Start dashboard server (main thread)
        logger.info("🎛️  Starting main dashboard...")
        start_dashboard_server()
        
    except KeyboardInterrupt:
        logger.info("⏹️  Shutting down application...")
        
        # Stop data collection
        if data_collector:
            data_collector.stop_collection()
            
        logger.info("✅ Application stopped")
        
    except Exception as e:
        logger.error(f"❌ Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
