#!/usr/bin/env python3
"""
Debug database schema to fix SQL ambiguity
"""
import sqlite3
import os

def debug_database():
    """Debug the database schema"""
    db_path = os.path.join("models", "transfer_learning.db")
    
    print(f"🔍 Debugging database: {db_path}")
    print("=" * 50)
    
    if not os.path.exists(db_path):
        print("❌ Database doesn't exist yet")
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
        for col in columns:
            print(f"   {col[1]} ({col[2]})")
    
    conn.close()

if __name__ == "__main__":
    debug_database()
