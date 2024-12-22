import socket
import json
import threading
import time
from CosmException import CosmException

class Client:
    def __init__(self, config, log):
        self.log = log
        self.config = config
        self.start_client()
    
    
    def add_jenkins(self, jenkins):
        self.jenkins= jenkins
        
    
    def start_client(self):
        host = self.config['socket']['host']
        port = self.config['socket']['port']
        server_found = False
        max_retry = self.config['socket']['maxRetryError']
        
        while not server_found:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                # Connect to the server
                self.client_socket.connect((host, port))
                self.log.info(f"Connected to server at {host}:{port}")

                # Spawn a task (e.g., a long-running process)
                task_thread = threading.Thread(target=self.handle_task)
                task_thread.start()

                # Wait for the task to complete
                task_thread.join()

            except Exception as e:
                self.log.error(f"Exception {e}\n Wait ")
                time.sleep(self.config['socket']['secErrorWait'])
                max_retry-=1
                if max_retry==0:
                    raise CosmException("Cannot connect on a Server Socket application. ")
 



    def handle_task(self):
        # Simulate some long-running task
        self.log.info("Task is running...")
    
        while True:
            max_retry = self.config['socket']['maxRetryError']
            try:
                # Receive the JSON data from the server
                data = self.client_socket.recv(1024)  # buffer size 1024 bytes
    
                # Deserialize JSON data
                self.log.info (f"Retrieved {len(data)} characters")
                received_data = json.loads(data.decode("utf-8"))
                self.log.info(f"Received JSON data: {received_data}")
            except Exception as e:
                self.log.error(f"Exception {e}\n Wait ")
                time.sleep(self.config['socket']['secErrorWait'])
                max_retry-=1
                if max_retry==0:
                    self.client_socket.close()
                    raise CosmException("Cannot connect on a Server Socket application. ")

        self.log.info("Task completed.")
        
        
            
            
        