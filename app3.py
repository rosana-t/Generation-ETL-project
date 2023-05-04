import boto3
import psycopg2
import csv
import json
from app import *

#print function for testing
def print_first3_dic(list_of_dic):
    for dic in [list_of_dic[0], list_of_dic[1], list_of_dic[2]]:
        print(dic)


def lambda_handler(event, context):
    try:
        s3 = boto3.client('s3')
        bucket = 'delon9-daily-grind-raw-data'
        file_key = '2023/5/2/chesterfield_02-05-2023_09-00-00.csv' # for testing the extract
        csv_object = s3.get_object(Bucket=bucket, Key=file_key)  #get the csv_object
        csv_file = csv_object['Body'].read().decode('utf-8').splitlines()  #get the csv_file (body of the object)
    
        raw_sales_data = []
    
        source_file = csv.DictReader(csv_file, fieldnames=['date_time', 'location', 'name', 'orders', 'total_price', 'payment_method', 'card_number'], delimiter=',')
            # next(source_file) #ignore the header row
        for row in source_file:
            if '' not in row.values():
                raw_sales_data.append(row)
    except Exception as error:
        print("An error occurred: " + str(error))
    
    ssm_client = boto3.client('ssm')
    parameter_details = ssm_client.get_parameter(Name='daily-grind-redshift-settings')
    redshift_details = json.loads(parameter_details['Parameter']['Value'])
    
    print(redshift_details)
    
    # clean_sensitive_data(raw_sales_data)
    # cleaned_sales_data = clean_sensitive_data(raw_sales_data)
    
    
    # raw_sales_data = extract_data(filename)
    # # clean sensitive data
    # cleaned_sales_data = clean_sensitive_data(raw_sales_data)

# ------------------------------------Main App ----------------------------------------------------------------------------------------------
    # if __name__ =='__main__':
    #     csv_file = 'csvfile_for_testing.csv'
    #     raw_data = extract_data(csv_file)

    cleaned_data = clean_sensitive_data(raw_sales_data)
    date_time_split_tranactions = split_date_time(cleaned_data)
    formatted_date = convert_all_dates(date_time_split_tranactions, ['date'])
    transactions = change_type_total_prize(formatted_date)
    print("\nTransformed Data ready to be converted in 3NF\n")
    for i in transactions:
        print(i)
    
    #branches
    list_of_branches = branch_location(transactions)
    print("\nBranch table\n")
    print(list_of_branches)
    
    #products
    product_list = split_products(transactions)
    unique_product = unique_products(product_list)
    list_of_unique_product_dicts = split_unique_products(unique_product)
    print("\nProducts table\n")
    for i in list_of_unique_product_dicts:
        print(i)
    
    #orders
    transformed_data = split_items_for_transactions(transactions)
    items_with_qty_per_transaction = item_quantity(transformed_data)
    data_for_orders_table = product_dict_in_order(items_with_qty_per_transaction)
    print("\nOrders table\n")
    for i in data_for_orders_table:
         print(i)
    
    # #transactions
    transaction_table_data = remove_orders_data(data_for_orders_table)
    print("\nTransaction tables\n")
    for i in transaction_table_data:
        print(i)


    # #calling Product(table) functions------------------------------------------------------------
    # print("Product(table)")
    # products_split_list = split_products(cleaned_sales_data)
    # unique_product_list = unique_products(products_split_list)

    # ready_data_for_products_table = split_unique_products(unique_product_list)

    # print_first3_dic(ready_data_for_products_table)



    # # calling Transaction(table) functions------------------------------------------------------
    # print("Transaction(table)")
    # first_step_listdic = split_date_time(cleaned_sales_data)
    # second_step_listdic = convert_all_dates(first_step_listdic, ['date'])
    # third_step_listdic = remove_orders_data(second_step_listdic)

    # ready_data_for_transaction_table = change_type_total_prize(third_step_listdic)
    
    # print_first3_dic(ready_data_for_transaction_table)
    
    
    # #calling Branch(table) functions--------------------------------------------------------------
    # print("Branch(table)")
    # ready_data_for_branches_table = branch_location(cleaned_sales_data)

    # print(ready_data_for_branches_table)
   
    