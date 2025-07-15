from main import Base, engine, SessionLocal, User
from sqlalchemy import inspect

# Recreate database
print("Recreating database...")
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Check table structure
inspector = inspect(engine)
columns = inspector.get_columns('users')
print("Users table columns:")
for column in columns:
    print(f"  - {column['name']}: {column['type']}")

# Test if username column exists
username_exists = any(col['name'] == 'username' for col in columns)
print(f"\nUsername column exists: {username_exists}")
