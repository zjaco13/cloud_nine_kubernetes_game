import pygame
import sys
import pygame.freetype
import subprocess

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 1280 
screen_height = 900 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Kubernetes Game")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0,0, 255)

# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.dockerIsland = pygame.image.load("DockerImg.png").convert()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.dx = 0
        self.dy = 0
        self.frozen = False
        self.is_colliding = False
    def update(self, *args, **kwargs):
        key = pygame.key.get_pressed()
        self.dx = 0
        self.dy = 0 
        dist = 2 # distance moved in 1 frame, try changing it to 5
        if key[pygame.K_s]: # down key
            self.dy += dist
        elif key[pygame.K_w]: # up key
            self.dy -= dist
        if key[pygame.K_d]: # right key
            self.dx+= dist
        elif key[pygame.K_a]: # left key
            self.dx-= dist
        if not self.frozen:
            self.rect.x += self.dx
            self.rect.y += self.dy
        collisions = pygame.sprite.spritecollide(self, npcs, False)
        if collisions:
            self.is_colliding = True

        self.rect.left = max(self.rect.left, 0)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, screen_height)
        self.rect.right = min(self.rect.right, screen_width)

# Define NPC class
class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, text):
        super().__init__()
        self.dockerIsland = pygame.image.load("DockerImg.png").convert()
        self.kubeIsland = None
        self.image = screen.blit(self.dockerIsland, (x, y))
        # self.image.fill(BLACK)
        self.rect = self.image
        self.rect.center = (x, y)
        self.is_colliding = False
        self.col = 0 
        self.text = text
        self.last_keypress = 0
        self.spoken = False

    def update(self, *args, **kwargs) -> None:
        collisions = pygame.sprite.spritecollide(self, players, False)
        player = None
        for p in collisions:
            if self.spoken:
                p.rect.x -= p.dx
                p.rect.y -= p.dy
            else:
                p.frozen = True
                self.is_colliding = True
                player = p
        if self.is_colliding:
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                curr_keypress = pygame.time.get_ticks()
                if curr_keypress - self.last_keypress > 750:
                    self.col += 1
                    self.last_keypress = curr_keypress
            if self.col < len(self.text):
                word_wrap(screen, self.text[self.col], font, BLACK)
            else:
                player.frozen = False
                self.is_colliding = False
                player.is_colliding = False
                self.spoken = True

class Helm_NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, text):
        super().__init__()
        self.dockerIsland = pygame.image.load("DockerImg.png").convert()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.is_colliding = False
        self.col = 0 
        self.text = text
        self.spoken_y = False
        self.spoken_n = False
    def update(self, *args, **kwargs) -> None:
        collisions = pygame.sprite.spritecollide(self, players, False)
        player = None
        if not collisions and self.spoken_n:
            self.spoken_n = False 
            self.col = 0
            
        for p in collisions:
            if self.spoken_y or self.spoken_n:
                p.rect.x -= p.dx
                p.rect.y -= p.dy
            else:
                p.frozen = True
                self.is_colliding = True
                player = p
            if pygame.key.get_pressed()[pygame.K_y]:
                self.spoken_y = True
                self.col += 1
            if pygame.key.get_pressed()[pygame.K_n]:
                self.col += 1
                self.spoken_n = True
            if self.col < len(self.text):
                word_wrap(screen, self.text[self.col], font, BLACK)
            else:
                player.frozen = False
                self.is_colliding = False
                player.is_colliding = False

def word_wrap(surf, text, font, color=(0, 0, 0)):
    font.origin = True
    words = text.split(' ')
    width, height = surf.get_size()
    line_spacing = font.get_sized_height() + 2
    x, y = 0, screen_height - line_spacing*5
    space = font.get_rect(' ')
    for word in words:
        bounds = font.get_rect(word)
        if x + bounds.width + bounds.x >= width:
            x, y = 0, y + line_spacing
        if x + bounds.width + bounds.x >= width:
            raise ValueError("word too wide for the surface")
        if y + bounds.height - bounds.y >= height:
            raise ValueError("text to long for the surface")
        font.render_to(surf, (x, y), None, color)
        x += bounds.width + space.width
    return x, y

# Create sprite groups
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
npcs = pygame.sprite.Group()

# Create player and NPC objects
player = Player()
all_sprites.add(player)
players.add(player)
kube_text = ["k1", "k2", "k3"]
docker_text = ["d1", "d2", "d3"]
start_text = ["Set Sail? (Y/N)"]

kube_npc = NPC(300, 800, kube_text)
docker_npc = NPC(700, 200,docker_text)
start_npc = Helm_NPC(200,450, start_text)
  # Adjust position as needed
all_sprites.add(kube_npc, docker_npc, start_npc)
npcs.add(kube_npc, docker_npc, start_npc)
font = pygame.freetype.SysFont('firacode', 20)

# Font for rendering text
font_input = pygame.font.Font(None, 32)

# Main loop
running = True
user_input = ""
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("User input:", user_input)
                user_input = ""
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            elif event.key >= 32 and event.key <= 126:  # Only handle printable ASCII characters
                user_input += event.unicode

	    redirect_collisions = pygame.sprite.spritecollide(self, all_sprites[1:], False)
		if redirect_collisions:
		    # Redirect to the other program
		    subprocess.Popen(["python", "docker_game.py"])
		    pygame.quit()
		    sys.exit()
		other_collisions = pygame.sprite.spritecollide(self, all_sprites[0] + all_sprites[-1], False)
		if redirect_collisions:
		    # Redirect to the other program
		    subprocess.Popen(["python", "docker_game.py"]) #will eventually be kubernetes.py
		    pygame.quit()
		    sys.exit()


    screen.fill(WHITE)
    # Update
    all_sprites.update()

    # Draw
    all_sprites.draw(screen)

    # Render user input text
    input_text_surface = font_input.render(user_input, True, BLACK)
    screen.blit(input_text_surface, (20, 20))

    # Refresh the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
