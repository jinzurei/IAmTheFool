import pygame
from core import settings

class Ground:
    def __init__(self):
        self.width = settings.SCREEN_WIDTH
        self.height = 50
        self.y = settings.SCREEN_HEIGHT - self.height

        # Two ground pieces for seamless scroll
        self.x1 = 0
        self.x2 = self.width

        self.speed = settings.SCROLL_SPEED

        # Placeholder themes: can later become images/textures
        self.colors = [settings.BLACK, (139, 115, 85), (200, 200, 255)]
        self.current_color_index = 0
        self.color = self.colors[self.current_color_index]
        self.region_change_threshold = 2000  # change after 2000px

        self.distance_traveled = 0

    def update(self):
        self.x1 -= self.speed
        self.x2 -= self.speed
        self.distance_traveled += self.speed

        # Loop segments
        if self.x1 <= -self.width:
            self.x1 = self.width
        if self.x2 <= -self.width:
            self.x2 = self.width

        # Theme shift based on distance
        if self.distance_traveled >= self.region_change_threshold:
            self.distance_traveled = 0
            self.current_color_index = (self.current_color_index + 1) % len(self.colors)
            self.color = self.colors[self.current_color_index]

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x1, self.y, self.width, self.height))
        pygame.draw.rect(surface, self.color, (self.x2, self.y, self.width, self.height))