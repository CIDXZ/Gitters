import socket
import threading
import time
import os
import uuid

def handle_client(client_socket, client_address, clients, client_names, last_identifier):
    try:
       
        client_socket.sendall("Enter your name: ".encode('utf-8'))
        client_name = client_socket.recv(1024).decode('utf-8')
        print(f"Client {client_address} is now known as {client_name}")
        client_names[client_address] = client_name

       
        if os.path.exists("TEXT-LOG"):
            with open("TEXT-LOG", "r") as file:
                previous_messages = file.read()
                client_socket.sendall(f"{last_identifier}\n{previous_messages}".encode('utf-8'))

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

         
            with open("TEXT-LOG", "a") as file:
                file.write(f"{client_name}: {message}\n")

            
            identifier = str(uuid.uuid4())
            for other_client_socket, _ in clients:
                if other_client_socket != client_socket:
                    other_client_socket.sendall(f"{identifier}\n{client_name}: {message}".encode('utf-8'))
                    
           
            last_identifier[client_address] = identifier
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        
        clients.remove((client_socket, client_address))
        client_names.pop(client_address, None)
        print(f"Connection with {client_address} closed.")
        client_socket.close()

def broadcast_messages(clients):
    while True:
        time.sleep(2)
        
        if os.path.exists("TEXT-LOG"):
            with open("TEXT-LOG", "r") as file:
                messages = file.read()
                for client_socket, _ in clients:
                    client_socket.sendall(messages.encode('utf-8'))

def start_server():
   
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    host = '192.168.1.3'
    port = 12345

   
    with open("TEXT-LOG", "w") as file:
        pass

    
    server_socket.bind((host, port))

    
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

  
    clients = []
    client_names = {}
    last_identifier = {}

    
    broadcast_thread = threading.Thread(target=broadcast_messages, args=(clients,), daemon=True)
    broadcast_thread.start()

    while True:
        
        client_socket, client_address = server_socket.accept()
        print(f"Got connection from {client_address}")

       
        clients.append((client_socket, client_address))

      
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, clients, client_names, last_identifier))
        client_thread.start()

if __name__ == "__main__":
    start_server()

