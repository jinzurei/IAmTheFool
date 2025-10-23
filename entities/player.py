import pygame
import settings


class Player:
    """Player character with movement and jumping capabilities."""

    def __init__(self) -> None:
        """Initialize the player with starting position and properties."""
        self.width = settings.PLAYER_WIDTH
        self.height = settings.PLAYER_HEIGHT
        self.x = settings.PLAYER_START_X
        self.y = settings.SCREEN_HEIGHT - self.height - settings.PLAYER_GROUND_OFFSET
        self.vel_y = 0
        self.vel_x = 0  # Horizontal velocity for momentum
        self.on_ground = True
        self.color = settings.BROWN

        # Enhanced jump mechanics
        self.coyote_time = 0  # Frames since leaving ground
        self.jump_buffer = 0  # Frames jump has been buffered
        self.jump_held = False  # Is jump button currently held

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle player input events like jumping."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_w):
                self.jump_buffer = settings.JUMP_BUFFER_TIME
                self.jump_held = True
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_SPACE, pygame.K_w):
                self.jump_held = False

    def update(self, keys: pygame.key.ScancodeWrapper, tilemap=None) -> None:
        """Update player position based on physics and input."""
        # Update timers
        if self.jump_buffer > 0:
            self.jump_buffer -= 1

        if not self.on_ground:
            self.coyote_time += 1

        # Apply gravity with different rates based on state
        gravity = settings.GRAVITY

        # Reduced gravity when holding jump and moving upward (variable jump height)
        if self.jump_held and self.vel_y < 0:
            gravity *= settings.JUMP_HOLD_MULTIPLIER

        # Increased gravity when pressing down (fast fall)
        if keys[pygame.K_s]:
            gravity *= settings.FAST_FALL_MULTIPLIER

        # Apply gravity
        self.vel_y += gravity

        # Cap falling speed at terminal velocity
        if self.vel_y > settings.TERMINAL_VELOCITY:
            self.vel_y = settings.TERMINAL_VELOCITY

        # Handle jumping with coyote time and jump buffering
        if self.jump_buffer > 0 and (
            self.on_ground or self.coyote_time <= settings.COYOTE_TIME
        ):
            self.vel_y = settings.JUMP_VELOCITY
            self.on_ground = False
            self.coyote_time = (
                settings.COYOTE_TIME + 1
            )  # Disable coyote time after jumping
            self.jump_buffer = 0  # Clear jump buffer

        # Update vertical position
        self.y += self.vel_y

        # Enhanced horizontal movement with momentum
        self._update_horizontal_movement(keys)

        # Ground collision using tilemap
        if tilemap:
            # Use tile-based collision
            self._handle_tile_collision(tilemap)
        else:
            # Fallback to old ground collision
            ground = (
                settings.SCREEN_HEIGHT - self.height - settings.PLAYER_GROUND_OFFSET
            )
            if self.y >= ground:
                self.y = ground
                self.vel_y = 0
                if not self.on_ground:  # Just landed
                    self.on_ground = True
                    self.coyote_time = 0
            else:
                # Player is in the air
                if self.on_ground:  # Just left ground
                    self.on_ground = False
                    self.coyote_time = 0

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the player with enhanced visuals."""
        # Main body
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

        # Simple highlight for 3D effect
        highlight_color = tuple(min(255, c + 30) for c in self.color)
        pygame.draw.rect(surface, highlight_color, (self.x, self.y, self.width, 5))
        pygame.draw.rect(surface, highlight_color, (self.x, self.y, 5, self.height))

        # Shadow/outline
        shadow_color = tuple(max(0, c - 40) for c in self.color)
        pygame.draw.rect(
            surface, shadow_color, (self.x, self.y, self.width, self.height), 2
        )

    def _update_horizontal_movement(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Update horizontal movement with realistic physics."""
        # Determine movement intent
        move_left = keys[pygame.K_a]
        move_right = keys[pygame.K_d]
        is_dashing = move_right  # Right movement acts as dash

        # Get movement parameters based on ground state
        if self.on_ground:
            acceleration = settings.ACCELERATION
            if is_dashing:
                acceleration *= settings.DASH_BOOST
                max_speed = settings.DASH_MAX_SPEED
            else:
                max_speed = settings.MAX_SPEED
        else:
            # Air control - reduced but still present
            acceleration = settings.ACCELERATION * settings.AIR_CONTROL
            if is_dashing:
                acceleration *= settings.DASH_BOOST
                max_speed = settings.DASH_MAX_SPEED
            else:
                max_speed = settings.MAX_SPEED

        # Apply acceleration based on input
        if move_left and not move_right:
            # Moving left
            self.vel_x -= acceleration
            if self.vel_x < -max_speed:
                self.vel_x = -max_speed
        elif move_right and not move_left:
            # Moving right (dash)
            self.vel_x += acceleration
            if self.vel_x > max_speed:
                self.vel_x = max_speed
        else:
            # No input or conflicting input - apply deceleration
            if self.on_ground:
                # Ground friction
                self.vel_x *= settings.FRICTION
                # Stop small movements to prevent jitter
                if abs(self.vel_x) < 0.1:
                    self.vel_x = 0
            else:
                # Air deceleration (much slower)
                air_decel = settings.ACCELERATION * settings.AIR_CONTROL * 0.5
                if self.vel_x > 0:
                    self.vel_x -= air_decel
                    if self.vel_x < 0:
                        self.vel_x = 0
                elif self.vel_x < 0:
                    self.vel_x += air_decel
                    if self.vel_x > 0:
                        self.vel_x = 0

        # Update position with velocity
        new_x = self.x + self.vel_x

        # Keep player within screen bounds
        if new_x < 0:
            new_x = 0
            self.vel_x = 0  # Stop when hitting left wall
        elif new_x > settings.SCREEN_WIDTH - self.width:
            new_x = settings.SCREEN_WIDTH - self.width
            self.vel_x = 0  # Stop when hitting right wall

        self.x = new_x

    def get_rect(self) -> pygame.Rect:
        """Get the player's bounding rectangle for collision detection."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def _handle_tile_collision(self, tilemap) -> None:
        """Handle collision with tiles."""
        # Get tiles that overlap with player
        solid_tiles = tilemap.get_tiles_in_rect(self.x, self.y, self.width, self.height)

        landed_on_solid = False

        for tile in solid_tiles:
            tile_rect = pygame.Rect(
                tile["world_x"], tile["world_y"], settings.TILE_SIZE, settings.TILE_SIZE
            )
            player_rect = self.get_rect()

            if player_rect.colliderect(tile_rect):
                # Vertical collision (landing on tiles)
                if self.vel_y > 0:  # Player is falling
                    # Check if player was above the tile in the previous frame
                    prev_player_bottom = self.y + self.height - self.vel_y
                    if prev_player_bottom <= tile_rect.top + 5:  # Was above tile
                        # Land on top of tile
                        self.y = tile_rect.top - self.height
                        self.vel_y = 0
                        landed_on_solid = True
                        if not self.on_ground:
                            self.on_ground = True
                            self.coyote_time = 0
                        break

        # If no solid ground found, player is in air
        if not landed_on_solid:
            if self.on_ground:
                self.on_ground = False
                self.coyote_time = 0
