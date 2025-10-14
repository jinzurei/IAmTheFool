

import pygame
from src.core.constants import PLAYER_COLLIDER_W, PLAYER_COLLIDER_H, PLAYER_INTEGER_SCALE, PLAYER_PAD
from src.core.sprite_align import align_frame_to_midbottom
from src.core.support import load_vertical_sprite_frames
from src.config.settings import *
TILE_SIZE = 32
## Utility functions world_to_tile, tile_to_world, move_and_collide_rect are defined in core/collision.py and should be imported if needed

class Player(pygame.sprite.Sprite):
    # ...existing code...

    def _rescale_draw_image_to_collider(self, pad=PLAYER_PAD):
        rect = self.rect
        img = self.image
        avail_w = rect.width - pad[0] - pad[2]
        avail_h = rect.height - pad[1] - pad[3]
        img_w, img_h = img.get_width(), img.get_height()
        new_w = img_w * PLAYER_INTEGER_SCALE
        new_h = img_h * PLAYER_INTEGER_SCALE
        scaled_img = pygame.transform.scale(img, (new_w, new_h))
        offset_x = pad[0] + (avail_w - new_w) // 2
        offset_y = pad[1] + (avail_h - new_h)
        self._draw_image = scaled_img
        self._draw_offset = pygame.Vector2(offset_x, offset_y)

    def set_frame(self, new_frame: pygame.Surface):
        prev_midbottom = self.rect.midbottom
        self.image = new_frame
        self.rect = self.image.get_rect()
        self.rect.size = (PLAYER_COLLIDER_W, PLAYER_COLLIDER_H)
        self.rect.midbottom = prev_midbottom
        self._rescale_draw_image_to_collider()

    def __init__(self, pos, groups):
        super().__init__(groups)
        # Load animation frames
        try:
            # Load and align all frames to midbottom using loader utility
            from src.core.support import load_aligned_vertical_sprite_frames
            self.walk_frames = load_aligned_vertical_sprite_frames(
                "assets/mage.samurai/walk.png", 128, 48, 5, align_size=(48,48)
            )
            self.idle_frames = [self.walk_frames[0]]
    # If you ever flip or scale frames at runtime, always recompute alignment after transform:
    # new_frame = pygame.transform.flip(self.image, True, False)
    # aligned_frame = align_frame_to_midbottom(new_frame, (PLAYER_WIDTH, PLAYER_HEIGHT))
    # self.set_frame(aligned_frame)
        except Exception as e:
            print(f"Animation loading failed: {e}")
            fallback_surface = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
            fallback_surface.fill((70, 130, 180))
            self.walk_frames = [align_frame_to_midbottom(fallback_surface, (PLAYER_WIDTH, PLAYER_HEIGHT))]
            self.idle_frames = [self.walk_frames[0]]
        self.current_frames = self.idle_frames
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = self.current_frames[0]
        self.rect = self.image.get_rect()
        self.rect.size = (PLAYER_COLLIDER_W, PLAYER_COLLIDER_H)
        self.rect.midbottom = pos
        self._draw_image = self.image
        self._draw_offset = pygame.Vector2(0, 0)
        self._rescale_draw_image_to_collider()
        self.vel_x = RUN_SPEED
        self.vel_y = 0
        self.on_ground = False
        self.is_alive = True
        self.spawn_midbottom = pos

    def draw(self, screen, off=None):
        """
        Draw the player sprite and green collider debug rectangle using the camera offset.
        The offset is provided by the camera group for render-physics alignment.
        """
        if off is None:
            off = pygame.Vector2(0, 0)
        draw_pos = pygame.Vector2(self.rect.topleft) + self._draw_offset - off
        screen.blit(self._draw_image, draw_pos)
        # Green debug rect for collider
        debug_rect = pygame.Rect(self.rect.x - off.x, self.rect.y - off.y, self.rect.width, self.rect.height)
        pygame.draw.rect(screen, (0, 255, 0), debug_rect, 2)

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
        # self.rect is authoritative; no sprite_rect needed
    
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
        bounding_rect = self.image.get_bounding_rect()
        if bounding_rect.width > 0 and bounding_rect.height > 0:
            self.rect = bounding_rect.copy()
        else:
            self.rect = self.image.get_rect()
        self.rect.midbottom = self.spawn_midbottom
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
        # Update sprite image and rebuild rect to preserve midbottom
        prev_midbottom = self.rect.midbottom
        self.set_frame(self.current_frames[int(self.frame_index)])
    
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
    
    def flip_horiz(self, facing_left: bool):
        """
        Flip the currently aligned image horizontally if facing_left is True, preserve rect.midbottom, and re-run _rescale_draw_image_to_collider().
        """
        prev_midbottom = self.rect.midbottom
        # Flip only if needed
        if facing_left:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            # Optionally restore to original if you keep a reference
            pass
        self.rect = self.image.get_rect()
        self.rect.size = (PLAYER_COLLIDER_W, PLAYER_COLLIDER_H)
        self.rect.midbottom = prev_midbottom
        self._rescale_draw_image_to_collider()