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
    
    return conn
connection = setup_db_connection()
def create_db_tables(connection):
    create_chesterfield_data_table = """
        CREATE TABLE IF NOT EXISTS chesterfield (
            id INT NOT NULL AUTO_INCREMENT,
            date DATE NOT NULL,
            time TIME NOT NULL,
            location VARCHAR(100) NOT NULL,
            order VARCHAR(250) NOT NULL,
            total_price DECIMAL(10,2) NOT NULL,
            payment_method VARCHAR(20) NOT NULL,
        PRIMARY KEY (id)
        );
    """
    
    cursor = connection.cursor()
    cursor.execute(create_chesterfield_data_table)
    connection.commit()
    cursor.close()


