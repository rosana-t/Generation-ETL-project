import boto3
import psycopg2
import csv
import json
from app import *
from redshift_connection import setup_rs_connection
from redshift_load_functions import *



def lambda_handler(event, context):
    try:
        print(f"lambda_handler connecting to Redshift; for file_key = {file_key}")
        
        ssm_client = boto3.client('ssm')
        parameter_details = ssm_client.get_parameter(Name='daily-grind-redshift-settings')
        redshift_details = json.loads(parameter_details['Parameter']['Value'])
        
        connection = setup_rs_connection(
            rs_host= redshift_details["host"],
            rs_port= redshift_details["port"],
            rs_dbname= redshift_details["database-name"],
            rs_user= redshift_details["user"],
            rs_password= redshift_details["password"])
        
        print(f"lambda_handler ready to load transformed data to Redshift; for file_key = {file_key}")
        
        load_into_branch_table(connection, list_of_branches)
        print(f"lambda_handler: data loaded to the branch table, for file_key = {file_key}")
        
        load_into_product_table(connection, list_of_unique_product_dicts)
        print(f"lambda_handler: data loaded to the product table, for file_key = {file_key}")
        
        load_into_transaction_table(connection, data_for_orders_and_transaction_table)
        print(f"lambda_handler: data loaded to the transaction table, for file_key = {file_key}")
        
        load_into_orders_table(connection, data_for_orders_and_transaction_table)
        print(f"lambda_handler: data loaded to the orders table, for file_key = {file_key}")
        
        print(f"all data loaded to Redshift, for file_key = {file_key}")
        
        print(f"lambda_handler done, for file_key = {file_key}")
        
    except Exception as error:
        print(f"lambda_handler error occurred: {error}, for file_key = {file_key}")