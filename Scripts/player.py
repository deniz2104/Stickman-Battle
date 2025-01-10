import pygame
import math
from Wall import Wall
from variables_and_constants import screen,GRAVITY,SCREEN_WIDTH
wall_left=Wall(0,0,20, SCREEN_WIDTH)
wall_right=Wall(780,0,20, SCREEN_WIDTH)
class Urzicarius(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.default_image = pygame.image.load('../Textures/personaj_joc.png').convert_alpha()
        self.image = self.default_image
        self.mask = pygame.mask.from_surface(self.image)
        self.jump=False
        self.in_air=True
        self.flip = False
        self.displayed_health=False
        self.velocity_y=0
        self.direction = 1
        self.image_left = pygame.image.load('../Textures/personaj_joc_left.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.weapon_image=None
        self.medkit_image=None
        self.rect.center = (x, y)
        self.current_health = 1000
        self.max_health = 1000
        self.health_bar_length = 300
        self.health_ratio = self.max_health / self.health_bar_length
        self.alive = True
        self.frame = 1
        self.last_frame_update = 0
        self.frame_duration = 100

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
        dy = 0
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

        if self.jump==True and self.in_air==False:
            self.velocity_y = -11
            self.jump=False
            self.in_air=True

        self.velocity_y += GRAVITY
        if self.velocity_y > 10:
            self.velocity_y = 10
        dy += self.velocity_y

        if dy + self.rect.bottom > 500:
            dy = 500 - self.rect.bottom
            self.in_air=False
        else:
            self.in_air=True
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
            if not self.displayed_health:
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
    
    def animate_idle(self):
        self.frame_duration = 2500  
        self.scale_range=(0.97,1.03)
        now =pygame.time.get_ticks()  

        cycle_progress = (now % self.frame_duration) / self.frame_duration

        min_scale, max_scale = self.scale_range
        scale_factor = min_scale + (max_scale - min_scale) * (0.5 * (1 + math.sin(2 * math.pi * cycle_progress)))
        
        original_width, original_height = self.default_image.get_size()
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)

        self.image = pygame.transform.scale(self.default_image, (new_width, new_height))
        self.rect = self.image.get_rect(center=self.rect.center)  
        self.mask = pygame.mask.from_surface(self.image)
