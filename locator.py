import pyautogui
import tkinter as tk

# Function to update the label text with current mouse coordinates
def update_coordinates_label():
    # Get current mouse coordinates
    x, y = pyautogui.position()
    
    # Update label text with current coordinates
    coordinates_label.config(text=f"X: {x}, Y: {y}")
    
    # Call this function again after a short delay to update the coordinates continuously
    root.after(100, update_coordinates_label)

# Create a Tkinter window
root = tk.Tk()
root.title("Mouse Coordinates Tracker")

# Create a label to display mouse coordinates
coordinates_label = tk.Label(root, text="")
coordinates_label.pack(padx=10, pady=10)

# Call the update_coordinates_label function to start updating the coordinates
update_coordinates_label()

# Hide the Tkinter window when closed
root.protocol("WM_DELETE_WINDOW", root.quit)

# Start the Tkinter event loop
root.mainloop()
