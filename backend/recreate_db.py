#!/usr/bin/env python3
"""
Script to recreate the database with the correct schema.
This script removes old database files and creates new ones with the complete schema.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def recreate_database():
    """Remove old database files and let main.py recreate them with correct schema"""
    
    # Remove existing database files
    db_files = ["test.db", "vibe.db"]
    for db_file in db_files:
        db_path = backend_dir / db_file
        if db_path.exists():
            db_path.unlink()
            print(f"✅ Removed old database file: {db_file}")
    
    print("🔄 Database files removed. The main.py will recreate them with the correct schema when started.")
    print("💡 To recreate the database, restart the backend server (python main.py)")

if __name__ == "__main__":
    recreate_database()
