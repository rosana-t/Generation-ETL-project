import csv
from datetime import datetime
# from connection_database import setup_db_connection, create_db_table, insert_data

#-------------------------EXTRACT data from csv file into a list of dictionaries------------------------------------------------------------------
def extract_data(filename):
    raw_sales_data = []
    try:
        with open(filename, 'r') as file:
            source_file = csv.DictReader(file, fieldnames=['date_time', 'location', 'name', 'orders', 'total_price', 'payment_method', 'card_number'], delimiter=',')
            for row in source_file:
                raw_sales_data.append(row)
    except Exception as error:
        print("An error occurred: " + str(error))

    return raw_sales_data

#---------------------------TRANSFORM data --------------------------------------------------------------------------------------------------------

# Clean sensitive data function
def clean_sensitive_data(raw_sales_d):
    
    for data in raw_sales_d:
        del data['name']
        del data['card_number']
    return raw_sales_d

#-------------------------------- Transaction(table) functions ------------------------------------------------------------------------------------

# SPLIT date and time into different columns function
def split_date_time(cleaned_sales_d):
    for data in cleaned_sales_d:
        date_time = data['date_time']
        date_time_split_list= date_time.split()
        data['date'] = date_time_split_list[0].replace('/','-')
        data['time'] = date_time_split_list[1]
        del data['date_time']
    return cleaned_sales_d

# Convert date from (day-month-year) into American style (month-day-year) function
def convert_all_dates(list_of_dicts, date_cols, 
                      current_format='%d-%m-%Y',
                      expected_format='%m-%d-%Y'):
    # Uniformity
    for dict in list_of_dicts:
        for col in date_cols:
            try:
                str_to_date = datetime.strptime(dict[col], current_format)
                date_to_str = datetime.strftime(str_to_date, expected_format)
                dict[col] = date_to_str
            except ValueError as e:
                print(f"Error parsing value '{dict[col]}' in column '{col}': {e}")
                dict[col] = None        
    return list_of_dicts

# Remove orders from data (we do not need it in the Transaction(table)) function
def remove_orders_data(second_step_d):
    for data in second_step_d:
        del data['orders']
    return second_step_d

# Change type of total_price str to float function
def change_type_total_prize(third_step_l):
    for data in third_step_l:
        data['total_price'] = float(data['total_price'])
    return third_step_l

#-------------------------------- Product(table) functions ---------------------------------------------------------------------------------------
# SPLIT products from orders into different columns function
def split_products(cleaned_sales_d):
    all_products_list = []
    for data in cleaned_sales_d:
        orders = data['orders']  #e.g. ["Large Hot Chocolate - 1.70, Large Filter coffee - 1.80"]
        products_split_list = orders.split(',') #e.g. ['Large Flavoured iced latte - Vanilla - 3.25', ' Large Latte - 2.45']
        all_products_list.append(products_split_list)
    return all_products_list

#get the unique products function 
def unique_products(products_split_l):
    unique_product_list = []
    for products in products_split_l:
        for product in products:
            x = product.strip()
            if x not in unique_product_list:
                unique_product_list.append(x)
    return unique_product_list

def split_unique_products(unique_product_l):
        list_of_product_dic = []
        for x in unique_product_l:
            item = x.split()  #e.g. ['Large', 'Flavoured', 'iced', 'latte', '-', 'Vanilla', '-', '3.25']
            item_dic = {}  
            item_dic["name"] = ' '.join(item[1:-1]).replace(' -','') # remove all extra spaces and '-'
            item_dic["size"] = item[0]
            item_dic["price"] = float(item[-1])
            list_of_product_dic.append(item_dic) # append all items dictionary into a list
        return list_of_product_dic

#-------------------------------- Branch(table) functions ---------------------------------------------------------------------------------------
def branch_location(cleaned_sales_d):
    list_of_locations = []
    for data in cleaned_sales_d:
        location = data['location']
        if location not in list_of_locations:
            list_of_locations.append(location)
    return list_of_locations   

#--------------------------Order(table) functions-------------------------------------------------------------------------
def split_items_for_transactions(sales_data: list[dict]):
    try:
        for data in sales_data:
            order = data['orders']
            separated_order = order.split(',')
            data['orders'] = separated_order 
    except Exception as e:
        print(e)
    
    return sales_data

def strip_items_in_order(sales_data: list[dict]):
    try:
        for data in sales_data:
            order = data['orders']
            new_order = []
            for i in order:
                item = i.strip()
                new_order.append(item)
            data['orders'] = new_order
    except Exception as e:
        print(e)
    
    return sales_data

def item_quantity(sales_data: list[dict]):
    try:
        for data in sales_data:
            all_items_in_order = data['orders']
            new_order = []
            for item in set(all_items_in_order):
                count = all_items_in_order.count(item)
                qty = item + f", {count}"
                new_order.append(qty)
            data['orders'] = new_order
    except Exception as e:
        print(e)
    
    return sales_data

def product_dict_in_order(sales_data: list[dict]):
    try:
        for transaction in sales_data:
            order = transaction['orders']
            edited_order = []
            for item in order:
                item_dict = {}
                item_attribute = item.split()
            
                item_dict['product_size'] = item_attribute[0]
                item_dict['product_name'] = " ".join(item_attribute[1:-2]).replace(" -", "")
                item_dict['product_qty'] = int(item_attribute[-1])
                item_dict['product_price'] = float(item_attribute[-2].replace(",", ""))
                edited_order.append(item_dict)
            transaction['orders'] = edited_order
    except Exception as e:
        print(e)

    return sales_data

#---------------------------EXTRA functions --------------------------------------------------------------------------------------------------------

def print_orders_listt(list_of_dic):
    for dic in list_of_dic:
        print(f'{dic["date_time"]},{dic["location"]},{dic["name"]},{dic["orders"]},{dic["payment_method"]},{dic["orders"]}')
# print raw list
def print_orders_list(orders_l):
    order_number = 0
    for order in orders_l:
        order_number +=1
        print(f'{order_number}. {order["date_time"]}, {order["location"]}, {order["name"]}, {order["orders"]}, {order["total_price"]}, {order["payment_method"]}, {order["card_number"]}')

# print removed sensitive data list
def print_cleaned_list(orders_l):
    order_number = 0
    for order in orders_l:
        order_number +=1
        print(f'{order_number}. {order["date_time"]}, {order["location"]}, {order["orders"]}, {order["total_price"]}, {order["payment_method"]}')

# print transformed data list
def print_transformed_list(orders_l):
    order_number = 0
    for order in orders_l:
        order_number +=1
        print(f'{order_number}. {order["date"]}, {order["time"]}, {order["location"]}, {order["orders"]}, {order["total_price"]}, {order["payment_method"]}')

# print unique_products_list
def print_unique_products_list(orders_l):
    order_number = 0
    for order in orders_l:
        order_number +=1
        print(f'{order_number}. {order["name"]}, {order["size"]}, {order["price"]}')

# print Orders table and Transaction table data list
def print_transaction_list(orders_l):
    order_number = 0
    for order in orders_l:
        order_number +=1
        print(f'{order_number}. {order["location"]}, \n{order["orders"]},\n {order["payment_method"]}, {order["date"]}, {order["time"]}')

# print whole list of dictionaries for testing fonction
# def print_orders_list(list_of_dic):
#     for dic in list_of_dic:
#         print(f'{dic["date"]},{dic["time"]},{dic["location"]},{dic["orders"]},{dic["total_price"]},{dic["payment_method"]}')

# print the first 3 dictionaries from the list
def print_first3_dic(list_of_dic):
    for dic in [list_of_dic[0], list_of_dic[1], list_of_dic[2]]:
        print(dic)

def print_unique_orders_list(unique_orders_list):
    for dic in unique_orders_list:
        print(f'{dic["name"]},{dic["price"]},{dic["size"]}')


#------------------------------------Main App ------------------------------------------------------------------------------------------------
if __name__ =='__main__':
    csv_file = 'csvfile_for_testing.csv'
    raw_data = extract_data(csv_file)
    print("\n1.) Extracted raw data from .csv file:\n")
    print_orders_list(raw_data)

    cleaned_data = clean_sensitive_data(raw_data)
    print("\n\n2.) Removed sensitive data (name and card number):\n")
    print_cleaned_list(cleaned_data)

    date_time_split_tranactions = split_date_time(cleaned_data)
    formatted_date = convert_all_dates(date_time_split_tranactions, ['date'])
    transactions = change_type_total_prize(formatted_date)
    print("\n\n3.) Transformed data (split date/time, change type of total_price):\n")
    print_transformed_list(transactions)

    print("\nTransformed Data ready to be converted in 3NF\n")
    
    #branches
    list_of_branches = branch_location(transactions)
    print("\n\nBranch table data ready (list of locations):\n")
    print(list_of_branches)
    

    #products
    product_list = split_products(transactions)
    unique_product = unique_products(product_list)
    list_of_unique_product_dicts = split_unique_products(unique_product)
    print("\n\nProducts table data ready (split products by name/size/price)(unique products list of dictionary):\n")
    print_unique_products_list(list_of_unique_product_dicts)
   

    # orders and transactions
    transformed_data = split_items_for_transactions(transactions)
    transformed_data_2 = strip_items_in_order(transformed_data)
    items_with_qty_per_transaction = item_quantity(transformed_data_2)
    data_for_orders_table = product_dict_in_order(items_with_qty_per_transaction)
    print("\n\nOrders table and Transaction table data ready (count quantity of products)\n")
    print_transaction_list(data_for_orders_table)

    print("\nAll data ready to load!")
  
   

