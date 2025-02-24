import pygame
from src.controllers.game import run_game
from src.utils.fs import load_best_genome

pygame.init()
if __name__ == "__main__":
    #change window name
    pygame.display.set_caption("Dino Game Python")
    #change window icon
    icon = pygame.image.load('assets/Dino/DinoDead.png')
    pygame.display.set_icon(icon)
    run_game(best_genome = load_best_genome())