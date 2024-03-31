import socket
import os
import threading

HOST = 'localhost'
PORT = 59
BUFFER_SIZE = 1024

def handle_client_request(data, client_address, server_socket):
    filename = data.decode().strip()
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            file_data = file.read()
        server_socket.sendto(file_data, client_address)
    else:
        error_message = "File not found"
        server_socket.sendto(error_message.encode(), client_address)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print("Server is listening for incoming requests...")

def handle_requests():
    while True:
        data, client_address = server_socket.recvfrom(BUFFER_SIZE)
        print(f"Received request from {client_address}")
        client_thread = threading.Thread(target=handle_client_request, args=(data, client_address, server_socket))
        client_thread.start()

handle_requests()
