import socket, time
import threading

class ClientSocket:

    def __init__(self, config, log):
        self.config = config
        self.log = log
        # Define the server address and port
        self.host = config['host'] # Replace with the server's IP address
        self.server_port = config['port']            # Replace with the server's port

        # Create a TCP/IP socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_thread = threading.Thread(target=self.read_data)
        self.main_stop_event = threading.Event()
        self.main_thread.start()
        self.max_connection = config['maxRetryError']

    def read_data(self):
        while True:
            try:
                self.log.info(f"Connectiong {self.host}:{self.server_port}")
                # Connect the socket to the server's address and port
                self.client_socket.connect((self.host, self.server_port))

                # Receive data from the server
                data = self.client_socket.recv(1024)
                self.info.trace(f"Received: {data.decode('utf-8')}")

            except Exception as e:
                self.max_connection -= 1
                self.log.error(f"connection failed due to : {e}. \n retry again {self.max_connection} time.")
                time.sleep(self.config['secErrorWait'])
                if self.max_connection == 0:
                    # Close the socket
                    self.client_socket.close()
                    self.log.info("Connection closed")