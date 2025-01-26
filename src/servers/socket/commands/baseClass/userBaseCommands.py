
import logger 
from users.commonUser.users import User
from servers.socket.commands.baseClass.baseCommands import BaseCommands

class UserBaseCommands(BaseCommands):

    def __init__(self, users:User):
        self.users= users