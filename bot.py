import tkinter as tk

def display_battles():
    # Code to display information about WW2 battles
    print("Displaying information about WW2 battles...")

def display_leaders():
    # Code to display information about WW2 leaders
    print("Displaying information about WW2 leaders...")

# Create the main window
root = tk.Tk()
root.title("World War II Information")

# Create a label for the title
title_label = tk.Label(root, text="World War II Information")
title_label.pack()

# Create a frame for the options
options_frame = tk.Frame(root)
options_frame.pack()

# Create a button to display information about WW2 battles
battles_button = tk.Button(options_frame, text="Display Battles", command=display_battles)
battles_button.pack(side="left")

# Create a button to display information about WW2 leaders
leaders_button = tk.Button(options_frame, text="Display Leaders", command=display_leaders)
leaders_button.pack(side="right")

# Start the main loop
root.mainloop()





