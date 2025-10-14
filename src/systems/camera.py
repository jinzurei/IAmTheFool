# Camera system (moved from src/core/camera.py)
import pygame
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class CameraSystem(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH // 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT // 2
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            if hasattr(sprite, 'draw') and sprite.__class__.__name__ == 'Player':
                sprite.draw(self.display_surface)
            else:
                self.display_surface.blit(sprite.image, offset_pos)
