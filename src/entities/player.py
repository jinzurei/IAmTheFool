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
    GRAVITY,
    MAX_FALL_SPEED,
    FALL_MULTIPLIER,
    LOW_JUMP_MULTIPLIER,
    COYOTE_TIME,
    JUMP_BUFFER,
    JUMP_HOLD_TIME,
    EASING_ENABLE,
    EASING_ASCENT_GAIN_K,
    EASING_DOMAIN_SCALE,
    EASING_POWER,
    EASING_CURVE,
    DEBUG_JUMP_PHYSICS,
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
        # Position as float vector for sub-pixel movement (tied to rect)
        self.pos = pygame.Vector2(self.rect.topleft)
        # Velocities are in px/s (time-based physics)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.on_ground = False
        self.is_alive = True
        # Variable jump state
        self.jump_held = False
        self.jump_hold_time = 0.0
        # Time since the current jump started (seconds). Used for easing overlay.
        self.jump_time = 0.0
        # Input / timing helpers (seconds)
        self.time_since_grounded = 0.0
        self.time_since_jump_pressed = 999.0
        self.time_holding_jump = 0.0
        self.prev_jump_pressed = False
        self.spawn_midbottom = pos
        # small grace timer after a jump to avoid immediate re-grounding
        self._just_jumped_timer = 0.0

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
        # Deprecated: input handling is performed in update(dt, ...)
        return

    def update(self, dt, tiles, hazards=None):
        """Update player state using time-based physics.

        dt: seconds since last frame (float). Uses semi-implicit Euler:
          v += a * dt
          x += v * dt
        """
        if not self.is_alive:
            return

        # Guard dt
        if dt is None:
            return

        # Input polling and edge detection
        keys = pygame.key.get_pressed()
        left = any(keys[k] for k in LEFT_KEYS)
        right = any(keys[k] for k in RIGHT_KEYS)
        jump_pressed = any(keys[k] for k in JUMP_KEYS)

        # Optional per-frame jump diagnostics (off by default)
        # When enabled this prints a single compact line per frame giving the
        # key input and vertical physics state. Guarded so there's zero
        # runtime cost when DEBUG_JUMP_PHYSICS is False.
        if DEBUG_JUMP_PHYSICS:
            try:
                # Format: [DEBUG] jump={jump_pressed} ground={on_ground} v_y={vel_y:.2f} y={rect.y:.2f} dt={dt:.3f}
                # Also include the tracked timers for easier diagnosis.
                print(
                    f"[DEBUG] jump={bool(jump_pressed)} ground={bool(self.on_ground)} "
                    f"v_y={self.vel_y:.2f} y={float(self.rect.y):.2f} dt={dt:.3f} "
                    f"time_since_grounded={self.time_since_grounded:.3f} "
                    f"time_since_jump_pressed={self.time_since_jump_pressed:.3f}"
                )
            except Exception:
                # Never raise from debug printing
                pass

        # Jump press edge -> buffer the press
        if jump_pressed and not self.prev_jump_pressed:
            self.time_since_jump_pressed = 0.0
        self.prev_jump_pressed = jump_pressed

        # Update timing helpers
        if self.on_ground:
            self.time_since_grounded = 0.0
        else:
            self.time_since_grounded += dt

        if self.time_since_jump_pressed < 999.0:
            self.time_since_jump_pressed += dt

        # Horizontal velocity: immediate target speed (no accel provided)
        direction = 0
        if left:
            direction = -1
        elif right:
            direction = 1
        self.vel_x = RUN_SPEED * direction

        # Jump triggering (coyote + buffer)
        can_use_coyote = self.time_since_grounded <= COYOTE_TIME
        buffered_jump = self.time_since_jump_pressed <= JUMP_BUFFER
        if (self.on_ground or can_use_coyote) and buffered_jump:
            # Perform jump
            self.vel_y = JUMP_SPEED
            # Debug: log jump values so we can verify the configured jump
            # impulse is actually applied at runtime. Remove or guard this
            # behind a verbosity flag if you don't want console output.
            try:
                print(f"[DEBUG] Jump triggered: JUMP_SPEED={JUMP_SPEED}, vel_y={self.vel_y}")
            except Exception:
                pass
            # initialize easing timer for ascent shaping
            self.jump_time = 0.0
            self.on_ground = False
            # short grace so collision resolution and easing don't cancel the impulse
            self._just_jumped_timer = 0.08
            if DEBUG_JUMP_PHYSICS:
                try:
                    print("[DEBUG] Jump triggered! entering grace window")
                except Exception:
                    pass
            self.jump_held = True
            self.time_holding_jump = 0.0
            # consume buffer
            self.time_since_jump_pressed = 999.0

        # Update jump holding timer
        if self.jump_held and jump_pressed:
            self.time_holding_jump += dt
        else:
            self.jump_held = False

        # Gravity multipliers and semi-implicit Euler integration
        if self.vel_y < 0:  # rising
            if self.jump_held and self.time_holding_jump < JUMP_HOLD_TIME:
                g_eff = GRAVITY
            else:
                g_eff = GRAVITY * LOW_JUMP_MULTIPLIER
        elif self.vel_y > 0:  # falling
            g_eff = GRAVITY * FALL_MULTIPLIER
        else:
            g_eff = GRAVITY

        # Integrate velocity and position (semi-implicit)
        self.vel_y += g_eff * dt
        # Clamp downward velocity only
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED

        # --- EASING-ASSISTED ASCENT OVERLAY ---
        # Enhance ascent feel without replacing physics. This modulation only
        # acts while rising (v_y < 0) and multiplies the upward velocity by
        # M(u) = 1 - k * (e(u) ** POWER), where e(u) is the chosen easing curve.
        # - jump_time is incremented in seconds, so behavior is deterministic
        #   across FPS.
        # - u is clamped to [0,1].
        # - EASING_DOMAIN_SCALE compresses the denominator so easing acts
        #   earlier in the ascent (values < 1.0 start the curve sooner).
        if EASING_ENABLE and self.vel_y < 0:
            # advance ascent timer
            self.jump_time += dt
            # estimated physical time to apex (seconds); protect divide-by-zero
            # Physics reminder:
            #  - peak height h ≈ v0**2 / (2 * GRAVITY)
            #  - time to apex t_up ≈ |v0| / GRAVITY
            # Using these relations helps reason about how JUMP_SPEED and
            # GRAVITY trade off for height and airtime.
            if GRAVITY != 0:
                phys_time_to_apex = abs(JUMP_SPEED) / float(GRAVITY)
            else:
                phys_time_to_apex = 0.0
            # compress the domain so easing takes effect earlier in the jump
            time_to_apex = phys_time_to_apex * (EASING_DOMAIN_SCALE if EASING_DOMAIN_SCALE else 1.0)

            # compute normalized progress u in [0,1]
            u = 0.0
            if time_to_apex > 0.0:
                u = max(0.0, min(1.0, self.jump_time / time_to_apex))

            # easing curve selection
            if EASING_CURVE == "quint":
                # easeOutQuint: starts fast and eases strongly near the end
                e = 1.0 - (1.0 - u) ** 5
            else:
                # fallback: easeOutCubic to preserve previous behavior
                e = 1.0 - (1.0 - u) ** 3

            # non-linear power to emphasize apex region
            power = EASING_POWER if EASING_POWER is not None else 1.0
            k = EASING_ASCENT_GAIN_K if EASING_ASCENT_GAIN_K is not None else 0.25

            # multiplicative modulation factor (clamped to avoid sign flips)
            M = 1.0 - (k * (e ** power))
            if M < 0.0:
                M = 0.0

            # apply modulation only to upward motion (v_y is negative)
            self.vel_y = self.vel_y * M
        else:
            # reset jump_time when not rising
            self.jump_time = 0.0

        # Move horizontally by vx * dt, resolve collisions
        self.pos.x += self.vel_x * dt
        # Sync rect to float position before collision checks
        self.rect.x = int(round(self.pos.x))
        self.check_horizontal_collision(tiles)
        # After collision resolution, sync pos
        self.pos.x = float(self.rect.x)

        # Move vertically by vy * dt, resolve collisions
        self.pos.y += self.vel_y * dt
        self.rect.y = int(round(self.pos.y))
        self.check_vertical_collision(tiles)
        # After collision resolution, sync pos and grounded state
        self.pos.y = float(self.rect.y)

        # Hazards
        if hazards:
            self.check_hazard_collision(hazards)

        # Animation (kept frame-based increment for compatibility)
        self.update_animation()

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
        # Keep internal float position in sync with the rect so the next
        # physics update doesn't overwrite the respawn placement.
        try:
            self.pos = pygame.Vector2(self.rect.topleft)
        except Exception:
            # Older codepaths may not have self.pos; ignore if missing.
            pass
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
