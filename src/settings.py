"""
Unified settings for the project.

All project modules should import this module for configuration constants.
"""

import pygame

# Display & Runtime (WIDTH, HEIGHT, FPS, CAPTION, etc.)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (70, 130, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Physics & Movement (GRAVITY, PLAYER_SPEED, JUMP_FORCE, TILE_SIZE, etc.)
TILE_SIZE = 32

# Player dimensions and collision
# NOTE: collision sizes are authoritative in src/core/constants.py
# Use PLAYER_COLLIDER_W and PLAYER_COLLIDER_H from that module.
PLAYER_WIDTH = 400
PLAYER_HEIGHT = 128

# Movement & jumping
RUN_SPEED = 4
JUMP_SPEED = -15
GRAVITY = 0.7
MAX_FALL_SPEED = 15

# Variable jump controls
MIN_JUMP_SPEED = -10
JUMP_HOLD_TIME = 0.55

# Controls
JUMP_KEYS = [pygame.K_SPACE, pygame.K_w, pygame.K_UP]
LEFT_KEYS = [pygame.K_a, pygame.K_LEFT]
RIGHT_KEYS = [pygame.K_d, pygame.K_RIGHT]
