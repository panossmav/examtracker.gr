from db.db_connection import connect_db
class Subject:
    def __init__(self,name,classrooms,students,teachers,id):
        self.name = name
        self.classrooms = classrooms 
        self.students = students #fetch from db!!
        self.teachers = teachers
        self.id = id


    def add_classroom(self,classroom_name):
        conn, cur = connect_db()
        try:
            if classroom_name in self.classrooms:
                raise Exception
            self.classrooms.append(classroom_name)
            cur.execute(
                "UPDATE subjects SET classrooms = %s WHERE id = %s"
            (self.classrooms,self.id)) #TODO: Add student changes
            conn.commit()
        except Exception:
            conn.rollback()
        finally:
            conn.close()

    #TODO: def remove_classroom(self)
    #TODO: def add_teacher(self,t_name)
    #TODO: def remove_teacher(self,t_name)
    #TODO: def add_db(self)

    def get_id(self):
        conn,cur =connect_db()
        try:
            cur.execute(
                """
                SELECT id FROM subjects WHERE name = %s AND classrooms = %s AND students %s and teachers = %s
                """
            ,(self.name,self.classrooms,self.students,self.teachers))
            res = cur.fetchone()
            if res is None:
                raise Exception
            self.id = res[0]
            return self.id
        except Exception:
            return None
        finally:
            conn.close()
            
        

    