import socket

def main():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    client_socket.connect(('localhost', 5006))

    try:
        while True:
            # Request a file from the user
            file_name = input("Enter file name (or 'exit' to quit): ")
            if file_name.lower() == 'exit':
                break
            # Send the file name to the server
            client_socket.send(file_name.encode())
            # Receive the file content from the server
            data = client_socket.recv(4096)
            response = data.decode()
            if response == "File not found":
                print("File not found on server.")
            else:
                with open(file_name, 'wb') as file:
                    file.write(data)
                print(f"File '{file_name}' received successfully.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
