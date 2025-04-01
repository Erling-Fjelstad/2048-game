import pygame
from gui.constants import (
    WIDTH, HEIGHT, FPS,
    RECT_WIDTH, RECT_HEIGHT,
    OUTLINE_COLOR, OUTLINE_THICKNESS,
    BACKGROUND_COLOR, ROWS, COLS
)
from game import Tile
from game import Board


pygame.init()

class GameDisplay:
    def __init__(self):
        # Set up the main game window, title, and default font
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2048")
        self.font = pygame.font.SysFont("comicsans", 60, bold=True)

    def run(self):
        # Create a clock object to manage frame rate
        clock = pygame.time.Clock()

        # Variable to control the main game loop
        run = True
        
        # Create the Board object and generate tiles
        board = Board()
        board.generate_tiles()

        while run:
            # Limit the loop to run at FPS frames per second
            clock.tick(FPS)

            # Handle all events 
            for event in pygame.event.get():
                # If the user clicks the window's close button
                if event.type == pygame.QUIT:
                    run = False
                    break

                # Handle key presses for movement
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        # Move all tiles to the left
                        board.move_tiles(clock, "left", self.draw)
                    if event.key == pygame.K_RIGHT:
                        # Move all tiles to the right
                        board.move_tiles(clock, "right", self.draw)
                    if event.key == pygame.K_UP:
                        # Move all tiles upward
                        board.move_tiles(clock, "up", self.draw)
                    if event.key == pygame.K_DOWN:
                        # Move all tiles downward
                        board.move_tiles(clock, "down", self.draw)


            # Call draw method to update visuals every frame
            self.draw(board.tiles)

        # Exit pygame after loop ends
        pygame.quit()

    def draw(self, tiles):
        # Fill the window with the background color
        self.window.fill(BACKGROUND_COLOR)

        # Draw each tile onto the window
        for tile in tiles.values():
            tile.draw(self.window, self.font)

        # Draw grid lines on top of the background
        self.draw_grid()

        # Update the display with any changes made this frame
        pygame.display.update()


    def draw_grid(self):
        # Draw horizontal lines 
        for row in range(1, ROWS):
            y = row * RECT_HEIGHT
            pygame.draw.line(self.window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)
        
        # Draw vertical lines 
        for col in range(1, COLS):
            x = col * RECT_WIDTH
            pygame.draw.line(self.window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)
        
        # Draw vertical lines (between columns)
        pygame.draw.rect(self.window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)
