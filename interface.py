import pygame

def bar(a, b, length, height):
    a = abs(a)
    surf = pygame.Surface((length,height))
    surf.set_colorkey((0,0,0))
    pygame.draw.rect(surf, (0,255,0), [0,0,length*a/b,height])

    return surf
