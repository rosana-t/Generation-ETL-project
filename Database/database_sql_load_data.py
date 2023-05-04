def load_into_branch_table(connection, location):
    try:
        with connection.cursor() as cursor:
            for loc in location:
                sql_insert_query = f"INSERT INTO branch (branch_location) VALUES (%s)"""
                cursor.execute(sql_insert_query, loc)
            connection.commit()
    except Exception as e:
        print(e)
            

def load_into_product_table(connection, product_info):
    try:
        with connection.cursor() as cursor:
            for product in product_info:
                sql_insert_query = f"INSERT INTO product (product_name, product_size, product_price) VALUES (%s, %s, %s)"""
                cursor.execute(sql_insert_query, product["name"], product["size"], product["price"])
            connection.commit()
    except Exception as e:
        print(e)

def load_into_transaction_table(connection, transaction_info):
    try:
        with connection.cursor() as cursor:
            for transaction in transaction_info:
                sql_insert_query = f"INSERT INTO product (transaction_date, transaction_time, total_price, payment_method, branch_id) VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(sql_insert_query, transaction["date"], transaction["time"], transaction["total_price"], transaction["payment_method"], transaction["location"])
            connection.commit()
    except Exception as e:
        print(e)

def load_into_basket_table(connection, basket_info):
    try:
        with connection.cursor() as cursor:
            sql_insert_query = f"INSERT INTO basket (transaction_id, product_id, quantity) VALUES (%s, %s, %s)"""
        
            cursor.execute(sql_insert_query, basket_info)
            connection.commit()
    except Exception as e:
        print(e)