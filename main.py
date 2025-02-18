import pygame
from src.controllers.menu import menu

pygame.init()
if __name__ == "__main__":
    #change window name
    pygame.display.set_caption("Dino Game Python")
    #change window icon
    icon = pygame.image.load('assets/Dino/DinoDead.png')
    pygame.display.set_icon(icon)
    menu(0, 0)