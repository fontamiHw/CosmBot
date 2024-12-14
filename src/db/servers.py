import logger
from db.db import DB

log = logger.getLogger()

class Servers(DB):
    JENKINS="jenkins"
    GIT="git"
    SERVER_TYPE_POS = 0
    URL_POS = 1
    USER_NAME_POS= 2
    PROJECT_POS = 3
    TOKEN_POS = 4

    def __init__(self, file):
        super().__init__(file)
        # Create the users table
        self.create('''
            CREATE TABLE IF NOT EXISTS users (
            user_name TEXT PRIMARY KEY
            )
            ''')
        # Create the services table with a foreign key reference to the users table
        self.create('''
            CREATE TABLE IF NOT EXISTS services (
            type TEXT PRIMARY KEY,
            url TEXT NOT NULL,
            user_name TEXT NOT NULL,
            project TEXT NOT NULL,
            token TEXT NOT NULL,
            FOREIGN KEY (user_name) REFERENCES users(user_name)
            )
            ''')

    # Function to check if a user is already present
    def is_user_present(self, user_name):
        cursor = self.execute_with_data('''
        SELECT 1 FROM users WHERE user_name = ?
        ''', (user_name,))
        present=cursor.fetchone()
        return present is not None

    # Function to add a new user
    def add_user(self, user_name):
        if not self.is_user_present(user_name):
            self.execute_with_data('''
            INSERT INTO users (user_name) VALUES (?)
            ''', (user_name,))

    # Function to add a new service for a user
    def add_service(self, user_name, url, project, token, server_name):
        self.execute_with_data('''
        INSERT INTO services (type, url, user_name, project, token) VALUES (?, ?, ?, ?, ?)
        ''', (server_name, url, user_name, project, token))

    # Function to update the URL, project, and token for a specific service
    def update_service(self, url, new_project, new_token):
        self.execute_with_data('''
        UPDATE services SET project = ?, token = ? WHERE url = ?
        ''', (new_project, new_token, url))

    # Function to get all services for a specific user
    def get_services_by_user(self, user_name):
        cursor = self.execute_with_data('''
        SELECT * FROM services WHERE user_name = ?
        ''', (user_name,))
        return cursor.fetchall()    

    # old code 
    # Function to insert user details
    def insert_server_user(self, user_name, url, project, token, server_name):
        self.add_user(user_name)
        self.add_service(user_name, url, project, token, server_name)
        self.conn.commit()


    # Function to query by user_name and type with partial match
    def query_server_data_by_user_name_and_type(self, user_name, server_type):
        cursor = self.execute_with_data('''
        SELECT * FROM services WHERE user_name LIKE ? AND type LIKE ?
        ''', ('%' + user_name + '%', '%' + server_type + '%'))
        return cursor.fetchall()


    # Function to query by user_name with partial match
    def are_servers_configurated(self, user_name):
        cursor = self.execute_with_data('''
        SELECT * FROM services WHERE user_name LIKE ?
        ''', ('%' + user_name + '%',))
        services = cursor.fetchall()
        return len(services) >= 2
    
    