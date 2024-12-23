import pygame
import random

class Urzicarius(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.default_image = pygame.image.load('personaj_joc.png')
        self.image = self.default_image
        self.image_left = pygame.image.load('personaj_joc_left.png')
        self.image_right = pygame.image.load('personaj_joc_right.png')
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
            screen.blit(self.image, self.rect)
            if self.weapon_image:
                screen.blit(self.weapon_image, (self.rect.centerx + 50, self.rect.centery))
            self.basic_health()

    def move(self, moving_left, moving_right):
        if not self.alive:
            return

        dx = 0
        if moving_left:
            self.image = self.image_left
            dx -= self.speed
        elif moving_right:
            self.image = self.image_right
            dx += self.speed
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

        pygame.draw.rect(screen, (0, 255, 0), (10, 10, self.current_health / self.health_ratio, 20))
        pygame.draw.rect(screen, (255, 255, 255), (10, 10, self.health_bar_length, 20), 4)

        pygame.draw.rect(screen, (204, 160, 29), (10 + self.current_health / self.health_ratio, 10, 
                     (self.displayed_health - self.current_health) / self.health_ratio, 20))
        pygame.draw.rect(screen, (255, 255, 255), (10, 10, self.health_bar_length, 20), 4)

        if self.current_health < self.max_health / 2:
            pygame.draw.rect(screen, (255, 255, 0), (10, 10, self.current_health / self.health_ratio, 20))
            pygame.draw.rect(screen, (255, 255, 255), (10, 10, self.health_bar_length, 20), 4)
        if self.current_health < self.max_health / 4:
            pygame.draw.rect(screen, (255, 0, 0), (10, 10, self.current_health / self.health_ratio, 20))
            pygame.draw.rect(screen, (255, 255, 255), (10, 10, self.health_bar_length, 20), 4)


class Weapon(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10 * direction

    def update(self):
        self.rect.x += self.speed
        if self.rect.colliderect(enemy.rect):
            enemy.get_damage(40)
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.health = 200
        self.max_health = 200
        self.health_bar_length = 100
        self.health_ratio = self.max_health / self.health_bar_length

    def draw(self):
        screen.blit(self.image, self.rect)
        self.basic_health()

    def update(self, player):
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
            self.kill()

    def basic_health(self):
        if not hasattr(self, 'displayed_health'):
            self.displayed_health = self.health

        if self.displayed_health > self.health:
            self.displayed_health -= 1

        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x + 45, self.rect.y, self.health / self.health_ratio, 5))
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x + 45, self.rect.y, self.health_bar_length, 5), 1)

        pygame.draw.rect(screen, (204, 160, 29), (self.rect.x + 45 + self.health / self.health_ratio, self.rect.y, 
                     (self.displayed_health - self.health) / self.health_ratio, 5))
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x+45,self.rect.y , self.health_bar_length, 5), 1)

        if self.health < self.max_health / 2:
            pygame.draw.rect(screen, (255, 255, 0), (self.rect.x + 45, self.rect.y, self.health / self.health_ratio, 5))
            pygame.draw.rect(screen, (255, 255, 255), (self.rect.x + 45, self.rect.y, self.health_bar_length, 5), 1)
        if self.health < self.max_health / 4:
            pygame.draw.rect(screen, (255, 0, 0), (self.rect.x + 45, self.rect.y, self.health / self.health_ratio, 5))
            pygame.draw.rect(screen, (255, 255, 255), (self.rect.x + 45, self.rect.y, self.health_bar_length, 5), 1)


pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Stickman Battle')
clock = pygame.time.Clock()
FPS = 60

player = Urzicarius(100, SCREEN_HEIGHT // 2, 5)
enemy = Enemy(700, SCREEN_HEIGHT // 2, 1, 'big_boss.png')
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

    if player.alive:
        player.draw()
        player.move(moving_left, moving_right)

    weapon_group.draw(screen)

    bullet_group.update()
    bullet_group.draw(screen)

    for enemy in enemy_group:
        enemy.update(player)
        enemy.attack(player)
        enemy.draw()

    font = pygame.font.SysFont(None, 36)
    bullet_text = font.render(f'Bullets: {bullets}', True, (0, 0, 0))
    screen.blit(bullet_text, (10, 40))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == WEAPON_SPAWN_EVENT and not weapon_collected and bullets == 0:
            if not weapon_group:
                x = random.randint(100, SCREEN_WIDTH - 50)
                y = SCREEN_HEIGHT // 2
                weapon = Weapon(x, y, 'gun.png')
                weapon_group.add(weapon)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_SPACE and bullets > 0 and player.alive:
                bullet = Bullet(player.rect.centerx, player.rect.centery, 1, 'bullet.png')
                bullet_group.add(bullet)
                bullets -= 1
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = False

    if pygame.sprite.spritecollide(player, weapon_group, True) and player.alive:
        bullets = 15
        weapon_collected = True
        player.weapon_image = pygame.image.load('gun.png')

    if bullets == 0:
        weapon_collected = False
        player.weapon_image = None
pygame.quit()
