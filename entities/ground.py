import pygame
from typing import List, Tuple
from core import settings
from entities.scrollable import ScrollableEntity

class Ground(ScrollableEntity):
    """Scrolling ground with theme colors that change by region."""
    def __init__(self) -> None:
        """Initialize the scrolling ground with multiple segments for camera."""
        ground_y = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        # Make ground segments wider to handle camera movement
        super().__init__(settings.SCREEN_WIDTH * 2, settings.GROUND_HEIGHT, ground_y)

        # Placeholder themes: can later become images/textures
        self.colors = settings.GROUND_COLORS
        self.current_color_index = 0
        self.color = self.colors[self.current_color_index]

    def set_region(self, region_index: int) -> None:
        """Set the ground color based on the region index."""
        self.current_color_index = region_index % len(self.colors)
        self.color = self.colors[self.current_color_index]

    def draw(self, surface: pygame.Surface, camera_offset=None) -> None:
        """
        Draw the ground segments on the given surface, subtracting camera offset.
        All world objects must use the same camera offset for consistent scrolling.
        """
        if camera_offset is None:
            camera_offset = (0, 0)
        pygame.draw.rect(surface, self.color, (self.x1 - camera_offset[0], self.y - camera_offset[1], self.width, self.height))
        pygame.draw.rect(surface, self.color, (self.x2 - camera_offset[0], self.y - camera_offset[1], self.width, self.height))