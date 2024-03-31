import socket
import threading

peers = []  # List to store connected peers

def handle_connection(client_socket, peer_address):
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Message from {peer_address}: {data}")
    except Exception as e:
        print(f"Error handling connection with {peer_address}: {e}")
    finally:
        client_socket.close()
        peers.remove(peer_address)  # Remove the peer when the connection is closed

def start_peer():
    # Create a socket object
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 12345
    peer_socket.bind((host, port))

    # Listen for incoming connections
    peer_socket.listen()

    print(f"Peer listening on {host}:{port}")

    try:
        while True:
            # Accept a connection from a client
            client_socket, client_address = peer_socket.accept()
            print(f"Accepted connection from {client_address}")

            # Send the list of connected peers to the new client
            client_socket.sendall(str(peers).encode('utf-8'))

            # Add the new peer to the list
            peers.append(client_address)

            # Start a thread to handle the connection
            connection_thread = threading.Thread(target=handle_connection, args=(client_socket, client_address), daemon=True)
            connection_thread.start()

    except KeyboardInterrupt:
        print("Peer shutting down.")

if __name__ == "__main__":
    start_peer()


