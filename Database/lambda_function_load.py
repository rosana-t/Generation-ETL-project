import boto3
import psycopg2
import csv
import json
from app import *
from redshift_connection import setup_rs_connection
from redshift_load_functions import *



def lambda_handler(event, context):
    try:
    #     sqs_client = boto3.client('sqs')
    #     response = sqs_client.receive_message(
    #     QueueUrl="https://sqs.eu-west-1.amazonaws.com/015206308301/daily-grind-queue2",
    #     MaxNumberOfMessages=1,
    #     WaitTimeSeconds=10,
    # )

    #     print(f"Number of messages received: {len(response.get('Messages', []))}")

    #     for message in response.get("Messages", []):
    #         message_body = message["Body"]
    #     print(f"Message body: {json.loads(message_body)}")
    #     print(f"Receipt Handle: {message['ReceiptHandle']}")
        

    #     print(f"lambda_handler connecting to Redshift")
    #     print(f"lambda_handler connecting to Redshift; for file_key = {file_key}")

        x = event['Records'][0]['body']
    #   list_of_branches = x['branch']
    #   list_of_unique_product_dicts = x['product']
    #   data_for_orders_and_transaction_table = x['orders_and_transaction']
        print(x['branch'])
        print(x['product'])
        print(x['orders_and_transaction'])
        print(event)
        
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