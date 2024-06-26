from docker.api.build import random
import difflib
import pygame
import sys
from util.util import FONT_SIZE_BIG, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL, word_wrap, word_wrap_with_box, WHITE, BLACK, font, OCEAN_BLUE, WIDTH, HEIGHT, RED
pygame.init()

deployment_sections = [("apiVersion: apps/v1\nkind: Deployment", "- Tells the kubernetes API which version use and which object is getting created/updated/deleted by this file, in this case a Deployment"),
                       ("metadata:\n\tname: ai-demo", "- Gives a name to the deployment"),
                       ("spec:\n\treplicas: 2", "- Specifies how many Pods of this app should be running on a Node at all times.\n- This is managed by a ReplicaSet object"),
                       ("selector:\n\tmatchLabels:\n\t\tapp: ai-demo", "- Tells the ReplicaSet which Pods it should manage using the app label"),
                       ("template:\n\tmetadata:\n\t\tlabels:\n\t\t\tapp: ai-demo", "- Gives each Pod a label so that it can be managed by the correct ReplicaSet"),
                       ("spec:\n\tcontainers:\n\t- name: ai-demo\n\t\timage: ai-demo:latest\n\t\tports:\n\t\t- containerPort: 3000", "- Tells the Pod which container image(the application) to run\n- Gives the container a name\n- Tells the container which ports it wants to be exposed on kubernetes")]

deployment_text = ["apiVersion: apps/v1\nkind: Deployment", "metadata:\n\tname: ai-demo" ,"spec:\n\treplicas: 2", "\tselector:\n\t\tmatchLabels:\n\t\t\tapp: ai-demo", "\ttemplate:\n\t\tmetadata:\n\t\t\tlabels:\n\t\t\t\tapp: ai-demo", "\t\tspec:\n\t\t\tcontainers:\n\t\t\t- name: ai-demo\n\t\t\t\timage: ai-demo:latest\n\t\t\t\tports:\n\t\t\t\t- containerPort: 3000"]
deployment_description = "- This YAML file creates a Deployment in kubernetes\n- A Deployment describes the desired state of an application on the cluster\n- This includes the number of Pods to run, which container is to be on each Pod, and how to communicate with the containers."

dockerfile_sections = [("FROM python:3.11", "- Tells docker which already created image to start with\n- In this case a python image so we have everything needed to run a python app"), 
                       ("WORKDIR /app","- Sets the working directory in the container to be the /app directory"),
                       ("COPY . /app", "- Copies all files from the application on a local machine to the containers /app directory"),
                       ("RUN pip install -r requirements.txt", "- Installs the dependencies of the application to the container from a file using the pip package manager"),
                       ("EXPOSE 3000", "- Exposes port 3000 on the container to internet traffic so the application running on the container can send and recieve data"),
                       ('CMD ["python", "server.py"]', "- Tells the container how to run the application")]
dockerfile_text = [text for text, _ in dockerfile_sections]
dockerfile_description = "- This Dockerfile outlines the steps docker will take to package an application into a container\n- Each step in the file creates a new container and caches it, so that during repeated builds these caches can be used"

service_sections = [("apiVersion: v1\nkind: Service", "- Tells the kubernetes API which version to use and which object is getting created/updated/deleted by this file, in this case a Service"),
                    ("metadata:\n\tname: ai-demo", "- Gives a name to the Service"),
                    ("spec:\n\tselector:\n\t\tapp: ai-demo", "- Tells the Service which group of Pods it should expose to the internet\n- In this case Pods with the app label ai-demo"),
                    ("ports:\n\t- protocol: TCP\n\t\tport: 80\n\t\ttargetPort: 3000", "- Describes the port that will be exposed by the service object either on the Node or through a Load Balancer.\n- The target port is the port to forward traffic to in each of the Pods in the group"),
                    ("type: LoadBalancer", "- Describes where the traffic will be handled\n- LoadBalancer - exposes to external load balancer handled by cloud provider\n- NodePort - exposed on a static port of the clusters ip address\n- ClusterIP - cluster internal access only\n- ExternalName - maps service to some hostname and sets up DNS on the cluster for that name")]
service_text = ["apiVersion: v1\nkind: Service", "metadata:\n\tname: ai-demo", "spec:\n\tselector:\n\t\tapp: ai-demo", "\tports:\n\t\t- protocol: TCP\n\t\t\tport: 80\n\t\t\ttargetPort: 3000", "\ttype: LoadBalancer"]
service_description = "- This YAML files creates a Service in kubernetes\n- A Service exposes a group of Pods on the network, allowing an application to recieve and send internet traffic."

islandSprites =['sprites/island1.png', 'sprites/island2.png', 'sprites/island3.png', 'sprites/island4.png', 'sprites/island5.png', 'sprites/island6.png', 'sprites/island7.png', 'sprites/island8.png',
                'sprites/island9.png', 'sprites/island10.png', 'sprites/island11.png', 'sprites/island12.png', 'sprites/island13.png', 'sprites/island14.png', 'sprites/island15.png', 'sprites/island16.png',
                'sprites/island17.png', 'sprites/island18.png']

all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
islands = pygame.sprite.Group()
oceanBackground = pygame.transform.scale(pygame.image.load('sprites/oceanBackground.jpg'), (WIDTH, HEIGHT))

# Define player class
class Boat(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.sprite = pygame.image.load('sprites/shipSprite.png')
        self.sprite = pygame.transform.scale(self.sprite, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.dx = 0
        self.dy = 0
        self.frozen = False
        self.is_colliding = False
        self.files = [File("Dockerfile", dockerfile_text, dockerfile_sections, dockerfile_description), File("deployment.yaml", deployment_text, deployment_sections, deployment_description), File("service.yaml", service_text, service_sections, service_description)]
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
    def __init__(self, x, y, text, image, filename):
        super().__init__()
        self.image = pygame.Surface((60, 60))
        self.sprite = pygame.image.load(image)
        self.sprite = pygame.transform.scale(self.sprite, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.is_colliding = False
        self.text = text[0]
        self.description = text[1]
        self.filename = filename
        self.spoken = False
        self.input = ""
    def update(self, *args, **kwargs) -> None:
        screen = None
        if len(args) > 0:
            screen = args[0]
        else:
            raise ValueError("Missing Screen argument")
        if self.spoken:
            self.kill()

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
                word_wrap_with_box(screen, "\n" +self.text, font, BLACK, box_surface=pygame.Surface((WIDTH // 2, HEIGHT - 310)),starty = HEIGHT-250, size=FONT_SIZE_SMALL)
                word_wrap_with_box(screen, "Copy this text to your file:\n" + self.input, font, BLACK, box_surface=pygame.Surface((WIDTH // 2, HEIGHT - 310)), startx = WIDTH//2, starty = HEIGHT - 250, size=FONT_SIZE_SMALL)
                word_wrap_with_box(screen, "What this code does:\n" + self.description, font, BLACK, box_surface=pygame.Surface((WIDTH, 250)),size=FONT_SIZE_SMALL)
                word_wrap_with_box(screen, self.filename, font, BLACK, size = FONT_SIZE_BIG, box_surface = pygame.Surface((WIDTH, 60)), starty=60)
                if not self.input == self.text:
                    output_list = [li.replace("- ", "", 1) for li in difflib.ndiff(self.text, self.input) if li[0] != ' ']
                    print_list = "".join(str(x) for x in output_list).replace("\t", "TAB")
                    word_wrap_with_box(screen, "INCORRECT TEXT!\n" + print_list,  font, RED, size=FONT_SIZE_SMALL, box_surface=pygame.Surface((WIDTH //2, 250)), startx=WIDTH//2, starty=HEIGHT-250)
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

            for file in player.files:
                if file.name == self.filename:
                    file.find_section(self.text)
            pygame.time.delay(1000)
            player.frozen = False
            self.is_colliding = False
            player.is_colliding = False
            self.spoken = True

class File():
    def __init__(self, name, text, sections, description):
        self.sections = [(0, input) for input, _ in sections]
        self.text = text
        self.name = name
        self.description = description
    def get_text(self):
        ret_text = ""
        for (found, section), text  in zip(self.sections, self.text):
            if found == 0:
                ret_text += "\n"* len(section.split("\n"))
            elif found == 1:
                ret_text += text + "\n"
        return ret_text
    def find_section(self, section):
        for i in range(len(self.sections)):
            if section == self.sections[i][1]:
                self.sections[i] = (1, self.sections[i][1])

    def done(self):
        return all(sec[0] == 1 for sec in self.sections)
        

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
def to_final_ship(screen):
    from screens.final_ship_screen import final_ship_screen 
    final_ship_screen(screen)

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
    files = ["Dockerfile", "deployment.yaml", "service.yaml"]
    island_positions = generate_island_positions(len(dockerfile_sections) + len(deployment_sections) + len(service_sections), 100)
    pos_idx = 0
    while any(idx < len(lst) for idx, lst in zip(indices, sections)):
        x,y = island_positions[pos_idx]
        island = None
        idx = random.randint(0,2)
        if indices[idx] < len(sections[idx]):
            island = Island(x,y, sections[idx][indices[idx]], islandSprites[pos_idx], files[idx])
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
        if all(file.done() for file in player.files):
            show_file = True
            while show_file:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        show_file = False 
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        show_file = False 
                x = 0
                for file in player.files:
                    word_wrap_with_box(screen, file.name, font, BLACK, size = FONT_SIZE_MEDIUM, box_surface= pygame.Surface((WIDTH // 3, 60)), startx = x, starty = 60)
                    word_wrap_with_box(screen, file.get_text(), font, BLACK, size = FONT_SIZE_SMALL - 7, box_surface = pygame.Surface((WIDTH//3, HEIGHT-360)), startx = x, starty = HEIGHT-300)
                    word_wrap_with_box(screen, "Description:\n" + file.description, font, BLACK, size = FONT_SIZE_SMALL-5, box_surface=pygame.Surface((WIDTH//3, 300)), startx = x)
                    if file.done():
                        word_wrap_with_box(screen, "FILE COMPLETE!", font, BLACK, size = FONT_SIZE_SMALL, box_surface=pygame.Surface((WIDTH//3, 40)), startx = x, starty=HEIGHT-300)
                    x += WIDTH//3
                pygame.display.flip()
            to_final_ship(screen)
            # goto win screen or screen 4
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    # Quit Pygame
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                show_file = True
                while show_file:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            show_file = False 
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                            show_file = False 
                    x = 0
                    for file in player.files:
                        word_wrap_with_box(screen, file.name, font, BLACK, size = FONT_SIZE_MEDIUM, box_surface= pygame.Surface((WIDTH // 3, 60)), startx = x, starty = 60)
                        word_wrap_with_box(screen, file.get_text(), font, BLACK, size = FONT_SIZE_SMALL - 7, box_surface = pygame.Surface((WIDTH//3, HEIGHT-360)), startx = x, starty = HEIGHT-300)
                        word_wrap_with_box(screen, "Description:\n" + file.description, font, BLACK, size = FONT_SIZE_SMALL - 5, box_surface=pygame.Surface((WIDTH//3, 300)), startx = x)
                        if file.done():
                            word_wrap_with_box(screen, "FILE COMPLETE!", font, BLACK, size = FONT_SIZE_SMALL, box_surface=pygame.Surface((WIDTH//3, 40)), startx = x, starty=HEIGHT-300)
                        x += WIDTH//3
                    pygame.display.flip()
                    

    
        #screen.fill(OCEAN_BLUE)
        screen.blit(oceanBackground, (0, 0))
        # Update
        all_sprites.update(screen)
    
        # Draw
        #all_sprites.draw(screen)
        screen.blit(player.sprite, player.rect)
        for island in islands.sprites():
            screen.blit(island.sprite, island.rect)
    
        # Refresh the display
        pygame.display.flip()
    
        # Cap the frame rate
        pygame.time.Clock().tick(60)
    
