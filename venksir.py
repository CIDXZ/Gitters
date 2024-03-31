import tkinter as tk
from tkinter import filedialog

def filter_content(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    filtered_lines = [line.strip() for line in lines if "'" in line]

    with open(output_file, 'w') as f:
        for line in filtered_lines:
            f.write(line + '\n')

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def main():
    input_file_path = select_file()
    if input_file_path:
        output_file_path = "filtered_output.txt"
        filter_content(input_file_path, output_file_path)
        print("Filtered content saved to filtered_output.txt")

if __name__ == "__main__":
    main()
