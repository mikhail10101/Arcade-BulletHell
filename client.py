import pygame
from game import Game
pygame.font.init()

LENGTH = 1440
WIDTH = 810

window = pygame.display.set_mode((LENGTH, WIDTH))
pygame.display.set_caption("Arcade Game")

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game()
    
    #Inputs to be passed to the game
    inputs = {
        "up": False,
        "down": False,
        "left": False,
        "right": False
    }

    while run:
        clock.tick(60)        

        window.fill((0,0,0))
        game.draw(window)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    inputs["up"] = True
                if event.key == pygame.K_s:
                    inputs["down"] = True
                if event.key == pygame.K_a:
                    inputs["left"] = True
                if event.key == pygame.K_d:
                    inputs["right"] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    inputs["up"] = False
                if event.key == pygame.K_s:
                    inputs["down"] = False
                if event.key == pygame.K_a:
                    inputs["left"] = False
                if event.key == pygame.K_d:
                    inputs["right"] = False
            
        game.update(inputs)
        
        

main()