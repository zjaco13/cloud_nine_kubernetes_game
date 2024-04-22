from docker.api.build import random
import pygame
import sys
from util.util import word_wrap_with_box, WHITE, BLACK, font, OCEAN_BLUE, WIDTH, HEIGHT
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
        self.sprite = pygame.transform.scale(self.sprite, (50, 50))
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
        self.image = pygame.Surface((30, 30))
        self.sprite = pygame.image.load(image)
        self.sprite = pygame.transform.scale(self.sprite, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.is_colliding = False
        self.text = text[0]
        self.description = text[1]
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
                word_wrap_with_box(screen, self.text, font, BLACK, box_surface=pygame.Surface((WIDTH // 2, HEIGHT - 250)),starty = HEIGHT-250, size=20)
                word_wrap_with_box(screen, "Copy this text to your file:\n" + self.input, font, BLACK, box_surface=pygame.Surface((WIDTH // 2, HEIGHT - 250)), startx = WIDTH//2, starty = HEIGHT - 250, size=20)
                word_wrap_with_box(screen, self.description, font, BLACK, box_surface=pygame.Surface((WIDTH, 250)),size=20)
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

def circles_collide(circle1, circle2, min_distance):
    distance_squared = (circle1[0] - circle2[0]) ** 2 + (circle1[1] - circle2[1]) ** 2
    min_distance_squared = min_distance ** 2
    return distance_squared < min_distance_squared
def generate_island_positions(num_islands, min_distance):
    island_positions = []
    for _ in range(num_islands):
        valid_position = False
        while not valid_position:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            valid_position = True
            for island_pos in island_positions:
                if circles_collide((x, y), island_pos, min_distance) or (x in range(WIDTH//2-50, WIDTH//2+50) and y in range(HEIGHT//2-50 ,HEIGHT//2+50)):
                    valid_position = False
                    break
        island_positions.append((x, y))
    return island_positions

def island_screen(screen):
    # Create player and NPC objects
    
    player = Boat(WIDTH, HEIGHT)
    all_sprites.add(player)
    players.add(player)
    

    docker_idx = 0
    deploy_idx = 0
    service_idx = 0
    indices = [docker_idx, deploy_idx, service_idx]
    sections = [dockerfile_sections, deployment_sections, service_sections]
    island_positions = generate_island_positions(len(dockerfile_sections) + len(deployment_sections) + len(service_sections), 100)
    pos_idx = 0
    while any(idx < len(lst) for idx, lst in zip(indices, sections)):
        x,y = island_positions[pos_idx]
        island = None
        idx = random.randint(0,2)
        if indices[idx] < len(sections[idx]):
            island = Island(x,y, sections[idx][indices[idx]], 'sprites/islandSpriteNeedCrop.jpg')
            indices[idx] += 1
            pos_idx += 1
        if island:
            all_sprites.add(island)
            islands.add(island)
    print(len(islands.sprites()))
    
    # Font for rendering text
    
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
        for island in islands.sprites():
            screen.blit(island.sprite, island.rect)
    
        # Refresh the display
        pygame.display.flip()
    
        # Cap the frame rate
        pygame.time.Clock().tick(60)
    
    # Quit Pygame
    pygame.quit()
    sys.exit()
