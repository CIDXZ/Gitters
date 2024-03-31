import socket
import pyautogui

# Function to move the mouse based on the received command
def move_mouse(direction):
    # Adjust the mouse movement distance as needed
    distance = 50
    if direction == 'up':
        pyautogui.move(0, -distance)
    elif direction == 'down':
        pyautogui.move(0, distance)
    elif direction == 'left':
        pyautogui.move(-distance, 0)
    elif direction == 'right':
        pyautogui.move(distance, 0)

# Function to perform left click
def left_click():
    pyautogui.click()

# Function to perform right click
def right_click():
    pyautogui.rightClick()

# Function to handle commands received from the Android app
def handle_command(command):
    if command.startswith('move_'):
        move_direction = command.split('_')[1]
        move_mouse(move_direction)
    elif command == 'left_click':
        left_click()
    elif command == 'right_click':
        right_click()

def main():
    HOST = '172.19.242.223'  # Listen on all network interfaces
    PORT = 12345  # Choose a port number

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")

                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    
                    command = data.decode()
                    print(f"Received command: {command}")
                    handle_command(command)

if __name__ == "__main__":
    main()
