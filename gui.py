import pygame
import random
from cards import Player,Game

# Initialize Pygame
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple GUI")

# Font for text rendering
font = pygame.font.Font(None, 32)

#Game
p1 = Player()
p2 = Player()
game = Game([p1,p2])


# Button class
class Button:
    def __init__(self, text, x, y, width, height, color, click_func):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.click_func = click_func
        self.text_surface = font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(
            center=(self.x + self.width // 2, self.y + self.height // 2)
        )

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, pos):
        return (
            self.x <= pos[0] <= self.x + self.width
            and self.y <= pos[1] <= self.y + self.height
        )


# Create a button
draw_button = Button(
    "Deal", 100, 100, 100, 50, (0, 200, 0), game.start()
)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if draw_button.is_clicked(pos):
                draw_button.click_func()  # Call the button's function

    # Clear screen before redrawing
    screen.fill((255, 255, 255))

    # Draw the button
    draw_button.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
