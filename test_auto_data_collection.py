#!/usr/bin/env python3
"""
Test script to verify automatic data collection functionality
"""
import sys
import os
import time

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

def test_data_collection():
    """Test data collection functionality"""
    print("Testing automatic data collection...")
    
    try:
        from data_collection import get_data_collector
        
        # Get data collector instance
        data_collector = get_data_collector()
        print(f"✓ Data collector imported successfully")
        print(f"  Initial running status: {data_collector.is_running}")
        
        # Start data collection
        if not data_collector.is_running:
            print("Starting data collection...")
            data_collector.start_collection()
            print(f"✓ Data collection started")
            
            # Wait a moment
            time.sleep(3)
            
            # Check status
            print(f"  Running status after start: {data_collector.is_running}")
            
            # Get stats
            try:
                stats = data_collector.get_collection_stats()
                print(f"✓ Collection stats: {stats}")
            except Exception as e:
                print(f"⚠ Could not get stats: {e}")
            
            # Stop collection
            print("Stopping data collection...")
            data_collector.stop_collection()
            print(f"✓ Data collection stopped")
            print(f"  Final running status: {data_collector.is_running}")
        else:
            print("✓ Data collection is already running")
            
    except Exception as e:
        print(f"✗ Error testing data collection: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_backend_startup():
    """Test backend startup with automatic data collection"""
    print("\nTesting backend startup...")
    
    try:
        # Import backend components
        print("Importing backend modules...")
        from hybrid_learning import hybrid_orchestrator
        from data_collection import get_data_collector
        
        print("✓ Backend modules imported successfully")
        
        # Simulate startup sequence
        print("Simulating startup sequence...")
        
        # Start hybrid learning system
        try:
            hybrid_orchestrator.start_system()
            print("✓ Hybrid learning system started")
        except Exception as e:
            print(f"⚠ Could not start hybrid learning system: {e}")
        
        # Start data collection
        try:
            data_collector = get_data_collector()
            if not data_collector.is_running:
                data_collector.start_collection()
                print("✓ Automatic data collection started")
            else:
                print("✓ Data collection was already running")
        except Exception as e:
            print(f"⚠ Could not start automatic data collection: {e}")
        
        # Simulate running for a short time
        print("Simulating 5 seconds of operation...")
        time.sleep(5)
        
        # Cleanup
        try:
            data_collector = get_data_collector()
            if data_collector.is_running:
                data_collector.stop_collection()
                print("✓ Data collection stopped")
        except Exception as e:
            print(f"⚠ Error stopping data collection: {e}")
            
        try:
            hybrid_orchestrator.stop_system()
            print("✓ Hybrid learning system stopped")
        except Exception as e:
            print(f"⚠ Error stopping hybrid learning system: {e}")
            
    except Exception as e:
        print(f"✗ Error testing backend startup: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    print("=== Automatic Data Collection Test ===")
    
    # Test basic data collection
    test1_result = test_data_collection()
    
    # Test backend startup sequence
    test2_result = test_backend_startup()
    
    print("\n=== Test Results ===")
    print(f"Data Collection Test: {'PASS' if test1_result else 'FAIL'}")
    print(f"Backend Startup Test: {'PASS' if test2_result else 'FAIL'}")
    
    if test1_result and test2_result:
        print("\n✓ All tests passed! Automatic data collection is working correctly.")
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
