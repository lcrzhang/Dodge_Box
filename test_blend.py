import pygame
pygame.init()
s = pygame.Surface((3, 3), pygame.SRCALPHA)
s.set_at((0,0), (0,0,0,0)) # transparent
s.set_at((1,1), (255,255,255,255)) # white
s.set_at((2,2), (0,0,0,255)) # black

def test_mult():
    c = s.copy()
    c2 = pygame.Surface((3,3), pygame.SRCALPHA)
    c2.fill((255, 0, 0, 255))
    c.blit(c2, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    print("MULT(255,0,0,255):", c.get_at((0,0)), c.get_at((1,1)), c.get_at((2,2)))

def test_rgb_add():
    c = s.copy()
    c2 = pygame.Surface((3,3), pygame.SRCALPHA)
    c2.fill((255, 0, 0, 255))
    c.blit(c2, (0,0), special_flags=pygame.BLEND_RGB_ADD)
    print("ADD(255,0,0,255):", c.get_at((0,0)), c.get_at((1,1)), c.get_at((2,2)))

test_mult()
test_rgb_add()
