import pygame
from physics import *
from interface import Button

LENGTH = 1440
WIDTH = 810

INNERCOLOR = 20
LOWERCOLORBOUND = 100
UPPERCOLORBOUND = 200


class Menu:
    def __init__(self):
        self.window = pygame.Surface((LENGTH, WIDTH))
        self.buttons = [
            Button((400,470), 250, 66, "Singleplayer", 255, (255,0,0)),
            Button((770,470), 250, 66, "Multiplayer", 255, (255,0,0))
        ]

        self.last = True

    def update(self, inputs):
        for b in self.buttons:
            if b.clicked(inputs["click_pos"]) and inputs["click"] and not self.last:
                if b.text == "Singleplayer":
                    return "Singleplayer"
                if b.text == "Multiplayer":
                    return "Multiplayer"
        self.last = inputs["click"]
        return ""


    def draw(self, screen, mousepos):
        self.window.fill((INNERCOLOR,INNERCOLOR,INNERCOLOR))

        f = pygame.font.SysFont("Times New Roman", 200)
        text = f.render("P O L A R", True, (255,255,255))
        self.window.blit(text, (self.window.get_width()//2 - text.get_width()//2, 250))

        for b in self.buttons:
            if b.clicked(mousepos):
                b.draw_hover(self.window)
            else:
                b.draw(self.window)

        screen.blit(self.window, (0,0))

