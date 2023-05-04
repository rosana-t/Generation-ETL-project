import boto3
import psycopg2
import csv
import json
from app import *



def lambda_handler(event, context):
    print(f"lambda_handler called event ={event}")
    try:
        s3 = boto3.client('s3')
        # bucket = 'delon9-daily-grind-raw-data'
        # file_key = '2023/5/2/chesterfield_02-05-2023_09-00-00.csv' # for testing the extract
        
        bucket = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']
        
        print(f"lambda_handler loading bucket = {bucket}, file_key = {file_key}")
        csv_object = s3.get_object(Bucket=bucket, Key=file_key)  #get the csv_object
        csv_file = csv_object['Body'].read().decode('utf-8').splitlines()  #get the csv_file (body of the object)
        print(f"lambda_handler file loaded file_key = {file_key}")
        raw_sales_data = []
    
        source_file = csv.DictReader(csv_file, fieldnames=['date_time', 'location', 'name', 'orders', 'total_price', 'payment_method', 'card_number'], delimiter=',')
            # next(source_file) #ignore the header row
        for row in source_file:
            if '' not in row.values():
                raw_sales_data.append(row)
    except Exception as error:
        print("An error occurred: " + str(error))
        

 # ------------------------------------Main App ----------------------------------------------------------------------------------------------

    cleaned_data = clean_sensitive_data(raw_sales_data)
    date_time_split_tranactions = split_date_time(cleaned_data)
    formatted_date = convert_all_dates(date_time_split_tranactions, ['date'])
    transactions = change_type_total_prize(formatted_date)
    print("\nTransformed Data ready to be converted in 3NF\n")
    
    
    #branches
    list_of_branches = branch_location(transactions)
    print("\nBranch table\n")
    print(list_of_branches)
    
    #products
    product_list = split_products(transactions)
    unique_product = unique_products(product_list)
    list_of_unique_product_dicts = split_unique_products(unique_product)
    print("\nProducts table\n")
    
    
    #orders
    transformed_data = split_items_for_transactions(transactions)
    items_with_qty_per_transaction = item_quantity(transformed_data)
    data_for_orders_table = product_dict_in_order(items_with_qty_per_transaction)
    print("\nOrders table\n")
    
    
    #transactions
    transaction_table_data = remove_orders_data(data_for_orders_table)
    print(f"lambda_handler transaction table ready found {len(transaction_table_data)} rows")

    print(f"lambda_handler connecting to Redshift")
    ssm_client = boto3.client('ssm')
    parameter_details = ssm_client.get_parameter(Name='daily-grind-redshift-settings')
    redshift_details = json.loads(parameter_details['Parameter']['Value'])
    
    print(redshift_details)

    print("lambda_handler done")