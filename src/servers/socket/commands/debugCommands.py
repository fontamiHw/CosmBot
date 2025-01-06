import logger 
class DebugCommands(object):

    def __init__(self, user_db):
        self.user_db= user_db
        self.log = logger.getLogger("DebugCommands")  
        
    def process_command(self, command, data):        
        match command:
            case "debug-users":
                self.log.info(f"processing data: {data}")
                return            
            case _:
                self.log.error(f"Unknown command received: {command}")