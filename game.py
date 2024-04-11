import pygame
import sys
import pygame.freetype

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

# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
    def update(self):
        key = pygame.key.get_pressed()
        dist = 2 # distance moved in 1 frame, try changing it to 5
        if key[pygame.K_s]: # down key
            self.rect.y += dist # move down
            self.rect.bottom = min(self.rect.bottom, screen_height)
        elif key[pygame.K_w]: # up key
            self.rect.y -= dist # move up
            self.rect.top = max(self.rect.top, 0)
        if key[pygame.K_d]: # right key
            self.rect.x += dist # move right
            self.rect.right = min(self.rect.right, screen_width)
        elif key[pygame.K_a]: # left key
            self.rect.x -= dist # move left
            self.rect.left = max(self.rect.left, 0)

    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.rect.x, self.rect.y))

# Define NPC class
class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

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

npc = NPC(500, 500)  # Adjust position as needed
all_sprites.add(npc)
npcs.add(npc)
font = pygame.freetype.SysFont('firacode', 20)
# Main loop
running = True
is_colliding = False 
text = ["Collision 1, test long text, test long text, test long text, test long text", "C2", "C3", "c4"]
col = -1
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    #player.handle_keys()
    # Check for collisions
    hits = pygame.sprite.spritecollide(player, npcs, False)
    if hits: 
        if not is_colliding:
            col += 1
        is_colliding = True
        if col < len(text):
            word_wrap(screen, text[col], font, BLACK)
    else:
        is_colliding = False
        # Here you can add code to display the blob of text

    # Update
    all_sprites.update()

    # Draw
    all_sprites.draw(screen)

    # Refresh the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
