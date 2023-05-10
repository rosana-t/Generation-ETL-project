import psycopg2

def setup_rs_connection(rs_host, rs_port, rs_dbname, rs_user, rs_password):
    try:
        print(f"setup_rs_connection: new connection starting... {rs_host}")
        connect = psycopg2.connect(
                    host = rs_host,
                    port = rs_port,
                    dbname = rs_dbname,
                    user = rs_user,
                    password = rs_password)
            
        print(f"setup_rs_connection: ...connection achieved {rs_host}")
            
    except Exception as e:
        print(f"set_up_rs_connection: error occured + {e}")
    
    return connect



