import pygame
import pygame.freetype

pygame.init()


font = pygame.freetype.Font('Minecraft.ttf', 30)
# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0,0, 255)
BROWN = (139, 69, 19)
OCEAN_BLUE = (25, 25, 112)

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

    surf.blit(box_surface, box_rect)  # Blit the text surface onto the screen
    pygame.draw.rect(surf, (0, 0, 0), box_rect, 2)  # Draw the bounding box around the text
    return box_surface, box_rect

def word_wrap(surf, text, font, color=(0, 0, 0)):
    font.origin = True
    words = text.split(' ')
    width, height = surf.get_size()
    line_spacing = font.get_sized_height() + 2
    x, y = 0, surf.get_size()[1] - line_spacing*5
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
