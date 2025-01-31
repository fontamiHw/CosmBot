
import logger 
from servers.socket.commands.baseClass.baseCommands import BaseCommands
class PrCommands(BaseCommands):

    def __init__(self, jenkins):
        self.jenkins_processor = jenkins
        self.log = logger.getLogger("PrCommands")  
        
    def process_command(self, command, data):        
        if "prFile" in command:
            self.log.info(f"processing data: {data}")                
        elif "pr" in command:
            self.log.info(f"processing data: {data}")
            self.jenkins_processor.event_received(data)
        else:
            self.log.error(f"Unknown command received: {command}")