import pygame
from interface import Button

LENGTH = 1440
WIDTH = 810

INNERCOLOR = 20
LOWERCOLORBOUND = 100
UPPERCOLORBOUND = 200


class Scoreboard():
    def __init__(self):
        self.window = pygame.display.set_mode((LENGTH, WIDTH))
        self.score = 0
        self.buttons = [
            Button((595,470), 250, 66, "Exit", 255, (255,0,0))
        ]

        self.last = True

    def update(self, inputs):
        for b in self.buttons:
            if b.clicked(inputs["click_pos"]) and inputs["click"] and not self.last:
                if b.text == "Exit":
                    return "MainMenu"
        self.last = inputs["click"]
        return ""


    def draw(self, screen, mousepos):
        self.window.fill((INNERCOLOR,INNERCOLOR,INNERCOLOR))

        f = pygame.font.SysFont("Times New Roman", 200)
        text = f.render(str(self.score), True, (255,255,255))
        self.window.blit(text, (self.window.get_width()//2 - text.get_width()//2, 250))

        for b in self.buttons:
            if b.clicked(mousepos):
                b.draw_hover(self.window)
            else:
                b.draw(self.window)

        screen.blit(self.window, (0,0))