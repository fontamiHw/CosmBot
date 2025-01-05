

class BaseUser(object):

    def __init__(self, api, users_db, servers_db):
        self.users_db = users_db
        self.api = api
        self.servers_db = servers_db
        
    def send_user_message(self, email, msg):
        self.api.messages.create(toPersonEmail=email, markdown=msg)