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
            self.classrooms.remove(classroom_name)
            conn.rollback()
        finally:
            conn.close()

    def remove_classroom(self,classroom_name):
        conn , cur = connect_db()
        try:
            if classroom_name not in self.classrooms:
                raise Exception
            self.classrooms.remove(classroom_name)
            cur.execute(
                """
                UPDATE subjects SET classrooms = %s WHERE id = %s
                """
            ,(self.classrooms,self.id))
            conn.commit()
            return True
        except Exception:
            conn.rollback()
        finally:
            conn.close()

    def add_teacher(self,t_name):
        conn,cur = connect_db()
        try:
            if t_name in self.teachers:
                raise Exception
            cur.execute(
                """
                UPDATE subjects SET teachers = %s WHERE id = %s
                """
            ,(self.teachers,self.id))
            conn.commit()
        except Exception:
            conn.rollback()
            


    #TODO: def remove_teacher(self,t_name):

    def add_to_db(self):
        conn,cur = connect_db()
        try:
            cur.execute(
                """
                INSERT into subjects (name,classrooms,students,teachers) VALUES (%s,%s,%s,%s)
                """
            ,(self.name,self.classrooms,self.students,self.teachers))
            conn.commit()
            self.id = cur.fetchone()[0]
            return True
        except:
            conn.rollback()
        finally:
            conn.close()

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
            
        

    