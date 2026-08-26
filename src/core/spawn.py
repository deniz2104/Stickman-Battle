import random
from src.entities.weapon import Weapon
from src.entities.medkit import Medkit
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT


def spawn_weapon_if_needed(event, context):
    if event.type == context['WEAPON_SPAWN_EVENT'] and not context['weapon_collected'] and context['bullets'] == 0:
        if not context['weapon_group']:
            x = random.randint(100, SCREEN_WIDTH - 50)
            y = SCREEN_HEIGHT // 1.5
            weapon = Weapon(x, y, 'gun.png')
            context['weapon_group'].add(weapon)


def spawn_medkit_if_needed(event, context):
    if event.type == context['MEDkit_SPAWN_EVENT'] and not context['medkit_collected'] and context['player'].alive and context['player'].health < context['player'].max_health // 1.3:
        if not context['medkit_group']:
            x = random.randint(100, SCREEN_WIDTH - 50)
            y = SCREEN_HEIGHT // 1.5
            medkit = Medkit(x, y, 'medkit.png')
            context['medkit_group'].add(medkit)
