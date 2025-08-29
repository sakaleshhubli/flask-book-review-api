from utils.database import get_connection
import hashlib

class UserModel:
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @staticmethod
    def get_by_id(user_id):
        con = get_connection()
        cursor = con.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            con.close()


    @staticmethod
    def create_user(username, email, password, role="user"):
        hashed_password = UserModel.hash_password(password)

        con = get_connection()
        cursor = con.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
                (username, email, hashed_password, role)
            )
            con.commit()
            user_id = cursor.lastrowid
            return user_id
        except Exception as e:
            con.rollback()
            raise e
        finally:
            cursor.close()
            con.close()

    @staticmethod
    def update_user(user_id, username=None, email=None, password=None, role=None):
        """Update user details. Only provided fields will be updated."""
        fields = []
        values = []

        if username:
            fields.append("username = %s")
            values.append(username)
        if email:
            fields.append("email = %s")
            values.append(email)
        if password:
            fields.append("password = %s")
            values.append(UserModel.hash_password(password))
        if role:
            fields.append("role = %s")
            values.append(role)

        if not fields:
            return False  # nothing to update

        values.append(user_id)

        query = f"UPDATE users SET {', '.join(fields)} WHERE user_id = %s"

        con = get_connection()
        cursor = con.cursor()
        try:
            cursor.execute(query, tuple(values))
            con.commit()
            return cursor.rowcount > 0
        except Exception as e:
            con.rollback()
            raise e
        finally:
            cursor.close()
            con.close()

    @staticmethod
    def delete_user(user_id):
        con = get_connection()
        cursor = con.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            con.commit()
            return cursor.rowcount > 0
        except Exception as e:
            con.rollback()
            raise e
        finally:
            cursor.close()
            con.close()
