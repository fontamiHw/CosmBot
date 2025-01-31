import logger 
from users.commonUser.users import User
from users.userException import UserException
from servers.socket.commands.baseClass.userBaseCommands import UserBaseCommands

class DebugCommands(UserBaseCommands):

    def __init__(self, users:User):
        super().__init__(users)
        self.log = logger.getLogger("DebugCommands")  
        
    def process_command(self, command, data):     
        if "debug-users" in command:
            self.log.info(f"processing data: {data}")
            users = []
            msg="these are the configured"
            if (data['only_admin'] == True):
                users = self.users.get_admins()
                msg = f"{msg} admins"
            else :
                users = self.users.get_users()
                msg = f"{msg} users"
            self.log.info(f"{msg} {users}")
            return {"users": users}
        elif "debug-server" in command:
            self.log.info(f"processing data: {data}")
            server_data = self.users.get_server_data(data['server'], data['admin'])
            self.log.info(f"server data: {server_data}")
            return {'servers' : server_data}                
        else:
            raise UserException(f"Unknown 'debug' path received: {command}")
                     