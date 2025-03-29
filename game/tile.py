import math
import pygame
from gui.constants import (
    RECT_HEIGHT, RECT_WIDTH, FONT_COLOR
)

pygame.init()

class Tile:
    # RGB colors for different tile values
    COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247,  95,  59),
        (237, 208, 115),
        (237, 204,  99),
        (236, 202,  80),
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

    def set_pos(self):
        pass

    def move(self, delta):
        pass 