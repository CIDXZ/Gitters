import tkinter as tk
from tkinter import filedialog

def parse_srt(file_path):
    timestamps = []
    subtitles = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        current_subtitle = ""
        for line in lines:
            current_subtitle += line
            if line == "\n":
                subtitles.append(current_subtitle.strip())
                current_subtitle = ""

            if line.startswith("Start:"):
                start_time = line.split(":")[1].strip()
                timestamps.append(float(start_time))

    return timestamps, subtitles

def write_to_files(timestamps, subtitles):
    with open("timestamps.txt", 'w', encoding='utf-8') as timestamps_file:
        timestamps_file.write("Timestamps:\n")
        for timestamp in timestamps:
            timestamps_file.write(f"Start: {timestamp}\n")

    with open("subtitles.txt", 'w', encoding='utf-8') as subtitles_file:
        subtitles_file.write("Subtitles:\n")
        for subtitle in subtitles:
            subtitles_file.write(f"{subtitle}\n\n")

def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("SRT Files", "*.srt")])
    return file_path

if __name__ == "__main__":
    print("Choose the SRT file:")
    srt_file_path = choose_file()

    try:
        timestamps, subtitles = parse_srt(srt_file_path)

        write_to_files(timestamps, subtitles)
        print("Timestamps written to timestamps.txt")
        print("Subtitles written to subtitles.txt")

    except Exception as e:
        print(f"Error: {e}")






