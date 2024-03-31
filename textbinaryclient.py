import socket

def main():
    # Define server IP and port
    server_ip = '127.0.0.1'
    server_port = 12345

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((server_ip, server_port))

    # Ask user for filename
    filename = input("Enter the filename you want to request: ")

    # Send filename to server
    client_socket.send(filename.encode())

    # Receive file data from server
    file_data = client_socket.recv(1024)

    # Write file data to a file
    with open('received_file', 'wb') as file:
        file.write(file_data)

    print("File received successfully.")

    # Close connection
    client_socket.close()

if __name__ == "__main__":
    main()

