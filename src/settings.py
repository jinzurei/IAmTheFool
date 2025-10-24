"""
Unified settings for the project.

All project modules must import this module for configuration constants.
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
#
# Physics notes:
# - Peak height (approx): h ≈ v0^2 / (2 * GRAVITY)
# - Time to apex (approx): t_up ≈ |v0| / GRAVITY
# - Total airtime (approx): t_total ≈ 2 * t_up
# - Horizontal distance (approx): d ≈ RUN_SPEED * t_total
# The constants below raise jump height and airtime while keeping the
# easing overlay and deterministic dt-based physics intact.
RUN_SPEED = 380            # px/s, steady-state horizontal speed when held
GRAVITY = 1400             # px/s^2, base downward acceleration (positive)
# JUMP_SPEED (v0) is negative for upward impulse. Increasing |v0| raises
# peak height h ≈ v0^2 / (2 * GRAVITY) and increases time to apex t_up ≈ |v0|/GRAVITY.
JUMP_SPEED = -1300         # px/s, initial vertical velocity at jump (negative = up)
MAX_FALL_SPEED = 2600      # px/s, clamp terminal velocity |v_y| when falling

# --- Jump feel multipliers (dimensionless) ---
FALL_MULTIPLIER = 1.8      # multiplies GRAVITY when v_y > 0 (falling)
LOW_JUMP_MULTIPLIER = 1.7  # extra gravity when jump released while rising

# --- Forgiveness windows (UNITS: seconds) ---
COYOTE_TIME = 0.10         # jump allowed this long after leaving ground
JUMP_BUFFER = 0.10         # jump press buffer window (seconds)
JUMP_HOLD_TIME = 0.35      # max duration that “hold jump for higher jump” is honored

# Controls
JUMP_KEYS = [pygame.K_SPACE, pygame.K_w, pygame.K_UP]
LEFT_KEYS = [pygame.K_a, pygame.K_LEFT]
RIGHT_KEYS = [pygame.K_d, pygame.K_RIGHT]

# Game states
MENU = "menu"
PLAYING = "playing"
DEAD = "dead"

# --- Easing overlay for ascent shaping (dimensionless / feature flag) ---
# When enabled, this gently modulates the upward velocity during ascent
# using easeOutCubic to produce a fast takeoff and gentle apex.
EASING_ENABLE = True
# Gain k used in M(u) = 1 - k * e(u) where e(u) is the chosen easing curve.
# Increasing k strengthens the apex softening. Typical tuning range: 0.15 - 0.5
# Set to 0.4 for a more noticeable effect (cuts upward velocity by up to 40%).
EASING_ASCENT_GAIN_K = 0.25

# Domain scaling: multiply the physics time_to_apex by this value so easing
# acts earlier in the ascent. Values < 1.0 make easing start sooner.
EASING_DOMAIN_SCALE = 1.0  # fraction of physical time_to_apex

# Power applied to the easing value e before modulation (non-linear gain).
# e_effective = e ** EASING_POWER. Values > 1 emphasize the apex region.
EASING_POWER = 1.2

# Easing curve selector (string). Supported values: "cubic", "quint".
# 'quint' gives a stronger slow-down near the end of the ascent.
EASING_CURVE = "quint"

# Notes:
# - The overlay is multiplicative and only affects upward velocity while rising.
# - u is clamped to [0,1] so behavior is deterministic across FPS.

# Runtime debug helpers
# Set to True to enable per-frame jump diagnostics printed to stdout.
DEBUG_JUMP_PHYSICS = False
