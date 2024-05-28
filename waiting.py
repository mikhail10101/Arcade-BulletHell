import pygame

LENGTH = 1440
WIDTH = 810

INNERCOLOR = 20
LOWERCOLORBOUND = 100
UPPERCOLORBOUND = 200


class Waiting():
    def __init__(self):
        self.window = pygame.display.set_mode((LENGTH, WIDTH))

    def draw(self, screen):
        self.window.fill((INNERCOLOR,INNERCOLOR,INNERCOLOR))

        f = pygame.font.SysFont("Times New Roman", 200)
        text = f.render("WAITING", True, (255,255,255))
        self.window.blit(text, (self.window.get_width()//2 - text.get_width()//2, self.window.get_height()//2 - text.get_height()//2))

        screen.blit(self.window, (0,0))