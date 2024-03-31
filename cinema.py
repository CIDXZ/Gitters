import tkinter as tk
from tkinter import filedialog, simpledialog
import re
import time


def parse_timestamps_and_subtitles(file_path):
    timestamps = []
    subtitles = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        is_timestamp = False
        current_subtitle = ""

        for line in lines:
            if re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line):
                is_timestamp = True
                timestamps.append(line.strip())
            elif is_timestamp:
                if line == '\n':
                    is_timestamp = False
                    subtitles.append(current_subtitle.strip())
                    current_subtitle = ""
                else:
                    current_subtitle += line

    return timestamps, subtitles


class SubtitleViewer:
    def __init__(self, root, timestamps, subtitles):
        self.root = root
        self.timestamps = timestamps
        self.subtitles = subtitles
        self.index = 0
        self.is_running = False
        self.start_time_offset = 0
        self.start_time = 0

        self.label = tk.Label(root, text="", font=("Arial", 24), bg="black", fg="white")
        self.label.pack(fill=tk.BOTH, expand=True)

        self.start_button = tk.Button(root, text="Start", command=self.start_display, bg="black", fg="white")
        self.start_button.pack(pady=10, side=tk.LEFT)

        self.jump_button = tk.Button(root, text="Jump", command=self.jump_to_time, bg="black", fg="white")
        self.jump_button.pack(pady=10, side=tk.RIGHT)

        # Set the window transparency
        root.attributes("-alpha", 0.8)

        # Set the position and size of the main window
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        taskbar_height = root.winfo_screenmmheight()
        window_height = int(screen_height * 0.2)  # You can adjust the height as needed
        window_position_y = screen_height - window_height - taskbar_height
        root.geometry(f"{screen_width}x{window_height}+0+{window_position_y}")

        # Make the window always on top
        root.attributes('-topmost', 1)

    def start_display(self):
        self.is_running = True
        self.start_button.pack_forget()  # Hide the start button once pressed
        start_timestamp = self.timestamps[0].split(" --> ")[0]
        self.start_time_offset = self.convert_timestamp_to_milliseconds(start_timestamp)

        # Start the timer
        self.start_time = time.time()

        # Display the first subtitle when the timer reaches the start time
        self.root.after(10, self.update_timer, self.start_time)

    def update_timer(self, start_time):
        current_time = time.time()
        elapsed_time = int((current_time - start_time) * 1000)

        if elapsed_time >= self.start_time_offset and self.is_running:
            self.display_subtitle()
        else:
            self.root.after(10, self.update_timer, start_time)

    def display_subtitle(self):
        if self.index < len(self.timestamps):
            timestamp = self.timestamps[self.index]

            start_time, end_time = re.findall(r'\d{2}:\d{2}:\d{2},\d{3}', timestamp)
            start_time_in_ms = self.convert_timestamp_to_milliseconds(start_time)

            subtitle = self.subtitles[self.index]
            self.label.config(text=subtitle)
            self.index += 1

            # Schedule the next subtitle display
            if self.index < len(self.timestamps):
                next_timestamp = self.timestamps[self.index]
                next_start_time, _ = re.findall(r'\d{2}:\d{2}:\d{2},\d{3}', next_timestamp)
                next_start_time_in_ms = self.convert_timestamp_to_milliseconds(next_start_time)
                duration_until_next_subtitle = next_start_time_in_ms - start_time_in_ms
                self.root.after(int(duration_until_next_subtitle), self.display_subtitle)

    def jump_to_time(self):
        jump_time = simpledialog.askstring("Jump to Time", "Enter the time (HH:MM:SS,SSS):")
        if jump_time:
            self.is_running = False  # Pause the timer
            self.index = 0  # Reset the index
            self.start_button.pack(side=tk.LEFT)  # Show the start button again
            self.label.config(text="")  # Clear the displayed subtitle

            # Find the closest timestamp to the entered time
            for i, timestamp in enumerate(self.timestamps):
                if timestamp.startswith(jump_time):
                    self.index = i
                    break

            # Set the start_time to the jumped time
            self.start_time = time.time() - self.convert_timestamp_to_milliseconds(jump_time) / 1000

            # Update the display based on the jumped time
            self.display_subtitle()

    def convert_timestamp_to_milliseconds(self, timestamp):
         parts = re.split('[:,]', timestamp)
         hours = int(parts[0])
         minutes = int(parts[1])
         seconds = int(parts[2])
         milliseconds = int(parts[3])
         total_milliseconds = (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds
         return total_milliseconds


def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    return file_path


if __name__ == "__main__":
    print("Choose the timestamps and subtitles text file:")
    file_path = choose_file()

    try:
        timestamps, subtitles = parse_timestamps_and_subtitles(file_path)

        root = tk.Tk()
        root.title("Subtitle Viewer")
        root.configure(bg="black")

        viewer = SubtitleViewer(root, timestamps, subtitles)

        root.mainloop()

    except Exception as e:
        print(f"Error: {e}")




























































