import csv
# from connection_database import setup_db_connection, create_db_table, insert_data

sales_data = []

#-------------------------EXTRACT data from csv file into a list of dictionaries------------------------------------------------------------------
def extract_data():
    try:
        with open('leeds_01-01-2020_09-00-00.csv', 'r') as file:
            source_file = csv.DictReader(file, fieldnames=['date_time', 'location', 'name', 'orders', 'total_price', 'payment_method', 'card_number'], delimiter=',')
            # next(source_file) #ignore the header row
            for row in source_file:
                if '' not in row.values():
                    sales_data.append(row)
    except Exception as error:
        print("An error occurred: " + str(error))

    return sales_data

#---------------------------TRANSFORM data --------------------------------------------------------------------------------------------------------

# DELETE sensitive data function
def clean_sensitive_data():
    
    for data in sales_data:
        del data['name']
        del data['card_number']
    return sales_data

#-------------------------------- Transaction(table) functions ------------------------------------------------------------------------------------
# SPLIT date and time into different columns function
def split_date_time():
    for data in sales_data:
        date_time = data['date_time']
        date_time_split_list= date_time.split()
        data['date'] = date_time_split_list[0].replace('/','-')
        data['time'] = date_time_split_list[1]
        del data['date_time']
    return sales_data

def remove_extra_data():
    for data in sales_data:
        del data['orders']
    return sales_data

def change_type():
    for data in sales_data:
        data['total_price'] = float(data['total_price'])
    return sales_data

#-------------------------------- Product(table) functions ---------------------------------------------------------------------------------------
# SPLIT items from orders into different columns function
def split_items():
    all_orders_list = []
    for data in sales_data:
        orders = data['orders']  #e.g. ["Large Hot Chocolate - 1.70, Large Filter coffee - 1.80"]
        items_split_list = orders.split(',') #e.g. ['Large Flavoured iced latte - Vanilla - 3.25', ' Large Latte - 2.45']
        all_orders_list.append(items_split_list)
    return all_orders_list

#get the unique items function 
def unique_items(items_split_l):
    unique_product_list = []
    for items in items_split_l:
        for product in items:
            x = product.strip()
            if x not in unique_product_list:
                unique_product_list.append(x)
    return unique_product_list

def split_unique_items(unique_product_list):
        list_of_product_dic = []
        for x in unique_product_list:
            item = x.split()  #e.g. ['Large', 'Flavoured', 'iced', 'latte', '-', 'Vanilla', '-', '3.25']
            item_dic = {}  
            item_dic["name"] = ' '.join(item[1:-1]).replace(' -','') # remove all extra spaces and '-'
            item_dic["size"] = item[0]
            item_dic["price"] = float(item[-1])
            list_of_product_dic.append(item_dic) # append all items dictionary into a list
        return list_of_product_dic

#-------------------------------- Branch(table) functions ---------------------------------------------------------------------------------------
def branch_location():
    list_of_locations = []
    for data in sales_data:
        location = data['location']
        if location not in list_of_locations:
            list_of_locations.append(location)
    return list_of_locations   

#---------------------------EXTRA functions --------------------------------------------------------------------------------------------------------

# print whole list of dictionaries for testing fonction
def print_orders_list():
    for dic in sales_data:
        print(f'{dic["date"]},{dic["time"]},{dic["location"]},{dic["orders"]},{dic["total_price"]},{dic["payment_method"]}')

# print the first 3 dictionaries from the list
def print_first3_dic():
    for dic in [sales_data[0], sales_data[2], sales_data[3]]:
        # print(f'{dic["date"]},{dic["time"]},{dic["location"]},{dic["orders"]},{dic["total_price"]},{dic["payment_method"]}')
        print(dic)

def print_unique_orders_list(unique_orders_list):
    for dic in unique_orders_list:
        print(f'{dic["name"]},{dic["price"]},{dic["size"]}')


#------------------------------------Main App ------------------------------------------------------------------

# connection = setup_db_connection()
extract_data()
clean_sensitive_data()
split_date_time()

#calling Product(table) functions
items_split_list = split_items()
x = unique_items(items_split_list)
y = split_unique_items(x)

#calling Transaction(table) functions
remove_extra_data()
change_type()
print_first3_dic()

#calling Branch(table) functions
z = branch_location()
print(z)


