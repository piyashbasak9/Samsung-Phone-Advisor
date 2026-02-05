import os
import sys
from db_setup import create_table, get_db_connection
from scraper import seed_database

def run_setup():
    print("--- Samsung Smart Phone Advisor Setup ---")
    
    # 1. Verify .env file exists
    if not os.path.exists('.env'):
        print("Error: .env file not found. Please create it first.")
        return False

    # 2. Test Database Connection
    print("Testing database connection...")
    try:
        conn = get_db_connection()
        if conn is None:
            raise Exception("Connection returned None")
        conn.close()
        print("Success: Database connected.")
    except Exception as e:
        print(f"Error: Could not connect to PostgreSQL. {e}")
        return False

    # 3. Initialize Database and Seed Data
    print("Creating tables and inserting 30 phones...")
    try:
        # This calls the functions from your other files
        seed_database() 
        print("Success: Database is ready with 30 premium models.")
    except Exception as e:
        print(f"Error during data insertion: {e}")
        return False

    print("\n--- Setup Complete! ---")
    print("You can now start the server using: uvicorn main:app --reload")
    return True

if __name__ == "__main__":
    success = run_setup()
    sys.exit(0 if success else 1)