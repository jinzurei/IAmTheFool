"""
Camera system with Y-sorted group and offset for jitter-free scrolling
"""

import pygame
from src.config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, RIGHT_KEYS

class YSortCameraGroup(pygame.sprite.Group):
    """
    Y-sorted camera group with offset for smooth scrolling
    Offset is applied only at draw time, never to physics rects
    """
    
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        
    def custom_draw(self, player):
        """
        Draw all sprites with camera offset
        Camera centers player even further to the right (e.g., 60% of screen width)
        """
        # Align the green collision box (player.rect) at 60% of the screen width
        desired_x = int(SCREEN_WIDTH * 0.6)
        desired_y = SCREEN_HEIGHT // 2
        self.offset.x = player.rect.centerx - desired_x
        self.offset.y = player.rect.centery - desired_y

        # Sort sprites by y position for proper depth
        sorted_sprites = sorted(self.sprites(), key=lambda sprite: sprite.rect.centery)

        # Draw each sprite with offset applied
        for sprite in sorted_sprites:
            offset_pos = sprite.rect.topleft - self.offset
            if hasattr(sprite, 'draw') and sprite.__class__.__name__ == 'Player':
                # Draw player with custom alignment
                sprite.draw(self.display_surface)
            else:
                self.display_surface.blit(sprite.image, offset_pos)