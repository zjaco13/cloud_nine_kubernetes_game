import pygame
import sys
import pygame.freetype
from util.util import HEIGHT, WIDTH, word_wrap, WHITE, GRAY, BLACK, RED, font
from screens.main_screen import main_screen

# Load the image
background_image = pygame.transform.scale(pygame.image.load('sprites/background.jpg'), (WIDTH, HEIGHT))

def game_over_screen(screen):
    screen.blit(background_image, (0, 0))
    screen_width, screen_height = screen.get_size()

    # Render the "Game Over" text
    text, _ = font.render("Game Over", BLACK)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    text_box_rect = text_rect.inflate(10, 10)
    pygame.draw.rect(screen, WHITE, text_box_rect)
    screen.blit(text, text_rect)

    # Render a "Play Again" button
    play_again_button = pygame.Rect(screen_width // 2, (screen_height // 2) + 160, 200, 50)
    pygame.draw.rect(screen, GRAY, play_again_button)
    play_again_text, _ = font.render("Play Again", BLACK)
    play_again_text_rect = play_again_text.get_rect(center=play_again_button.center)
    screen.blit(play_again_text, play_again_text_rect)
    global play_again_button_rect
    play_again_button_rect = play_again_button

    # Update the display
    pygame.display.flip()

    # Wait for user input to decide what to do next
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    return_main(screen)

def return_main(screen):
    main_screen(screen)
