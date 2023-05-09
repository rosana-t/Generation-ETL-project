def load_into_branch_table(connection, location):
    try:
        with connection.cursor() as cursor:
            for loc in location:
                sql_insert_query = f"""INSERT INTO branch (branch_location) SELECT (%s) \
                                WHERE NOT EXISTS (SELECT branch_location FROM branch WHERE branch_location= (%s))"""
                data_values = [loc, loc]
                cursor.execute(sql_insert_query, data_values)
            connection.commit()
    except Exception as e:
        print(e)
            

def load_into_product_table(connection, product_info):
    try:
        with connection.cursor() as cursor:
            for product in product_info:
                sql_insert_query = f"""INSERT INTO product (product_size, product_name, product_price) SELECT %s, %s, %s\
                                   WHERE NOT EXISTS (SELECT product_size, product_name, product_price FROM product \
                                    WHERE product_size = (%s) and product_name = (%s) and product_price = (%s))"""
                data_values = [product["size"], product["name"], product["price"], product["size"], product["name"], product["price"]]
                cursor.execute(sql_insert_query, data_values)
            connection.commit()
    except Exception as e:
        print(e)

def load_into_transaction_table(connection, transaction_info):
    try:
        with connection.cursor() as cursor:
            for transaction in transaction_info:
                sql_insert_query = f"INSERT INTO transaction (transaction_date, transaction_time, total_price, payment_method, branch_id) \
                    VALUES (%s, %s, %s, %s, (SELECT branch_id FROM branch WHERE branch_location = %s))"""
                data_values = [transaction["date"], transaction["time"], transaction["total_price"], transaction["payment_method"], transaction["location"]]
                cursor.execute(sql_insert_query, data_values)
            connection.commit()
    except Exception as e:
        print(e)

def load_into_orders_table(connection, orders_info):
    try:
        with connection.cursor() as cursor:
            for order in orders_info:
                for item in order['orders']:
                    sql_insert_query = f"INSERT INTO orders (transaction_id, product_id, product_qty) VALUES ( \
                    (SELECT transaction_id FROM transaction WHERE transaction_date = (%s) and transaction_time = (%s) \
                    and total_price = (%s) and payment_method = (%s)), \
                    (SELECT product_id FROM product WHERE product_size = (%s) and product_name = (%s) and product_price = (%s)), (%s))"""
                    data_values = [order['date'], order['time'], order['total_price'], order['payment_method'],
                                   item['product_size'], item['product_name'], item['product_price'], item['product_qty']]
                    cursor.execute(sql_insert_query, data_values)
                    connection.commit()
    except Exception as e:
        print(e)
