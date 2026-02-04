import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST", "localhost")
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS phones;")
        cursor.execute("""
            CREATE TABLE phones (
                id SERIAL PRIMARY KEY,
                model_name TEXT UNIQUE,
                display TEXT,
                camera TEXT,
                battery TEXT,
                storage TEXT,
                price TEXT,
                color TEXT  -- New Column Added
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database table 'phones' created successfully.")

# ... (fetch functions remain the same) ...
def fetch_all_phones():
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor()
    cursor.execute("SELECT model_name, price FROM phones ORDER BY model_name;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"model": row[0], "price": row[1]} for row in rows]

def fetch_phone_by_model(model_name: str):
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor()
    query = """
        SELECT id, model_name, display, camera, battery, storage, price, color
        FROM phones
        WHERE model_name ILIKE %s
        LIMIT 1;
    """
    cursor.execute(query, (f'%{model_name}%',))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return {
            'id': row[0], 'model_name': row[1], 'display': row[2],
            'camera': row[3], 'battery': row[4], 'storage': row[5],
            'price': row[6], 'color': row[7]
        }
    return None