from abc import ABC, abstractmethod
import pygame
from Scripts.config import screen, load_texture

class GameObject(pygame.sprite.Sprite, ABC): 
    def __init__(self, x, y, image_path=None):
        pygame.sprite.Sprite.__init__(self)
        if image_path:
            self._load_image(image_path)
        self._setup_position(x, y)

    def _load_image(self, image_path):
        try:
            self.image = load_texture(image_path)
            self.mask = pygame.mask.from_surface(self.image)
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            self.image = pygame.Surface((32, 32))
            self.image.fill((255, 0, 255))
            self.mask = pygame.mask.from_surface(self.image)

    def _setup_position(self, x, y):
        if hasattr(self, 'image'):
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
        else:
            self.rect = pygame.Rect(x, y, 32, 32) 

    @abstractmethod
    def draw(self, surface=None):
        pass


class HealthEntity(GameObject):
    def __init__(self, x, y, image_path, max_health, health_bar_length=100):
        super().__init__(x, y, image_path)
        self._setup_health(max_health, health_bar_length)

    def _setup_health(self, max_health, health_bar_length):
        self.max_health = max_health
        self.health = max_health
        self.alive = True
        self.health_bar_length = health_bar_length
        self.health_ratio = self.max_health / self.health_bar_length
        self.displayed_health = self.health

    def get_damage(self, amount):
        if self.alive:
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.alive = False
                self._on_death()

    def get_health(self, amount):
        if self.alive:
            self.health += amount
            if self.health > self.max_health:
                self.health = self.max_health

    def _draw_health_bar(self, x, y, height=5, surface=None):
        if not self.alive:
            return
            
        if surface is None:
            surface = screen

        if self.displayed_health > self.health:
            self.displayed_health -= max(1, (self.displayed_health - self.health) * 0.1)

        pygame.draw.rect(surface, (0, 255, 0), 
                        (x, y, self.health / self.health_ratio, height))
        
        if self.displayed_health > self.health:
            pygame.draw.rect(surface, (204, 160, 29), 
                            (x + self.health / self.health_ratio, y, 
                             (self.displayed_health - self.health) / self.health_ratio, height))
        if self.health < self.max_health / 2:
            pygame.draw.rect(surface, (255, 255, 0), 
                            (x, y, self.health / self.health_ratio, height))
        if self.health < self.max_health / 4:
            pygame.draw.rect(surface, (255, 0, 0), 
                            (x, y, self.health / self.health_ratio, height))
        
        pygame.draw.rect(surface, (255, 255, 255), 
                        (x, y, self.health_bar_length, height), 1)

    @abstractmethod
    def _on_death(self):
        pass


class MovableEntity(HealthEntity):
    
    def __init__(self, x, y, image_path, max_health, speed, health_bar_length=100):
        super().__init__(x, y, image_path, max_health, health_bar_length)
        self._setup_movement(speed)

    def _setup_movement(self, speed):
        self.speed = speed
        self.direction = 1 
        self.flip = False

    @abstractmethod
    def update(self, *args, **kwargs):
        pass


class CollectibleItem(GameObject):
    
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path)

    def draw(self, surface=None):
        if surface is None:
            surface = screen
        surface.blit(self.image, self.rect)

    @abstractmethod
    def use(self, player):
        pass