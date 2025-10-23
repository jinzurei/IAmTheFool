import pygame
from src.settings import TILE_SIZE


class Trigger(pygame.sprite.Sprite):

    def __init__(self, pos, image=None):
        super().__init__()
        self.image = (
            image if image is not None else pygame.Surface((TILE_SIZE, TILE_SIZE))
        )
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos
        self.spawn_midbottom = pos

    def update_frame(self, new_image):
        prev_midbottom = self.rect.midbottom
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.midbottom = prev_midbottom

    def draw(self, screen, off=None):
        if off is None:
            off = pygame.Vector2(0, 0)
        draw_pos = (self.rect.x - off.x, self.rect.y - off.y)
        screen.blit(self.image, draw_pos)
