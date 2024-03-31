import socket
import threading

def receive_messages(client_socket):
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(data)
    except Exception as e:
        print(f"Error receiving messages: {e}")
    finally:
        client_socket.close()

def start_chat_client():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Input the peer's IP address
    peer_ip = input("Enter the peer's IP address: ")
    peer_port = 12345

    # Connect to the peer
    client_socket.connect((peer_ip, peer_port))
    print("Connected to the peer.")

    # Receive the list of connected peers
    peer_list_data = client_socket.recv(1024).decode('utf-8')
    peer_list = eval(peer_list_data)

    print("List of connected peers:")
    for peer in peer_list:
        print(peer)

    # Start a thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
    receive_thread.start()

    try:
        receive_thread.join()
    except KeyboardInterrupt:
        print("Chat client shutting down.")

if __name__ == "__main__":
    start_chat_client()


