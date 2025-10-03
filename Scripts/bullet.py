import pygame
from Scripts.config import SCREEN_HEIGHT, load_texture

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, image_path, damage=40):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_texture(image_path)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10 * direction
        self.damage = damage

    def update(self, walls=None, enemies=None):
        self.rect.x += self.speed

        if enemies:
            for enemy in enemies:
                if pygame.sprite.collide_mask(self, enemy):
                    enemy.get_damage(self.damage)
                    self.kill()
                    return

        if walls:
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    self.kill()
                    return

        if self.rect.x < -50 or self.rect.x > SCREEN_HEIGHT + 50:
            self.kill()