from dotenv import load_dotenv
import psycopg2 as pgsql
import os

load_dotenv()

global cur,conn

conn = pgsql.connect(
    dbname = os.getenv("BASE_NAME"),
    dbuser = os.getenv("BASE_USER"),
    password = os.getenv("PWD"),
    host = os.getenv("HOST"),
    port = os.getenv("PORT")
)

cur = conn.cursor()



class Student:
    def __init__(self,name,age,grade):
        self.name = name
        self.age = age
        self.grade = grade

    def get_avg_subj(self,subject):
        try:
            cur.execute("""
                SELECT AVG(mark) FROM exams WHERE name = %s AND subject = %s      
                        """,(self.name,subject))
            res = cur.fetchone()
            if res and res[0]:
                return round(res[0],2)
            else:
                raise Exception
        except Exception:
            return -1 
    
    def get_avg(self):
        try:
            cur.execute("""
                SELECT AVG(mark) FROM exams WHERE name = %s      
                        """,(self.name,))
            res = cur.fetchone()
            if res and res[0]:
                return round(res[0],2)
            else:
                raise Exception
        except Exception:
            return -1 
        
    def list_grades(self,subject):
            cur.execute("""
                SELECT mark FROM exams WHERE name = %s AND subject = %s        
                        """,(self.name,subject))
            res = cur.fetchall()
            res_list = [row[0] for row in res]
            return res_list

class mock_exam:
    def __init__(self,s_name,date,subject,mark):
        self.s_name = s_name
        self.date = date
        self.subject = subject
        self.mark = mark

    def log_exam(self):
        try:
            cur.execute("""
                INSERT INTO exams (mark,s_name,date,subject)
                    VALUES (%s,%s,%s,%s)        
                        """,(self.mark,self.s_name,self.date,self.subject))
            conn.commit()
        except Exception:
            conn.rollback()
    

class Grade:
    def __init__(self,name):
        self.name = name


class Backend_user:
    def __init__(self,username,pwd,user_type):
        self.username = username
        self.pwd = pwd
        self.user_type = user_type

    def log_in(self):
        try:
            cur.execute("""
                SELECT user_type FROM users WHERE username = %s AND pwd = %s        
                        """,(self.username,self.pwd))
            res = cur.fetchone()
            if res and res[0]:
                return res
            else:
                raise Exception
        except Exception:
            return 'Error!'


    