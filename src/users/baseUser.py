

class BaseUser(object):

    def __init__(self, api, users_db, servers_db, bot):
        self.users_db = users_db
        self.api = api
        self.servers_db = servers_db
        self.bot = bot
        
    def send_user_message(self, email, msg):
        self.api.messages.create(toPersonEmail=email, markdown=msg)                                            
                    
    def add_command(self, command):
        #add any user command
        self.bot.add_command(command)