"""
Migration script to add display_id to existing users
"""
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import User, SQLALCHEMY_DATABASE_URL

# Create database connection
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def migrate_display_ids():
    db = SessionLocal()
    try:
        # Get all users without display_id
        users = db.query(User).filter(User.display_id == None).all()
        
        print(f"Found {len(users)} users without display_id")
        
        for user in users:
            # Generate unique random display_id
            while True:
                random_display_id = str(random.randint(1000000000, 9999999999))
                existing = db.query(User).filter(User.display_id == random_display_id).first()
                if not existing:
                    break
            
            user.display_id = random_display_id
            print(f"Assigned display_id {random_display_id} to user {user.first_name} {user.last_name}")
        
        db.commit()
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_display_ids()
