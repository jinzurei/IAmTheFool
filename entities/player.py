import pygame
from core import settings

class Player:
    def __init__(self):
        self.width, self.height = 50, 100
        self.x = 100
        self.y = settings.SCREEN_HEIGHT - self.height - 50
        self.vel_y = 0
        self.jumping = False
        self.speed = 5
        self.color = settings.BROWN

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_w):
                if not self.jumping:
                    self.vel_y = -settings.JUMP_FORCE
                    self.jumping = True

    def update(self, keys):
        self.vel_y += settings.GRAVITY
        self.y += self.vel_y

        # Downforce
        if keys[pygame.K_s]:
            self.vel_y += 2  # fast drop

        # Move left but not off screen
        if keys[pygame.K_a]:
            self.x = max(self.x - self.speed, 0)

        # Speed up / dash forward
        if keys[pygame.K_d]:
            self.x = min(self.x + self.speed * 1.5, settings.SCREEN_WIDTH - self.width)

        # Floor collision
        ground = settings.SCREEN_HEIGHT - self.height - 50
        if self.y >= ground:
            self.y = ground
            self.jumping = False
            self.vel_y = 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)