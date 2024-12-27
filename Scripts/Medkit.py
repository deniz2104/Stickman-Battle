import pygame
class Medkit(pygame.sprite.Sprite):
    def __init__(self,x, y,image_path):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert_alpha()  
        self.rect =self.image.get_rect()      
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center=(x,y)