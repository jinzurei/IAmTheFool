import pygame


def align_frame_to_midbottom(frame, canvas_size=(48, 48)):
    bbox = frame.get_bounding_rect()
    cropped = frame.subsurface(bbox).copy()
    canvas = pygame.Surface(canvas_size, pygame.SRCALPHA)
    canvas_rect = canvas.get_rect()
    dx = canvas_rect.midbottom[0] - cropped.get_rect().midbottom[0]
    dy = canvas_rect.midbottom[1] - cropped.get_rect().midbottom[1]
    canvas.blit(cropped, (dx, dy))
    return canvas
