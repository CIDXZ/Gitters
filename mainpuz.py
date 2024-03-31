import tkinter as tk
import random

class PuzzleGame:
    def __init__(self, master):
        self.master = master
        self.size = 2
        self.tiles = [[None] * self.size for _ in range(self.size)]
        self.empty_row, self.empty_col = self.size - 1, self.size - 1
        self.create_puzzle()
    
    def create_puzzle(self):
        numbers = [1, 2, 3, None]  # None represents the empty space
        random.shuffle(numbers)

        for i in range(self.size):
            for j in range(self.size):
                if numbers:
                    number = numbers.pop(0)
                    if number is not None:
                        label = tk.Label(self.master, text=str(number), font=("Arial", 16), width=4, height=2, relief=tk.RAISED, borderwidth=2)
                        label.grid(row=i, column=j, sticky="nsew")
                        label.bind("<Button-1>", self.on_click)
                    self.tiles[i][j] = label if number is not None else None

        self.tiles[self.empty_row][self.empty_col] = None

        for i in range(self.size):
            self.master.grid_rowconfigure(i, weight=1)
            self.master.grid_columnconfigure(i, weight=1)

    def on_click(self, event):
        clicked_label = event.widget
        row, col = self.get_label_position(clicked_label)

        if self.is_adjacent(row, col, self.empty_row, self.empty_col):
            self.swap_labels(row, col, self.empty_row, self.empty_col)
            if self.check_winner():
                self.display_winner()

    def get_label_position(self, label):
        for i in range(self.size):
            for j in range(self.size):
                if self.tiles[i][j] == label:
                    return i, j

    def is_adjacent(self, row1, col1, row2, col2):
        return abs(row1 - row2) + abs(col1 - col2) == 1

    def swap_labels(self, row1, col1, row2, col2):
        self.tiles[row1][col1], self.tiles[row2][col2] = self.tiles[row2][col2], self.tiles[row1][col1]
        self.empty_row, self.empty_col = row1, col1

        self.update_labels()

    def update_labels(self):
        for i in range(self.size):
            for j in range(self.size):
                label = self.tiles[i][j]
                if label:
                    label.grid(row=i, column=j)

    def check_winner(self):
        current_numbers = [label.cget("text") for row in self.tiles for label in row if label]
        return current_numbers == ["1", "2", "3"]

    def display_winner(self):
        winner_label = tk.Label(self.master, text="Congratulations! You won!", font=("Arial", 16), fg="green")
        winner_label.grid(row=self.size, columnspan=self.size, sticky="nsew")

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGame(root)
    root.mainloop()










