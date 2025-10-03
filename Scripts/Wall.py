import pygame
from Scripts.config import screen, load_texture


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, texture_path='wall_texture.png'):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, width, height)

        self.image = load_texture(texture_path)
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, surface=None):
        if surface is None:
            surface = screen

        pygame.draw.rect(surface, (255, 255, 255), self.rect)
        surface.blit(self.image, self.rect)