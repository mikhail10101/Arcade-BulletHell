import pygame
from entities import *
from map import Map

class Game:
    def __init__(self, length, width):
        self.player = Player()
        self.enemies = []
        self.map = Map()
        self.bullet_container = []

        self.window = pygame.display.set_mode((length, width))
        pygame.display.set_caption("Arcade Game")

        self.scroll = [0,0]

    def draw(self):
        render_scroll = [int(self.scroll[0]), int(self.scroll[1])]
        self.window.fill((0,0,0))
        
        self.map.draw(self.window, render_scroll)
        self.player.draw(self.window, render_scroll)
        for b in self.bullet_container:
            b.draw(self.window, render_scroll)

        pygame.display.update()

    def update(self, inputs):

        self.player.update(inputs, self.bullet_container, self.scroll)

        self.bullet_container[:] = [b for b in self.bullet_container if b.active]
        for b in self.bullet_container:
            if self.map.is_in_wall(b.pos):
                b.active = False
            b.update()

        self.scroll[0] += (self.player.pos[0] - self.window.get_width()/2 - self.scroll[0]) / 10
        self.scroll[1] += (self.player.pos[1] - self.window.get_height()/2 - self.scroll[1]) / 10
