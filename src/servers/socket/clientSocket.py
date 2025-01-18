import socket, time
import threading
import logger 
import json
from servers.socket.commands.prCommands import PrCommands
from servers.socket.commands.debugCommands import DebugCommands
from servers.socket.commands.systemCommands import SystemCommands
from users.userException import UserException

class ClientSocket:

    def __init__(self, config, jenkins, user_db):
        self.config = config
        self.log = logger.getLogger("ClientSocket")  
        # Define the server address and port
        self.host = config['host'] # Replace with the server's IP address
        self.server_port = config['port']            # Replace with the server's port
        
        self.jenkins_processor = jenkins
        self.pr_commands = PrCommands(jenkins)
        self.pr_debug = DebugCommands(user_db)
        self.system_debug = SystemCommands(user_db)

        # Create a TCP/IP socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_thread = threading.Thread(target=self.read_data)
        self.main_stop_event = threading.Event()
        self.main_thread.start()
        self.max_connection = config['maxRetryError']

    def read_data(self):
        connected = False
        while not connected:
            try:
                self.log.info(f"Connecting {self.host}:{self.server_port}")
                # Connect the socket to the server's address and port
                self.client_socket.connect((self.host, self.server_port))
                connected = True
                self.log.info("Connected !!!!!!!!!!!!!")

            except Exception as e:
                #decrement only if the config does not report -1 that measn infinite retry
                if self.max_connection > 0:
                    self.max_connection -= 1
                self.log.error(f"connection failed due to : {e}. \n retry again {self.max_connection} time.")
                time.sleep(self.config['secErrorWait'])
                if self.max_connection == 0:
                    # Close the socket
                    self.client_socket.close()
                    self.log.info("Connection closed")
                    return
                    
        while True:
            self.log.info("Waiting data.....")
            try:
                # Receive data from the server
                data = self.client_socket.recv(1024).decode('utf-8')                
                self.log.info(f"Received: {data}")
                
                # prepare the data to be processed
                data_json = json.loads(data)
                command = data_json['command']
                del data_json['command']  # remove all those elements are not part of data
                send, data = self.process_command(command, data_json)
                if send:
                    self.client_socket.send(json.dumps(data).encode('utf-8'))
                
            except Exception as e:
                self.log.error(f"Error due to : {e}.")
                
                
    def process_command(self, command, data):  
        self.log.info(f"Received command: {command}") 
        answer = {}
        ret = False
        
        try: 
            if "debug" in command:
                answer = self.pr_debug.process_command(command, data)
            elif "pr" in command:
                self.pr_commands.process_command(command, data)
            elif "system" in command:
                answer = self.system_debug.process_command(command, data)
            else:
                self.log.error(f"Unknown command received: {command}")
                raise UserException(f"Unknown command received: {command}")
        except UserException as e:
            answer = {"error": e.get_message()}            

        if answer:
            ret = True
            
        return ret, answer
