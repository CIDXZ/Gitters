import socket
import os

def handle_client(server_socket):
    while True:
        # Receive the requested file name from the client
        file_name, client_address = server_socket.recvfrom(1024)
        file_name = file_name.decode()

        try:
            # Read the content of the file
            with open(file_name, 'rb') as file:
                data = file.read()
            # Send the file content to the client
            server_socket.sendto(data, client_address)
        except FileNotFoundError:
            # If file not found, send an error message
            server_socket.sendto("File not found".encode(), client_address)

def main():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    server_socket.bind(('localhost', 59))

    print("Server listening on port 59...")

    try:
        while True:
            # Create a new thread to handle each client
            handle_client(server_socket)
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
