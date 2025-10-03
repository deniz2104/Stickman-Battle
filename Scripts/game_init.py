import pygame, math
from Scripts.player import Player
from Scripts.enemy import Enemy
from Scripts.player import wall_left, wall_right
from Scripts.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, load_texture, screen, font


def create_context():
    pygame.init()
    pygame.display.set_caption('Urzicarius Battle')
    clock = pygame.time.Clock()
    player = Player(100, SCREEN_HEIGHT // 1.5, 5)
    player.weapon_damage = 20
    weapon_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    medkit_group = pygame.sprite.Group()
    enemy = Enemy(400, 425, 1, 'big_boss.png')
    enemy_group.add(enemy)

    bullets = 0
    enemies_killed = 0
    bg = load_texture("bg.png")
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
    weapon_collected = False

    game_state = "menu"

    from Scripts.button import Button
    start_button = Button("Start", 300, 200, 200, 50)
    restart_button = Button("Restart", 300, 200, 200, 50)
    quit_button = Button("Quit", 300, 300, 200, 50)
    resume_button = Button("Resume", 300, 200, 200, 50)

    menu_background = load_texture('win_and_first_background.png')
    game_over_image = load_texture('lose_screen.png')
    win_image = load_texture('win_screen.png')

    context = {
        'clock': clock,
        'player': player,
        'weapon_group': weapon_group,
        'bullet_group': bullet_group,
        'enemy_group': enemy_group,
        'medkit_group': medkit_group,
        'enemy': enemy,
        'bullets': bullets,
        'enemies_killed': enemies_killed,
        'bg': bg,
        'bg_width': bg_width,
        'bg_rect': bg_rect,
        'scroll': scroll,
        'tiles': tiles,
        'WEAPON_SPAWN_EVENT': WEAPON_SPAWN_EVENT,
        'MEDkit_SPAWN_EVENT': MEDkit_SPAWN_EVENT,
        'moving_left': moving_left,
        'moving_right': moving_right,
        'medkit_collected': medkit_collected,
        'weapon_collected': weapon_collected,
        'game_state': game_state,
        'start_button': start_button,
        'restart_button': restart_button,
        'quit_button': quit_button,
        'resume_button': resume_button,
        'menu_background': menu_background,
        'game_over_image': game_over_image,
        'win_image': win_image,
        'screen': screen,
        'font': font,
        'FPS': FPS,
        'SCREEN_WIDTH': SCREEN_WIDTH,
        'SCREEN_HEIGHT': SCREEN_HEIGHT,
        'wall_left': wall_left,
        'wall_right': wall_right,
    }

    return context
