from db.db_connection import connect_db

class Student:
    def __init__(self,name,dob,classroom,subjects,status,phone,parent):
        self.name = name
        self.dob = dob
        self.classroom = classroom
        self.subject = subjects
        self.status = status
        self.phone = phone
        self.parent = parent

    def update_info(self,name,dob,classroom,subjects,status,phone,parent,id):
        conn , cur = connect_db()
        try:
            cur.execute(
                """
                UPDATE students SET name = %s, dob = %s , classroom = %s,subjects=%s,status=%s,phone=%s,parent=%s 
                """
            ,(name,dob,classroom,subjects,status,phone,parent))