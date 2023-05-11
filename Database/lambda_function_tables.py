import json
import boto3
import psycopg2
from redshift_connection import setup_rs_connection
from redshift_tables_schema import create_branch_table, create_product_table, create_transaction_table, create_order_table


def lambda_handler(event, context):
    try:
        print(f"lambda_handler connecting to Redshift")
        
        ssm_client = boto3.client('ssm')
        parameter_details = ssm_client.get_parameter(Name='daily-grind-redshift-settings')
        redshift_details = json.loads(parameter_details['Parameter']['Value'])
            
        connection = setup_rs_connection(
                rs_host= redshift_details["host"],
                rs_port= redshift_details["port"],
                rs_dbname= redshift_details["database-name"],
                rs_user= redshift_details["user"],
                rs_password= redshift_details["password"])
                
        print(f"lambda_handler: connection created")
        
        create_branch_table(connection)
        print(f"lambda_handler: branch table created")
        
        create_product_table(connection)
        print(f"lambda_handler: product table created")
        
        create_transaction_table(connection)
        print(f"lambda_handler: transaction table created")
        
        create_order_table(connection)
        print(f"lambda_handler: orders table created")
        
        print("lambda_handler done")
    
    except Exception as error:
        print("lambda_handler error occurred: " + str(error))