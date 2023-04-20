def create_database(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS daily_grind" )
            cursor.execute('CREATE DATABASE daily_grind')
    except Exception as e:
        print(e)


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
            branch_id INT,
            CONSTRAINT fk_branch_id FOREIGN KEY (branch_id)
                REFERENCES branch (branch_id)
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
            branch_id INT,
            CONSTRAINT fk_branch_id FOREIGN KEY (branch_id)
                REFERENCES branch (branch_id)
            );
            """
            cursor.execute(postgres)
            connection.commit()
    except Exception as e:
        print(e)

def create_basket_table(connection):
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


def create_all_database_tables(connection):
    try: 
        create_branch_table(connection)
        create_product_table(connection)
        create_transaction_table(connection)
        create_basket_table(connection)
        print("Tables created")
    except Exception as e:
        print(e)