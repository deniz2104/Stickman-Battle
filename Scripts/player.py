import pygame
from project import screen,wall_left,wall_right
class Urzicarius(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.default_image = pygame.image.load('personaj_joc.png')
        self.image = self.default_image
        self.flip = False
        self.direction = 1
        self.image_left = pygame.image.load('personaj_joc_left.png')
        self.rect = self.image.get_rect()
        self.weapon_image=None
        self.rect.center = (x, y)
        self.current_health = 1000
        self.max_health = 1000
        self.health_bar_length = 300
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_ratio_for_healthbar =self.max_health / self.health_bar_length 
        self.alive = True

    def draw(self):
        if self.alive:
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
            if self.weapon_image:
                if not self.flip:
                    screen.blit(self.weapon_image, (self.rect.centerx + 60, self.rect.centery))
                else:  
                    screen.blit(pygame.transform.flip(self.weapon_image, True, False), (self.rect.centerx - 100, self.rect.centery))
        self.basic_health()


    def move(self, moving_left, moving_right):
        if not self.alive:
            return

        dx = 0
        if moving_left:
            dx -= self.speed
            self.flip = True
            self.direction = -1
            if self.rect.colliderect(wall_left):
                self.rect.left = wall_left.rect.right
        elif moving_right:
            self.image = self.image_left
            dx += self.speed
            self.flip = False
            self.direction = 1
            if self.rect.colliderect(wall_right):
                self.rect.right = wall_right.rect.left
        else:
            self.image = self.default_image
        self.rect.x += dx

    def get_damage(self, amount):
        if self.alive:
            self.current_health -= amount
            if self.current_health <= 0:
                self.current_health = 0
                self.alive = False

    def get_health(self, amount):
        if self.alive:
            self.current_health += amount
            if self.current_health > self.max_health:
                self.current_health = self.max_health

    def basic_health(self):
        if not hasattr(self, 'displayed_health'):
            self.displayed_health = self.current_health

        if self.displayed_health > self.current_health:
            self.displayed_health -= 3 

        pygame.draw.rect(screen, (0, 255, 0), (25, 10, self.current_health / self.health_ratio, 20))
        pygame.draw.rect(screen, (255, 255, 255), (25, 10, self.health_bar_length, 20), 4)

        pygame.draw.rect(screen, (204, 160, 29), (25 + self.current_health / self.health_ratio, 10, 
                     (self.displayed_health - self.current_health) / self.health_ratio, 20))
        pygame.draw.rect(screen, (255, 255, 255), (25, 10, self.health_bar_length, 20), 4)

        if self.current_health < self.max_health / 2:
            pygame.draw.rect(screen, (255, 255, 0), (25, 10, self.current_health / self.health_ratio, 20))
            pygame.draw.rect(screen, (255, 255, 255),(25, 10, self.health_bar_length, 20), 4)
        if self.current_health < self.max_health / 4:
            pygame.draw.rect(screen, (255, 0, 0), (25, 10, self.current_health / self.health_ratio, 20))
            pygame.draw.rect(screen, (255, 255, 255), (25, 10, self.health_bar_length, 20), 4)

