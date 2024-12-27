import pygame
from variables_and_constants import screen
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect =pygame.Rect(x,y,width,height)
        self.image=pygame.image.load('../Textures/wall_texture.png').convert_alpha()

    def draw(self):
        pygame.draw.rect(screen,(255,255,255),self.rect)
        screen.blit(self.image,self.rect)