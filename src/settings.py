"""
Unified settings for the project.

All project modules should import this module for configuration constants.
"""

import pygame

# Display & Runtime (WIDTH, HEIGHT, FPS, CAPTION, etc.)
# SCREEN_WIDTH / SCREEN_HEIGHT: window size in pixels. Used when creating
# the pygame display surface and for camera centering calculations.
# Changing these values changes the visible viewport and may require
# adjustments to UI/camera logic.
SCREEN_WIDTH = 800  # pixels
SCREEN_HEIGHT = 600  # pixels
# FPS: target frames-per-second used with pygame.time.Clock.tick(FPS).
# Affects how often update/draw run; movement code sometimes assumes
# per-frame steps (not always dt-corrected), so test gameplay when
# changing FPS.
FPS = 60

# Colors
# RGB tuples used for drawing. Change for theme/visibility.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (70, 130, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Level geometry
# TILE_SIZE: size of one tile in pixels. This is the grid unit for tilemaps
# and collision geometry. Changing it affects level layout and collider
# calculations throughout the codebase.
TILE_SIZE = 32  # pixels

# Player dimensions and visual fallback
# PLAYER_WIDTH / PLAYER_HEIGHT: only used as a fallback visual surface
# when sprite frame loading fails. The authoritative collision size is
# defined in src/core/constants.py (PLAYER_COLLIDER_W/H).
PLAYER_WIDTH = 400  # fallback visual width (pixels)
PLAYER_HEIGHT = 128  # fallback visual height (pixels)

# --- Time-based physics (UNITS: px/s and px/s^2) ---
# RUN_SPEED: px/s steady horizontal speed when holding left/right.
# GRAVITY: px/s^2 base downward acceleration (positive downwards).
# JUMP_SPEED: px/s initial vertical velocity at jump (negative = up).
# MAX_FALL_SPEED: px/s clamp on downward velocity.
RUN_SPEED = 320            # px/s, steady-state horizontal speed when held
GRAVITY = 1800             # px/s^2, base downward acceleration (positive)
JUMP_SPEED = -900          # px/s initial vertical velocity at jump (negative = up)
MAX_FALL_SPEED = 2400      # px/s, clamp terminal velocity |v_y| when falling

# --- Jump feel multipliers (dimensionless) ---
FALL_MULTIPLIER = 1.8      # multiplies GRAVITY when v_y > 0 (falling)
LOW_JUMP_MULTIPLIER = 2.0  # extra gravity when jump released while rising

# --- Forgiveness windows (UNITS: seconds) ---
COYOTE_TIME = 0.10         # jump allowed this long after leaving ground
JUMP_BUFFER = 0.10         # jump press buffer window (seconds)
JUMP_HOLD_TIME = 0.25      # max duration that “hold jump for higher jump” is honored

# Controls
JUMP_KEYS = [pygame.K_SPACE, pygame.K_w, pygame.K_UP]
LEFT_KEYS = [pygame.K_a, pygame.K_LEFT]
RIGHT_KEYS = [pygame.K_d, pygame.K_RIGHT]

# Game states
MENU = "menu"
PLAYING = "playing"
DEAD = "dead"
