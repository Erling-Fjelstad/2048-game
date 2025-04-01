import random
from game.tile import Tile
from gui.constants import (
    ROWS, COLS, MOVE_VEL,
    RECT_WIDTH, RECT_HEIGHT, FPS
)


class Board:
    def __init__(self):
        # Dictionary to hold all tiles on the board
        self.tiles = {}

    def get_random_pos(self) -> int:
        # Find a random empty position on the board that doesn't already contain a tile.
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
        # Generate and place 2 tiles with value 2 in random empty positions on the board.
        for _ in range(2):
            row, col = self.get_random_pos()
            self.tiles[f"{row}{col}"] = Tile(2, row, col)

        return self.tiles
    
    def end_move(self) -> str:
        # If the board is full (no empty spaces), the game is lost
        if len(self.tiles) == 16:
            return "lost"

        # Otherwise, spawn a new tile (2 or 4) at a random empty position
        row, col = self.get_random_pos()
        self.tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)

        return "continue"

    def update_tiles(self, sorted_tiles: list, draw_callback):
        # Clear and reassign tile positions based on sorted result
        self.tiles.clear()
        for tile in sorted_tiles:
            self.tiles[f"{tile.row}{tile.col}"] = tile

        # Redraw the board after updating tile positions
        draw_callback(self.tiles)

    def move_tiles(self, clock, direction, draw_callback):
        # Controls the movement loop for animation and logic
        updated = True
        blocks = set()  # Used to prevent merging the same tile twice

        # Direction-specific logic (boundaries, sorting, delta movement, etc.)
        if direction == "left":
            sort_func = lambda x: x.col
            reverse = False
            delta = (-MOVE_VEL, 0)
            boundary_check = lambda tile: tile.col == 0
            get_next_tile = lambda tile: self.tiles.get(f"{tile.row}{tile.col - 1}")
            merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL
            move_check = lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
            ceil = True

        elif direction == "right":
            sort_func = lambda x: x.col
            reverse = True
            delta = (MOVE_VEL, 0)
            boundary_check = lambda tile: tile.col == COLS - 1
            get_next_tile = lambda tile: self.tiles.get(f"{tile.row}{tile.col + 1}")
            merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
            move_check = lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
            ceil = False

        elif direction == "up":
            sort_func = lambda x: x.row
            reverse = False
            delta = (0, -MOVE_VEL)
            boundary_check = lambda tile: tile.row == 0
            get_next_tile = lambda tile: self.tiles.get(f"{tile.row - 1}{tile.col}")
            merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
            move_check = lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
            ceil = True

        elif direction == "down":
            sort_func = lambda x: x.row
            reverse = True
            delta = (0, MOVE_VEL)
            boundary_check = lambda tile: tile.row == ROWS - 1
            get_next_tile = lambda tile: self.tiles.get(f"{tile.row + 1}{tile.col}")
            merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
            move_check = lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y
            ceil = False

        # Main animation + logic loop
        while updated:
            clock.tick(FPS)  # Limit FPS for consistent animation
            updated = False

            # Sort tiles in move direction
            sorted_tiles = sorted(self.tiles.values(), key=sort_func, reverse=reverse)

            for i, tile in enumerate(sorted_tiles):
                # Stop if at edge
                if boundary_check(tile):
                    continue

                next_tile = get_next_tile(tile)

                if not next_tile:
                    tile.move(delta)  # Move if space is empty
                elif (
                    tile.value == next_tile.value
                    and tile not in blocks
                    and next_tile not in blocks
                ):
                    if merge_check(tile, next_tile):
                        tile.move(delta)  # Slide into merge position
                    else:
                        # Merge tiles
                        next_tile.value *= 2
                        sorted_tiles.pop(i)  # Remove tile from list
                        blocks.add(next_tile)
                elif move_check(tile, next_tile):
                    tile.move(delta)
                else:
                    continue

                tile.set_pos(ceil)  # Snap to grid if needed
                updated = True  # Continue animation

            # Update and redraw all tiles
            self.update_tiles(sorted_tiles, draw_callback)

        # Once movement is over, possibly add new tile
        self.end_move()
