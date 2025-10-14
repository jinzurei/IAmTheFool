"""
Game settings for I Am The Fool - Auto-Runner Platformer
"""

import pygame

# ================================
# DISPLAY SETTINGS
# ================================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# ================================
# COLORS
# ================================
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# ================================
# TILE SETTINGS
# ================================
TILE_SIZE = 32

# ================================
# PLAYER SETTINGS
# ================================
PLAYER_WIDTH = 400  # Comically wide for extreme effect
PLAYER_HEIGHT = 128  # Less tall, matches sprite aspect ratio
PLAYER_COLLISION_WIDTH = 50  # Reasonable collision box width
PLAYER_COLLISION_HEIGHT = 100  # Reasonable collision box height
RUN_SPEED = 4
JUMP_SPEED = -16
GRAVITY = 0.8
MAX_FALL_SPEED = 15

# ================================
# CONTROLS
# ================================
JUMP_KEYS = [pygame.K_SPACE, pygame.K_w, pygame.K_UP]
LEFT_KEYS = [pygame.K_a, pygame.K_LEFT]
RIGHT_KEYS = [pygame.K_d, pygame.K_RIGHT]