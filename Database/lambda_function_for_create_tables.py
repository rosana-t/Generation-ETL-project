import json
import boto3
import psycopg2
from connect_rs_database import set_up_rs_connection
    
    
def create_branch_table(connection): 
    try: 
        with connection.cursor() as cursor:
            postgres = """
            CREATE TABLE IF NOT EXISTS branch(
            branch_id int identity (1,1) PRIMARY KEY,
            branch_location VARCHAR (30) NOT NULL
            )
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
            product_id int identity (1,1) PRIMARY KEY,
            product_name VARCHAR (30) NOT NULL,
            product_size VARCHAR (7) NOT NULL,
            product_price DECIMAl(10,2) NOT NULL,
            )
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
            transaction_id int identity (1,1) PRIMARY KEY,
            transaction_date date NOT NULL,
            transaction_time time NOT NULL,
            total_price DECIMAL(10,2) NOT NULL,
            payment_method VARCHAR(4) NOT NULL
            branch_id INT,
            CONSTRAINT fk_branch_id FOREIGN KEY (branch_id)
                REFERENCES branch (branch_id)
            )
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
            )
            """ 
           cursor.execute(postgres)
           connection.commit()
    except Exception as e:
        print(e)


def lambda_handler(event, context):
    try:
        print(f"lambda_handler connecting to Redshift")
        
        ssm_client = boto3.client('ssm')
        parameter_details = ssm_client.get_parameter(Name='daily-grind-redshift-settings')
        redshift_details = json.loads(parameter_details['Parameter']['Value'])
            
        connection = set_up_rs_connection(
                rs_host= redshift_details["host"],
                rs_port= redshift_details["port"],
                rs_dbname= redshift_details["database-name"],
                rs_user= redshift_details["user"],
                rs_password= redshift_details["password"])
                
        print(f"lambda_handler: connection created")
                
        create_branch_table(connection)
        print(f"lambda_handler: branch table created")
        
        create_product_table(connection)
        print(f"lambda_handler: product table created")
        
        create_transaction_table(connection)
        print(f"lambda_handler: transaction table created")
        
        create_order_table(connection)
        print(f"lambda_handler: order table created")
    
    except Exception as error:
        print("lambda_handler error occurred: " + str(error))