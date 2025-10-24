import pygame
from src import settings


class CameraLookAhead:
    def __init__(self):
        self.offset = pygame.Vector2(0, 0)

    def update(self, target_pos, dt):
        self.offset.x = int(target_pos[0])
        self.offset.y = int(target_pos[1])


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, target_sprite):
        screen_center = pygame.Vector2(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)
        self.offset.x = int(target_sprite.rect.centerx - screen_center.x)
        self.offset.y = int(target_sprite.rect.centery - screen_center.y)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if hasattr(sprite, "draw"):
                try:
                    sprite.draw(self.display_surface, self.offset)
                except TypeError:
                    offset_pos = (
                        sprite.rect.x - self.offset.x,
                        sprite.rect.y - self.offset.y,
                    )
                    self.display_surface.blit(sprite.image, offset_pos)
            else:
                offset_pos = (
                    sprite.rect.x - self.offset.x,
                    sprite.rect.y - self.offset.y,
                )
                self.display_surface.blit(sprite.image, offset_pos)
