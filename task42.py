import socket

def start_client():
   
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    server_ip = input("Enter the server's IP address: ")
    server_port = 12345

    try:
       
        client_socket.connect((server_ip, server_port))
        print(f"Connected to the server at {server_ip}:{server_port}")

        while True:
            
            message = input("Enter your message (type 'bye' to exit): ")
            client_socket.sendall(message.encode('utf-8'))

            
            reply = client_socket.recv(1024).decode('utf-8')
            print(f"Server reply: {reply}")

            
            if message.lower() == 'bye':
                print("Closing connection.")
                break

    except Exception as e:
        print(f"Error communicating with the server: {e}")
    finally:
        
        client_socket.close()

if __name__ == "__main__":
    start_client()
