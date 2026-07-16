from dotenv import load_dotenv
from datetime import date as _date
import psycopg2 as pgsql
import os
import string

load_dotenv()


def _months_elapsed(enroll_date_str):
    # Μετράει τον μήνα εγγραφής ως μήνα 1, μέχρι και τον τρέχοντα μήνα.
    try:
        y, m, _ = [int(p) for p in enroll_date_str.split("-")]
        today = _date.today()
        return (today.year - y) * 12 + (today.month - m) + 1
    except Exception as e:
        print(f"Error in _months_elapsed: {e}")
        return -1

global cur, conn
db_url = os.getenv("DATABASE_URL")
conn = pgsql.connect(db_url)
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
                        """, (self.name.upper(), subject))
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
                        """, (self.name.upper(),))
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
                        """, (self.name.upper(), subject))
            res = cur.fetchall()
            return [row[0] for row in res]
        except Exception as e:
            print(f"Error in list_grades: {e}")
            return []

    def save(self, c_name, enroll_date):
        try:
            # Δεν υπάρχει πεδίο ημ/νίας γέννησης στο UI, οπότε αποθηκεύουμε
            # την ηλικία στο dob (NOT NULL) για να μην αλλάξουμε το schema.
            cur.execute("""
                INSERT INTO students (s_name, dob, c_name, enroll_date)
                VALUES (%s, %s, %s, %s)
                        """, (self.name.upper(), str(self.age), c_name, enroll_date))
            conn.commit()
            print("Η εγγραφή του μαθητή έγινε επιτυχώς!")
        except Exception as e:
            conn.rollback()
            print(f"Σφάλμα κατά την καταχώρηση (Student.save): {e}")

    def get_total_paid(self):
        try:
            cur.execute("""
                SELECT SUM(amount) FROM payments WHERE s_name = %s
                        """, (self.name.upper(),))
            res = cur.fetchone()
            if res and res[0] is not None:
                return round(res[0], 2)
            else:
                return 0
        except Exception as e:
            print(f"Error in get_total_paid: {e}")
            return -1

    def list_payments(self):
        try:
            cur.execute("""
                SELECT c_date, amount FROM payments WHERE s_name = %s ORDER BY c_date
                        """, (self.name.upper(),))
            res = cur.fetchall()
            return [(row[0], row[1]) for row in res]
        except Exception as e:
            print(f"Error in list_payments: {e}")
            return []

    def get_balance(self):
        try:
            cur.execute("""
                SELECT c_name, enroll_date FROM students WHERE s_name = %s
                        """, (self.name.upper(),))
            row = cur.fetchone()
            if not row or not row[0] or not row[1]:
                return (-1, -1, -1)
            c_name, enroll_date = row

            cur.execute("""
                SELECT student_amount FROM grade WHERE c_name = %s
                        """, (c_name.upper(),))
            grow = cur.fetchone()
            if not grow:
                return (-1, -1, -1)
            monthly_fee = grow[0]

            months = _months_elapsed(enroll_date)
            if months < 1:
                months = 1

            expected_total = monthly_fee * months
            paid = self.get_total_paid()
            if paid == -1:
                paid = 0
            balance = expected_total - paid
            return (expected_total, paid, balance)
        except Exception as e:
            conn.rollback()
            print(f"Error in get_balance: {e}")
            return (-1, -1, -1)


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
                        """, (self.mark, self.s_name.upper(), self.date, self.subject))
            conn.commit()
            print("Η εγγραφή της εξέτασης έγινε επιτυχώς!")
        except Exception as e:
            conn.rollback()
            print(f"Σφάλμα κατά την καταχώρηση (log_exam): {e}")


class payment:
    def __init__(self, s_name, date, amount):
        self.s_name = s_name
        self.date = date
        self.amount = amount

    def log_payment(self):
        try:
            cur.execute("""
                INSERT INTO payments (s_name, amount, c_date)
                VALUES (%s, %s, %s)
                        """, (self.s_name.upper(), self.amount, self.date))
            conn.commit()
            print("Η καταχώρηση της πληρωμής έγινε επιτυχώς!")
        except Exception as e:
            conn.rollback()
            print(f"Σφάλμα κατά την καταχώρηση (log_payment): {e}")


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
        