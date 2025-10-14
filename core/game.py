import pygame
from typing import Tuple, List
from core import settings
from src.core.camera import YSortCameraGroup
from src.core.menus import MainMenu, PauseMenu, GameOverMenu
from world.tilemap import TileMap
from entities.background import Background
from entities.ground import Ground
from src.entities.player import Player
from src.entities.tile import StaticTile

class Game:
    """Main game class that manages the game loop and entities."""
    def __init__(self) -> None:
        """Initialize the game with all necessary components."""
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("I Am The Fool")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont(None, 36)

        # Game state management
        self.game_state = settings.MENU
        self.main_menu = MainMenu()
        self.pause_menu = PauseMenu()
        self.game_over_menu = GameOverMenu()

        # Camera system
        self.camera = Camera()

        # Game entities (initialized when starting game)
        self.player = None
        self.obstacles = []  # Multiple obstacles for better world generation
        self.tilemap = TileMap()  # Infinite tile-based world
        self.background = None
        self.ground = None

        self.collision_state = "none"  # none, collision, game_over
        self.current_region = 0
        self.distance_traveled = 0

    def run(self) -> None:
        """Run the main game loop."""
        while self.running:
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            
            self.handle_events(events, keys)
            self.update(keys)
            self.draw()
            self.clock.tick(settings.FPS)
        pygame.quit()

    def handle_events(self, events: List[pygame.event.Event], keys: pygame.key.ScancodeWrapper) -> None:
        """Handle pygame events based on current game state."""
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return
            elif event.type == pygame.VIDEORESIZE:
                self.handle_resize(event.w, event.h)
                return
        
        if self.game_state == settings.MENU:
            new_state = self.main_menu.handle_events(events)
            if new_state == "quit":
                self.running = False
            elif new_state == settings.PLAYING:
                self.start_game()
        
        elif self.game_state == settings.PLAYING:
            # Handle pause and fullscreen
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = settings.PAUSED
                        return
                    elif event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                        return
            
            # Handle player events
            if self.player:
                for event in events:
                    self.player.handle_event(event)
        
        elif self.game_state == settings.PAUSED:
            new_state = self.pause_menu.handle_events(events)
            if new_state:
                if new_state == settings.MENU:
                    self.reset_game()
                self.game_state = new_state
        
        elif self.game_state == settings.GAME_OVER:
            new_state = self.game_over_menu.handle_events(events)
            if new_state:
                if new_state == settings.PLAYING:
                    self.start_game()
                elif new_state == settings.MENU:
                    self.reset_game()
                self.game_state = new_state

    def update(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Update all game entities and game state."""
        if self.game_state == settings.PLAYING and self.player:
            self.player.update(keys, self.tilemap)
            
            # Update camera to follow player
            player_center_x = self.player.x + self.player.width // 2
            player_center_y = self.player.y + self.player.height // 2
            self.camera.update(player_center_x, player_center_y, self.player.vel_x)
            
            # Update tilemap based on camera position
            camera_x, camera_y = self.camera.get_offset()
            self.tilemap.update(camera_x, camera_y)
            
            # Keep obstacles for now (can integrate into tilemap later)
            for obstacle in self.obstacles:
                obstacle.update(camera_x)

            # Distance-based region switching
            self.distance_traveled += settings.SCROLL_SPEED
            if self.distance_traveled >= settings.REGION_CHANGE_THRESHOLD:
                self.distance_traveled = 0
                self.current_region = (self.current_region + 1) % 3
                self.background.set_region(self.current_region)
                self.ground.set_region(self.current_region)

            # Collision detection
            self.collision_state = self._check_collisions()
            if self.collision_state == "collision":
                self.camera.add_screen_shake(15)  # Add screen shake on collision
                self._handle_collision()

    def _check_collisions(self) -> str:
        """Check for collisions between game entities."""
        if self.player:
            player_rect = self.player.get_rect()
            for obstacle in self.obstacles:
                if player_rect.colliderect(obstacle.get_rect()):
                    return "collision"
        return "none"
    
    def _handle_collision(self) -> None:
        """Handle collision with enhanced feedback."""
        # Stop player movement
        if self.player:
            self.player.vel_x *= 0.3  # Reduce momentum
            self.player.vel_y = min(self.player.vel_y, 5)  # Limit bounce
        
        # Transition to game over
        self.game_state = settings.GAME_OVER

    def handle_resize(self, width: int, height: int) -> None:
        """Handle window resize events."""
        # Enforce minimum size
        width = max(width, settings.MIN_SCREEN_WIDTH)
        height = max(height, settings.MIN_SCREEN_HEIGHT)
        
        # Update settings
        settings.SCREEN_WIDTH = width
        settings.SCREEN_HEIGHT = height
        
        # Recreate the screen surface
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        
        # Recreate menus to adjust to new screen size
        self.main_menu = MainMenu()
        self.pause_menu = PauseMenu()
        self.game_over_menu = GameOverMenu()
        
        # If game is active, recreate entities to adjust to new screen size
        if self.game_state == settings.PLAYING and self.player:
            self.background = Background()
            self.ground = Ground()
            # Adjust player and obstacle positions if they're outside the new bounds
            self.player.x = min(self.player.x, settings.SCREEN_WIDTH - self.player.width)
            self.player.y = min(self.player.y, settings.SCREEN_HEIGHT - self.player.height - settings.PLAYER_GROUND_OFFSET)

    def toggle_fullscreen(self) -> None:
        """Toggle between fullscreen and windowed mode."""
        if self.screen.get_flags() & pygame.FULLSCREEN:
            # Switch to windowed mode
            self.screen = pygame.display.set_mode((settings.DEFAULT_SCREEN_WIDTH, settings.DEFAULT_SCREEN_HEIGHT), pygame.RESIZABLE)
            settings.SCREEN_WIDTH = settings.DEFAULT_SCREEN_WIDTH
            settings.SCREEN_HEIGHT = settings.DEFAULT_SCREEN_HEIGHT
        else:
            # Switch to fullscreen mode
            info = pygame.display.Info()
            self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
            settings.SCREEN_WIDTH = info.current_w
            settings.SCREEN_HEIGHT = info.current_h
        
        # Recreate menus and entities for new screen size
        self.main_menu = MainMenu()
        self.pause_menu = PauseMenu()
        self.game_over_menu = GameOverMenu()
        
        if self.game_state == settings.PLAYING and self.player:
            self.tilemap = TileMap()
            
            if self.game_state == settings.PLAYING and self.player:
                self.player.x = min(self.player.x, settings.SCREEN_WIDTH - self.player.width)
                self.player.y = min(self.player.y, settings.SCREEN_HEIGHT - self.player.height - settings.PLAYER_GROUND_OFFSET)

    def start_game(self) -> None:
        """Initialize or reset the game entities and start playing."""
        self.player = Player()
        
        # Create multiple obstacles spread across the world
        self.obstacles = []
        for i in range(5):  # Create 5 obstacles
            obstacle_x = settings.SCREEN_WIDTH + (i * 400)  # Space them 400 pixels apart
            self.obstacles.append(Obstacle(obstacle_x))
        
        # Create tilemap for infinite world generation
        self.tilemap = TileMap()
        self.collision_state = "none"
        self.current_region = 0
        self.distance_traveled = 0
        self.camera.reset()  # Reset camera position
        self.game_state = settings.PLAYING

    def reset_game(self) -> None:
        """Reset game to menu state."""
        self.player = None
        self.obstacles = []
        self.tilemap = None
        self.collision_state = "none"
        self.current_region = 0
        self.distance_traveled = 0
        self.game_state = settings.MENU

    def _draw_game_world(self) -> None:
        """Draw the game world with camera offset."""
        camera_x, camera_y = self.camera.get_offset()
        
        # Draw tile-based world
        if self.tilemap:
            self.tilemap.draw(self.screen, camera_x, camera_y)
        
        # Draw player
        self._draw_with_camera(self.player, camera_x, camera_y)
        
        # Draw obstacles (keeping for now)
        for obstacle in self.obstacles:
            self._draw_with_camera(obstacle, camera_x, camera_y)
    
    def _draw_with_camera(self, entity, camera_x: float, camera_y: float) -> None:
        """Draw an entity with camera offset."""
        if hasattr(entity, 'draw_with_offset'):
            entity.draw_with_offset(self.screen, camera_x, camera_y)
        else:
            # Fallback: modify entity position temporarily
            if hasattr(entity, 'x') and hasattr(entity, 'y'):
                original_x, original_y = entity.x, entity.y
                entity.x -= camera_x
                entity.y -= camera_y
                entity.draw(self.screen)
                entity.x, entity.y = original_x, original_y
            elif hasattr(entity, 'x1') and hasattr(entity, 'x2'):  # For scrollable entities
                original_x1, original_x2 = entity.x1, entity.x2
                original_y = entity.y
                entity.x1 -= camera_x
                entity.x2 -= camera_x
                entity.y -= camera_y
                entity.draw(self.screen)
                entity.x1, entity.x2 = original_x1, original_x2
                entity.y = original_y

    def _draw_background_with_parallax(self, camera_x: float, camera_y: float) -> None:
        """Draw background with parallax effect (moves slower than world)."""
        if self.background:
            # Background moves at 30% of camera speed for parallax effect
            parallax_x = camera_x * 0.3
            parallax_y = camera_y * 0.1  # Very little vertical parallax
            
            original_x1, original_x2 = self.background.x1, self.background.x2
            original_y = self.background.y
            
            self.background.x1 -= parallax_x
            self.background.x2 -= parallax_x
            self.background.y -= parallax_y
            
            self.background.draw(self.screen)
            
            self.background.x1, self.background.x2 = original_x1, original_x2
            self.background.y = original_y

    def draw(self) -> None:
        """Render the current screen based on game state."""
        if self.game_state == settings.MENU:
            self.main_menu.draw(self.screen)
        
        elif self.game_state == settings.PLAYING:
            if self.tilemap and self.player:
                self._draw_game_world()
        
        elif self.game_state == settings.PAUSED:
            # Draw game in background (dimmed)
            if self.tilemap and self.player:
                self._draw_game_world()
            
            # Draw semi-transparent overlay
            overlay = pygame.Surface(self.screen.get_size())
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            # Draw pause menu
            self.pause_menu.draw(self.screen)
        
        elif self.game_state == settings.GAME_OVER:
            # Draw game in background (dimmed)
            if self.tilemap and self.player:
                self._draw_game_world()
            
            # Draw semi-transparent overlay
            overlay = pygame.Surface(self.screen.get_size())
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            # Draw game over menu
            self.game_over_menu.draw(self.screen)

        pygame.display.flip()