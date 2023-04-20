import csv
from connection_database import setup_db_connection, create_db_table, insert_data

sales_data = []

#-------------------------EXTRACT data from csv file into a list of dictionaries------------------------------------------------------------------
def extract_data():
    try:
        with open('chesterfield_25-08-2021_09-00-00.csv', 'r') as file:
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


# SPLIT date and time into different columns function
def split_date_time():
    for data in sales_data:
        date_time = data['date_time']
        date_time_split_list= date_time.split()
        data['date'] = date_time_split_list[0]
        data['time'] = date_time_split_list[1]
        del data['date_time']
    return sales_data

# SPLIT items from orders into different columns function
def split_items():
    basket = []
    for data in sales_data:
        orders = data['orders']
        items_split_list = orders.split(',')
        print(items_split_list)
        
        for x in items_split_list:
            item = x.split()
            product_size = item[0] 
            product_name = ' '.join(item[1:-1]) 
            product_price = item[-1] 
            basket.append(product_size)
            basket.append(product_price)
            basket.append(product_name)
            print(basket)
    return sales_data



#---------------------------EXTRA functions --------------------------------------------------------------------------------------------------------

# print whole list of dictionaries for testing fonction
def print_orders_list():
    for dic in sales_data:
        print(f'{dic["date"]},{dic["time"]},{dic["location"]},{dic["orders"]},{dic["total_price"]},{dic["payment_method"]}')

# print the first 3 dictionaries from the list
def print_first3_dic():
    for dic in [sales_data[0], sales_data[2], sales_data[3]]:
        print(f'{dic["date"]},{dic["time"]},{dic["location"]},{dic["orders"]},{dic["total_price"]},{dic["payment_method"]}')



#------------------------------------Main App ------------------------------------------------------------------

# connection = setup_db_connection()
extract_data()
clean_sensitive_data()
split_date_time()
# print_orders_list()
print_first3_dic()

# create a table with raw data
# create_db_table(connection)
# insert_data(connection, sales_data)

