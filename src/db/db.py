import sqlite3


class DB(object):
    NAME_POS=0
    EMAIL_POS=1
    ADMIN_POS=2

    def __init__(self, file):
        # Connect to SQLite database (or create it if it doesn't exist)
        self.file = file
        
    def open(self):
        self.conn = sqlite3.connect(self.file)
        return self.conn.cursor()
        
    def create(self, table):
        return self.open().execute(table)
        
    def execute_with_data(self, command, data):
        cursor = self.open()
        return cursor.execute(command, data)
        
    def execute(self, command):
        cursor = self.open()
        return cursor.execute(command)
        
    def take_one(self, command, data):
        cursor = self.open()
        cursor.execute(command, data)
        
        return cursor.fetchone()
    
    