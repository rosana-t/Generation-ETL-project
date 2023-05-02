import csv
from datetime import datetime
# from connection_database import setup_db_connection, create_db_table, insert_data

#-------------------------EXTRACT data from csv file into a list of dictionaries------------------------------------------------------------------
def extract_data(filename):
    raw_sales_data = []
    try:
        with open(filename, 'r') as file:
            source_file = csv.DictReader(file, fieldnames=['date_time', 'location', 'name', 'orders', 'total_price', 'payment_method', 'card_number'], delimiter=',')
            # next(source_file) #ignore the header row
            for row in source_file:
                if '' not in row.values():
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

# print whole list of dictionaries for testing fonction
def print_orders_list(list_of_dic):
    for dic in list_of_dic:
        print(f'{dic["date"]},{dic["time"]},{dic["location"]},{dic["orders"]},{dic["total_price"]},{dic["payment_method"]}')

# print the first 3 dictionaries from the list
def print_first3_dic(list_of_dic):
    for dic in [list_of_dic[0], list_of_dic[1], list_of_dic[2]]:
        print(dic)

def print_unique_orders_list(unique_orders_list):
    for dic in unique_orders_list:
        print(f'{dic["name"]},{dic["price"]},{dic["size"]}')


#------------------------------------Main App ----------------------------------------------------------------------------------------------
# extract raw data
filename = "csvfile_for_testing.csv"
raw_sales_data = extract_data(filename)
# clean sensitive data
cleaned_sales_data = clean_sensitive_data(raw_sales_data)


#calling Product(table) functions------------------------------------------------------------
products_split_list = split_products(cleaned_sales_data)
unique_product_list = unique_products(products_split_list)

ready_data_for_products_table = split_unique_products(unique_product_list)

# print_first3_dic(ready_data_for_products_table)





# calling Transaction(table) functions-------------------------------------------------------
first_step_listdic = split_date_time(cleaned_sales_data)
second_step_listdic = convert_all_dates(first_step_listdic, ['date'])
third_step_listdic = remove_orders_data(second_step_listdic)

ready_data_for_transaction_table = change_type_total_prize(third_step_listdic)

# print_first3_dic(ready_data_for_transaction_table)


#calling Branch(table) functions--------------------------------------------------------------
ready_data_for_branches_table = branch_location(cleaned_sales_data)

# print(ready_data_for_branches_table)



# connection = setup_db_connection()

# print(extract_data(filename))

x = item_quantity(second_step_listdic)
# print(x)
y = product_dict_in_order(x)
# print(y)


