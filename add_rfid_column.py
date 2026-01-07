#!/usr/bin/env python3
"""
Migration script to add rfid column to User table.
"""
import sqlite3
import sys

DB_PATH = "app.db"

def migrate():
    """Add rfid column to user table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(user)")
        columns = {col[1] for col in cursor.fetchall()}
        
        if "rfid" in columns:
            print("✓ rfid column already exists in user table")
            conn.close()
            return
        
        # Add the column (without UNIQUE constraint initially)
        cursor.execute("""
            ALTER TABLE user
            ADD COLUMN rfid VARCHAR(100)
        """)
        conn.commit()
        
        print("✓ Successfully added rfid column to user table")
        
        # Show the schema
        cursor.execute("PRAGMA table_info(user)")
        cols = cursor.fetchall()
        print("\nUser table schema:")
        for col in cols:
            print(f"  - {col[1]} ({col[2]})")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"✗ Database error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    print("Running migration: add_rfid_column.py")
    migrate()
