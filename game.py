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

def main_screen():
    while True:

        # Fill the screen with white color
        screen.fill(WHITE)

        # Render title of the game on the screen
        title = font.render("Game's Name Space", True, BLACK)
        title_rect = title.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(title, title_rect)

        # Render tutorial on the screen
        font_40 = pygame.font.Font(None, 40) 
        tutorial = font_40.render("Tutorial: Use wasd to move around, enter to interact", True, BLACK)
        tutorial_rect = tutorial.get_rect(topleft=(0, 20))
        screen.blit(tutorial, tutorial_rect)

        # Render description on the screen
        font_15 = pygame.font.Font(None, 15) 
        description = font_15.render("Description: This games will teach you about how to build a ML application, deploy it on the cloud using open source tooling, specifically Docker and Kubernetes", True, BLACK)
        description_rect = description.get_rect(topleft=(0, 60))
        screen.blit(description, description_rect)

        # Render team member's names on the screen
        font_20 = pygame.font.Font(None, 20) 
        team = font_20.render("Team: Shreiyas Saraf, Phong Duong, Zach Jacobson, Om Patel", True, BLACK)
        team_rect = team.get_rect(bottomleft=(0, screen_height - 20))
        screen.blit(team, team_rect)

        # Draw play button
        play_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 50, 200, 50)
        pygame.draw.rect(screen, GRAY, play_button)
        play_text = font.render("Play", True, BLACK)
        play_text_rect = play_text.get_rect(center=play_button.center)
        screen.blit(play_text, play_text_rect)
        global play_button_rect
        play_button_rect = play_button


        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is within the play button area
                if play_button_rect.collidepoint(event.pos):
                    # Call a function to start the game
                    start_game()

        # Update the display
        pygame.display.flip()

def start_game():
    # Here you can define the logic to start the actual game
    print("Game started!")

if __name__ == "__main__":
    main_screen()
