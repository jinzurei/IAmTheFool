"""
Player class with auto-run, collision, and walk animation
"""

import pygame
from src.config.settings import *
from src.core.support import load_vertical_sprite_frames

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        # Load animation frames
        try:
            self.walk_frames = load_vertical_sprite_frames("assets/mage.samurai/walk.png", 128, 48, 5)
            scaled_frames = []
            for frame in self.walk_frames:
                scaled_frame = pygame.transform.scale(frame, (PLAYER_WIDTH, PLAYER_HEIGHT))
                scaled_frames.append(scaled_frame)
            self.walk_frames = scaled_frames
            self.idle_frames = [self.walk_frames[0]]
        except Exception as e:
            print(f"Animation loading failed: {e}")
            fallback_surface = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
            fallback_surface.fill((70, 130, 180))
            self.walk_frames = [fallback_surface]
            self.idle_frames = [fallback_surface]
        self.current_frames = self.idle_frames
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = self.current_frames[0]
        self.rect = pygame.Rect(pos[0], pos[1], PLAYER_COLLISION_WIDTH, PLAYER_COLLISION_HEIGHT)
        self.sprite_rect = self.image.get_rect(topleft=pos)
        self.vel_x = RUN_SPEED
        self.vel_y = 0
        self.on_ground = False
        self.is_alive = True
        self.spawn_position = pos
    def draw(self, surface):
        sprite_x = self.rect.centerx - PLAYER_WIDTH // 2
        sprite_y = self.rect.bottom - PLAYER_HEIGHT
        surface.blit(self.image, (sprite_x, sprite_y))
        pygame.draw.rect(surface, (0, 255, 0), self.rect, 2)
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if any(keys[key] for key in LEFT_KEYS):
            self.vel_x = RUN_SPEED - 2
        elif any(keys[key] for key in RIGHT_KEYS):
            self.vel_x = RUN_SPEED + 2
        else:
            self.vel_x = RUN_SPEED
        if any(keys[key] for key in JUMP_KEYS) and self.on_ground:
            self.vel_y = JUMP_SPEED
            self.on_ground = False
    def update(self, dt, tiles, hazards=None):
        if not self.is_alive:
            return
        self.handle_input()
        self.vel_y += GRAVITY
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED
        # Move horizontally
        self.rect.x += self.vel_x
        self.check_horizontal_collision(tiles)
        # Move vertically
        self.rect.y += self.vel_y
        self.check_vertical_collision(tiles)
        # Check hazard collision
        if hazards:
            self.check_hazard_collision(hazards)
        # Update animation
        self.update_animation()
        # Update sprite rect to follow collision rect (for reference, not used for blit)
        self.sprite_rect.centerx = self.rect.centerx
        self.sprite_rect.bottom = self.rect.bottom
    
    def check_hazard_collision(self, hazards):
        """Check if player touches any hazard and die if so"""
        collisions = pygame.sprite.spritecollide(self, hazards, False)
        if collisions:
            self.die()
    
    def die(self):
        """Kill the player"""
        self.is_alive = False
        self.vel_x = 0
        self.vel_y = 0
    
    def respawn(self):
        """Respawn the player at spawn position, directly on ground"""
        # Align collision box so its bottom sits on top of the ground tile
        spawn_x, spawn_y = self.spawn_position
        self.rect.x = spawn_x + (PLAYER_WIDTH - PLAYER_COLLISION_WIDTH) // 2
        self.rect.y = spawn_y + PLAYER_HEIGHT - PLAYER_COLLISION_HEIGHT
        self.sprite_rect.centerx = self.rect.centerx
        self.sprite_rect.bottom = self.rect.bottom
        self.vel_x = RUN_SPEED
        self.vel_y = 0
        self.on_ground = True
        self.is_alive = True
        self.frame_index = 0
        self.current_frames = self.walk_frames
    
    def update_animation(self):
        """Update player animation based on movement state"""
        # Choose animation frames based on movement
        if self.vel_x != 0:  # Moving
            self.current_frames = self.walk_frames
        else:  # Idle
            self.current_frames = self.idle_frames
        # Update animation frame
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.current_frames):
            self.frame_index = 0
        # Update sprite image
        self.image = self.current_frames[int(self.frame_index)]
        # Keep sprite_rect in sync
        self.sprite_rect.topleft = self.rect.topleft
    
    def check_horizontal_collision(self, tiles):
        collisions = pygame.sprite.spritecollide(self, tiles, False)
        if collisions:
            if self.vel_x > 0:  # Moving right
                self.rect.right = collisions[0].rect.left
            else:  # Moving left
                self.rect.left = collisions[0].rect.right
    
    def check_vertical_collision(self, tiles):
        self.on_ground = False
        collisions = pygame.sprite.spritecollide(self, tiles, False)
        if collisions:
            if self.vel_y > 0:  # Falling
                self.rect.bottom = collisions[0].rect.top
                self.vel_y = 0
                self.on_ground = True
            else:  # Jumping up
                self.rect.top = collisions[0].rect.bottom
                self.vel_y = 0