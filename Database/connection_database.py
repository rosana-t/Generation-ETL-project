import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
HOST = os.environ.get("postgres_host")
USER = os.environ.get("postgres_user")
PASSWORD = os.environ.get("postgres_pass")
WAREHOUSE_DB_NAME = os.environ.get("postgres_db")

def setup_db_connection(host=HOST, user=USER, password=PASSWORD, warehouse_db_name=WAREHOUSE_DB_NAME):
    
    conn = psycopg2.connect(
        host="localhost",
        database="daily_grind",
        user="postgres",
        password="password"
    )
    
    cursor = conn.cursor()
    return conn, cursor


