from db.db_connection import connect_db
from src.services.student_service import *
class Student:
    def __init__(self,name,dob,classroom,subjects,status,phone,parent,id):
        self.name = name
        self.dob = dob
        self.classroom = classroom
        self.subjects = subjects
        self.status = status
        self.phone = phone
        self.parent = parent
        self.id = id


    def update_info(self,name,dob,classroom,subjects,status,phone,parent,id):
        conn , cur = connect_db()
        try:
            cur.execute(
                """
                UPDATE students SET name = %s, dob = %s , classroom = %s,subjects=%s,status=%s,phone=%s,parent=%s WHERE id = %s
                """
            ,(name,dob,classroom,subjects,status,phone,parent,id))
            conn.commit()
            self.name = name
            self.dob = dob
            self.classroom = classroom
            self.subjects = subjects
            self.status = status
            self.phone = phone
            self.parent = parent
            self.id = id
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

    def register_db(self):
        conn, cur = connect_db()
        try:
            cur.execute(
                """
                INSERT into STUDENTS (name,dob,classroom,subjects,status,parent,phone) VALUES (%s,%s,%s,%s,%s,%s,%s)
                """
            ,(self.name,self.dob,self.classroom,self.subjects,self.status,self.parent,self.phone))
            conn.commit()
            self.id = cur.fetchone()[0]
        except Exception:
            conn.rollback()
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
            ,(self.subjects,self.id))
        except Exception:
            if subject_name not in self.subjects:
                self.subjects.append(subject_name)
            conn.rollback()
        finally:
            conn.close()

    def get_id(self):
        conn,cur = connect_db()
        try:
            cur.execute(
                """
                SELECT id FROM students WHERE name = %s AND dob = %s AND classroom = %s AND subjects = %s AND status = %s AND parent = %s AND phone =%s
                """
            ,(self.name,self.dob,self.classroom,self.subjects,self.status,self.parent,self.phone))
            res = cur.fetchone()
            if res is None:
                raise Exception
            self.id = res[0]
            return self.id
        except Exception:
            return None
        finally:
            conn.close() 



