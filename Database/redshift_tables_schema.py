def create_branch_table(connection): 
    try: 
        with connection.cursor() as cursor:
            postgres = """CREATE TABLE IF NOT EXISTS branch(
            branch_id int identity (1,1) PRIMARY KEY,
            branch_location VARCHAR (70) NOT NULL)"""
            
            cursor.execute(postgres)
            connection.commit()

    except Exception as e:
        print(f"create_branch_table: error occurred + {e}")
        
    
def create_product_table(connection):
    try:
        with connection.cursor() as cursor:
            postgres = """CREATE TABLE IF NOT EXISTS product(
            product_id int identity (1,1) PRIMARY KEY,
            product_name VARCHAR (70) NOT NULL,
            product_size VARCHAR (10) NOT NULL,
            product_price DECIMAl(10,2) NOT NULL)"""
            
            cursor.execute(postgres)
            connection.commit()
            
    except Exception as e:
        print(f"create_product_table: error occurred + {e}")
        
        
def create_transaction_table(connection):
    try:
        with connection.cursor() as cursor:
            postgres = """CREATE TABLE IF NOT EXISTS transaction(
            transaction_id int identity (1,1) PRIMARY KEY,
            transaction_date date NOT NULL,
            transaction_time time NOT NULL,
            total_price DECIMAL(10,2) NOT NULL,
            payment_method VARCHAR(4) NOT NULL,
            branch_id INT,
            CONSTRAINT fk_branch_id FOREIGN KEY (branch_id)
                REFERENCES branch (branch_id))"""
                
            cursor.execute(postgres)
            connection.commit()
            
    except Exception as e:
        print(f"create_transaction_table: error occurred + {e}")
        

def create_order_table(connection):
    try:
        with connection.cursor() as cursor:
           postgres = """CREATE TABLE IF NOT EXISTS orders(
            transaction_id INT,
            product_id INT,
            product_qty INT,
            PRIMARY KEY (transaction_id, product_id),
            CONSTRAINT fk_transaction_id FOREIGN KEY (transaction_id)
                REFERENCES transaction (transaction_id),
            CONSTRAINT fk_product_id FOREIGN KEY (product_id)
                REFERENCES product (product_id))"""
                
           cursor.execute(postgres)
           connection.commit()
           
    except Exception as e:
        print(f"create_order_table: error occurred + {e}")