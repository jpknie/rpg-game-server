import random

class GameWorld:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = self._generate_grid()

    def _generate_grid(self):
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1:
                    row.append('#')  # Walls at the edges
                else:
                    row.append('.')  # Walkable area
            grid.append(row)
        # Place an item 'i' at a specific position (example: center of the grid)
        if self.width > 2 and self.height > 2:
            grid[self.height // 2][self.width // 2] = 'i'
        return grid
    
    def find_random_walkable_tile(self):
        """Find a random walkable tile in the world."""
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.is_walkable(x, y):
                return x, y
    
    def is_walkable(self, x, y):
        """Check if the position (x, y) is walkable."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x] == '.'
        return False
    
    def display_grid(self):
        for row in self.grid:
            print(''.join(row))