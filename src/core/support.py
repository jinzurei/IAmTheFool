"""
Support functions for loading CSV maps and sprite animations
"""

import csv
import pygame

def load_csv_layout(path):
    """
    Load CSV layout file and return as list of lists
    CSV format: '0' or '-1' = empty; any other integer = solid tile index
    """
    terrain_map = []
    
    with open(path, 'r') as file:
        layout = csv.reader(file, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
    
    return terrain_map

def load_sprite_frames(image_path, frame_width, frame_height, num_frames):
    """
    Load and cut sprite sheet into individual frames
    Returns list of pygame surfaces
    """
    sprite_sheet = pygame.image.load(image_path).convert_alpha()
    frames = []
    
    for i in range(num_frames):
        frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
        frame_surface.blit(sprite_sheet, (0, 0), frame_rect)
        frames.append(frame_surface)
    
    return frames

def load_vertical_sprite_frames(image_path, frame_width, frame_height, num_frames):
    """
    Load vertical sprite sheet where frames are stacked top to bottom
    Returns list of pygame surfaces
    """
    sprite_sheet = pygame.image.load(image_path).convert_alpha()
    frames = []
    
    for i in range(num_frames):
        frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        frame_rect = pygame.Rect(0, i * frame_height, frame_width, frame_height)
        frame_surface.blit(sprite_sheet, (0, 0), frame_rect)
        frames.append(frame_surface)
    
    return frames

def load_individual_frames(file_paths):
    """
    Load individual image files as animation frames
    Returns list of pygame surfaces
    """
    frames = []
    for path in file_paths:
        try:
            frame = pygame.image.load(path).convert_alpha()
            frames.append(frame)
        except pygame.error as e:
            print(f"Could not load frame {path}: {e}")
    return frames