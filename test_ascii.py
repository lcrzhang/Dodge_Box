import pygame
pygame.init()
img = pygame.image.load('images/general (All levels)/ghost.png').convert_alpha()
w, h = img.get_size()
img = pygame.transform.scale(img, (30, 30))
out = ""
for y in range(30):
    for x in range(30):
        r, g, b, a = img.get_at((x, y))
        if a < 128:
            out += " "
        elif r > 200 and g > 200 and b > 200:
            out += "W" # White
        elif r < 50 and g < 50 and b < 50:
            out += "B" # Black
        else:
            out += "*" # Other
    out += "\n"
print(out)
