import socket
import threading

def handle_client(client_socket):
    try:
        while True:
            
            data = client_socket.recv(1024).decode('utf-8')

            if not data:
                break  

            print(f"Received from client: {data}")

           
            reply = f"Server received: {data}"
            client_socket.sendall(reply.encode('utf-8'))

            
            if data.lower() == 'bye':
                break

        print("Connection closed by client.")

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
      
        client_socket.close()

def start_server():
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   
    host = '192.168.1.3' 
    port = 12345
    server_socket.bind((host, port))

   
    server_socket.listen()

    print(f"Server listening on {host}:{port}")

    try:
        while True:
            
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")

            
            client_thread = threading.Thread(target=handle_client, args=(client_socket,), daemon=True)
            client_thread.start()

    except KeyboardInterrupt:
        print("Server shutting down.")

if __name__ == "__main__":
    start_server()
