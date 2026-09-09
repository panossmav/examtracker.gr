from db.db_connection import connect_db
from src.hasher import hash_password
from src.models.user import User

def log_in(username,password):
    conn , cur = connect_db()
    try:
        cur.execute(
            """
            SELECT role,is_active FROM users WHERE username = %s AND password = %s 
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

def create_account(username,password,role,is_active = 'active'):
    conn , cur = connect_db()
    try:
        cur.execute(
            """
            INSERT INTO users (username,password,role,is_active) VALUES (%s,%s,%s,%s)
            
            """
        ,((username,password,role,is_active)))
        conn.commit()
        return cur.lastrowid()
    except Exception:
        conn.rollback()
    finally:
        conn.close()
    
#TODO check username availability
