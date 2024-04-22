import pygame
import sys
from screens.main_screen import main_screen
from util.util import WIDTH, HEIGHT

# Initialize Pygame
pygame.init()
# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kubernetes Pirate Adventure")

if __name__ == "__main__":
    main_screen(screen)

