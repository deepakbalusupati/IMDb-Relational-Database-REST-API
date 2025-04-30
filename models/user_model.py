from werkzeug.security import generate_password_hash, check_password_hash
from database.db_connection import mysql

class UserModel:
    @staticmethod
    def create_user(username, email, password):
        hashed_password = generate_password_hash(password)
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
        """, (username, email, hashed_password))
        user_id = cursor.lastrowid
        mysql.connection.commit()
        cursor.close()
        return user_id

    @staticmethod
    def get_user_by_username(username):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        return user

    @staticmethod
    def get_user_by_email(email):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        return user

    @staticmethod
    def get_user_by_id(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return user

    @staticmethod
    def verify_user(username, password):
        user = UserModel.get_user_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            return user
        return None

    @staticmethod
    def update_user(user_id, user_data):
        cursor = mysql.connection.cursor()
        
        if 'password' in user_data:
            hashed_password = generate_password_hash(user_data['password'])
            cursor.execute("""
                UPDATE users 
                SET username = %s, email = %s, password_hash = %s
                WHERE user_id = %s
            """, (user_data['username'], user_data['email'], 
                  hashed_password, user_id))
        else:
            cursor.execute("""
                UPDATE users 
                SET username = %s, email = %s
                WHERE user_id = %s
            """, (user_data['username'], user_data['email'], user_id))
        
        mysql.connection.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        return affected_rows > 0

    @staticmethod
    def delete_user(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        mysql.connection.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        return affected_rows > 0