import pygame
from core import settings

class Background:
    def __init__(self):
        self.bg_width = settings.SCREEN_WIDTH
        self.bg_height = settings.SCREEN_HEIGHT
        self.x1 = 0
        self.x2 = self.bg_width
        self.speed = settings.SCROLL_SPEED

        self.colors = [
            (135, 206, 250),  # sky blue
            (255, 204, 153),  # desert orange
            (220, 220, 255)   # light snowy blue
        ]
        self.color_index = 0
        self.color1 = self.colors[self.color_index]
        self.color2 = self.colors[(self.color_index + 1) % len(self.colors)]

    def update(self):
        self.x1 -= self.speed
        self.x2 -= self.speed

        if self.x1 <= -self.bg_width:
            self.x1 = self.bg_width
        if self.x2 <= -self.bg_width:
            self.x2 = self.bg_width

    def draw(self, surface):
        pygame.draw.rect(surface, self.color1, (self.x1, 0, self.bg_width, self.bg_height))
        pygame.draw.rect(surface, self.color2, (self.x2, 0, self.bg_width, self.bg_height))

    def set_region(self, index):
        self.color_index = index % len(self.colors)
        self.color1 = self.colors[self.color_index]
        self.color2 = self.colors[(self.color_index + 1) % len(self.colors)]