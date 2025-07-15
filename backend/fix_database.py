#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import Base, engine, SessionLocal, User, Post, hash_password
from datetime import datetime

def recreate_database():
    """Recreate database with correct schema"""
    print("🔄 Recreating database with correct schema...")
    
    # Drop all tables and recreate them
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database recreated successfully!")
    
    # Test by creating a sample user
    db = SessionLocal()
    try:
        # Check if username field exists by trying to create a user with it
        sample_user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password_hash=hash_password("123456"),
            username="testuser",  # This should work now
            is_active=True,
            created_at=datetime.utcnow(),
            last_seen=datetime.utcnow()
        )
        db.add(sample_user)
        db.commit()
        db.refresh(sample_user)
        
        print(f"✅ Test user created successfully with username: {sample_user.username}")
        print("✅ Database schema is correct!")
        
    except Exception as e:
        print(f"❌ Error testing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    recreate_database()
