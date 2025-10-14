import pygame
from typing import List, Tuple
from core import settings
from entities.scrollable import ScrollableEntity

class Background(ScrollableEntity):
    """Scrolling background with multiple region themes."""
    def __init__(self) -> None:
        """Initialize the scrolling background with segments for camera."""
        # Make background segments wider to handle camera movement
        super().__init__(settings.SCREEN_WIDTH * 2, settings.SCREEN_HEIGHT, 0)
        
        self.colors = settings.BACKGROUND_COLORS
        self.color_index = 0
        self.color1 = self.colors[self.color_index]
        self.color2 = self.colors[(self.color_index + 1) % len(self.colors)]

    def draw(self, surface: pygame.Surface, camera_offset=None) -> None:
        """
        Draw the background segments on the given surface, subtracting camera offset.
        All world objects must use the same camera offset for consistent scrolling.
        """
        if camera_offset is None:
            camera_offset = (0, 0)
        pygame.draw.rect(surface, self.color1, (self.x1 - camera_offset[0], 0 - camera_offset[1], self.width, self.height))
        pygame.draw.rect(surface, self.color2, (self.x2 - camera_offset[0], 0 - camera_offset[1], self.width, self.height))

    def set_region(self, index: int) -> None:
        """Set the background region/theme based on index."""
        self.color_index = index % len(self.colors)
        self.color1 = self.colors[self.color_index]
        self.color2 = self.colors[(self.color_index + 1) % len(self.colors)]