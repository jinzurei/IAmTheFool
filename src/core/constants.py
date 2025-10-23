# Player sprite and collider constants
from src.settings import TILE_SIZE

# Choose a smaller collider (narrower/taller) to match the visible player and
# keep platforming feel. We'll derive a 50x100 collider from a 48x96 native
# sprite canvas plus padding (1 left + 1 right = 2, 2 top + 2 bottom = 4).
PLAYER_INTEGER_SCALE = 2
PLAYER_NATIVE_W = 48
PLAYER_NATIVE_H = 96
PLAYER_PAD = (1, 2, 1, 2)  # (L, T, R, B)

# Derived collider size (authoritative)

# Target collider expressed in tiles (width = 1.5 tiles, height = 2 tiles)
# Using TILE_SIZE ensures consistency with level geometry.
PLAYER_COLLIDER_W = int(1.5 * TILE_SIZE)
PLAYER_COLLIDER_H = 2 * TILE_SIZE

# Visual-only scale factor. When >1, the drawn sprite will be scaled up
# for presentation while the collision rect (PLAYER_COLLIDER_W/H) remains
# authoritative for physics. Set to 1 to keep visuals matching collider by default.
PLAYER_VISUAL_SCALE = 2
