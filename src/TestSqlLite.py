import sqlite3
import json

# JSON data
json_data = '''
{
  "servers": [
    {
      "admin": "mfontane",
      "servers": [
        {
          "type": "git",
          "url": "http://example.com/api1",
          "project": "svo",
          "token": "abc123"
        },
        {
          "type": "jenkins",
          "url": "http://example.com/api2",
          "project": "views/changes",
          "token": "def456"
        }
      ]
    }
  ]
}
'''

# Parse the JSON data
data = json.loads(json_data)

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('tests.db')
cursor = conn.cursor()

# Create the users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_name TEXT PRIMARY KEY
)
''')

# Create the services table with a foreign key reference to the users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS services (
    url TEXT PRIMARY KEY,
    user_name TEXT NOT NULL,
    type TEXT NOT NULL,
    project TEXT NOT NULL,
    token TEXT NOT NULL,
    FOREIGN KEY (user_name) REFERENCES users(user_name)
)
''')

# Insert data into the tables
for server in data['servers']:
    admin = server['admin']
    
    # Insert admin into users table
    cursor.execute('''
    INSERT OR IGNORE INTO users (user_name) VALUES (?)
    ''', (admin,))
    
    for service in server['servers']:
        url = service['url']
        service_type = service['type']
        project = service['project']
        token = service['token']
        
        # Insert service into services table
        cursor.execute('''
        INSERT OR REPLACE INTO services (url, user_name, type, project, token) VALUES (?, ?, ?, ?, ?)
        ''', (url, admin, service_type, project, token))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data inserted successfully.")