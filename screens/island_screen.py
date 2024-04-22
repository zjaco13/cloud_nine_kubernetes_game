import pygame
import sys
from util.util import word_wrap_with_box, WHITE, BLACK, font
pygame.init()

kube_text = ["Kubernetes is a portable, extensible, open source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation. It has a large, rapidly growing ecosystem. Kubernetes services, support, and tools are widely available.", "Kubernetes provides you with a framework to run distributed systems resiliently. It takes care of scaling and failover for your application, provides deployment patterns, and more.", "Kubernetes runs your workload by placing containers into Pods to run on Nodes. A node may be a virtual or physical machine, depending on the cluster. Each node is managed by the control plane and contains the services necessary to run Pods."]
docker_text = [
"Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications. By taking advantage of Docker's methodologies for shipping, testing, and deploying code, you can significantly reduce the delay between writing code and running it in production.", 
"Docker provides the ability to package and run an application in a loosely isolated environment called a container. The isolation and security lets you run many containers simultaneously on a given host. Containers are lightweight and contain everything needed to run the application, so you don't need to rely on what's installed on the host. You can share containers while you work, and be sure that everyone you share with gets the same container that works in the same way.", "Docker's container-based platform allows for highly portable workloads. Docker containers can run on a developer's local laptop, on physical or virtual machines in a data center, on cloud providers, or in a mixture of environments. Docker's portability and lightweight nature also make it easy to dynamically manage workloads, scaling up or tearing down applications and services as business needs dictate, in near real time."]
start_text = ["Set Sail? (Y/N)"]
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
npcs = pygame.sprite.Group()

# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.sprite = pygame.image.load('sprites/humanSprite.jpg')
        self.sprite = pygame.transform.scale(self.sprite, (50, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.screen_height = screen_height
        self.screen_width = screen_width
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
        self.rect.bottom = min(self.rect.bottom, self.screen_height)
        self.rect.right = min(self.rect.right, self.screen_width)


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
        screen = None
        if len(args) > 0:
            screen = args[0]
        else:
            raise ValueError("Missing Screen argument")
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
                word_wrap_with_box(screen, self.text[self.col], font, BLACK, size=20)
            else:
                player.frozen = False
                self.is_colliding = False
                player.is_colliding = False
                self.spoken = True

class Helm_NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, text):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.sprite = pygame.image.load('sprites/helmNPC.jpg')
        self.sprite = pygame.transform.scale(self.sprite, (50, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.is_colliding = False
        self.col = 0 
        self.text = text
        self.spoken_y = False
        self.spoken_n = False
    def update(self, *args, **kwargs) -> None:
        screen = None
        if len(args) > 0:
            screen = args[0]
        else:
            raise ValueError("Missing Screen argument")
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

def island_screen(screen):
    screen_width, screen_height = screen.get_size()
    # Create player and NPC objects
    
    player = Player(screen_width, screen_height)
    all_sprites.add(player)
    players.add(player)
    kube_text = ["k1", "k2", "k3"]
    docker_text = ["d1", "d2", "d3"]
    start_text = ["Set Sail? (Y/N)"]
    
    kube_npc = NPC(300, 800, kube_text, 'sprites/KuberNPC.jpg')
    docker_npc = NPC(700, 200,docker_text, 'sprites/dockerSprite.jpg')
    start_npc = Helm_NPC(200,450, start_text)
      # Adjust position as needed
    all_sprites.add(kube_npc, docker_npc, start_npc)
    npcs.add(kube_npc, docker_npc, start_npc)
    
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
    
        screen.fill(WHITE)
        # Update
        all_sprites.update(screen)
    
        # Draw
        all_sprites.draw(screen)
        screen.blit(player.sprite, player.rect)
        screen.blit(kube_npc.sprite, kube_npc.rect)
        screen.blit(start_npc.sprite, start_npc.rect)
        screen.blit(docker_npc.sprite, docker_npc.rect)
    
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
