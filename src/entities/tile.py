import pygame
from src.config.settings import TILE_SIZE

class Tile(pygame.sprite.Sprite):
    # Base tile class
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)

class StaticTile(Tile):
    # Solid tile for collision detection
    def __init__(self, pos, groups, surface):
        super().__init__(pos, groups)
        self.image = surface