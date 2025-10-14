"""
Hazard tiles that kill the player on contact
"""

import pygame
from src.config.settings import TILE_SIZE

class HazardTile(pygame.sprite.Sprite):
    """Base hazard tile class that kills player on contact"""
    
    def __init__(self, pos, groups, surface):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.is_hazard = True  # Flag to identify hazard tiles

class VisibleHazard(HazardTile):
    """Visible hazard tile (red spikes/lava)"""
    
    def __init__(self, pos, groups):
        # Create red hazard surface with spikes pattern
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surface.fill((220, 20, 20))  # Bright red
        
        # Draw spikes pattern
        points = [
            (0, TILE_SIZE), (TILE_SIZE//4, 0), (TILE_SIZE//2, TILE_SIZE),
            (3*TILE_SIZE//4, 0), (TILE_SIZE, TILE_SIZE)
        ]
        pygame.draw.polygon(surface, (180, 0, 0), points)  # Darker red spikes
        
        super().__init__(pos, groups, surface)

class InvisibleHazard(HazardTile):
    """Invisible hazard tile (pitfalls, death zones)"""
    
    def __init__(self, pos, groups):
        # Create completely transparent surface
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))  # Fully transparent
        
        super().__init__(pos, groups, surface)