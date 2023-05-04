import json
import boto3
import psycopg2

# configuration


def set_up_rs_connection(rs_host, rs_port, rs_dbname, rs_user, rs_password):
    
    print(f"set_up_rs_connection connecting to rs_host = {rs_host}")
    
    conn = psycopg2.connect(
        host = rs_host,
        port = rs_port,
        dbname = rs_dbname,
        user = rs_user,
        password = rs_password)
    
    return conn
    
    
def create_branch_table(connection): 
    try: 
        with connection.cursor() as cursor:
            postgres = """
            CREATE TABLE IF NOT EXISTS branch(
            branch_id serial PRIMARY KEY,
            branch_location VARCHAR (30) NOT NULL
            );
            """
        cursor.execute(postgres)
        connection.commit()

    except Exception as e:
        print(e)

def create_product_table(connection):
    try:
        with connection.cursor() as cursor:
            postgres = """
            CREATE TABLE IF NOT EXISTS product(
            product_id serial PRIMARY KEY,
            product_name VARCHAR (30) NOT NULL,
            product_size VARCHAR (7) NOT NULL,
            product_price DECIMAl(10,2) NOT NULL,
            );
            """
            cursor.execute(postgres)
            connection.commit()
    except Exception as e:
        print(e)
    
def create_transaction_table(connection):
    try:
        with connection.cursor() as cursor:
            postgres = """
            CREATE TABLE IF NOT EXISTS transaction(
            transaction_id serial PRIMARY KEY,
            transaction_date date NOT NULL,
            transaction_time time NOT NULL,
            total_price DECIMAL(10,2) NOT NULL,
            payment_method VARCHAR(4) NOT NULL
            branch_id INT,
            CONSTRAINT fk_branch_id FOREIGN KEY (branch_id)
                REFERENCES branch (branch_id)
            );
            """
            cursor.execute(postgres)
            connection.commit()
    except Exception as e:
        print(e)

def create_order_table(connection):
    try:
        with connection.cursor() as cursor:
           postgres = """
            CREATE TABLE IF NOT EXISTS basket(
            transaction_id INT,
            product_id INT,
            product_quanity INT,
            PRIMARY KEY (transaction_id, product_id),
            CONSTRAINT fk_transaction_id FOREIGN KEY (transaction_id)
                REFERENCES transaction (transaction_id),
            CONSTRAINT fk_product_id FOREIGN KEY (product_id)
                REFERENCES product (product_id)
            );
            """ 
           cursor.execute(postgres)
           connection.commit()
    except Exception as e:
        print(e)


