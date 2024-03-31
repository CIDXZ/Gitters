import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button

def receive_messages(client_socket, chat_text):
    try:
        while True:
           
            messages = client_socket.recv(1024).decode('utf-8')
            
            
            if messages:
                
                chat_text.config(state=tk.NORMAL)
                chat_text.delete(1.0, tk.END)  
                chat_text.insert(tk.END, messages + '\n')
                chat_text.config(state=tk.DISABLED)
                chat_text.yview(tk.END) 
    except Exception as e:
        print(f"Error receiving messages: {e}")

def send_message(entry, client_socket):
    message = entry.get()
    if message:
        client_socket.sendall(message.encode('utf-8'))
        entry.delete(0, tk.END)

def start_client():
   
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    host = '192.168.1.3'
    port = 12345

    try:
      
        client_socket.connect((host, port))
    except Exception as e:
        print(f"Error connecting to the server: {e}")
        return

   
    client_window = tk.Tk()
    client_window.title("Chat Client")

    
    window_width = 400
    window_height = 300
    client_window.geometry(f"{window_width}x{window_height}")

    
    chat_text = scrolledtext.ScrolledText(client_window, wrap=tk.WORD, font=("Helvetica", 12), state=tk.DISABLED)
    chat_text.pack(expand=True, fill=tk.BOTH)

    
    entry = Entry(client_window, font=("Helvetica", 12))
    entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

    
    send_button = Button(client_window, text="Send", command=lambda: send_message(entry, client_socket))
    send_button.pack(side=tk.RIGHT)

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, chat_text), daemon=True)
    receive_thread.start()

    client_window.protocol("WM_DELETE_WINDOW", lambda: client_window.destroy())

    
    client_window.mainloop()

if __name__ == "__main__":
    start_client()






