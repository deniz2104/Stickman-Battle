import pygame
from project import screen
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect =pygame.Rect(x,y,width,height)
        self.image=pygame.image.load('wall_texture.png')

    def draw(self):
        pygame.draw.rect(screen,(255,255,255),self.rect)
        screen.blit(self.image,self.rect)