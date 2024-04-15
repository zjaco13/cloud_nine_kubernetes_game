import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Main Screen")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Set up fonts
font = pygame.font.Font(None, 36)

# Define game states
MAIN_MENU = 0
PLAY = 1
DESCRIPTION = 2
TEAM = 3
TUTORIAL = 4

# Initial game state
current_state = MAIN_MENU

def main_screen():
    global current_state
    
    while True:

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == MAIN_MENU:
                    # Check if the mouse click is within the play button area
                    if play_button1_rect.collidepoint(event.pos):
                        # Change to the new screen state
                        current_state = PLAY
                    elif play_button2_rect.collidepoint(event.pos):
                        current_state = DESCRIPTION
                    elif play_button3_rect.collidepoint(event.pos):
                        current_state = TEAM
                    elif play_button4_rect.collidepoint(event.pos):
                        current_state = TUTORIAL
                elif current_state == PLAY:
                    # Handle events specific to the PLAY screen
                    if back_button_rect.collidepoint(event.pos):
                        current_state = MAIN_MENU
                elif current_state == DESCRIPTION:
                    # Handle events specific to the DESCRIPTION screen
                    if back_button_rect.collidepoint(event.pos):
                        current_state = MAIN_MENU
                elif current_state == TEAM:
                    # Handle events specific to the TEAM screen 
                    if back_button_rect.collidepoint(event.pos):
                        current_state = MAIN_MENU
                elif current_state == TUTORIAL:
                    # Handle events specific to the TUTORIAL screen 
                    if back_button_rect.collidepoint(event.pos):
                        current_state = MAIN_MENU


        # Render different screens based on current state
        if current_state == MAIN_MENU:
            render_main_menu()
        elif current_state == PLAY:
            render_new_screen1()
        elif current_state == DESCRIPTION:
            render_new_screen2()
        elif current_state == TEAM:
            render_new_screen3()
        elif current_state == TUTORIAL:
            render_new_screen4()

        # Update the display
        pygame.display.flip()

def render_main_menu():
    # Fill the screen with white color
    screen.fill(WHITE)

    # Render title of the game on the screen
    title = font.render("Kubernetes Pirate Adventure", True, BLACK)
    title_rect = title.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(title, title_rect)

    # Draw play button 1 - PLAY
    play_button1 = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 50, 200, 50)
    pygame.draw.rect(screen, GRAY, play_button1)
    play_text1 = font.render("PLAY", True, BLACK)
    play_text_rect1 = play_text1.get_rect(center=play_button1.center)
    screen.blit(play_text1, play_text_rect1)
    global play_button1_rect
    play_button1_rect = play_button1

    # Draw play button 2 - DESCRIPTION
    play_button2 = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 120, 200, 50)
    pygame.draw.rect(screen, GRAY, play_button2)
    play_text2 = font.render("DESCRIPTION", True, BLACK)
    play_text_rect2 = play_text2.get_rect(center=play_button2.center)
    screen.blit(play_text2, play_text_rect2)
    global play_button2_rect
    play_button2_rect = play_button2

    # Draw play button 3 - TEAM
    play_button3 = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 190, 200, 50)
    pygame.draw.rect(screen, GRAY, play_button3)
    play_text3 = font.render("TEAM", True, BLACK)
    play_text_rect3 = play_text3.get_rect(center=play_button3.center)
    screen.blit(play_text3, play_text_rect3)
    global play_button3_rect
    play_button3_rect = play_button3

    # Draw play button 3 - TUTORIAL
    play_button4 = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 260, 200, 50)
    pygame.draw.rect(screen, GRAY, play_button4)
    play_text4 = font.render("TUTORIAL", True, BLACK)
    play_text_rect4 = play_text4.get_rect(center=play_button4.center)
    screen.blit(play_text4, play_text_rect4)
    global play_button4_rect
    play_button4_rect = play_button4

def render_new_screen1():
    # Fill the screen with a different color
    screen.fill(BLACK)

    # Render content for the new screen 1
    text = font.render("Play Screen", True, WHITE)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)

    # Render back button
    back_button = pygame.Rect(20, 20, 100, 50)
    pygame.draw.rect(screen, GRAY, back_button)
    back_text = font.render("Back", True, BLACK)
    back_text_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_text_rect)
    global back_button_rect
    back_button_rect = back_button

def render_new_screen2():
    # Fill the screen with a different color
    screen.fill(BLACK)

    # Render content for the new screen 2
    font_16 = pygame.font.Font(None, 16)
    text = font_16.render("The purpose of this game is to teach you about open source tools that are critical to know for todays cloud focused environment.  The 2 tools focused on in this game are Docker and Kubernetes.  With a grasp of these tools, you will be primed for success when developing and deploying your application to the world", True, WHITE)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)

    # Render back button
    back_button = pygame.Rect(20, 20, 100, 50)
    pygame.draw.rect(screen, GRAY, back_button)
    back_text = font.render("Back", True, BLACK)
    back_text_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_text_rect)
    global back_button_rect
    back_button_rect = back_button

def render_new_screen3():
    # Fill the screen with a different color
    screen.fill(BLACK)

    # Render content for the new screen 3
    text = font.render("Team: Zach Jacobson, Phong Duong, Om Patel, Shreiyas Saraf", True, WHITE)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)

    # Render back button
    back_button = pygame.Rect(20, 20, 100, 50)
    pygame.draw.rect(screen, GRAY, back_button)
    back_text = font.render("Back", True, BLACK)
    back_text_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_text_rect)
    global back_button_rect
    back_button_rect = back_button

def render_new_screen4():
    # Fill the screen with a different color
    screen.fill(BLACK)

    # Render content for the new screen 4
    text = font.render("Tutorial: Use wasd to move around your player and the ship. Use Enter to interact with characters", True, WHITE)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)

    # Render back button
    back_button = pygame.Rect(20, 20, 100, 50)
    pygame.draw.rect(screen, GRAY, back_button)
    back_text = font.render("Back", True, BLACK)
    back_text_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_text_rect)
    global back_button_rect
    back_button_rect = back_button

if __name__ == "__main__":
    main_screen()
