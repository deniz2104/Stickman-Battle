from Scripts.config import screen, font

def draw_background(context):
    bg = context['bg']
    bg_width = context['bg_width']
    scroll = context['scroll']
    tiles = context['tiles']
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + scroll, 0))
        context['bg_rect'].x = i * bg_width + scroll


def draw_hud(context):
    bullet_text = font.render(f"Bullets: {context['bullets']}", True, (0, 0, 0))
    screen.blit(bullet_text, (25, 40))
