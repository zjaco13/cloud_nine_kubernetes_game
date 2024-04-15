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
BLUE = (0,0, 255)
BROWN = (139, 69, 19)
OCEAN_BLUE = (25, 25, 112)

boat_width = 1100
boat_height = 650 
boat_x = (screen_width - boat_width) // 2
boat_y = (screen_height - boat_height) // 2
boat_rect = pygame.Rect(boat_x, boat_y, boat_width, boat_height)

# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.sprite = pygame.image.load('sprites/humanSprite.jpg')
        self.sprite = pygame.transform.scale(self.sprite, (50, 80))
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

        self.rect.clamp_ip(boat_rect)
        # self.rect.left = max(self.rect.left, 0)
        # self.rect.top = max(self.rect.top, 0)
        # self.rect.bottom = min(self.rect.bottom, screen_height)
        # self.rect.right = min(self.rect.right, screen_width)


# Define NPC class
class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, text, image):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.sprite = pygame.image.load(image)
        self.sprite = pygame.transform.scale(self.sprite, (50, 80))
        self.rect = self.image.get_rect()
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
                if curr_keypress - self.last_keypress > 500:
                    self.col += 1
                    self.last_keypress = curr_keypress
            if self.col < len(self.text):
                word_wrap_with_box(screen, self.text[self.col], font, BLACK)
            else:
                player.frozen = False
                self.is_colliding = False
                player.is_colliding = False
                self.spoken = True

class Helm_NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, text):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.sprite = pygame.image.load('sprites/humanSprite.jpg')
        self.sprite = pygame.transform.scale(self.sprite, (50, 80))
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
        if self.is_colliding:
            if pygame.key.get_pressed()[pygame.K_y]:
                self.spoken_y = True
                self.col += 1
            if pygame.key.get_pressed()[pygame.K_n]:
                self.col += 1
                self.spoken_n = True
            if self.col < len(self.text):
                word_wrap_with_box(screen, self.text[self.col], font, BLACK)
            else:
                player.frozen = False
                self.is_colliding = False
                player.is_colliding = False

def word_wrap_with_box(surf, text, font, color=(0, 0, 0), box_color=(205, 133, 63)):
    font.origin = True
    words = text.split(' ')
    width, height = surf.get_size()
    line_spacing = font.get_sized_height() + 2
    space = font.get_rect(' ')
    
    # Calculate text size
    text_width = 0
    text_height = 0
    for word in words:
        bounds = font.get_rect(word)
        text_width += bounds.width + space.width
        if text_width > width:  # Adjust text width to fit within screen width
            text_width = width
            break
        if text_height + line_spacing + bounds.height - bounds.y > height:  # Adjust text height to fit within screen height
            text_height = height
            break
        text_height += line_spacing + bounds.height - bounds.y

    # Create bounding box surface
    box_surface = pygame.Surface((width,  line_spacing*5+20))
    box_surface.fill(box_color)
    box_rect = box_surface.get_rect()
    box_rect.bottomleft = (0, height)

    # Render text onto the box surface
    x, y = 0, 0
    for word in words:
        bounds = font.get_rect(word)
        if x + bounds.width + bounds.x >= width - 10:
            x, y = 0, y + line_spacing
        font.render_to(box_surface, (x + 10, y + line_spacing), None, color)
        x += bounds.width + space.width

    screen.blit(box_surface, box_rect)  # Blit the text surface onto the screen
    pygame.draw.rect(screen, (0, 0, 0), box_rect, 2)  # Draw the bounding box around the text
    return box_surface, box_rect

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
kube_text = ["Kubernetes is a portable, extensible, open source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation. It has a large, rapidly growing ecosystem. Kubernetes services, support, and tools are widely available.", "Kubernetes provides you with a framework to run distributed systems resiliently. It takes care of scaling and failover for your application, provides deployment patterns, and more.", "Kubernetes runs your workload by placing containers into Pods to run on Nodes. A node may be a virtual or physical machine, depending on the cluster. Each node is managed by the control plane and contains the services necessary to run Pods."]
docker_text = [
"Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications. By taking advantage of Docker's methodologies for shipping, testing, and deploying code, you can significantly reduce the delay between writing code and running it in production.", 
"Docker provides the ability to package and run an application in a loosely isolated environment called a container. The isolation and security lets you run many containers simultaneously on a given host. Containers are lightweight and contain everything needed to run the application, so you don't need to rely on what's installed on the host. You can share containers while you work, and be sure that everyone you share with gets the same container that works in the same way.", "Docker's container-based platform allows for highly portable workloads. Docker containers can run on a developer's local laptop, on physical or virtual machines in a data center, on cloud providers, or in a mixture of environments. Docker's portability and lightweight nature also make it easy to dynamically manage workloads, scaling up or tearing down applications and services as business needs dictate, in near real time."]
start_text = ["Set Sail? (Y/N)"]

kube_npc = NPC(boat_x+700, boat_y + 150, kube_text, 'sprites/KuberNPC.jpg')
docker_npc = NPC(boat_x+850, boat_y + 400, docker_text, 'sprites/dockerSprite.jpg')
start_npc = Helm_NPC(boat_x+100,boat_y + boat_height//2, start_text)
  # Adjust position as needed
all_sprites.add(kube_npc, docker_npc, start_npc)
npcs.add(kube_npc, docker_npc, start_npc)
font = pygame.freetype.SysFont('firacode', 20)
# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(OCEAN_BLUE)
    pygame.draw.rect(screen, BROWN, boat_rect)
    # Update
    all_sprites.update()

    # Draw
    all_sprites.draw(screen)
    screen.blit(player.sprite, player.rect)

    # Refresh the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
