import pygame
from Scripts.config import screen
from Scripts.base_classes import MovableEntity


class Enemy(MovableEntity):
    def __init__(self, x, y, speed, image_path):
        super().__init__(x, y, image_path, max_health=200, speed=speed, health_bar_length=100)

    def _on_death(self):
        self.kill()
        self.rect = pygame.Rect(0, 0, 0, 0)

    def draw(self, surface=None):
        if surface is None:
            surface = screen

        if self.alive:
            surface.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

        x_offset = 50 if self.direction == 1 else 10
        bar_x = self.rect.x + x_offset
        bar_y = self.rect.y
        self._draw_health_bar(bar_x, bar_y, height=5, surface=surface)

    def update(self, *args, **kwargs):
        if args:
            player = args[0]
        else:
            return

        if self.alive:
            if player.rect.x > self.rect.x:
                self.rect.x += self.speed
                self.flip = True
                self.direction = -1
            elif player.rect.x < self.rect.x:
                self.rect.x -= self.speed
                self.flip = False
                self.direction = 1
        else:
            self.kill()
            self.rect = pygame.Rect(0, 0, 0, 0)

    def attack(self, player):
        if self.rect.colliderect(player.rect):
            player.get_damage(5)