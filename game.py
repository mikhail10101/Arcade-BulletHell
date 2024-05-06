import pygame
from entities import *

class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.map = [

        ]
        self.bullet_container = []

    def draw(self, window):
        self.player.draw(window)
        for b in self.bullet_container:
            b.draw(window)

    def update(self, inputs):
        print(self.bullet_container)

        self.player.update(inputs, self.bullet_container)

        self.bullet_container[:] = [b for b in self.bullet_container if b.active]
        for b in self.bullet_container:
            b.update()
