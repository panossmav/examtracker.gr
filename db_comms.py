from dotenv import load_dotenv
import psycopg2 as pgsql
import os

load_dotenv()

conn = pgsql.connect(
    dbname = os.getenv("BASE_NAME"),
    dbuser = os.getenv("BASE_USER"),
    password = os.getenv("PWD"),
    host = os.getenv("HOST"),
    port = os.getenv("PORT")
)

cur = conn.cursor()

def add_student(f_n,l_n,age,cl):
    try:
        cur.execute("""
            INSERT INTO students (first_name,last_name,age,class_name)        
            VALUES (%s , %s , %s , %s)
                    """,(f_n,l_n,age,cl))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    
def add_class(name):
    try:
        cur.execute("""
            INSERT INTO classes (class_name)
            VALUES(%s)        
                    """,(name,))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    
def add_subject(name):
    try:
        cur.execute("""
            INSERT INTO subjects (subject_name)
            VALUES (%s)        
                    """,(name,))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
