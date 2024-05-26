import pygame

def bar(a, b, length, height):
    a = abs(a)
    surf = pygame.Surface((length,height))
    pygame.draw.rect(surf, (255,255,255), [0,0,length*a/b,height])
    pygame.draw.rect(surf, (0,0,0), [0,0,length,height], 5)

    return surf

class Button:
    def __init__(self, topleft, length, height, text, monocolor=200, hovercolor=(255,0,0)):
        self.topleft = topleft
        self.length = length
        self.height = height
        self.text = text
        self.monocolor = monocolor
        self.hovercolor = hovercolor
    
    def clicked(self, mousepos):
        if self.topleft[0] <= mousepos[0] <= self.topleft[0]+self.length and self.topleft[1] <= mousepos[1] <= self.topleft[0]+self.height:
            return True
        return False
    
    def draw(self, window):
        pygame.draw.rect(window, (self.monocolor,self.monocolor,self.monocolor), (self.topleft[0], self.topleft[1], self.length, self.height), 5)
        f = pygame.font.SysFont("Tahoma", int(self.height * 0.5))
        text_finish = f.render(self.text, True, (self.monocolor,self.monocolor,self.monocolor))
        window.blit(text_finish, (self.topleft[0] + self.length//2 - text_finish.get_width()//2, self.topleft[1] + self.height//2 - text_finish.get_height()//2))

    def draw_hover(self, window):
        pygame.draw.rect(window, self.hovercolor, (self.topleft[0], self.topleft[1], self.length, self.height), 5)
        f = pygame.font.SysFont("Tahoma", int(self.height * 0.5))
        text_finish = f.render(self.text, True, self.hovercolor)
        window.blit(text_finish, (self.topleft[0] + self.length//2 - text_finish.get_width()//2, self.topleft[1] + self.height//2 - text_finish.get_height()//2))
