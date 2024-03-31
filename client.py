import socket

def start_client():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = '127.0.0.1'
    port = 12345

    # Connect to the server
    client_socket.connect((host, port))

    # Get user input
    message = input("Enter a line: ")

    # Send the input to the server
    client_socket.sendall(message.encode('utf-8'))

    # Receive the response from the server
    data = client_socket.recv(1024).decode('utf-8')
    print(f"Received response from server: {data}")

    # Close the connection
    client_socket.close()

start_client()


