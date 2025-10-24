"""Main game loop and engine.

This file previously contained placeholder imports and stubbed logic. The
engine here provides a small, correct game loop that wires the real
entity classes from `src.entities` and the `CameraSystem` and `DeathScreen`.

It is intentionally minimal: it creates the sprite groups, instantiates a
player (added to the camera/group), and runs a basic event/update/draw loop.
"""

import sys
import pygame
from src import settings

# Use the real modules under src so imports match the rest of the project
from src.core.camera import YSortCameraGroup
from src.entities.player import Player
from src.ui.death_screen import DeathScreen


class Game:
    """Simple, working game engine.

    - Creates sprite groups (all, tiles, hazards)
    - Adds player to groups and camera so it will be drawn
    - Runs a 60FPS loop, updates sprites, handles death menu
    """

    def __init__(self):
        pygame.init()
        # Ensure a display surface exists for CameraSystem
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("I Am The Fool - Engine")

        self.clock = pygame.time.Clock()

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()

        # Camera is a Group - use the core YSortCameraGroup implementation
        self.camera = YSortCameraGroup()

        # Instantiate player and add to both `all_sprites` and `camera` so it
        # will be included in camera drawing. Player expects (pos, groups).
        self.player = Player((100, 300), (self.all_sprites, self.camera))

        # Death screen will be created lazily
        self.death_screen = DeathScreen(self.screen)

    def run(self):
        """Run the main loop.

        Loop responsibilities:
        - handle quit events
        - pass input to player
        - update sprites (dt in milliseconds)
        - draw via camera
        - when player dies, show DeathScreen and handle retry/quit
        """
        while True:
            # Compute dt in seconds and clamp to avoid instability on stalls
            dt_ms = self.clock.tick(settings.FPS)
            dt = dt_ms / 1000.0
            dt = min(dt, 1.0 / 30.0)  # cap at ~33ms

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # When dead, forward events to the death screen to handle menu actions
                if not self.player.is_alive:
                    result = self.death_screen.handle_input(event)
                    if result == "retry":
                        self.player.respawn()
                    elif result == "quit":
                        pygame.quit()
                        sys.exit()

            # Update sprites (pass dt in seconds). Many sprite.update
            # implementations accept optional args; Group.update will forward
            # these to each sprite.update.
            self.all_sprites.update(dt, self.tiles, self.hazards)

            # Clear, draw and flip
            self.screen.fill((30, 30, 30))
            # Camera draws the sprites it knows about (we added player to it on init)
            try:
                self.camera.custom_draw(self.player)
            except Exception:
                # Defensive fallback: if camera.custom_draw raises, blit all
                # sprites directly using their rect positions.
                for sprite in self.all_sprites.sprites():
                    if hasattr(sprite, "image") and hasattr(sprite, "rect"):
                        self.screen.blit(sprite.image, sprite.rect.topleft)

            # If player is dead, draw the death overlay
            if not self.player.is_alive:
                self.death_screen.draw()

            pygame.display.flip()
