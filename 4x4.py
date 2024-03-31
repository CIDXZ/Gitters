def __init__(self, master):
    self.master = master
    self.puzzle_size = 4
    self.puzzle_entries = []
    self.create_puzzle_grid()
    self.create_puzzle_entries()
    self.solver = SudokuSolver(self.create_puzzle())