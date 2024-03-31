import random

class WumpusWorld:
    def __init__(self, size=4):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.agent_position = (0, 0)
        self.wumpus_position = self.random_position()
        self.gold_position = self.random_position()
        self.pit_positions = [self.random_position() for _ in range(size)]

    def random_position(self):
        return (random.randint(0, self.size - 1), random.randint(0, self.size - 1))

    def is_valid_position(self, position):
        x, y = position
        return 0 <= x < self.size and 0 <= y < self.size

    def is_safe_position(self, position):
        return position not in self.pit_positions and position != self.wumpus_position

    def percept(self):
        x, y = self.agent_position
        perceptions = []
        if (x, y) == self.wumpus_position:
            perceptions.append("Stench")
        if (x, y) == self.gold_position:
            perceptions.append("Glitter")
        if (x - 1, y) in self.pit_positions or \
           (x + 1, y) in self.pit_positions or \
           (x, y - 1) in self.pit_positions or \
           (x, y + 1) in self.pit_positions:
            perceptions.append("Breeze")
        return perceptions

    def move_agent(self, direction):
        x, y = self.agent_position
        if direction == "up":
            new_position = (x - 1, y)
        elif direction == "down":
            new_position = (x + 1, y)
        elif direction == "left":
            new_position = (x, y - 1)
        elif direction == "right":
            new_position = (x, y + 1)
        else:
            raise ValueError("Invalid direction")
        
        if self.is_valid_position(new_position):
            self.agent_position = new_position
            return True
        else:
            return False

    def grab_gold(self):
        if self.agent_position == self.gold_position:
            self.gold_position = None
            return True
        else:
            return False

    def kill_wumpus(self):
        if self.agent_position == self.wumpus_position:
            self.wumpus_position = None
            return True
        else:
            return False

# Example usage:
world = WumpusWorld()
print("Initial percept:", world.percept())
world.move_agent("right")
print("Percept after moving right:", world.percept())
world.move_agent("down")
print("Percept after moving down:", world.percept())
