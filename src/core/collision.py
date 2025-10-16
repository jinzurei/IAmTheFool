import pygame
TILE = 32
def world_to_tile(x, y):
    return x // TILE, y // TILE
def tile_to_world(tx, ty):
    return tx * TILE, ty * TILE
def move_and_collide_rect(rect, vx, vy, is_solid_tile):
    rect.x += vx
    if vx != 0:
        left, top = world_to_tile(rect.left, rect.top)
        right, bottom = world_to_tile(rect.right - 1, rect.bottom - 1)
        for ty in range(top, bottom + 1):
            if vx > 0:
                tx = right
                if is_solid_tile(tx, ty):
                    rect.right = tile_to_world(tx, ty)[0]
            else:
                tx = left
                if is_solid_tile(tx, ty):
                    rect.left = tile_to_world(tx, ty)[0] + TILE
    rect.y += vy
    if vy != 0:
        left, top = world_to_tile(rect.left, rect.top)
        right, bottom = world_to_tile(rect.right - 1, rect.bottom - 1)
        for tx in range(left, right + 1):
            if vy > 0:
                ty = bottom
                if is_solid_tile(tx, ty):
                    rect.bottom = tile_to_world(tx, ty)[1]
            else:
                ty = top
                if is_solid_tile(tx, ty):
                    rect.top = tile_to_world(tx, ty)[1] + TILE

    rect.x += vx
    if vx != 0:
        left, top = world_to_tile(rect.left, rect.top)
        right, bottom = world_to_tile(rect.right - 1, rect.bottom - 1)
        # Check each tile along the vertical span of the rect
        for ty in range(top, bottom + 1):
            if vx > 0:
                tx = right
                if is_solid_tile(tx, ty):
                    # Collision moving right: snap rect flush to left edge of tile
                    rect.right = tile_to_world(tx, ty)[0]
                    vx = 0
            else:
                tx = left
                if is_solid_tile(tx, ty):
                    # Collision moving left: snap rect flush to right edge of tile
                    rect.left = tile_to_world(tx + 1, ty)[0]
                    vx = 0
    # --- Move along Y axis ---
    rect.y += vy
    if vy != 0:
        left, top = world_to_tile(rect.left, rect.top)
        right, bottom = world_to_tile(rect.right - 1, rect.bottom - 1)
        # Check each tile along the horizontal span of the rect
        for tx in range(left, right + 1):
            if vy > 0:
                ty = bottom
                if is_solid_tile(tx, ty):
                    # Collision moving down: snap rect flush to top edge of tile
                    rect.bottom = tile_to_world(tx, ty)[1]
                    vy = 0
            else:
                ty = top
                if is_solid_tile(tx, ty):
                    # Collision moving up: snap rect flush to bottom edge of tile
                    rect.top = tile_to_world(tx, ty + 1)[1]
                    vy = 0
    # Return corrected rect and possibly adjusted velocities
    return rect, vx, vy
