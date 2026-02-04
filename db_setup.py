
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

def drop_smartphones_table():
    """Drop smartphones table (for testing/cleanup)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DROP TABLE IF EXISTS smartphones CASCADE;")
        conn.commit()
        print("✓ Table 'smartphones' dropped successfully")
    except Exception as e:
        conn.rollback()
        print(f"✗ Error dropping table: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def insert_smartphone(model_name, display, battery, camera, ram, storage, price):
    """Insert a single smartphone record into the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        insert_query = """
        INSERT INTO smartphones (model_name, display, battery, camera, ram, storage, price)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (model_name) DO NOTHING;
        """
        cursor.execute(insert_query, (model_name, display, battery, camera, ram, storage, price))
        conn.commit()
        print(f"✓ Inserted: {model_name}")
    except Exception as e:
        conn.rollback()
        print(f"✗ Error inserting {model_name}: {e}")
    finally:
        cursor.close()
        conn.close()

def fetch_phone_by_model(model_name):
    """Fetch phone details by model name (case-insensitive)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "SELECT * FROM smartphones WHERE model_name ILIKE %s;"
        cursor.execute(query, (f'%{model_name}%',))
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"✗ Error fetching phone: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_all_phones():
    """Fetch all phones from database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM smartphones;")
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"✗ Error fetching all phones: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Setup: Create table
    print("Setting up Samsung Phone Advisor Database...")
    create_smartphones_table()
    print("Database setup complete!\n")
