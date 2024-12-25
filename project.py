import pygame
import random
import math

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect =pygame.Rect(x,y,width,height)
        self.image=pygame.image.load('Textures/wall_texture.png').convert_alpha()

    def draw(self):
        pygame.draw.rect(screen,(255,255,255),self.rect)
        screen.blit(self.image,self.rect)
    
class Urzicarius(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.default_image = pygame.image.load('Textures/personaj_joc.png').convert_alpha()
        self.image = self.default_image
        self.mask = pygame.mask.from_surface(self.image)
        self.jump=False
        self.in_air=True
        self.flip = False
        self.velocity_y=0
        self.direction = 1
        self.image_left = pygame.image.load('Textures/personaj_joc_left.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.weapon_image=None
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
        self.rect.y+=dy
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
    
    def animate_idle(self):
        self.frame_duration = 2500  
        self.scale_range=(0.99,1.02)
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

class Weapon(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.mask =pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


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


pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Stickman Battle')
clock = pygame.time.Clock()
FPS = 60
GRAVITY=0.75

player = Urzicarius(100, SCREEN_HEIGHT // 1.5, 5)
enemy = Enemy(680, SCREEN_HEIGHT // 1.5, 1, 'Textures/big_boss.png')
wall_left=Wall(0,0,20, SCREEN_WIDTH)
wall_right=Wall(780,0,20, SCREEN_WIDTH)

weapon_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_group.add(enemy)

bullets = 0

WEAPON_SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(WEAPON_SPAWN_EVENT, 2000)

moving_left = False
moving_right = False

run = True
while run:

    clock.tick(FPS)
    screen.fill((144, 201, 120))
    wall_left.draw()
    wall_right.draw()
    if player.alive:
        player.draw()
        player.move(moving_left, moving_right)
    if not moving_left and not moving_right and player.alive:
        player.animate_idle()

    weapon_group.draw(screen)

    bullet_group.update()
    bullet_group.draw(screen)

    for enemy in enemy_group:
        enemy.update(player)
        enemy.attack(player)
        enemy.draw()

    font = pygame.font.SysFont(None, 36)
    bullet_text = font.render(f'Bullets: {bullets}', True, (0, 0, 0))
    screen.blit(bullet_text, (25, 40))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == WEAPON_SPAWN_EVENT and not weapon_collected and bullets == 0:
            if not weapon_group:
                x = random.randint(100, SCREEN_WIDTH - 50)
                y = SCREEN_HEIGHT // 1.5
                weapon = Weapon(x, y, 'Textures/gun.png')
                weapon_group.add(weapon)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_SPACE and bullets > 0 and player.alive:
                if  player.flip: 
                    bullet = Bullet(player.rect.left, player.rect.centery + 15, player.direction, 'Textures/bullet.png')
                else:  
                    bullet = Bullet(player.rect.right, player.rect.centery + 15, player.direction, 'Textures/bullet.png')
                bullet_group.add(bullet)
                bullets -= 1
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_w:
                player.jump=True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = False

    if pygame.sprite.spritecollide(player, weapon_group, True,pygame.sprite.collide_mask) and player.alive:
        bullets = 15
        weapon_collected = True
        player.weapon_image = pygame.image.load('Textures/gun.png')

    if bullets == 0:
        weapon_collected = False
        player.weapon_image = None

    
pygame.quit()
