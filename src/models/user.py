from src.hasher import hash_password
from db.db_connection import connect_db


class User:
    def __init__(self,username,pwd,role,is_active):
        self.username = username
        self.pwd = hash_password(pwd)
        self.role = role
        self.is_active=is_active

    def update_self_password(self,old_password,new_password):
        conn , cur = connect_db()
        try:
            if hash_password(old_password) != self.pwd:
                raise Exception
            cur.execute(
                """
                UPDATE users SET pwd = %s WHERE username = %s
                """
            ,(hash_password(new_password),self.username))
            conn.commit()
            self.pwd = hash_password(new_password)
            conn.close()
            return True
        except Exception:
            conn.rollback()
            conn.close()
            return False

    def deactivate_account(self):
        conn , cur = connect_db()
        try:
            cur.execute(
                """
                UPDATE users SET is_active = 'deactive' WHERE username = %s
                """
            ,(self.username,))
            conn.commit()
            self.is_active = 'deactive'
            conn.close()
            return True
        except Exception:
            conn.rollback()
            conn.close()
            return False

