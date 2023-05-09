from local_pg_connection import setup_db_connection

def create_branch_table(connection): 
    try: 
        with connection.cursor() as cursor:
            postgres = """
            CREATE TABLE IF NOT EXISTS branch(
            branch_id serial PRIMARY KEY,
            branch_location VARCHAR (50) NOT NULL
            )
            """
            cursor.execute(postgres)
            connection.commit()
        print("\ncreate_branch_table: branch table created")

    except Exception as e:
        print(e)


def create_product_table(connection):
    try:
        with connection.cursor() as cursor:
            postgres = """
            CREATE TABLE IF NOT EXISTS product(
            product_id serial PRIMARY KEY,
            product_size VARCHAR (7) NOT NULL,
            product_name VARCHAR (70) NOT NULL,
            product_price DECIMAl(10,2) NOT NULL
            )
            """
            cursor.execute(postgres)
            connection.commit()
            print("\ncreate_product_table: product table created")
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
            payment_method VARCHAR(4) NOT NULL,
            branch_id INT,
            CONSTRAINT fk_branch_id FOREIGN KEY (branch_id)
                REFERENCES branch (branch_id)
            )
            """
            cursor.execute(postgres)
            connection.commit()
            print("\ncreate_transaction_table: transaction table created")
    except Exception as e:
        print(e)

def create_order_table(connection):
    try:
        with connection.cursor() as cursor:
           postgres = """
            CREATE TABLE IF NOT EXISTS orders(
            transaction_id INT,
            product_id INT,
            product_qty INT,
            PRIMARY KEY (transaction_id, product_id),
            CONSTRAINT fk_transaction_id FOREIGN KEY (transaction_id)
                REFERENCES transaction (transaction_id),
            CONSTRAINT fk_product_id FOREIGN KEY (product_id)
                REFERENCES product (product_id)
            )
            """ 
           cursor.execute(postgres)
           connection.commit()
           print("\ncreate_order_table: orders table created")
    except Exception as e:
        print(e)


def create_all_database_tables(connection):
    try: 
        print("create_all_database_tables: database connected")
        create_branch_table(connection)
        create_product_table(connection)
        create_transaction_table(connection)
        create_order_table(connection)
        print("\ncreate_all_database_tables: All tables created")
    except Exception as e:
        print(e)

connection_status = False
connection = setup_db_connection(connection_status)
create_all_database_tables(connection)