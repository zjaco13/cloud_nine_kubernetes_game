import pygame
import pygame.freetype

pygame.init()


font = pygame.freetype.Font('arcade.ttf', 40)
FONT_SIZE_SMALL = 30
FONT_SIZE_MEDIUM = 40
FONT_SIZE_BIG = 60
WIDTH = 1280
HEIGHT = 900

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0,0, 255)
BROWN = (139, 69, 19)
OCEAN_BLUE = (25, 25, 112)

def word_wrap_with_box(surf, text, font, color=(0, 0, 0), box_surface = pygame.Surface((1280, 150)), box_color=(205, 133, 63), startx = 0, starty = HEIGHT, size=30):
    font.origin = True
    # words = text.split(' ')
    width = min(WIDTH, box_surface.get_size()[0])
    line_spacing = font.get_sized_height(size) + 2
    space = font.get_rect(' ', size=size)

    words = []
    word = ""
    for char in text:
        if char == "\n":
            words.append(word)
            word = ""
            words.append("\n")
        elif char == "\t":
            words.append(word)
            word = ""
            words.append("\t")
        elif char == " ":
            words.append(word)
            word = ""
        else:
            word += char
    words.append(word)
    

    # Create bounding box surface
    box_surface.fill(box_color)
    box_rect = box_surface.get_rect()
    box_rect.bottomleft = (startx, starty)

    # Render text onto the box surface
    x, y = 0, 0
    for word in words:
        if word == "\n":
            x = 0 
            y += line_spacing
        elif word == "\t":
            x += space.width * 2
        else:
            bounds = font.get_rect(word, size=size)
            if x + bounds.width + bounds.x >= width - 10:
                x, y = 0, y + line_spacing
            font.render_to(box_surface, (x + 10, y + line_spacing), None, color, size = size)
            x += bounds.width + space.width

    surf.blit(box_surface, box_rect)  # Blit the text surface onto the screen
    pygame.draw.rect(surf, (0, 0, 0), box_rect, 2)  # Draw the bounding box around the text
    return box_surface, box_rect

def word_wrap(surf, text, font, color=(0, 0, 0),  size = 30, startx = 0, starty = HEIGHT - 150):
    font.origin = True
    words = text.split(' ')
    line_spacing = font.get_sized_height(size) + 2
    x, y = startx, starty
    space = font.get_rect(' ', size=size)
    for word in words:
        bounds = font.get_rect(word)
        if x + bounds.width + bounds.x >= WIDTH:
            x, y = 0, y + line_spacing
        if x + bounds.width + bounds.x >= WIDTH:
            raise ValueError("word too wide for the surface")
        if y + bounds.height - bounds.y >= HEIGHT:
            raise ValueError("text to long for the surface")
        font.render_to(surf, (x, y), None, color, size = size)
        x += bounds.width + space.width
    return x, y
