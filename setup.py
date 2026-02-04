
import sys
import os
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def setup_project():
    """Complete project setup"""
    print_header("Samsung Smart Phone Advisor - Setup")
    
    # Step 1: Check dependencies
    print("📦 Step 1: Checking dependencies...")
    try:
        import fastapi
        import psycopg2
        import bs4
        import requests
        import dotenv
        print("✓ All required packages are installed\n")
    except ImportError as e:
        print(f"✗ Missing package: {e}")
        print("\n💡 Install dependencies with: pip install -r requirements.txt\n")
        return False
    
    # Step 2: Check .env file
    print("⚙️  Step 2: Checking configuration...")
    if not os.path.exists('.env'):
        print("⚠  .env file not found")
        print("💡 Create .env file from .env.example:")
        print("   cp .env.example .env")
        print("   Then update with your database credentials\n")
        return False
    else:
        print("✓ .env file found\n")
    
    # Step 3: Test database connection
    print("🗄️  Step 3: Testing database connection...")
    try:
        from db_setup import get_db_connection
        conn = get_db_connection()
        conn.close()
        print("✓ Database connection successful\n")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("\n💡 Ensure PostgreSQL is running and credentials in .env are correct\n")
        return False
    
    # Step 4: Create tables
    print("📊 Step 4: Creating database tables...")
    try:
        from db_setup import create_smartphones_table
        create_smartphones_table()
        print("✓ Database tables created\n")
    except Exception as e:
        print(f"✗ Error creating tables: {e}\n")
        return False
    
    # Step 5: Populate with sample data
    print("📱 Step 5: Populating database with sample data...")
    try:
        from scraper import save_to_db
        save_to_db()
        print("✓ Sample data loaded successfully\n")
    except Exception as e:
        print(f"✗ Error loading sample data: {e}\n")
        return False
    
    print_header("✓ Setup Complete!")
    print("""
🎉 Samsung Smart Phone Advisor is ready!

Next Steps:
1. Start the FastAPI server:
   python main.py

2. Open API documentation:
   http://localhost:8000/docs

3. Example API call:
   POST /ask
   {
     "question": "Tell me about the Galaxy S24 Ultra"
   }

Happy coding! 🚀
    """)
    return True

if __name__ == "__main__":
    success = setup_project()
    sys.exit(0 if success else 1)
