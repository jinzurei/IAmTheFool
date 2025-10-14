import pygame
from src.config.settings import TILE_SIZE

class HazardTile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surface):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.is_hazard = True
    def draw(self, screen, off=None):
        if off is None:
            off = pygame.Vector2(0, 0)
        draw_pos = (self.rect.x - off.x, self.rect.y - off.y)
        screen.blit(self.image, draw_pos)

class VisibleHazard(HazardTile):
    def __init__(self, pos, groups):
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surface.fill((220, 20, 20))
        points = [
            (0, TILE_SIZE), (TILE_SIZE//4, 0), (TILE_SIZE//2, TILE_SIZE),
            (3*TILE_SIZE//4, 0), (TILE_SIZE, TILE_SIZE)
        ]
        pygame.draw.polygon(surface, (180, 0, 0), points)
        super().__init__(pos, groups, surface)

class InvisibleHazard(HazardTile):
    def __init__(self, pos, groups):
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        super().__init__(pos, groups, surface)