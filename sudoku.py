import tkinter as tk
from tkinter import messagebox

class SudokuSolver:

    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.rows = [0] * 16
        self.cols = [0] * 16
        self.squares = [[0] * 4 for _ in range(4)]
        self.stack = []
        self.init()

    def init(self):
        for r in range(16):
            for c in range(16):
                val = self.puzzle[r][c]
                if val:
                    self.place(r, c, val)

    def place(self, r, c, val):
        self.rows[r] |= (1 << val)
        self.cols[c] |= (1 << val)
        self.squares[r//4][c//4] |= (1 << val)
        self.puzzle[r][c] = val

    def remove(self, r, c, val):
        self.rows[r] &= ~(1 << val)
        self.cols[c] &= ~(1 << val)
        self.squares[r//4][c//4] &= ~(1 << val)
        self.puzzle[r][c] = 0

    def undo(self):
        r, c, val = self.stack.pop()
        self.remove(r, c, val)

    def nextEmpty(self):
        for r in range(16):
            for c in range(16):
                if not self.puzzle[r][c]:
                    return r, c
        return -1, -1

    def legal(self, r, c, val):
        if (self.rows[r] & (1 << val)) or (self.cols[c] & (1 << val)) or (self.squares[r//4][c//4] & (1 << val)):
            return False
        return True

    def solve(self):
        r, c = self.nextEmpty()
        if r == -1:
            return True
        for val in range(1, 17):
            if self.legal(r, c, val):
                self.place(r, c, val)
                self.stack.append((r, c, val))
                if self.solve():
                    return True
                self.undo()
        return False

    def solvePuzzle(self):
        if self.solve():
            return self.puzzle
        else:
            return "No solution"

puzzle = [[0 for _ in range(16)] for _ in range(16)]
solver = SudokuSolver(puzzle)
solution = solver.solvePuzzle()
for row in solution:
    print(row)

class SudokuApp:
    def __init__(self, master):
        self.master = master
        self.solver = SudokuSolver([[0 for _ in range(16)] for _ in range(16)])
        self.puzzle_entries = [[0 for _ in range(16)] for _ in range(16)]

        self.create_widgets()

    def create_widgets(self):
        for r in range(16):
            for c in range(16):
                self.puzzle_entries[r][c] = tk.Entry(self.master, width=2)
                self.puzzle_entries[r][c].grid(row=r, column=c)

        self.solve_button = tk.Button(self.master, text="Solve", command=self.solve)
        self.solve_button.grid(row=16, column=8)
        
        for r in range(16):
            self.master.grid_rowconfigure(r, weight=1)

        for c in range(16):
            self.master.grid_columnconfigure(c, weight=1)

    def solve(self):
        for r in range(16):
            for c in range(16):
                val = self.puzzle_entries[r][c].get()
                if val:
                    self.solver.place(r, c, int(val))

        if self.solver.solve():
            for r in range(16):
                for c in range(16):
                    val = self.solver.puzzle[r][c]
                    self.puzzle_entries[r][c].delete(0, 'end')
                    self.puzzle_entries[r][c].insert(0, str(val))
        else:
            messagebox.showerror("Error", "No solution found")

root = tk.Tk()
app = SudokuApp(root)
root.mainloop()

