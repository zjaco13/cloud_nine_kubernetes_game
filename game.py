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
        self.dx = 0
        self.dy = 0
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
        self.rect.x += self.dx
        self.rect.y += self.dy
        collisions = pygame.sprite.spritecollide(self, npcs, False)
        #for npc in collisions:

        self.rect.left = max(self.rect.left, 0)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, screen_height)
        self.rect.right = min(self.rect.right, screen_width)
    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.rect.x, self.rect.y))

# Define NPC class
class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, text):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.is_colliding = False
        self.col = -1
        self.text = text
    def update(self, *args, **kwargs) -> None:

        collisions = pygame.sprite.spritecollide(self, players, False)
        if not collisions:
            self.is_colliding = False
        for player in collisions:
            if self.is_colliding:
                player.rect.center = (player.rect.centerx - player.dx, player.rect.centery -player.dy)
            if not self.is_colliding:
                self.col += 1
                print(self.col)
            self.is_colliding = True
            if self.col < len(self.text):
                word_wrap(screen, self.text[self.col], font, BLACK)



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

npc = NPC(500, 500, text = ["Collision 1, test long text, test long text, test long text, test long text", "C2", "C3", "c4"]
)  # Adjust position as needed
all_sprites.add(npc)
npcs.add(npc)
font = pygame.freetype.SysFont('firacode', 20)
# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
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
