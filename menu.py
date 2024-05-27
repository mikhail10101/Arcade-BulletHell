import pygame
from interface import Button

INNERCOLOR = 20
LOWERCOLORBOUND = 100
UPPERCOLORBOUND = 200

class Menu:
    def __init__(self,length,width):
        self.window = pygame.display.set_mode((length, width))
        self.buttons = [
            Button((630,470), 200, 66, "START", 255, (255,0,0)),
        ]
        self.bg_shapes = [] #each shape has: [position, size, amount of sides]


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

        f = pygame.font.SysFont("Ink Free", 200)
        text = f.render("P O L A R", True, (255,255,255))
        self.window.blit(text, (self.window.get_width()//2 - text.get_width()//2, 300))

        #pygame.draw.circle(self.window, (255,255,255),(self.window.get_height()//2 - text.get_height()//2, self.window.get_width()//2 - text.get_width()//2), 100)

        for b in self.buttons:
            if b.clicked(mousepos):
                b.draw_hover(self.window)
            else:
                b.draw(self.window)

        pygame.display.update()

