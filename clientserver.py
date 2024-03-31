import socket

def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = '127.0.0.1'
    port = 12345

    # Bind to the port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    while True:
        # Establish a connection with the client
        client_socket, addr = server_socket.accept()
        print(f"Got connection from {addr}")

        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')
        print(f"Received data from client: {data}")

        # Convert the data to uppercase
        data_upper = data.upper()

        # Send back the uppercase data to the client
        client_socket.sendall(data_upper.encode('utf-8'))

        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    start_server()


