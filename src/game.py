"""
Main game class for I Am The Fool - Auto-Runner Platformer
"""

import pygame
import sys
from src.core.settings import *
from src.core.support import load_csv_layout
from src.core.camera import YSortCameraGroup
from src.entities.player import Player
from src.entities.tile import StaticTile
from src.entities.hazard import VisibleHazard, InvisibleHazard
from src.ui.death_screen import DeathScreen

class Game:
    """Main game class that manages the game loop and infinite scene looping"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("I Am The Fool")
        self.clock = pygame.time.Clock()
        
        # Sprite groups
        self.camera_group = YSortCameraGroup()
        self.tiles = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        
        # Game state
        self.game_state = "playing"  # "playing" or "dead"
        self.death_screen = DeathScreen(self.screen)
        
        # Level data for infinite looping
        self.scene_layout = []
        self.scene_width = 0
        self.loop_offset = 0  # How many times we've looped
        
        # Find spawn tile in map
        spawn_pos = None
        layout_path = f"src/scenes/scene_1/map.csv"
        layout = load_csv_layout(layout_path)
        spawn_col = None
        spawn_row = None
        for row_idx, row in enumerate(layout):
            for col_idx, cell in enumerate(row):
                if cell == '9':
                    spawn_col = col_idx
                    spawn_row = row_idx
                    break
            if spawn_col is not None:
                break
        if spawn_col is not None:
            # Ensure the spawn tile is directly above a ground tile
            ground_row = spawn_row + 1
            if ground_row >= len(layout) or layout[ground_row][spawn_col] != '1':
                raise Exception("Spawn tile must be directly above a ground tile.")
            # Place player one tile above the spawn tile
            spawn_pos = (spawn_col * TILE_SIZE, spawn_row * TILE_SIZE - PLAYER_HEIGHT)
        else:
            spawn_pos = (100, 300)  # fallback
        self.player = Player(spawn_pos, [self.camera_group])
        
        # Load scene
        self.load_scene('scene_1')
        
    def load_scene(self, scene_name):
        """Load a scene from CSV tilemap data and store for infinite looping"""
        # Load CSV layout
        layout_path = f"src/scenes/{scene_name}/map.csv"
        self.scene_layout = load_csv_layout(layout_path)
        self.scene_width = len(self.scene_layout[0]) * TILE_SIZE if self.scene_layout else 0
        
        # Build initial tiles
        self.build_tiles()
        
    def build_tiles(self):
        """Build tiles for current view with infinite looping"""
        # Clear existing tiles and hazards
        self.camera_group.empty()
        self.tiles.empty()
        self.hazards.empty()
        
        # Re-add player to camera group
        self.camera_group.add(self.player)
        
        # Define tile colors (can be replaced with textures later)
        tile_colors = {
            0: None,
            1: (139, 69, 19),   # Brown (ground)
            2: (100, 100, 100), # Grey (platforms)
            3: (100, 100, 100), # Grey (platforms)
            9: (255, 215, 0)    # Gold/yellow for spawn tile
        }
        
        # Calculate how many screen widths to build (build extra for smooth scrolling)
        build_width = SCREEN_WIDTH * 3  # Build 3 screen widths worth
        start_x = max(0, int(self.player.rect.centerx - build_width // 2))
        end_x = start_x + build_width
        
        # Build tiles from layout with looping
        for row_index, row in enumerate(self.scene_layout):
            for world_x in range(start_x, end_x, TILE_SIZE):
                # Calculate which column in the original layout this represents
                col_index = (world_x // TILE_SIZE) % len(row)
                cell = row[col_index]
                
                y = row_index * TILE_SIZE
                
                tile_value = int(cell) if cell != '-1' else 0
                if tile_value == 9:
                    # Spawn tile, draw it but don't add collision
                    color = tile_colors[tile_value]
                    surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    surface.fill(color)
                    pygame.draw.rect(surface, BLACK, surface.get_rect(), 2)
                    tile = StaticTile((world_x, y), [self.camera_group], surface)  # No collision group
                elif tile_value > 0 and tile_value in tile_colors:
                    color = tile_colors[tile_value]
                    surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    surface.fill(color)
                    pygame.draw.rect(surface, BLACK, surface.get_rect(), 2)
                    tile = StaticTile((world_x, y), [self.camera_group, self.tiles], surface)
                elif tile_value == 4:  # Visible hazard
                    hazard = VisibleHazard((world_x, y), [self.camera_group, self.hazards])
                elif tile_value == 5:  # Invisible hazard
                    hazard = InvisibleHazard((world_x, y), [self.hazards])
    
    def update_tiles(self):
        """Update tiles based on player position for infinite scrolling"""
        # Rebuild tiles when player has moved significantly
        if hasattr(self, '_last_build_x'):
            if abs(self.player.rect.centerx - self._last_build_x) > SCREEN_WIDTH // 2:
                self.build_tiles()
                self._last_build_x = self.player.rect.centerx
        else:
            self._last_build_x = self.player.rect.centerx
    
    def run(self):
        """Main game loop"""
        while True:
            dt = self.clock.tick(FPS)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                
                # Handle death screen input
                if self.game_state == "dead":
                    action = self.death_screen.handle_input(event)
                    if action == "retry":
                        self.restart_game()
                    elif action == "quit":
                        pygame.quit()
                        sys.exit()
            
            # Update game based on state
            if self.game_state == "playing":
                # Update player and check for death
                self.player.update(dt, self.tiles, self.hazards)
                self.update_tiles()  # Update tiles for infinite scrolling
                
                # Check if player died
                if not self.player.is_alive:
                    self.game_state = "dead"
            
            # Draw
            self.screen.fill((135, 206, 250))  # Sky blue background
            self.camera_group.custom_draw(self.player)
            
            # Draw death screen if player is dead
            if self.game_state == "dead":
                self.death_screen.draw()
            
            pygame.display.flip()
    
    def restart_game(self):
        """Restart the game after death"""
        self.player.respawn()
        self.game_state = "playing"
        self.build_tiles()  # Rebuild tiles around spawn position