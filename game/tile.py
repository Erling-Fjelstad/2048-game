import math
import pygame
from gui.constants import (
    RECT_HEIGHT, RECT_WIDTH, FONT_COLOR
)

pygame.init()

class Tile:
    # RGB colors for different tile values
    COLORS = [
        (238, 228, 218),  # 2
        (237, 224, 200),  # 4
        (242, 177, 121),  # 8
        (245, 149, 99),   # 16
        (246, 124, 95),   # 32
        (246, 94, 59),    # 64
        (237, 207, 114),  # 128
        (237, 204, 97),   # 256
        (237, 200, 80),   # 512
        (237, 197, 63),   # 1024
        (237, 194, 46),   # 2048
        (60, 58, 50),     # 4096+
    ]

    def __init__(self, value, row, col):
        # Initialize the tile with its value and position in the grid
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH  # X-pixel coordinate on screen
        self.y = row * RECT_HEIGHT  # Y-pixel coordinate on screen

    def get_color(self) -> tuple:
        # Calculate tile color based on its value (log2-based index)
        color_index = int(math.log2(self.value)) - 1
        color = self.COLORS[color_index]
        return color
    
    def draw(self, window, font):
        # Draw the tile rectangle 
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        # Render and draw the tile's number centered in the tile
        text = font.render(str(self.value), 1, FONT_COLOR)
        window.blit(
            text,
            (self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
             self.y + (RECT_HEIGHT / 2 - text.get_height() / 2))
        )

    def set_pos(self, ceil=False):
        if ceil:
            # Snap position upward to nearest row/column
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            # Snap position downward to nearest row/column
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move(self, delta):
        # Move tile position by delta (x, y) pixels
        self.x += delta[0]
        self.y += delta[1]
