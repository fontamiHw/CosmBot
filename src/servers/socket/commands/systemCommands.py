import logger 
from users.commonUser.users import User
from servers.socket.commands.baseClass.userBaseCommands import UserBaseCommands
class SystemCommands(UserBaseCommands):

    def __init__(self, users:User):
        self.users= users
        self.log = logger.getLogger("SystemCommands")  
        
    def process_command(self, command, data):        
        self.log.info(f"processing data: {data}")
        # meeter etutti gli stati
        # del webex
        # del git
        # del Jenkins
        return {"Cosm-webex": "connected"}
    