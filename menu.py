import pygame
from interface import Button

class Menu:
    def __init__(self,length,width):
        self.window = pygame.display.set_mode((length, width))
        self.buttons = [
            Button((570,500), 300, 100, "Start")
        ]

    def update(self, inputs):
        started = False

        for b in self.buttons:
            if inputs["click"] and b.clicked(inputs["click_pos"]):
                if b.text == "Start":
                    started = True
        
        if started:
            return True

    def draw(self):
        self.window.fill((0,0,0))

        for b in self.buttons:
            b.draw(self.window)

        pygame.display.update()

