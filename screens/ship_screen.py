import pygame
import sys
from util.util import FONT_SIZE_MEDIUM, FONT_SIZE_SMALL, HEIGHT, WIDTH, word_wrap_with_box, font, WHITE, RED, BLACK, BLUE, OCEAN_BLUE, BROWN

pygame.init()

boat_width = 1100
boat_height = 650 
kube_text = ["- Kubernetes is a portable, extensible, open source platform for managing containerized workloads and services\n- It uses YAML files for declarative configuration.", "- In Kubernetes, applications are deployed onto a Kubernetes cluster\n- A cluster is a set of worker machines, called Nodes\n- Nodes host the Pods where the application workloads are run", "- There are a few different types of objects that can be applied to a Kubernetes cluster\n- The 2 most critical, which you will be looking for on your journey today are Deployments and Services", "- A Deployment describes the desired state of an application on a cluster\n- This includes describing the number of replica Pods to run at all times and which application to run on the Pod.", "- A Service exposes a group of Pods on the network\n- This enables internet traffic to reach the application hosted on the Pods\n- This way, the application can send and receive traffic wihtout being directly exposed to the outside world for higher security", "- Kubernetes is critical in todays cloud environment\n- It allows for rapid, automated scaling\n- It can nearly eliminate downtime during application upgrades", "Now go out there and find the pieces to the deployment.yaml file and service.yaml file so we can get back at the evil pirates!"]
docker_text = ["- Docker is an open source tool for shipping and running applications\n- It gives you the ability to package and run an application in an isolated environment called a container", "- A container is lightweight, and contains everything that is needed to run a specific application\n- This allows you to not have to worry about what is installed on any given machine\n- Containers are sharable, so when working on an application or deploying an application, you can always be sure that people are seeing the exact same results", "- Docker containers can run on laptops, virtual machines, data centers, the cloud, or a mix of all of the above\n- These containers are highly portable, so instead of waiting minutes for a big application to be downloaded across the world, it can happen instantaneously","- The build process of a container is specified by a Dockerfile\n- A Dockerfile contains a series of steps to run in order to build the end container for the application", "- At each step, a new container is created and cached, called a layer\n- This way on subsequent builds layers that have not changed can be loaded from the cache rather than rebuilt", "- Docker is critical in todays cloud environment\n- It allows developers to quickly share, test, and deploy applications\n- It allows for near instantaneous transfers across the globe\n- It adds another layer of security to every application running on top of it", "Go explore the world to find pieces of a Dockerfile to build your very own container!"]
start_text = ["Set Sail? (Y/N)"]
instructor_text = ["Talk to the two helper pirates about Kubernetes and Docker before asking the pirate at the wheel to set sail thorugh the ocean."]
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
npcs = pygame.sprite.Group()
shipBackground = pygame.transform.scale(pygame.image.load('sprites/shipBackground.jpg'), (WIDTH, HEIGHT))

# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self, boat_rect):
        super().__init__()
        self.boat_rect = boat_rect
        self.image = pygame.Surface((60, 108))
        self.sprite = pygame.image.load('sprites/humanSprite.png')
        self.sprite = pygame.transform.scale(self.sprite, (60, 108))
        self.rect = self.image.get_rect()
        self.rect.center = (850, 250)
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

        self.rect.clamp_ip(self.boat_rect)


# Define NPC class
class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, text, image, name):
        super().__init__()
        self.image = pygame.Surface((90, 120))
        self.sprite = pygame.image.load(image)
        self.sprite = pygame.transform.scale(self.sprite, (90, 120))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.is_colliding = False
        self.name = name
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
                word_wrap_with_box(screen, self.name, font, BLACK, box_surface=pygame.Surface((WIDTH, 50)),starty=HEIGHT-220, size=FONT_SIZE_MEDIUM)
                word_wrap_with_box(screen, self.text[self.col], font, BLACK, box_surface=pygame.Surface((WIDTH, 220)), size=FONT_SIZE_SMALL)
            else:
                player.frozen = False
                self.is_colliding = False
                player.is_colliding = False
                self.spoken = True

class Helm_NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, text):
        super().__init__()
        self.image = pygame.Surface((60, 120))
        self.sprite = pygame.image.load('sprites/helmNPC.png')
        self.sprite = pygame.transform.scale(self.sprite, (60, 120))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.is_colliding = False
        self.col = 0 
        self.text = text
        self.spoken_y = False
        self.spoken_n = False
        self.can_speak = False
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
            if self.spoken_y or self.spoken_n or not self.can_speak:
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


def to_island_screen(screen):
    from screens.island_screen import island_screen
    island_screen(screen)

def ship_screen(screen):
    boat_x = (WIDTH - boat_width) // 2
    boat_y = (HEIGHT - boat_height) // 2
    boat_rect = pygame.Rect(boat_x, boat_y, boat_width, boat_height)
    # Create player and NPC objects
    player = Player(boat_rect)
    all_sprites.add(player)
    players.add(player)
    
    kube_npc = NPC(510, 260, kube_text, 'sprites/kubernetesPirate.png', "Kubernetes Mate")
    docker_npc = NPC(420, 570, docker_text, 'sprites/dockerPirate.png', "Docker Mate")
    instructor_npc = NPC(1100, 450, instructor_text, 'sprites/pirateNPC.png', "Instructor Mate")
    start_npc = Helm_NPC(boat_x+200,(boat_y + boat_height//2) - 25, start_text)
      # Adjust position as needed
    all_sprites.add(kube_npc, docker_npc, start_npc, instructor_npc)
    npcs.add(kube_npc, docker_npc, start_npc, instructor_npc)
    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
        #screen.fill(OCEAN_BLUE)
        #pygame.draw.rect(screen, BROWN, boat_rect)
        screen.blit(shipBackground, (0, 0))
        # Update
        all_sprites.update(screen)
    
        if start_npc.spoken_y:
            to_island_screen(screen)
        if kube_npc.spoken and docker_npc.spoken:
            start_npc.can_speak = True

            
        # Draw
        #all_sprites.draw(screen)
        screen.blit(player.sprite, player.rect)
        screen.blit(kube_npc.sprite, kube_npc.rect)
        screen.blit(docker_npc.sprite, docker_npc.rect)
        screen.blit(start_npc.sprite, start_npc.rect)
        screen.blit(instructor_npc.sprite, instructor_npc.rect)
    
        # Refresh the display
        pygame.display.flip()
    
        # Cap the frame rate
        pygame.time.Clock().tick(60)
