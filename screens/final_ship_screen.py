import pygame
import sys
from util.util import FONT_SIZE_MEDIUM, FONT_SIZE_SMALL, HEIGHT, WIDTH, word_wrap_with_box, font, WHITE, RED, BLACK, BLUE, OCEAN_BLUE, BROWN

pygame.init()

boat_width = 1100
boat_height = 650 
kube_text = ["I will teach you how you can deploy your completed Deployment and Service onto a Kubernetes Cluster", 
             "To deploy the Deployment, you will run: kubectl apply -f deployment.yaml\nTo deploy the Service, you will run: kubectl apply -f service.yaml",
             "These commands search in the current directory for the files deployment.yaml and service.yaml, and applies the objects defined in them to the kubernetes cluster."]
docker_text = ["I will teach you how to build your application into a container using the Dockerfile we just created.",
               "To build the image, you will run: docker build -t ai-demo:latest .",
               "This command searches the current directory for a Dockerfile, then runs the steps in that file to create the container image.\nThis command then tags that image as ai-demo:latest and pushes it to the local docker registry of images"]
start_text = ["Would you like to go defeat the enemies with your Kubernetes and Docker knowledge?(Y/N)"]
instructor_text = ["Talk to each of the Kubernetes and Docker Mates to learn about how you can do combat by deploying your application onto the cluster!"]
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
npcs = pygame.sprite.Group()
oceanBackground = pygame.transform.scale(pygame.image.load('sprites/oceanBackground.jpg'), (WIDTH, HEIGHT))
shipBackground = pygame.transform.scale(pygame.image.load('sprites/shipOceanBackground.png'), (WIDTH, HEIGHT))

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


def to_end_screen(screen):
    from screens.game_over import game_over_screen 
    game_over_screen(screen)

def final_ship_screen(screen):
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
        screen.blit(oceanBackground, (0, 0))
        screen.blit(shipBackground, (0, 0))
        # Update
        all_sprites.update(screen)
    
        if start_npc.spoken_y:
            to_end_screen(screen)
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
