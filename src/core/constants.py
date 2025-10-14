# Player sprite and collider constants
PLAYER_NATIVE_W = 12  # native sprite width
PLAYER_NATIVE_H = 16  # native sprite height
PLAYER_INTEGER_SCALE = 4  # integer scale factor for crisp pixel art
PLAYER_PAD = (1, 2, 1, 2)  # (L, T, R, B) padding: left, top, right, bottom

# Derived collider size
PLAYER_COLLIDER_W = PLAYER_NATIVE_W * PLAYER_INTEGER_SCALE + PLAYER_PAD[0] + PLAYER_PAD[2]
PLAYER_COLLIDER_H = PLAYER_NATIVE_H * PLAYER_INTEGER_SCALE + PLAYER_PAD[1] + PLAYER_PAD[3]
