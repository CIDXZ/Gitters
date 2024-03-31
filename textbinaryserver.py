import socket
import os

# Function to handle client requests
def handle_client(client_socket):
    # Receive choice from client
    choice = client_socket.recv(1024).decode()
    if choice == '1':
        filename = 'text_file.txt'
    elif choice == '2':
        filename = 'binary_file.bin'
    else:
        print("Invalid choice.")
        return

    # Check if file exists
    if not os.path.exists(filename):
        print(f"File '{filename}' not found.")
        return

    # Open and send file to client
    with open(filename, 'rb') as file:
        file_data = file.read()
        client_socket.send(file_data)

    # Close connection
    client_socket.close()

def main():
    # Define server IP and port
    server_ip = '127.0.0.1'
    server_port = 12345

    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the server address
    server_socket.bind((server_ip, server_port))

    # Listen for incoming connections
    server_socket.listen(5)
    print("Server is listening...")

    while True:
        # Accept a new connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Handle client request
        handle_client(client_socket)

if __name__ == "__main__":
    main()
