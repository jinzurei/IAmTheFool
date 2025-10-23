import pygame
import settings


class Obstacle:
    """Obstacle entity that moves across the screen."""

    def __init__(self, start_x: float = None) -> None:
        """Initialize the obstacle at the specified position or right edge."""
        self.width = settings.OBSTACLE_WIDTH
        self.height = settings.OBSTACLE_HEIGHT
        self.x = start_x if start_x is not None else settings.SCREEN_WIDTH
        self.y = settings.SCREEN_HEIGHT - self.height - settings.PLAYER_GROUND_OFFSET
        self.speed = settings.SCROLL_SPEED
        self.color = settings.RED

    def update(self, camera_x: float = 0) -> None:
        """Update obstacle position and reset when far behind camera."""
        self.x -= self.speed
        # Reset obstacle far ahead of camera when it goes far behind
        if self.x < camera_x - settings.SCREEN_WIDTH:
            self.x = camera_x + settings.SCREEN_WIDTH * 2

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the obstacle with enhanced visuals."""
        # Main body
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

        # Danger stripes pattern
        stripe_color = (255, 255, 0)  # Yellow warning stripes
        for i in range(0, self.height, 8):
            if (i // 8) % 2 == 0:
                stripe_rect = (self.x + 2, self.y + i, self.width - 4, 4)
                pygame.draw.rect(surface, stripe_color, stripe_rect)

        # Dark outline
        pygame.draw.rect(
            surface, settings.BLACK, (self.x, self.y, self.width, self.height), 2
        )

    def get_rect(self) -> pygame.Rect:
        """Get the obstacle's bounding rectangle for collision detection."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
