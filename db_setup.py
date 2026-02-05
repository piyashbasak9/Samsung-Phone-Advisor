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
        print(f"Database connection error: {e}")
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
                color TEXT
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Table 'phones' created successfully.")

def fetch_all_phones_full_data():
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor()
    cursor.execute("SELECT model_name, display, camera, battery, storage, price, color FROM phones;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{
        "model": r[0], "display": r[1], "camera": r[2], 
        "battery": r[3], "storage": r[4], "price": r[5], "color": r[6]
    } for r in rows]

def fetch_phone_by_model(model_name: str):
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM phones WHERE model_name ILIKE %s LIMIT 1;", (f'%{model_name}%',))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return {"id": row[0], "model_name": row[1], "display": row[2], "camera": row[3], "battery": row[4], "storage": row[5], "price": row[6], "color": row[7]}
    return None