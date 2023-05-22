import boto3
import psycopg2
import csv
import json
from app import *
from redshift_connection import setup_rs_connection
from redshift_load_functions import *

# def get_bucket_and_key():
#     bucket = event['Records'][0]['s3']['bucket']['name']
#     file_key = event['Records'][0]['s3']['object']['key']
    
#     print(f"lambda_handler loading bucket = {bucket}, file_key = {file_key}")
    
#     return bucket, file_key
    
# def extract_from_csv(bucket, file_key):
#     s3 = boto3.client('s3')
    
#     csv_object = s3.get_object(Bucket=bucket, Key=file_key)  #get the csv_object
#     csv_file = csv_object['Body'].read().decode('utf-8').splitlines()  #get the csv_file (body of the object)
#     print(f"lambda_handler file loaded file_key = {file_key}")
        
#     raw_sales_data = []
    
#     source_file = csv.DictReader(csv_file, fieldnames=['date_time', 'location', 'name', 'orders', 'total_price', 'payment_method', 'card_number'], delimiter=',')
    
#     for row in source_file:
#         raw_sales_data.append(row)
    
#     return raw_sales_data
    
#Hello my friend!
def lambda_handler(event, context):
    print(f"lambda_handler called event ={event}")
    try:
        s3 = boto3.client('s3')
        # bucket = 'delon9-daily-grind-raw-data2'
        # file_key = '2023/5/3/york_03-05-2023_09-00-00.csv' # for testing the extract
        
        bucket = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']
        
        print(f"lambda_handler loading bucket = {bucket}, file_key = {file_key}")
        csv_object = s3.get_object(Bucket=bucket, Key=file_key)  #get the csv_object
        csv_file = csv_object['Body'].read().decode('utf-8').splitlines()  #get the csv_file (body of the object)
        print(f"lambda_handler file loaded file_key = {file_key}")
        raw_sales_data = []
    
        source_file = csv.DictReader(csv_file, fieldnames=['date_time', 'location', 'name', 'orders', 'total_price', 'payment_method', 'card_number'], delimiter=',')
        for row in source_file:
            raw_sales_data.append(row)

# -----------------------------------Extract--------------------------------------------------------------------------------------------------
                
        # get_bucket_and_key()
        # raw_sales_data = extract_from_csv()
    
        

# ------------------------------------Transform ----------------------------------------------------------------------------------------------
        #raw data 
        cleaned_data = clean_sensitive_data(raw_sales_data)
        date_time_split_tranactions = split_date_time(cleaned_data)
        formatted_date = convert_all_dates(date_time_split_tranactions, ['date'])
        transactions = change_type_total_prize(formatted_date)
        print(f"\nTransformed data ready for tables, file_key = {file_key}")
        
        #branches
        list_of_branches = branch_location(transactions)
        print(f"\nBranch table data ready, for file_key = {file_key}")
        
    
        #products
        product_list = split_products(transactions)
        unique_product = unique_products(product_list)
        list_of_unique_product_dicts = split_unique_products(unique_product)
        print(f"lambda_handler products table ready found {len(list_of_unique_product_dicts)} rows, for file_key = {file_key}")
       
    
        # orders and transactions
        transformed_data = split_items_for_transactions(transactions)
        transformed_data_2 = strip_items_in_order(transformed_data)
        items_with_qty_per_transaction = item_quantity(transformed_data_2)
        data_for_orders_and_transaction_table = product_dict_in_order(items_with_qty_per_transaction)
        print(f"lambda_handler orders and transaction table ready found {len(data_for_orders_and_transaction_table)} rows, for file_key = {file_key}")
    
        print(f"\nAll data ready to load, for file_key = {file_key}")
        
#----------------------------------------convert to dictionary--------------------------------------------------------------------------------------------------

        transformed_dict = {"branch":list_of_branches, "product": list_of_unique_product_dicts, "orders_and_transaction": data_for_orders_and_transaction_table, "file_key": file_key}
        
        print(f"Transformed data converted to a dictionary for file_key = {file_key}")
        
        
        # session = boto3.Session(profile_name)
        # sqs_client = session.client('sqs')
        
        sqs = boto3.client('sqs')
  
        message = transformed_dict
        response = sqs.send_message(
            QueueUrl="https://sqs.eu-west-1.amazonaws.com/015206308301/daily-grind-queue2",
            MessageAttributes={
                     'Author': {
                     'StringValue': 'extract_csv',
                     'DataType': 'String'
                     }
                },
            MessageBody=json.dumps(message)
                    )
        print("Connected to message queue")
        print(f"Message sent for file_key = {file_key}") 
        
    except Exception as error:
        print(f"lambda_handler error occurred: {error}, for file_key = {file_key}")