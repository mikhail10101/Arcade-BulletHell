import pygame

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

class Button:
    def __init__(self, topleft, length, height, text):
        self.topleft = topleft
        self.length = length
        self.height = height
        self.text = text
    
    def clicked(self, mousepos):
        if self.topleft[0] <= mousepos[0] <= self.topleft[0]+self.length and self.topleft[1] <= mousepos[1] <= self.topleft[0]+self.height:
            return True
        return False
    
    def draw(self, window):
        pygame.draw.rect(window, (255,255,255), (self.topleft[0], self.topleft[1], self.length, self.height), 5)
        f = pygame.font.SysFont("Consolas Bold", int(self.height * 0.8))
        text_finish = f.render(self.text, True, (255,255,255))
        window.blit(text_finish, (self.topleft[0] + self.length//2 - text_finish.get_width()//2, self.topleft[1] + self.height//2 - text_finish.get_height()//2))