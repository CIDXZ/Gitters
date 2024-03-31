import socket

HOST = 'localhost'
PORT = 59

def request_file(filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(filename.encode(), (HOST, PORT))
    file_data, _ = client_socket.recvfrom(504)
    with open(filename, 'wb') as file:
        file.write(file_data)
    print(f"Received file '{filename}'")
    client_socket.close()

if __name__ == "__main__":
    filename = input("Enter filename to request from the server: ")
    request_file(filename)
