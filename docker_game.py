import pygame
import docker



class docker_game: 

    def __init__(self):
       
        self.GRAY = (200, 200, 200)

        # Screen dimensions
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.font = pygame.font.Font(None, 36)

        # Initialize the screen
        
        pygame.display.set_caption("Docker Container Manager")

        # Fonts
        pygame.init()
        self.images = ['lab5_infosec', 'project1_CS34', 'project4']
        self.containers = []
        self.containers_on = []


    def draw_text(self, text, font, color, surface, x, y):
        text_obj = self.font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_obj, text_rect)

    def create_container():
        container_name = input("Enter a name for your container: ")
        image_name = input("Enter the Docker image name ")
        if image_name in self.images:
            self.containers.append(container_name)
            print(f"Container '{container_name}' created successfully!")
        else:
            print("Error: Image not found. Make sure you've entered the correct image name.")

    def stop_container(container_name):
        if container_name in self.containers_on:
            self.containers_on.remove(container_name)
        elif container_name in self.containers:
            print(f'Container not on.')
        else:
            print("Container does not exist.")

    def delete_container(container_name):
        if container_name in self.containers_on:
            print('This container needs to be switched off to remove it.')
        elif container_name in self.containers:
            print('Success.')
            self.containers.remove(container_name)
        else:
            print('Container does not exist.')


    def main(self):
        running = True
        screen = pygame.display.set_mode((800, 600))
        screen.fill((180, 180, 180))
        pygame.display.flip()
        while True:
            screen.fill((180, 180, 180))
            self.draw_text("Docker Container Manager", self.font, (0, 0, 0), screen, self.SCREEN_WIDTH // 2, 50)
            self.draw_text("Docker Container Manager", pygame.font.Font(None, 36), (0, 0, 0), screen, 800 // 2, 50)
            container_names = self.containers
            y = 150
            for name in container_names:
                self.draw_text(name, self.font, (255, 0, 0), self.screen, self.SCREEN_WIDTH // 2, y)
                y += 50


           

            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         running = False

if __name__ == "__main__":
    docker_game().main()
