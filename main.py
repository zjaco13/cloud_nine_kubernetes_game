import pygame
import sys
from screens.main_screen import main_screen

# Initialize Pygame
pygame.init()
# Set up the screen
screen_width = 1280 
screen_height = 900 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Kubernetes Pirate Adventure")

if __name__ == "__main__":
    main_screen(screen)

