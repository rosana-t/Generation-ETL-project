import csv

def extract_data():
    sales_data = []

    try:
        with open('chesterfield_25-08-2021_09-00-00.csv', 'r') as file:
            source_file = csv.DictReader(file, fieldnames=['date_time', 'location', 'name', 'order', 'total_price', 'payment_method', 'card_number'], delimiter=',')
            # next(source_file) #ignore the header row
            for row in source_file:
                if '' not in row.values():
                    sales_data.append(row)
    except Exception as error:
        print("An error occurred: " + str(error))

    return sales_data

sales_data = extract_data()

def clean_sensitive_data(sales_data):
    
    for data in sales_data:
        del data['name']
        del data['card_number']
    return sales_data

# clean_data = clean_sensitive_data()

def sep_date_time(sales_data):
    for data in sales_data:
        date_time = data['date_time']
        date_time_split_list= date_time.split()
        data['date'] = date_time_split_list[0]
        data['time'] = date_time_split_list[1]
        del data['date_time']
    return sales_data


# print list of dictionaries for test
def print_orders_list(sales_data):
    for dic in sales_data:
        print(f'{dic["date"]},{dic["time"]},{dic["location"]},{dic["order"]},{dic["total_price"]},{dic["payment_method"]}')

clean_sensitive_data(sales_data)
sep_date_time(sales_data)


print_orders_list(sales_data)


