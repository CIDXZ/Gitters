import socket

def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    host = '192.168.1.3'  # Listen on all available interfaces
    port = 53
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen()

    print(f"Server listening on {host}:{port}")

    try:
        while True:
            # Accept a connection from a client
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")

            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')

            if data.lower() == 'hello':
                # Send a reply to the client
                client_socket.sendall('hello'.encode('utf-8'))
            else:
                # Send an error message
                client_socket.sendall('hello'.encode('utf-8'))

            # Close the connection
            client_socket.close()
            print(f"Connection with {client_address} closed")

    except KeyboardInterrupt:
        print("Server shutting down.")

if __name__ == "__main__":
    start_server()
