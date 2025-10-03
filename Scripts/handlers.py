import pygame
from Scripts.bullet import Bullet


def handle_menu_events(event, context):
    if event.type == pygame.QUIT:
        return {'run': False}
    if event.type == pygame.MOUSEBUTTONDOWN:
        if context['start_button'] and context['start_button'].is_clicked(event.pos):
            return {'game_state': 'running'}
        if context['quit_button'] and context['quit_button'].is_clicked(event.pos):
            return {'run': False}
    return {}


def handle_running_events(event, context):
    res = {}
    player = context['player']
    if event.type == pygame.QUIT:
        res['run'] = False

    if event.type == context['WEAPON_SPAWN_EVENT'] or event.type == context['MEDkit_SPAWN_EVENT']:
        return res

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            res['moving_left'] = True
        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            res['moving_right'] = True
        if event.key == pygame.K_SPACE and context['bullets'] > 0 and player.alive:
            if player.flip:
                bullet = Bullet(player.rect.left, player.rect.centery + 15, player.direction, 'bullet.png', damage=player.weapon_damage)
            else:
                bullet = Bullet(player.rect.right, player.rect.centery + 15, player.direction, 'bullet.png', damage=player.weapon_damage)
            context['bullet_group'].add(bullet)
            context['bullets'] -= 1
        if event.key == pygame.K_ESCAPE:
            res['game_state'] = 'paused'
        if event.key == pygame.K_w:
            player.jump = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            res['moving_left'] = False
        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            res['moving_right'] = False

    return res


def handle_paused_events(event, context):
    if event.type == pygame.QUIT:
        return {'run': False}
    if event.type == pygame.MOUSEBUTTONDOWN:
        if context['resume_button'] and context['resume_button'].is_clicked(event.pos):
            return {'game_state': 'running'}
        if context['quit_button'] and context['quit_button'].is_clicked(event.pos):
            return {'run': False}
    return {}


def handle_game_over_events(event, context):
    if event.type == pygame.QUIT:
        return {'run': False}
    if event.type == pygame.MOUSEBUTTONDOWN:
        if context['restart_button'] and context['restart_button'].is_clicked(event.pos):
            from Scripts.enemy import Enemy
            eg = context['enemy_group']
            eg.empty()
            enemy = Enemy(680, 340, 1, 'big_boss.png')
            eg.add(enemy)
            context['enemy'] = enemy
            
            pl = context['player']
            pl.rect.x = 100
            pl.alive = True
            pl.health = pl.max_health
            pl.displayed_health = pl.health
            context['bullets'] = 0
            context['weapon_collected'] = False
            context['medkit_collected'] = False
            context['weapon_group'].empty()
            context['medkit_group'].empty()
            pl.flip = False
            pl.direction = 1
            return {'game_state': 'menu', 'moving_left': False, 'moving_right': False}
        if context['quit_button'] and context['quit_button'].is_clicked(event.pos):
            return {'run': False}
    return {}
