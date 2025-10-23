import pygame
from src.core.constants import PLAYER_COLLIDER_W, PLAYER_COLLIDER_H, PLAYER_PAD
from src.core.sprite_align import align_frame_to_midbottom
from src.core.support import load_aligned_vertical_sprite_frames
from src.settings import (
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    RUN_SPEED,
    LEFT_KEYS,
    RIGHT_KEYS,
    JUMP_KEYS,
    JUMP_SPEED,
    MIN_JUMP_SPEED,
    JUMP_HOLD_TIME,
    GRAVITY,
    MAX_FALL_SPEED,
)

# Utility functions world_to_tile, tile_to_world, move_and_collide_rect are
# defined in core/collision.py and should be imported if needed


class Player(pygame.sprite.Sprite):

    def _rescale_draw_image_to_collider(self, pad=None):
        # Use runtime padding lookup to avoid default-eval of module constants
        if pad is None:
            pad = PLAYER_PAD

        rect = self.rect
        img = self.image
        avail_w = rect.width - pad[0] - pad[2]
        avail_h = rect.height - pad[1] - pad[3]
        img_w, img_h = img.get_width(), img.get_height()

        # If image empty, fallback to 1x1 to avoid div-by-zero
        if img_w == 0 or img_h == 0:
            self._draw_image = pygame.Surface((1, 1))
            self._draw_offset = pygame.Vector2(0, 0)
            return

        # Compute scale to COVER the collider (fill at least one axis).
        scale_x = avail_w / img_w
        scale_y = avail_h / img_h
        cover_scale = max(scale_x, scale_y)

        # Get visual-only scale (default 1)
        try:
            from src.core.constants import PLAYER_VISUAL_SCALE
        except Exception:
            PLAYER_VISUAL_SCALE = 1

        final_scale = cover_scale * (PLAYER_VISUAL_SCALE if PLAYER_VISUAL_SCALE else 1)

        # Scale the full image by the final scale
        target_w = max(1, int(round(img_w * final_scale)))
        target_h = max(1, int(round(img_h * final_scale)))
        scaled_img = pygame.transform.scale(img, (target_w, target_h))

        # Compute the bounding rect of visible pixels and scale its integer
        # dimensions. Round positions/sizes so we can align in exact pixels.
        bounding = img.get_bounding_rect()
        scaled_bbox_left = int(round(bounding.left * final_scale))
        scaled_bbox_top = int(round(bounding.top * final_scale))
        scaled_bbox_w = max(1, int(round(bounding.width * final_scale)))
        scaled_bbox_h = max(1, int(round(bounding.height * final_scale)))

        # Target point inside collider: horizontally centered in available
        # width, and bottom at available height (integers). Use rect.height
        # so we align feet to the collider bottom exactly.
        target_point_x = int(pad[0] + (avail_w // 2))
        target_point_y = int(rect.height)

        # Compute integer pixel coordinates inside the scaled image for the
        # bounding midbottom (feet center) and bottom.
        scaled_mid_x_pixel = scaled_bbox_left + (scaled_bbox_w // 2)
        scaled_bottom_pixel = scaled_bbox_top + scaled_bbox_h

        # Offsets so the scaled bounding midbottom/bottom map exactly to the
        # target point inside the collider.
        offset_x = int(target_point_x - scaled_mid_x_pixel)
        offset_y = int(target_point_y - scaled_bottom_pixel)

        self._draw_image = scaled_img
        self._draw_offset = pygame.Vector2(int(offset_x), int(offset_y))

    def set_frame(self, new_frame: pygame.Surface):
        # Be defensive: self.rect might not exist yet (callers during init).
        # Use a default rect sized to the collider so we can preserve midbottom.
        prev_midbottom = getattr(
            self,
            "rect",
            pygame.Rect(0, 0, PLAYER_COLLIDER_W, PLAYER_COLLIDER_H),
        ).midbottom
        self.image = new_frame
        # Use the configured collider size as authoritative for physics.
        # Preserve midbottom (above) and set rect to the configured collider.
        self.rect = self.image.get_rect()
        self.rect.size = (PLAYER_COLLIDER_W, PLAYER_COLLIDER_H)
        self.rect.midbottom = prev_midbottom
        self._rescale_draw_image_to_collider()

    def __init__(self, pos, groups):
        super().__init__(groups)
        # Load animation frames
        try:
            # Load and align all frames to midbottom using loader utility
            self.walk_frames = load_aligned_vertical_sprite_frames(
                "assets/mage.samurai/walk.png", 128, 48, 5, align_size=(48, 48)
            )
            self.idle_frames = [self.walk_frames[0]]
    # If you flip or scale frames at runtime, recompute alignment after the
    # transform so the sprite stays aligned to its collider.
    # Example (commented):
    # new_frame = pygame.transform.flip(self.image, True, False)
    # aligned_frame = align_frame_to_midbottom(
    #     new_frame, (PLAYER_WIDTH, PLAYER_HEIGHT)
    # )
    # self.set_frame(aligned_frame)
        except Exception as e:
            print(f"Animation loading failed: {e}")
            fallback_surface = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
            fallback_surface.fill((70, 130, 180))
            self.walk_frames = [
                align_frame_to_midbottom(
                    fallback_surface, (PLAYER_WIDTH, PLAYER_HEIGHT)
                )
            ]
            self.idle_frames = [self.walk_frames[0]]
        self.current_frames = self.idle_frames
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = self.current_frames[0]
        self.rect = self.image.get_rect()
        # Use configured collider size so physics uses tile-based dimensions
        self.rect.size = (PLAYER_COLLIDER_W, PLAYER_COLLIDER_H)
        self.rect.midbottom = pos
        self._draw_image = self.image
        self._draw_offset = pygame.Vector2(0, 0)
        self._rescale_draw_image_to_collider()
        self.vel_x = RUN_SPEED
        self.vel_y = 0
        self.on_ground = False
        self.is_alive = True
        # Variable jump state
        self.jump_held = False
        self.jump_hold_time = 0.0
        self.spawn_midbottom = pos

    def draw(self, screen, off=None):
        """
        Draw the player sprite using the camera offset.

        Also draw a green collision box for debugging purposes.
        """
        if off is None:
            off = pygame.Vector2(0, 0)
        draw_pos = pygame.Vector2(self.rect.topleft) + self._draw_offset - off
        screen.blit(self._draw_image, draw_pos)
        # Draw green collision box
        debug_rect = pygame.Rect(
            self.rect.x - off.x, self.rect.y - off.y, self.rect.width, self.rect.height
        )
        pygame.draw.rect(screen, (0, 255, 0), debug_rect, 2)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if any(keys[key] for key in LEFT_KEYS):
            self.vel_x = RUN_SPEED - 2
        elif any(keys[key] for key in RIGHT_KEYS):
            self.vel_x = RUN_SPEED + 2
        else:
            self.vel_x = RUN_SPEED
        jump_pressed = any(keys[key] for key in JUMP_KEYS)
        if jump_pressed and self.on_ground:
            # start jump at max jump speed and begin hold tracking
            self.vel_y = JUMP_SPEED
            self.on_ground = False
            self.jump_held = True
            self.jump_hold_time = 0.0
        elif not jump_pressed and self.jump_held:
            # key released early: stop holding and clamp to minimum jump if necessary
            self.jump_held = False
            if self.vel_y < MIN_JUMP_SPEED:
                self.vel_y = MIN_JUMP_SPEED

    def update(self, dt, tiles, hazards=None):
        if not self.is_alive:
            return
        self.handle_input()
        # dt is passed in milliseconds from the game loop
        dt_seconds = dt / 1000.0 if dt is not None else 0

    # While the jump button is held and within the hold time window, use
    # reduced gravity so the player can reach a higher jump.
        if self.jump_held:
            self.jump_hold_time += dt_seconds
            if self.jump_hold_time < JUMP_HOLD_TIME:
                gravity_effect = GRAVITY * 0.35
            else:
                # hold window expired
                self.jump_held = False
                gravity_effect = GRAVITY
        else:
            gravity_effect = GRAVITY

        self.vel_y += gravity_effect
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
        # Respawn should restore collider sized to the configured collider
        # rather than deriving from the image bounding box.
        self.rect = pygame.Rect(0, 0, PLAYER_COLLIDER_W, PLAYER_COLLIDER_H)
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
        # Update sprite image and rebuild rect to preserve midbottom. The
        # `set_frame` call recomputes and preserves midbottom internally, so
        # we don't need to compute it here.
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
        Flip the currently aligned image horizontally if facing_left is True.

        This preserves rect.midbottom and calls
        _rescale_draw_image_to_collider() to recompute the draw image
        and offset so the sprite remains aligned to its collider.
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
