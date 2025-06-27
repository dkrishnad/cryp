#!/usr/bin/env python3
"""
Debug main database schema
"""
import sqlite3
import os

def debug_main_database():
    """Debug the main database schema"""
    db_path = "trades.db"
    
    print(f"🔍 Debugging main database: {db_path}")
    print("=" * 50)
    
    if not os.path.exists(db_path):
        print("❌ Database doesn't exist")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"📊 Found {len(tables)} tables:")
    for table in tables:
        print(f"   - {table[0]}")
    
    # Check schema for each table
    for table in tables:
        table_name = table[0]
        print(f"\n📋 Schema for {table_name}:")
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        accuracy_found = False
        for col in columns:
            print(f"   {col[1]} ({col[2]})")
            if 'accuracy' in col[1].lower():
                accuracy_found = True
                print(f"     ⚠️  ACCURACY COLUMN FOUND!")
        
        if accuracy_found:
            print(f"   🔴 Table {table_name} has accuracy column - potential conflict!")
    
    conn.close()

if __name__ == "__main__":
    debug_main_database()
