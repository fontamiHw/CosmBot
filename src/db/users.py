from db.db import DB
import logger


log = logger.getLogger()
class Users(DB):
    def __init__(self, file):
        super().__init__(file)
        # Create the users table
        success = self.create('''
            CREATE TABLE IF NOT EXISTS users (
            userId TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            fullName TEXT NOT NULL,
            admin BOOLEAN NOT NULL DEFAULT 0
            )
            ''')
        log.info(f"result of create {success}")

    def insert_user(self, userId, email, fullName, admin):
        self.execute_with_data('''
            INSERT INTO users (userId, email, fullName, admin) VALUES (?, ?, ?, ?)
            ''', (userId, email, fullName, admin))
        self.conn.commit()
    
    # Function to query by userId with partial match
    def query_by_userId(self, userId):
        cursor = self.execute_with_data('''
        SELECT * FROM users WHERE userId LIKE ?
        ''', ('%' + userId + '%',))
        return cursor.fetchall()
    
    # Function to query by email with partial match
    def query_by_email(self, email):
        cursor = self.execute_with_data('''
        SELECT * FROM users WHERE email LIKE ?
        ''', ('%' + email + '%',))
        return cursor.fetchall()
    
    # Function to remove a user by userId
    def remove_user_by_userId(self, userId):
        self.execute_with_data('''
        DELETE FROM users WHERE userId=?
        ''', (userId,))
        self.conn.commit()
    
    # Function to remove a user by email
    def remove_user_by_email(self, email):
        self.execute_with_data('''
        DELETE FROM users WHERE email=?
        ''', (email,))
        self.conn.commit()
        
    def is_admin_by_userId(self, userId):
        result = self.take_one('''
        SELECT admin FROM users WHERE userId=?
        ''', (userId,))
        return result[0] if result else False

    def is_admin_by_email(self, email):
        result = self.take_one('''
        SELECT admin FROM users WHERE email=?
        ''', (email,))
        return result[0] if result else False 
    
    def get_email_by_userId(self, userId):
        result = self.take_one('''
        SELECT email FROM users WHERE userId=?
        ''', (userId,))
        return result[0] if result else None
    
