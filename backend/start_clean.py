#!/usr/bin/env python3
"""
Clean startup script that ensures the database is correctly initialized.
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    print("🚀 Starting backend with clean database...")
    
    # Import and run the main application
    from main import app, Base, engine, init_sample_data
    import uvicorn
    
    print("✅ Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    print("✅ Initializing sample data...")
    init_sample_data()
    
    print("✅ Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
