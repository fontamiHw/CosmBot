
import logger 
class PrCommands(object):

    def __init__(self, jenkins):
        self.jenkins_processor = jenkins
        self.log = logger.getLogger("PrCommands")  
        
    def process_command(self, command, data):        
        match command:
            case "pr":
                self.jenkins_processor.event_received(data)
                return
            case "prFile":
                return
            case _:
                self.log.error(f"Unknown command received: {command}")