import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    """Establish connection to PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'samsung_advisor'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'password')
        )
        print("✓ Database connection established")
        return conn
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        raise
    
def create_smartphones_table():
    """Create smartphones table with required columns"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # SQL command to create table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS smartphones (
            id SERIAL PRIMARY KEY,
            model_name TEXT NOT NULL UNIQUE,
            display TEXT,
            battery TEXT,
            camera TEXT,
            ram TEXT,
            storage TEXT,
            price TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        cursor.execute(create_table_query)
        conn.commit()
        print("✓ Table 'smartphones' created successfully")
        
    except Exception as e:
        conn.rollback()
        print(f"✗ Error creating table: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Setup: Create table
    print("Setting up Samsung Phone Advisor Database...")
    create_smartphones_table()
    print("Database setup complete!\n")