import pygame
from interface import Button

INNERCOLOR = 20
LOWERCOLORBOUND = 100
UPPERCOLORBOUND = 200

class Menu:
    def __init__(self,length,width):
        self.window = pygame.display.set_mode((length, width))
        self.buttons = [
            Button((570,500), 300, 100, "START", 255, (255,0,0))
        ]

    def update(self, inputs):
        started = False

        for b in self.buttons:
            if b.clicked(inputs["click_pos"]) and inputs["click"]:
                if b.text == "START":
                    started = True
        
        if started:
            return True
        return False

    def draw(self, mousepos):
        self.window.fill((INNERCOLOR,INNERCOLOR,INNERCOLOR))

        for b in self.buttons:
            if b.clicked(mousepos):
                b.draw_hover(self.window)
            else:
                b.draw(self.window)

        pygame.display.update()

