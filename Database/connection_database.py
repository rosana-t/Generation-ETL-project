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

def create_db_table(connection):
    create_chesterfield_data_table = """
        CREATE TABLE IF NOT EXISTS chesterfield (
            id serial PRIMARY KEY,
            date DATE NOT NULL,
            time TIME NOT NULL,
            location VARCHAR(100) NOT NULL,
            orders VARCHAR(250) NOT NULL,
            total_price DECIMAL(10,2) NOT NULL,
            payment_method VARCHAR(20) NOT NULL
        );
    """
    
    cursor = connection.cursor()
    cursor.execute(create_chesterfield_data_table)
    connection.commit()
    cursor.close()

def insert_data(connection, data):
    sql = """
        INSERT INTO chesterfield (date, time, location, orders, total_price, payment_method)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    
    cursor = connection.cursor()
    for order_details in data:
        row = (order_details['date'],
            order_details['time'], order_details['location'],
            order_details['orders'], order_details['total_price'],
            order_details['payment_method'])
        cursor.execute(sql, row)
              
    connection.commit()
    cursor.close() 
    print('Rows inserted.')

