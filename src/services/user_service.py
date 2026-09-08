from src.db_connection import connect_db
from src.hasher import hash_password
from src.models.users import User

def log_in(username,password):
    conn , cur = connect_db()
    try:
        cur.execute(
            """
            SELECT role,is_active FROM users WHERE username = %s AND pwd = %s 
            """
        ,(username,hash_password(password)))
        res = cur.fetchone()
        
        if res is None: 
            raise Exception
        else: 
            return User(username,password,res[0],res[1])
    except Exception:
        return 'Error!'
    finally:
        conn.close()

#TODO sign up 
#TODO check username availability
