

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
BLUE = (70, 130, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# ================================
# GAME STATES
# ================================
MENU = 1
PLAYING = 2
PAUSED = 3
GAME_OVER = 4

# ================================
# TILE SETTINGS
# ================================
TILE_SIZE = 32

# ================================
# PLAYER SETTINGS
# ================================
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 48
RUN_SPEED = 4
JUMP_SPEED = -16
GRAVITY = 0.8
MAX_FALL_SPEED = 15

# Responsiveness settings
COYOTE_TIME = 200  # milliseconds
JUMP_BUFFER = 150  # milliseconds

# ================================
# CAMERA SETTINGS
# ================================
CAMERA_BORDER_LEFT = 200
CAMERA_BORDER_RIGHT = 200
CAMERA_BORDER_TOP = 100
CAMERA_BORDER_BOTTOM = 150

# ================================
# PARALLAX SETTINGS
# ================================
PARALLAX_SPEEDS = [0.2, 0.5, 0.8]

# ================================
# CONTROLS
# ================================
JUMP_KEYS = [pygame.K_SPACE, pygame.K_w, pygame.K_UP]
LEFT_KEYS = [pygame.K_a, pygame.K_LEFT]
RIGHT_KEYS = [pygame.K_d, pygame.K_RIGHT]
DOWN_KEYS = [pygame.K_s, pygame.K_DOWN]
PAUSE_KEY = pygame.K_ESCAPE

PAUSED = 3

GAME_OVER = 4
SCREEN_HEIGHT = 600



# Infinite RunnerFPS = 60# ================================DEFAULT_SCREEN_WIDTH = 800

WORLD_SCROLL_SPEED = 3

TILE_SIZE = 32

GROUND_HEIGHT_TILES = 6
# World scrollingRED = (255, 0, 0)PAUSED = "paused"


# ================================
# GAME PROGRESSION
# ================================

REGION_CHANGE_THRESHOLD = 2000

# ================================
# USER INTERFACE
# ================================

MENU_FONT_SIZE = 48
BUTTON_FONT_SIZE = 36
MENU_BUTTON_WIDTH = 200
MENU_BUTTON_HEIGHT = 60
MENU_BUTTON_SPACING = 80