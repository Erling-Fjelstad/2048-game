import pygame

pygame.init()

FPS = 60  

WIDTH, HEIGHT = 800, 800
ROWS = 4
COLS = 4

RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLS

OUTLINE_COLOR = (190, 170, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 190, 180)
FONT_COLOR = (120, 110, 100)

MOVE_VEL = 20

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

        while run:
            # Limit the loop to run at FPS frames per second
            clock.tick(FPS)

            # Handle all events 
            for event in pygame.event.get():
                # If the user clicks the window's close button
                if event.type == pygame.QUIT:
                    run = False
                    break

            # Call draw method to update visuals every frame
            self.draw()

        # Exit pygame after loop ends
        pygame.quit()

    def draw(self):
        # Fill the window with the background color
        self.window.fill(BACKGROUND_COLOR)

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
