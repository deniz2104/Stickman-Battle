import pygame, math, random, time
from player import Urzicarius
from enemy import Enemy
from bullet import Bullet
from Medkit import Medkit
from player import wall_left, wall_right
from weapon import Weapon
from variables_and_constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from Button import Button,screen,font

pygame.init()
pygame.display.set_caption('Urzicarius Battle')
clock = pygame.time.Clock()
player = Urzicarius(100, SCREEN_HEIGHT // 1.5, 5)
player.weapon_damage = 20
weapon_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
medkit_group = pygame.sprite.Group()
enemy = Enemy(400, 425, 1, '../Textures/big_boss.png')
enemy_group.add(enemy)

bullets = 0
bg = pygame.image.load("../Textures/bg.png").convert()
bg_width = bg.get_width()
bg_rect = bg.get_rect()

scroll = 0
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1

WEAPON_SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(WEAPON_SPAWN_EVENT, 2000)

MEDkit_SPAWN_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(MEDkit_SPAWN_EVENT, 3000)

moving_left = False
moving_right = False
medkit_collected = False

game_state = "menu"

start_button = Button("Start", 300, 200, 200, 50)
restart_button = Button("Restart", 300, 200, 200, 50)
quit_button = Button("Quit", 300, 300, 200, 50)
resume_button = Button("Resume", 300, 200, 200, 50)
menu_background = pygame.image.load('../Textures/win_and_first_background.png').convert_alpha()
game_over_image = pygame.image.load('../Textures/lose_screen.png').convert_alpha()
win_image = pygame.image.load('../Textures/win_screen.png').convert_alpha()

run = True

while run:
    clock.tick(FPS)
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + scroll, 0))
        bg_rect.x = i * bg_width + scroll

    scroll -= 3

    if abs(scroll) > bg_width:
        scroll = 0

    if game_state == "menu":
        start_button.draw()
        quit_button.draw()
        screen.blit(menu_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(event.pos):
                    game_state = "running"
                elif quit_button.is_clicked(event.pos):
                    run = False

    elif game_state == "running":
        wall_left.draw()
        wall_right.draw()
        if player.alive:
            player.draw()
            player.move(moving_left, moving_right)
        if not moving_left and not moving_right and player.alive:
            player.animate_idle()

        weapon_group.draw(screen)
        medkit_group.draw(screen)
        bullet_group.update()
        bullet_group.draw(screen)

        for enemy in enemy_group:
            enemy.update(player)
            enemy.attack(player)
            enemy.draw()

        for bullet in bullet_group:
            hit_enemy = pygame.sprite.spritecollideany(bullet, enemy_group, pygame.sprite.collide_mask)
            if hit_enemy:
                hit_enemy.health -= player.weapon_damage 
                bullet.kill()  

        bullet_text = font.render(f'Bullets: {bullets}', True, (0, 0, 0))
        screen.blit(bullet_text, (25, 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == WEAPON_SPAWN_EVENT and not weapon_collected and bullets == 0:
                if not weapon_group:
                    x = random.randint(100, SCREEN_WIDTH - 50)
                    y = SCREEN_HEIGHT // 1.5
                    weapon = Weapon(x, y, '../Textures/gun.png')
                    weapon_group.add(weapon)
            if event.type == MEDkit_SPAWN_EVENT and not medkit_collected and player.alive and player.current_health < player.max_health // 1.3:
                if not medkit_group:
                    x = random.randint(100, SCREEN_WIDTH - 50)
                    y = SCREEN_HEIGHT // 1.5
                    medkit = Medkit(x, y, '../Textures/medkit.png')
                    medkit_group.add(medkit)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    moving_left = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    moving_right = True
                if event.key == pygame.K_SPACE and bullets > 0 and player.alive:
                    if player.flip:
                        bullet = Bullet(player.rect.left, player.rect.centery + 15, player.direction, '../Textures/bullet.png')
                    else:
                        bullet = Bullet(player.rect.right, player.rect.centery + 15, player.direction, '../Textures/bullet.png')
                    bullet_group.add(bullet)
                    bullets -= 1
                if event.key == pygame.K_ESCAPE:
                    game_state = "paused"
                if event.key == pygame.K_w:
                    player.jump = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    moving_left = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    moving_right = False

        if pygame.sprite.spritecollide(player, weapon_group, True, pygame.sprite.collide_mask) and player.alive:
            bullets = 15
            weapon_collected = True
            player.weapon_image = pygame.image.load('../Textures/gun.png')

        if pygame.sprite.spritecollide(player, medkit_group, True, pygame.sprite.collide_mask) and player.alive:
            player.get_health(100)
            medkit_collected = True
            player.medkit_image = pygame.image.load('../Textures/medkit.png')

        if bullets == 0:
            weapon_collected = False
            player.weapon_image = None
        if medkit_collected:
            medkit_collected = False
            player.medkit_image = None

        if player.current_health <= 0:
            game_state = "game_over"

        if enemy.health <= 0:
            game_state = "win"

    elif game_state == "paused":
        screen.blit(menu_background, (0, 0))
        resume_button.draw()
        quit_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.is_clicked(event.pos):
                    game_state = "running"
                if quit_button.is_clicked(event.pos):
                    run = False

    elif game_state == "game_over" or game_state == "win":
        restart_button.draw()
        quit_button.draw()
        if game_state == "game_over":
            game_over_text = font.render('GAME OVER', True, (200, 200, 200))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - (game_over_text.get_width() / 2), SCREEN_HEIGHT // 5))
            screen.blit(game_over_image, (0, 0))
        else:
            win_text = font.render('YOU WIN', True, (200, 200, 200))
            screen.blit(win_text, (SCREEN_WIDTH // 2 - (win_text.get_width() / 2), SCREEN_HEIGHT // 5))
            screen.blit(win_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.is_clicked(event.pos):
                    enemy_group.empty()
                    enemy = Enemy(200, 200, 1.2, '../Textures/big_boss.png')
                    enemy.health = enemy.max_health
                    enemy_group.add(enemy)
                    enemy.rect.y = 340
                    player.rect.x = 100
                    player.alive = True
                    player.current_health = player.max_health
                    player.displayed_health=player.current_health
                    bullets = 0
                    weapon_collected = False
                    medkit_collected = False
                    weapon_group.empty()
                    medkit_group.empty()
                    enemy.rect.x = 680
                    game_state = "menu"
                    moving_left = False
                    moving_right = False
                    player.flip = False
                    player.direction = 1  
                if quit_button.is_clicked(event.pos):
                    run = False
    pygame.display.update()    
pygame.quit()