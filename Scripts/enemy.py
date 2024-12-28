import pygame
from variables_and_constants import screen
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.health = 200
        self.max_health = 200
        self.health_bar_length = 100
        self.health_ratio = self.max_health / self.health_bar_length

    def draw(self):
        if self.alive:
            screen.blit(self.image, self.rect)
            self.basic_health()
    def update(self, player):
        if self.alive:
            if player.rect.x > self.rect.x:
                self.rect.x += self.speed
            elif player.rect.x < self.rect.x:
                self.rect.x -= self.speed

    def attack(self, player):
        if self.rect.colliderect(player.rect):
            player.get_damage(5)

    def get_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.kill()
            self.rect = pygame.Rect(0, 0, 0, 0)

    def basic_health(self):
        if not hasattr(self, 'displayed_health'):
            self.displayed_health = self.health

        if self.displayed_health > self.health:
            self.displayed_health -= 1

        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x + 50, self.rect.y, self.health / self.health_ratio, 5))
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x + 50, self.rect.y, self.health_bar_length, 5), 1)

        pygame.draw.rect(screen, (204, 160, 29), (self.rect.x + 50 + self.health / self.health_ratio, self.rect.y, 
                     (self.displayed_health - self.health) / self.health_ratio, 5))
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x+50,self.rect.y , self.health_bar_length, 5), 1)

        if self.health < self.max_health / 2:
            pygame.draw.rect(screen, (255, 255, 0), (self.rect.x + 50, self.rect.y, self.health / self.health_ratio, 5))
            pygame.draw.rect(screen, (255, 255, 255), (self.rect.x + 50, self.rect.y, self.health_bar_length, 5), 1)
        if self.health < self.max_health / 4:
            pygame.draw.rect(screen, (255, 0, 0), (self.rect.x + 50, self.rect.y, self.health / self.health_ratio, 5))
            pygame.draw.rect(screen, (255, 255, 255), (self.rect.x + 50, self.rect.y, self.health_bar_length, 5), 1)