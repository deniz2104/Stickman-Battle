
import pygame
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont("arialblack", 35)


def load_texture(filename):
    possible_paths = [
        filename,
        f'../Textures/{filename}',
        f'Textures/{filename}',
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Textures', filename)
    ]

    for path in possible_paths:
        try:
            return pygame.image.load(path).convert_alpha()
        except (pygame.error, FileNotFoundError):
            continue

    print(f"Warning: Could not load texture '{filename}', using placeholder")
    placeholder = pygame.Surface((32, 32))
    placeholder.fill((255, 0, 255))
    return placeholder
