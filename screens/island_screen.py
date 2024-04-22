import pygame
import sys
from util.util import word_wrap_with_box, WHITE, BLACK, font, OCEAN_BLUE
pygame.init()

deployment_sections = [("apiVersion: apps/v1\nkind: Deployment", "tells kubernetes which version of the api to use and what type of object is getting created/updated/deleted by this file"),
                       ("metadata:\n\tname: ai-demo", "gives a name to the deployment"),
                       ("spec:\n\treplicas: 2", "How many pods of this app should be in the cluster at all times, controlled by the ReplicaSet"),
                       ("\tselector:\n\t\tmatchLabels:\n\t\t\tapp: ai-demo", "tells the ReplicaSet which pods it should manage based on the app selected"),
                       ("\ttemplate:\n\t\tmetadata:\n\t\t\tlabels:\n\t\t\t\tapp: ai-demo", "gives each pod a label so that it can be managed by the replicaset"),
                       ("\t\tspec:\n\t\t\tcontainers:\n\t\t\t- name: ai-demo\n\t\t\t\timage: ai-demo\n\t\t\t\t\tports:\n\t\t\t\t\t- containerPort: 3000", "tells the pod which container to one, the name of it, the image it should use, and which ports it should expose")]

dockerfile_sections = [("FROM python:3.11", "base image to pull from, normally use different language images as base"), 
                       ("WORKDIR /app","set the working directory in the container"),
                       ("COPY . /app", "copy app contents to the container working directory"),
                       ("RUN pip install --no-cache-dir -r requirements.txt", "run instructions to build/install dependencies"),
                       ("EXPOSE 3000", "Expose a port on a container if need to access externally"),
                       ("CMD [\"python\", \"server.py\"]"), "run the command specified for cmd"]

service_sections = [("apiVersion: v1\nkind: Service", "tells kubernetes which version of the api to use and which object will be created/updated/deleted by this file"),
                    ("metadata:\n\tname: ai-demo", "gives a name to the service"),
                    ("spec:\n\tselector:\n\t\tapp: ai-demo", "tells the service which pods are served traffic from this service"),
                    ("\tports:\n\t\t- protocol: TCP\n\t\tport: 80\n\t\ttargetPort: 3000", "The port that will be exposed to the internet by this service,The port on the container to pass the traffic to"),
                    ("\ttype: LoadBalancer", "The type of service (LoadBalancer - exposes to external load balancer handled by cloud provider - easiest option to setup, NodePort - exposed on a static port of the clusters ip address, ClusterIP - cluster internal only, ExternalName - maps service to some hostname and sets up DNS on the cluster for that name)")]

all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
islands = pygame.sprite.Group()

# Define player class
class Boat(pygame.sprite.Sprite):
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
        self.files = [File("Dockerfile"), File("deployment.yaml"), File("service.yaml")]
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
        collisions = pygame.sprite.spritecollide(self, islands, False)
        if collisions:
            self.is_colliding = True

        self.rect.left = max(self.rect.left, 0)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, self.screen_height)
        self.rect.right = min(self.rect.right, self.screen_width)


# Define NPC class
class Island(pygame.sprite.Sprite):
    def __init__(self, x, y, text, image):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.sprite = pygame.image.load(image)
        self.sprite = pygame.transform.scale(self.sprite, (50, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.is_colliding = False
        self.text = text
        self.spoken = False
        self.input = ""
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
            while True:
                word_wrap_with_box(screen, self.text + "\n\n" + self.input, font, BLACK, size=20)
                pygame.display.flip()
                if self.input == self.text:
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            self.input = self.input[:-1]
                        elif event.key >= 32 and event.key <= 126:  # Only handle printable ASCII characters
                            self.input += event.unicode
                        elif event.key == pygame.K_RETURN:
                            self.input += "\n"
                        elif event.key == pygame.K_TAB:
                            self.input += "\t"
            pygame.time.delay(1000)
            player.frozen = False
            self.is_colliding = False
            player.is_colliding = False
            self.spoken = True

class File(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.sprite = pygame.image.load('sprites/helmNPC.jpg')
        self.sprite = pygame.transform.scale(self.sprite, (50, 80))
        self.is_colliding = False
        self.col = 0 
        self.spoken_y = False
        self.spoken_n = False
    def update(self, *args, **kwargs) -> None:
        screen = None
        if len(args) > 0:
            screen = args[0]
        else:
            raise ValueError("Missing Screen argument")

def island_screen(screen):
    screen_width, screen_height = screen.get_size()
    # Create player and NPC objects
    
    player = Boat(screen_width, screen_height)
    all_sprites.add(player)
    players.add(player)
    

    kube_npc = Island(300, 800, deployment_sections[0][0], 'sprites/KuberNPC.jpg')
    docker_npc = Island(700, 200,dockerfile_sections[1][0], 'sprites/dockerSprite.jpg')
    start_npc = Island(200,450, dockerfile_sections[2][0], 'sprites/dockerSprite.jpg')
      # Adjust position as needed
    all_sprites.add(kube_npc, docker_npc, start_npc)
    islands.add(kube_npc, docker_npc, start_npc)
    
    # Font for rendering text
    font_input = pygame.font.Font(None, 32)
    
    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        screen.fill(OCEAN_BLUE)
        # Update
        all_sprites.update(screen)
    
        # Draw
        all_sprites.draw(screen)
        screen.blit(player.sprite, player.rect)
        screen.blit(kube_npc.sprite, kube_npc.rect)
        screen.blit(start_npc.sprite, start_npc.rect)
        screen.blit(docker_npc.sprite, docker_npc.rect)
    
        # Refresh the display
        pygame.display.flip()
    
        # Cap the frame rate
        pygame.time.Clock().tick(60)
    
    # Quit Pygame
    pygame.quit()
    sys.exit()
