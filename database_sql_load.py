
def load_into_branch(connection, location):
    try:
        with connection.cursor() as cursor:
            sql_insert_query = f"INSERT INTO branch (branch_location) VALUES (%s)"""
        
            cursor.execute(sql_insert_query, location)
            connection.commit()
    except Exception as e:
        print(e)
            

def load_into_product(connection, product_info):
    try:
        with connection.cursor() as cursor:
            sql_insert_query = f"INSERT INTO product (product_name, product_size, product_price) VALUES (%s, %s, %s)"""
        
            cursor.execute(sql_insert_query, product_info)
            connection.commit()
    except Exception as e:
        print(e)

def load_into_transaction(connection, transaction_info):
    try:
        with connection.cursor() as cursor:
            sql_insert_query = f"INSERT INTO product (transaction_date, transaction_time, total_price, payment_method, branch_id) VALUES (%s, %s, %s, %s, %s)"""
        
            cursor.execute(sql_insert_query, transaction_info)
            connection.commit()
    except Exception as e:
        print(e)

def load_into_basket(connection, basket_info):
    try:
        with connection.cursor() as cursor:
            sql_insert_query = f"INSERT INTO basket (transaction_id, product_id, quantity) VALUES (%s, %s, %s)"""
        
            cursor.execute(sql_insert_query, basket_info)
            connection.commit()
    except Exception as e:
        print(e)