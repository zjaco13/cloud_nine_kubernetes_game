import pygame
import sys
import pygame.freetype
from util.util import FONT_SIZE_MEDIUM, HEIGHT, WIDTH, word_wrap, WHITE, GRAY, BLACK, RED, font, word_wrap_with_box

# Define game states
MAIN_MENU = 0
PLAY = 1
DESCRIPTION = 2
TEAM = 3
TUTORIAL = 4

# Initial game state
current_state = MAIN_MENU

# Load the image
background_image = pygame.transform.scale(pygame.image.load('sprites/background.jpg'), (WIDTH, HEIGHT))
background2_image = pygame.transform.scale(pygame.image.load('sprites/background2.jpg'), (WIDTH, HEIGHT))

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
            current_state = MAIN_MENU
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

    title_button = pygame.Rect(screen_width // 2 - 300, screen_height // 2 - 50, 600, 50)
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
    from screens.ship_screen import ship_screen
    ship_screen(screen)


def render_description(screen):
    # Fill the screen with a different color
    #screen.fill(BLACK)
    screen.blit(background2_image, (0, 0))
    screen_width, screen_height = screen.get_size()

    #word_wrap(screen, "The purpose of this game is to teach you about open source tools that are critical to know for today's cloud focused environment.  The 2 tools focused on in this game are Docker and Kubernetes.  With a grasp of these tools, you will be primed for success when developing and deploying your application to the world", font, WHITE)
    word_wrap_with_box(screen, "The purpose of this game is to teach you about open source tools that are critical to know for today's cloud focused environment.  The 2 tools focused on in this game are Docker and Kubernetes.  With a grasp of these tools, you will be primed for success when developing and deploying your application to the world", font, BLACK, box_surface = pygame.Surface((WIDTH, 300)), starty = HEIGHT // 2 + 250, box_color= WHITE, size=FONT_SIZE_MEDIUM)

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
    word_wrap_with_box(screen, "Use wasd to move the player's sprite. Use Enter to interact with characters.  When traveling to islands, use F to open your file inventory, and Enter to close it.", font, BLACK, box_surface=pygame.Surface((WIDTH, 200)), box_color=WHITE, starty=HEIGHT //2 -100, size=FONT_SIZE_MEDIUM)

    # Render back button
    back_button = pygame.Rect(20, 20, 100, 50)
    pygame.draw.rect(screen, GRAY, back_button)
    back_text, _ = font.render("Back", BLACK)
    back_text_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_text_rect)
    global back_button_rect
    back_button_rect = back_button
