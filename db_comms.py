from dotenv import load_dotenv
import psycopg2 as pgsql
import os

load_dotenv()

global cur, conn

conn = pgsql.connect(
    dbname=os.getenv("BASE_NAME"),
    user=os.getenv("BASE_USER"),
    password=os.getenv("PWD"),
    host=os.getenv("HOST"),
    port=os.getenv("PORT")
)
conn.set_client_encoding('UTF8')

cur = conn.cursor()


class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade

    def get_avg_subj(self, subject):
        try:
            # Διόρθωση: s_name αντί για name, subj αντί για subject
            cur.execute("""
                SELECT AVG(mark) FROM exams WHERE s_name = %s AND subj = %s      
                        """, (self.name, subject))
            res = cur.fetchone()
            if res and res[0] is not None:
                return round(res[0], 2)
            else:
                return -1
        except Exception as e:
            print(f"Error in get_avg_subj: {e}")
            return -1 
    
    def get_avg(self):
        try:
            # Διόρθωση: s_name αντί για name
            cur.execute("""
                SELECT AVG(mark) FROM exams WHERE s_name = %s      
                        """, (self.name,))
            res = cur.fetchone()
            if res and res[0] is not None:
                return round(res[0], 2)
            else:
                return -1
        except Exception as e:
            print(f"Error in get_avg: {e}")
            return -1 
        
    def list_grades(self, subject):
        try:
            # Διόρθωση: s_name αντί για name, subj αντί για subject
            cur.execute("""
                SELECT mark FROM exams WHERE s_name = %s AND subj = %s        
                        """, (self.name, subject))
            res = cur.fetchall()
            return [row[0] for row in res]
        except Exception as e:
            print(f"Error in list_grades: {e}")
            return []


class mock_exam:
    def __init__(self, s_name, date, subject, mark):
        self.s_name = s_name
        self.date = date
        self.subject = subject
        self.mark = mark

    def log_exam(self):
        try:
            # Διόρθωση: s_name, c_date, subj με βάση το CREATE TABLE σου
            cur.execute("""
                INSERT INTO exams (mark, s_name, c_date, subj)
                VALUES (%s, %s, %s, %s)        
                        """, (self.mark, self.s_name, self.date, self.subject))
            conn.commit()
            print("Η εγγραφή της εξέτασης έγινε επιτυχώς!")
        except Exception as e:
            conn.rollback()
            print(f"Σφάλμα κατά την καταχώρηση (log_exam): {e}")
    

class Grade:
    def __init__(self, name):
        self.name = name


class Backend_user:
    def __init__(self, username, pwd, user_type):
        self.username = username
        self.pwd = pwd
        self.user_type = user_type

    def log_in(self):
        try:
            cur.execute("""
                SELECT id FROM users WHERE username = %s AND pwd = %s        
                        """, (self.username, self.pwd))
            res = cur.fetchone()
        
            if res:
                # Επειδή το GUI περιμένει ο ρόλος να είναι στη θέση [0], 
                # επιστρέφουμε ένα tuple π.χ. ("Χρήστης",) για να μην κρασάρει η αρχική σελίδα
                return ("Εκπαιδευτικός",)
            else:
                print("Login failed: Λάθος username ή password.")
                return None
            
        except Exception as e:
            print(f"Database Error στο login: {e}")
            return 'Error!'