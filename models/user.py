from utils.database import get_connection
import hashlib

class UserModel:
    @staticmethod
    def create_user(username, email, password, role="user"):
        # hash the password before saving
        hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()

        con = get_connection()
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO users (email, username, password, role) VALUES (%s, %s, %s, %s)",
            (email, username, hashed_password, role)
        )
        con.commit()
        user_id = cursor.lastrowid
        cursor.close()
        con.close()
        return user_id

    
    @staticmethod
    def update_user(user_id, username, email):
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("UPDATE users SET username = %s, email = %s WHERE user_id = %s", 
                       (username, email, user_id))
        con.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        con.close()
        return rows_affected > 0
    
    @staticmethod
    def delete_user(user_id):
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        con.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        con.close()
        return rows_affected > 0