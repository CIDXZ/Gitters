class VacuumCleaner:
    def __init__(self, grid):
        self.grid = grid 
        self.current_position = (0, 0)

    def clean(self):
        while self.has_dirty_cells():
            if self.is_current_cell_dirty():
                self.clean_current_cell()
            else:
                self.move_to_next_dirty_cell()

    def has_dirty_cells(self):
        for row in self.grid:
            if any(cell == 'dirty' for cell in row): 
                return True
        return False

    def is_current_cell_dirty(self):
        return self.grid[self.current_position[0]][self.current_position[1]] == 'dirty'

    def clean_current_cell(self):
        print(f"Cleaning cell {self.current_position}")
        self.grid[self.current_position[0]][self.current_position[1]] = 'clean'

    def move_to_next_dirty_cell(self):
        dirty_cells = [(i, j) for i, row in enumerate(self.grid) for j, cell in enumerate(row) if cell == 'dirty']

        if dirty_cells:
            next_dirty_cell = dirty_cells[0]
            self.move_towards(next_dirty_cell)

    def move_towards(self, destination):
        x, y = self.current_position
        dx = destination[0] - x
        dy = destination[1] - y

        if dx > 0:
            print("Moving down")
            self.current_position = (x + 1, y)
        elif dx < 0:
            print("Moving up")
            self.current_position = (x - 1, y)
        elif dy > 0:
            print("Moving right")
            self.current_position = (x, y + 1)
        elif dy < 0:
            print("Moving left")
            self.current_position = (x, y - 1)

grid = [
    ['clean', 'dirty', 'clean','dirty'],
    ['dirty', 'clean', 'dirty', 'dirty', 'dirty', 'dirty', 'dirty'],
    ['clean', 'dirty', 'clean', 'dirty', 'dirty', 'dirty', 'dirty']
]

vacuum = VacuumCleaner(grid)
vacuum.clean()

