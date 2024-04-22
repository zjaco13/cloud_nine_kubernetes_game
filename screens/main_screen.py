import pygame
import sys
import pygame.freetype
from util.util import word_wrap, WHITE, GRAY, BLACK, RED, font
from screens.ship_screen import ship_screen

# Define game states
MAIN_MENU = 0
PLAY = 1
DESCRIPTION = 2
TEAM = 3
TUTORIAL = 4

# Initial game state
current_state = MAIN_MENU

# Load the image
background_image = pygame.image.load('sprites/background.jpg')
background2_image = pygame.image.load('sprites/background2.jpg')

def main_screen(screen):
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
                    if play_button_rect.collidepoint(event.pos):
                        # Change to the new screen state
                        current_state = PLAY
                    elif description_button_rect.collidepoint(event.pos):
                        current_state = DESCRIPTION
                    elif team_button_rect.collidepoint(event.pos):
                        current_state = TEAM
                    elif tut_button_rect.collidepoint(event.pos):
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
            render_main_menu(screen)
        elif current_state == PLAY:
            play_game(screen)
        elif current_state == DESCRIPTION:
            render_description(screen)
        elif current_state == TEAM:
            render_team(screen)
        elif current_state == TUTORIAL:
            render_tutorial(screen)

        # Update the display
        pygame.display.flip()

def render_main_menu(screen):
    # Fill the screen with white color
    #screen.fill(WHITE)
    screen.blit(background_image, (0, 0))
    screen_width, screen_height = screen.get_size()

    # Render title of the game on the screen
    #font.render_to(screen, (screen_width // 2 - 200, screen_height // 2 - 50), "Kubernetes Pirate Adventure", RED)

    title_button = pygame.Rect(screen_width // 2 - 200, screen_height // 2 - 50, 450, 50)
    pygame.draw.rect(screen, GRAY, title_button)
    title_text,_ = font.render("Kubernetes Pirate Adventure", BLACK)
    title_text_rect = title_text.get_rect(center=title_button.center)
    screen.blit(title_text, title_text_rect)
    global title_button_rect 
    title_button_rect = title_button


    # Draw play button 1 - PLAY
    play_button = pygame.Rect(screen_width // 2 - 150, screen_height // 2 + 50, 300, 50)
    pygame.draw.rect(screen, GRAY, play_button)
    play_text, _ = font.render("PLAY", BLACK)
    play_text_rect = play_text.get_rect(center = play_button.center)
    screen.blit(play_text, play_text_rect)
    global play_button_rect
    play_button_rect = play_button

    # Draw play button 2 - DESCRIPTION
    description_button = pygame.Rect(screen_width // 2 - 150, screen_height // 2 + 120, 300, 50)
    pygame.draw.rect(screen, GRAY, description_button)
    description_text,_ = font.render("DESCRIPTION", BLACK)
    description_text_rect = description_text.get_rect(center=description_button.center)
    screen.blit(description_text, description_text_rect)
    global description_button_rect 
    description_button_rect = description_button

    # Draw play button 3 - TEAM
    team_button = pygame.Rect(screen_width // 2 - 150, screen_height // 2 + 190, 300, 50)
    pygame.draw.rect(screen, GRAY, team_button)
    team_text,_ = font.render("TEAM", BLACK)
    team_text_rect = team_text.get_rect(center=team_button.center)
    screen.blit(team_text, team_text_rect)
    global team_button_rect
    team_button_rect = team_button

    # Draw play button 3 - TUTORIAL
    tut_button = pygame.Rect(screen_width // 2 - 150, screen_height // 2 + 260, 300, 50)
    pygame.draw.rect(screen, GRAY, tut_button)
    tut_text,_ = font.render("TUTORIAL", BLACK)
    tut_text_rect = tut_text.get_rect(center=tut_button.center)
    screen.blit(tut_text, tut_text_rect)
    global tut_button_rect
    tut_button_rect = tut_button

def play_game(screen):
    ship_screen(screen)


def render_description(screen):
    # Fill the screen with a different color
    #screen.fill(BLACK)
    screen.blit(background2_image, (0, 0))
    screen_width, screen_height = screen.get_size()

    #word_wrap(screen, "The purpose of this game is to teach you about open source tools that are critical to know for today's cloud focused environment.  The 2 tools focused on in this game are Docker and Kubernetes.  With a grasp of these tools, you will be primed for success when developing and deploying your application to the world", font, WHITE)

    text, _ = font.render("The purpose of this game is to teach you about open source tools", BLACK)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    text_box_rect = text_rect.inflate(10, 10)
    pygame.draw.rect(screen, WHITE, text_box_rect)
    screen.blit(text, text_rect)

    text2, _ = font.render("that are critical to know for today's cloud focused environment.", BLACK)
    text2_rect = text.get_rect(center=(screen_width // 2, (screen_height // 2) + 40))
    text2_box_rect = text2_rect.inflate(10, 10)
    pygame.draw.rect(screen, WHITE, text2_box_rect)
    screen.blit(text2, text2_rect)

    text3, _ = font.render("The 2 tools focused on in this game are Docker and Kubernetes.", BLACK)
    text3_rect = text.get_rect(center=(screen_width // 2, (screen_height // 2) + 80))
    text3_box_rect = text3_rect.inflate(10, 10)
    pygame.draw.rect(screen, WHITE, text3_box_rect)
    screen.blit(text3, text3_rect)

    text4, _ = font.render("With a grasp of these tools, you will be primed for success when", BLACK)
    text4_rect = text.get_rect(center=(screen_width // 2, (screen_height // 2) + 120))
    text4_box_rect = text4_rect.inflate(10, 10)
    pygame.draw.rect(screen, WHITE, text4_box_rect)
    screen.blit(text4, text4_rect)

    text5, _ = font.render("developing and deploying your application to the world.", BLACK)
    text5_rect = text.get_rect(center=(screen_width // 2, (screen_height // 2) + 160))
    text5_box_rect = text5_rect.inflate(10, 10)
    pygame.draw.rect(screen, WHITE, text5_box_rect)
    screen.blit(text5, text5_rect)

    # Render back button
    back_button = pygame.Rect(20, 20, 100, 50)
    pygame.draw.rect(screen, GRAY, back_button)
    back_text, _ = font.render("Back", BLACK)
    back_text_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_text_rect)
    global back_button_rect
    back_button_rect = back_button

def render_team(screen):
    # Fill the screen with a different color
    #screen.fill(BLACK)
    screen.blit(background2_image, (0, 0))
    screen_width, screen_height = screen.get_size()

    # Render content for the new screen 3
    text, _ = font.render("Team: Zach Jacobson, Phong Duong, Om Patel, Shreiyas Saraf", BLACK)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    text_box_rect = text_rect.inflate(10, 10)
    pygame.draw.rect(screen, WHITE, text_box_rect)
    screen.blit(text, text_rect)

    # Render back button
    back_button = pygame.Rect(20, 20, 100, 50)
    pygame.draw.rect(screen, GRAY, back_button)
    back_text, _ = font.render("Back", BLACK)
    back_text_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_text_rect)
    global back_button_rect
    back_button_rect = back_button

def render_tutorial(screen):
    # Fill the screen with a different color
    #screen.fill(BLACK)
    screen.blit(background2_image, (0, 0))
    screen_width, screen_height = screen.get_size()

    # Render content for the new screen 4
    text, _ = font.render("Use wasd to move the player's sprite. Use Enter to interact with characters", BLACK)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    text_box_rect = text_rect.inflate(10, 10)
    pygame.draw.rect(screen, WHITE, text_box_rect)
    screen.blit(text, text_rect)

    # Render back button
    back_button = pygame.Rect(20, 20, 100, 50)
    pygame.draw.rect(screen, GRAY, back_button)
    back_text, _ = font.render("Back", BLACK)
    back_text_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_text_rect)
    global back_button_rect
    back_button_rect = back_button
