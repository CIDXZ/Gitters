import tkinter as tk
from tkinter import filedialog

def separate_names_and_numbers(input_file):
    names = []
    numbers = []
    
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            parts = line.split()
            if len(parts) >= 2:  # Check if the line contains at least two parts
                name = ' '.join(parts[:-1])  # Join all parts except the last one as the name
                number = parts[-1]  # Last part is the roll number
                names.append(name)
                numbers.append(number)

    return names, numbers

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def main():
    input_file = select_file()
    if input_file:
        names, numbers = separate_names_and_numbers(input_file)

        with open("names.txt", 'w') as f:
            for name in names:
                f.write(name + '\n')

        with open("roll_numbers.txt", 'w') as f:
            for number in numbers:
                f.write(number + '\n')

        print("Names saved to names.txt")
        print("Roll numbers saved to roll_numbers.txt")

if __name__ == "__main__":
    main()
