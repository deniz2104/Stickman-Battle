import pygame
from Scripts.game_init import create_context
from Scripts.spawn import spawn_weapon_if_needed, spawn_medkit_if_needed
from Scripts.handlers import handle_menu_events, handle_running_events, handle_paused_events, handle_game_over_events
from Scripts.render import draw_background, draw_hud
import pygame
from itertools import repeat


def make_screen_dynamic():
    s = -1
    for _ in range(0, 3):
        for offset_x in range(0, 20, 10):
            yield (offset_x * s, 0)
        for offset_x in range(20, 0, 10):
            yield (offset_x * s, 0)
        s *= -1
        while True:
            yield (0, 0)

def main():
    context = create_context()
    offset = repeat((0, 0))
    run = True

    while run:
        context['clock'].tick(context['FPS'])

        draw_background(context)
        context['scroll'] -= 3
        if abs(context['scroll']) > context['bg_width']:
            context['scroll'] = 0

        if context['game_state'] == 'menu':
            context['screen'].blit(context['menu_background'], (0, 0))
            if context['start_button']:
                context['start_button'].draw()
            if context['quit_button']:
                context['quit_button'].draw()

            for event in pygame.event.get():
                res = handle_menu_events(event, context)
                if 'run' in res and res['run'] is False:
                    run = False
                if 'game_state' in res:
                    context['game_state'] = res['game_state']

        elif context['game_state'] == 'running':
            context['wall_left'].draw()
            context['wall_right'].draw()
            if context['player'].alive:
                context['player'].draw()
                context['player'].move(context['moving_left'], context['moving_right'])
            if not context['moving_left'] and not context['moving_right'] and context['player'].alive:
                context['player'].animate_idle()

            context['weapon_group'].draw(context['screen'])
            context['medkit_group'].draw(context['screen'])
            context['bullet_group'].update(walls=[context['wall_left'], context['wall_right']], enemies=context['enemy_group'])
            context['bullet_group'].draw(context['screen'])

            for enemy in context['enemy_group']:
                enemy.update(context['player'])
                enemy.attack(context['player'])
                enemy.draw()

            draw_hud(context)

            for event in pygame.event.get():
                spawn_weapon_if_needed(event, context)
                spawn_medkit_if_needed(event, context)
                res = handle_running_events(event, context)
                if 'run' in res and res['run'] is False:
                    run = False
                if 'moving_left' in res:
                    context['moving_left'] = res['moving_left']
                if 'moving_right' in res:
                    context['moving_right'] = res['moving_right']
                if 'game_state' in res:
                    context['game_state'] = res['game_state']

            for weapon in list(context['weapon_group']):
                if weapon.use(context['player']) and context['player'].alive:
                    context['bullets'] = 15
                    context['weapon_collected'] = True

            for medkit in list(context['medkit_group']):
                if medkit.use(context['player']) and context['player'].alive:
                    context['medkit_collected'] = True
                    context['player'].medkit_image = context['menu_background']

            if context['bullets'] == 0:
                context['weapon_collected'] = False
                context['player'].weapon_image = None
            if context['medkit_collected']:
                context['medkit_collected'] = False
                context['player'].medkit_image = None

            if context['player'].health <= 0:
                context['game_state'] = 'game_over'

            if context['enemy'].health <= 0:
                context['game_state'] = 'win'

        elif context['game_state'] == 'paused':
            context['screen'].blit(context['menu_background'], (0, 0))
            if context['resume_button']:
                context['resume_button'].draw()
            if context['quit_button']:
                context['quit_button'].draw()

            for event in pygame.event.get():
                res = handle_paused_events(event, context)
                if 'run' in res and res['run'] is False:
                    run = False
                if 'game_state' in res:
                    context['game_state'] = res['game_state']

        elif context['game_state'] in ('game_over', 'win'):
            if context['restart_button']:
                context['restart_button'].draw()
            if context['quit_button']:
                context['quit_button'].draw()
            if context['game_state'] == 'game_over':
                game_over_text = context['font'].render('GAME OVER', True, (200, 200, 200))
                context['screen'].blit(game_over_text, (context['SCREEN_WIDTH'] // 2 - (game_over_text.get_width() / 2), context['SCREEN_HEIGHT'] // 5))
                context['screen'].blit(context['game_over_image'], (0, 0))
            else:
                win_text = context['font'].render('YOU WIN', True, (200, 200, 200))
                context['screen'].blit(win_text, (context['SCREEN_WIDTH'] // 2 - (win_text.get_width() / 2), context['SCREEN_HEIGHT'] // 5))
                context['screen'].blit(context['win_image'], (0, 0))

            for event in pygame.event.get():
                res = handle_game_over_events(event, context)
                if 'run' in res and res['run'] is False:
                    run = False
                if 'game_state' in res:
                    context['game_state'] = res['game_state']

        context['screen'].blit(context['screen'], next(offset))
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()