import pygame
from src import settings


class Tile(pygame.sprite.Sprite):
    # Base tile class
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((settings.TILE_SIZE, settings.TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)


class StaticTile(Tile):
    # Solid tile for collision detection
    def __init__(self, pos, groups, surface):
        super().__init__(pos, groups)
        self.image = surface


class SpawnTile(Tile):
    # Yellow tile for player spawn
    def __init__(self, pos, groups):
        super().__init__(pos, groups)
        self.image.fill((255, 255, 0))
