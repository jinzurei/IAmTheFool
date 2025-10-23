import csv
import pygame


def load_aligned_vertical_sprite_frames(
    image_path, frame_width, frame_height, num_frames, align_size=(48, 48)
):
    from src.core.sprite_align import align_frame_to_midbottom

    sprite_sheet = pygame.image.load(image_path).convert_alpha()
    frames = []
    for i in range(num_frames):
        frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        frame_rect = pygame.Rect(0, i * frame_height, frame_width, frame_height)
        frame_surface.blit(sprite_sheet, (0, 0), frame_rect)
        aligned = align_frame_to_midbottom(frame_surface, align_size)
        frames.append(aligned)
    return frames


def load_csv_layout(path):
    terrain_map = []
    with open(path, "r") as file:
        layout = csv.reader(file, delimiter=",")
        for row in layout:
            terrain_map.append(list(row))
    return terrain_map


def load_sprite_frames(image_path, frame_width, frame_height, num_frames):
    sprite_sheet = pygame.image.load(image_path).convert_alpha()
    frames = []
    for i in range(num_frames):
        frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
        frame_surface.blit(sprite_sheet, (0, 0), frame_rect)
        frames.append(frame_surface)
    return frames


def load_vertical_sprite_frames(image_path, frame_width, frame_height, num_frames):
    sprite_sheet = pygame.image.load(image_path).convert_alpha()
    frames = []
    for i in range(num_frames):
        frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        frame_rect = pygame.Rect(0, i * frame_height, frame_width, frame_height)
        frame_surface.blit(sprite_sheet, (0, 0), frame_rect)
        frames.append(frame_surface)
    return frames


def load_individual_frames(file_paths):
    frames = []
    for path in file_paths:
        try:
            frame = pygame.image.load(path).convert_alpha()
            frames.append(frame)
        except pygame.error as e:
            print(f"Could not load frame {path}: {e}")
    return frames
