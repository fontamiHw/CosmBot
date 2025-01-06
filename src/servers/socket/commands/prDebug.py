import logger 
class PrDebug(object):

    def __init__(self, user_db):
        self.user_db= user_db
        self.log = logger.getLogger("PrCommands")  
        
    def process_command(self, command, data):        
        match command:
            case "pr":
                self.log.info(f"Received command: {command}")
                return            
            case _:
                self.log.error(f"Unknown command received: {command}")