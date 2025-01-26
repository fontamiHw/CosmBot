

from webexteamssdk import WebexTeamsAPI
from webex_bot.webex_bot import WebexBot
from db.users import Users
from db.servers import Servers
from db.users import Users
class BaseUser(object):

    def __init__(self, api: WebexTeamsAPI, users_db:Users, servers_db:Servers, bot:WebexBot):
        self.users_db = users_db
        self.api = api
        self.servers_db = servers_db
        self.bot = bot
        
    def send_user_message(self, email, msg):
        self.api.messages.create(toPersonEmail=email, markdown=msg)                                            
                    
    def add_command(self, command):
        #add any user command
        self.bot.add_command(command)