import pygame
from core import settings

class Obstacle:
    def __init__(self):
        self.width, self.height = 30, 60
        self.x = settings.SCREEN_WIDTH
        self.y = settings.SCREEN_HEIGHT - self.height - 50
        self.speed = settings.SCROLL_SPEED
        self.color = settings.RED

    def update(self):
        self.x -= self.speed
        if self.x < -self.width:
            self.x = settings.SCREEN_WIDTH

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)