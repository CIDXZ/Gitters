import tkinter as tk
from tkinter import filedialog

def read_input_file(filename):
    roll_numbers = []
    percentages = []

    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines[:66]:
            roll_numbers.append(line.strip())
        for line in lines[66:]:
            percentages.append(float(line.strip()))

    return roll_numbers, percentages

def segregate_quotas(roll_numbers, percentages):
    quotas = {
        '90': [],
        '80_89': [],
        '70_79': [],
        '60_69': [],
        'below_60': []
    }

    for roll, percent in zip(roll_numbers, percentages):
        if percent >= 90:
            quotas['90'].append((roll, percent))
        elif 80 <= percent <= 89:
            quotas['80_89'].append((roll, percent))
        elif 70 <= percent <= 79:
            quotas['70_79'].append((roll, percent))
        elif 60 <= percent <= 69:
            quotas['60_69'].append((roll, percent))
        else:
            quotas['below_60'].append((roll, percent))

    return quotas

def write_output_file(quotas):
    with open('R_section_attendance.txt', 'w') as file:
        for quota, students in quotas.items():
            file.write(f'{quota} % QUOTA:\n')
            for roll, percent in students:
                file.write(f'{roll} - {percent}%\n')
            file.write('\n')

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        roll_numbers, percentages = read_input_file(filename)
        quotas = segregate_quotas(roll_numbers, percentages)
        write_output_file(quotas)
        status_label.config(text="File processed successfully!")
    else:
        status_label.config(text="No file selected.")

# Create a Tkinter window
window = tk.Tk()
window.title("Attendance Segregation Tool")

# Create a label for status messages
status_label = tk.Label(window, text="")
status_label.pack()

# Create a button to browse and select the input file
browse_button = tk.Button(window, text="Browse File", command=browse_file)
browse_button.pack()

# Run the Tkinter event loop
window.mainloop()
