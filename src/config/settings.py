# Game configuration settings
# (moved from src/core/settings.py)

SCREEN_WIDTH = 800
# Game configuration settings
# (moved from src/core/settings.py)
import pygame
SCREEN_HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (70, 130, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

TILE_SIZE = 32
PLAYER_WIDTH = 400
PLAYER_HEIGHT = 128
PLAYER_COLLISION_WIDTH = 50
PLAYER_COLLISION_HEIGHT = 100
RUN_SPEED = 4
JUMP_SPEED = -16
GRAVITY = 0.8
MAX_FALL_SPEED = 15
JUMP_KEYS = [pygame.K_SPACE, pygame.K_w, pygame.K_UP]
LEFT_KEYS = [pygame.K_a, pygame.K_LEFT]
RIGHT_KEYS = [pygame.K_d, pygame.K_RIGHT]
