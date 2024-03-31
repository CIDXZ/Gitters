import socket

def start_client():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Input the server's IP address
    server_ip = input("Enter the server's IP address: ")
    server_port = 53

    try:
        # Connect to the server
        client_socket.connect((server_ip, server_port))
        print(f"Connected to the server at {server_ip}:{server_port}")

        # Send a request to the server
        request = input("Enter your message: ")
        client_socket.sendall(request.encode('utf-8'))

        # Receive the server's response
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")

    except Exception as e:
        print(f"Error communicating with the server: {e}")
    finally:
        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    start_client()
