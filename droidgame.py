import socket
import threading
import json
import tkinter as tk

HOST = '172.19.200.144'
PORT = 5555

initial_character_position = {'x': 0, 'y': 0}
clients = {}
canvas_size = (600, 400)

def handle_client(client_socket, address):
    try:
        # Send the initial character position to the client
        client_socket.sendall(json.dumps(initial_character_position).encode('utf-8'))

        while True:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print(f"[{address[0]}:{address[1]}] disconnected")
                del clients[client_socket]
                client_socket.close()
                break
            else:
                try:
                    # Parse the received JSON data
                    movement = json.loads(data)
                    # Update the character position based on the received movement command
                    clients[client_socket] = {'x': clients[client_socket]['x'] + movement['dx'],
                                              'y': clients[client_socket]['y'] + movement['dy']}
                except json.JSONDecodeError:
                    print(f"Invalid JSON received from [{address[0]}:{address[1]}]: {data}")

                # Update Tkinter canvas with new character positions
                draw_character_positions()

                # Broadcast the updated character position to all clients
                for sock in clients:
                    sock.sendall(json.dumps(clients[client_socket]).encode('utf-8'))
    except Exception as e:
        print(f"Error handling client [{address[0]}:{address[1]}]: {e}")
        del clients[client_socket]
        client_socket.close()

def draw_character_positions():
    # Clear canvas
    canvas.delete('all')

    # Draw characters at their current positions
    for client_position in clients.values():
        x, y = client_position['x'], client_position['y']
        canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill='black')

def accept_connections():
    try:
        while True:
            # Accept incoming connections
            client_socket, address = server_socket.accept()
            print(f"Connection from [{address[0]}:{address[1]}]")

            # Add the client socket to the dictionary of clients
            clients[client_socket] = initial_character_position.copy()

            # Create a new thread to handle the client connection
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
    except Exception as e:
        print(f"Error accepting connections: {e}")

# Create Tkinter window
root = tk.Tk()
root.title("Server")

# Create Tkinter canvas for drawing
canvas = tk.Canvas(root, width=canvas_size[0], height=canvas_size[1], bg='white')
canvas.pack()

# Start server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")

accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()

# Tkinter event loop
root.mainloop()
