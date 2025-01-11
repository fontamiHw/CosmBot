import logger 
class SystemCommands(object):

    def __init__(self, users):
        self.users= users
        self.log = logger.getLogger("SystemCommands")  
        
    def process_command(self, command, data):        
        self.log.info(f"processing data: {data}")
        # meeter etutti gli stati
        # del webex
        # del git
        # del Jenkins
        return {"Cosm-webex": "connected"}
    