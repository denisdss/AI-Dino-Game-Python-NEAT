import random
from src.game_config import *
from src.utils.draw import draw_srq_obstacle

class Obstacle:
    def __init__(self, image, type, name):
        self.image = image
        self.type = type
        self.name = name
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width or self.rect.x < 0:
            obstacles.pop(0)

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)
        # draw_srq_obstacle(self) # Draw a red rectangle around the obstacle


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type, 1) # "Small Cactus"
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type, 2) # "Large Cactus"
        self.rect.y = 325


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type, 3) # "Bird"
        self.rect.y = random.choice([245])
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        # draw_srq_obstacle(self) # Draw a red rectangle around the obstacle
        self.index += 1
