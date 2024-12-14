import socket

def start_server(host='localhost', port=12345):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the host and port
    server_socket.bind((host, port))
    
    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")
    
    while True:
        # Accept a connection
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        
        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')
        print(f"Received: {data}")
        
        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    start_server()