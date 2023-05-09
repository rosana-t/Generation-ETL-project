import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
ps_host = os.environ.get("postgres_host")
ps_port = os.environ.get("postgres_port")
ps_user = os.environ.get("postgres_user")
ps_password = os.environ.get("postgres_pass")
ps_dbname = os.environ.get("postgres_db")


def setup_db_connection(connection_status):
    try:
        if connection_status == False:

            print("setup_db_connection: new connection starting...")
            connection_status = psycopg2.connect(host=ps_host, port = ps_port, user= ps_user,
                                             password= ps_password, dbname= ps_dbname)
            print("setup_db_connection: ...connection achieved")
        else:
            print("setup_dp_connection:...connection already exists")
    except Exception as e:
        print(e)
    
    return connection_status