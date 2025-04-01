import random
from game.tile import Tile
from gui.constants import (
    ROWS, COLS
)

class Board:
    def __init__(self):
        # Dictionary to hold all tiles on the board
        self.tiles = {}

    def get_random_pos(self) -> int:
        #Find a random empty position on the board that doesn't already contain a tile.
        row = None
        col = None
        
        while True:
            row = random.randrange(0, ROWS)
            col = random.randrange(0, COLS)

            # Check if this position is free
            if f"{row}{col}" not in self.tiles:
                break
        
        return row, col

    def generate_tiles(self) -> dict:
        #Generate and place 2 tiles with value 2 in random empty positions on the board.
        for _ in range(2):
            row, col = self.get_random_pos()
            self.tiles[f"{row}{col}"] = Tile(2, row, col)

        return self.tiles
