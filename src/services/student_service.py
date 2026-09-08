from db.db_connection import connect_db

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
        #TODO: when db schema is made
        return True
    except:
        return False
    finally:
        conn.close()
    