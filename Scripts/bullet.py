import pygame
from variables_and_constants import enemy,wall_left,wall_right
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10 * direction

    def update(self):
        self.rect.x += self.speed
        if pygame.sprite.collide_mask(self, enemy):
            enemy.get_damage(40)
            self.kill()
        if self.rect.colliderect(wall_right) or self.rect.colliderect(wall_left):
            self.kill()