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

def connect_to_peer(peer_ip, peer_port):
    # Create a socket object for the client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the peer
        client_socket.connect((peer_ip, peer_port))
        print(f"Connected to the peer at {peer_ip}:{peer_port}")

        # Receive the list of connected peers
        peer_list_data = client_socket.recv(1024).decode('utf-8')
        peer_list = eval(peer_list_data)

        print("List of connected peers:")
        for peer in peer_list:
            print(peer)

        # Start a thread to receive messages
        receive_thread = threading.Thread(target=handle_connection, args=(client_socket, (peer_ip, peer_port)), daemon=True)
        receive_thread.start()

        receive_thread.join()  # Wait for the thread to finish (shouldn't happen in this example)

    except Exception as e:
        print(f"Error connecting to the peer: {e}")
    finally:
        client_socket.close()

def start_peer():
    # Create a socket object for the server
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
    # Start the peer server in a separate thread
    server_thread = threading.Thread(target=start_peer, daemon=True)
    server_thread.start()

    # Get the peer's own IP address and port
    my_ip = socket.gethostbyname(socket.gethostname())
    my_port = 12345

    print(f"Your IP address: {my_ip}")
    print("Enter the IP address of a peer you want to connect to (or press Enter to skip):")

    while True:
        peer_ip = input("Peer IP: ")
        if not peer_ip:
            break

        connect_to_peer(peer_ip, my_port)
