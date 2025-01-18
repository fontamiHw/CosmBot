import logger 
from users.commonUser.users import User
from users.userException import UserException
class DebugCommands(object):

    def __init__(self, users: User):
        self.users= users
        self.log = logger.getLogger("DebugCommands")  
        
    def process_command(self, command, data):     
            match command:
                case "debug-users":
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
                case "debug-server":
                        self.log.info(f"processing data: {data}")
                        server_data = self.users.get_server_data(data['server'], data['admin'])
                        self.log.info(f"server data: {server_data}")
                        return {'servers' : server_data}                
                case _:
                    raise UserException(f"Unknown 'debug' path received: {command}")
                     