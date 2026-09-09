from db.db_connection import connect_db
from src.services.student_service import *
class Student:
    def __init__(self,name,dob,classroom,subjects,status,phone,parent):
        self.name = name
        self.dob = dob
        self.classroom = classroom
        self.subjects = subjects
        self.status = status
        self.phone = phone
        self.parent = parent
        self.id = fetch_student_id(self.name)


    def update_info(self,name,dob,classroom,subjects,status,phone,parent,id):
        conn , cur = connect_db()
        try:
            cur.execute(
                """
                UPDATE students SET name = %s, dob = %s , classroom = %s,subjects=%s,status=%s,phone=%s,parent=%s WHERE id = %s
                """
            ,(name,dob,classroom,subjects,status,phone,parent,fetch_student_id(self.name)))
            conn.commit()
            self.name = name
            self.dob = dob
            self.classroom = classroom
            self.subjects = subjects
            self.status = status
            self.phone = phone
            self.parent = parent
        except Exception: 
            conn.rollback()
        finally:
            conn.close()

    def get_info(self):
        return {
            "Student Name: ":self.name,
            "Date of Birth: ":self.dob,
            "Enrolled Classroom: ":self.classroom,
            "Enrolled Subjects: ":self.subjects,
            "Status: ":self.status,
            "Phone number: ":self.phone,
            "Parent number: ":self.parent
        }

    def add_subject(self,subject_name):
        conn , cur = connect_db()
        try: 
            self.subjects.append(subject_name)
            cur.execute(
                """
                UPDATE students SET subjects = %s WHERE id = %s
                """
            ,(self.subjects,fetch_student_id(self.name)))
            conn.commit()
        except Exception:
            conn.rollback()
            if subject_name in self.subjects:
                self.subjects.remove(subject_name)
        finally:
            conn.close()

def remove_subject(self,subject_name):
    conn,cur = connect_db()
    try:
        for subject in self.subjects:
            if subject == subject_name:
                self.subjects.remove(subject)
        cur.execute(
            """
            UPDATE students SET subjects = %s WHERE id = %s
            """
        ,(self.subjects,fetch_student_id(self.name)))
    except Exception:
        if subject_name not in self.subjects:
            self.subjects.append(subject_name)
        conn.rollback()
    finally:
        conn.close()

