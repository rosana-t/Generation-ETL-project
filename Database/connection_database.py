import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
HOST = os.environ.get("postgres_host")
PORT = os.environ.get("postfres_port")
USER = os.environ.get("postgres_user")
PASSWORD = os.environ.get("postgres_pass")
WAREHOUSE_DB_NAME = os.environ.get("postgres_db")

def setup_db_connection(ps_host, ps_port, ps_dbname, ps_user, ps_password):
    
    conn = psycopg2.connect(
        host=ps_host,
        port = ps_port,
        database= ps_dbname,
        user= ps_user,
        password= ps_password
    )
    
    return conn

y = setup_db_connection(
    ps_host = HOST,
    ps_port = PORT,
    ps_dbname = WAREHOUSE_DB_NAME,
    ps_user = USER,
    ps_password = PASSWORD
)

print(y)