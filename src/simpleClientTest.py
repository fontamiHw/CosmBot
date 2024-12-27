
import socket, time
import logger

log = logger.getLogger()

def main():        
    # Define the server address and port
    server_address = '10.58.1.10'  # Replace with the server's IP address
    server_port = 5000            # Replace with the server's port

    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect the socket to the server's address and port
        client_socket.connect((server_address, server_port))
        log.info(f"Connected to server at {server_address}:{server_port}")

        # Send data to the server
        message = "Hello, Server!"
        client_socket.sendall(message.encode('utf-8'))
        log.info(f"Sent: {message}")

        while True:
            print ("waiting data............")
            # Receive data from the server
            data = client_socket.recv(1024)
            log.info(f"Received: {data.decode('utf-8')}")

    finally:
        # Close the socket
        client_socket.close()
        log.info("Connection closed")

if __name__ == "__main__":
    main()