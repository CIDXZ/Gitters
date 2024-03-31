import socket
import threading
import os

def handle_client(client_socket):
    while True:
        # Receive the requested file name from the client
        file_name = client_socket.recv(1024).decode()
        if not file_name:
            break
        
        try:
            # Read the content of the file
            with open(file_name, 'r') as file:
                data = file.read()
            # Send the file content to the client
            client_socket.send(data.encode())
        except FileNotFoundError:
            # If file not found, send an error message
            client_socket.send("File not found".encode())
    
    client_socket.close()

def main():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the port
    server_socket.bind(('localhost', 57))
    # Set the server to listen for incoming connections
    server_socket.listen(5)

    print("Server listening on port 57...")

    try:
        while True:
            # Accept a new connection
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            # Create a new thread to handle the client
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
