from db.db_connection import connect_db
from src.models.student import Student

def generate_object_student(student_id):
    conn , cur = connect_db()
    try:
        cur.execute(
            """
            SELECT * FROM users WHERE id = %s
            """
        ,(student_id,))
        res = cur.fetchall()
        if res is None:
            raise Exception
        return Student(res[1],res[2],res[3],res[4],res[5],res[6],res[7])
    except:
        return None
    finally:
        conn.close()

