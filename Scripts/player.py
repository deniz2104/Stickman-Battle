import pygame
import math
from Scripts.wall import Wall
from Scripts.config import screen, SCREEN_WIDTH, load_texture
from Scripts.base_classes import MovableEntity

wall_left = Wall(0, 0, 20, SCREEN_WIDTH)
wall_right = Wall(780, 0, 20, SCREEN_WIDTH)


class Player(MovableEntity):
    def __init__(self, x, y, speed):
        super().__init__(x, y, 'personaj_joc.png', max_health=1000,
                         speed=speed, health_bar_length=300)
        self._load_additional_images()
        self._setup_physics()
        self._setup_animation()

    def _load_additional_images(self):
        self.default_image = self.image
        try:
            self.image_left = load_texture('personaj_joc_left.png')
        except Exception:
            self.image_left = self.default_image

    def _setup_physics(self):
        self.jump = False
        self.in_air = True
        self.velocity_y = 0

    def _setup_animation(self):
        self.weapon_image = None
        self.medkit_image = None
        self.frame = 1
        self.last_frame_update = 0
        self.frame_duration = 100

    def _on_death(self):
        pass

    def draw(self, surface=None):
        if surface is None:
            surface = screen

        if self.alive:
            surface.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
            self._draw_weapon(surface)
            self._draw_health_bar(25, 10, height=20, surface=surface)

    def _draw_weapon(self, surface):
        if self.weapon_image:
            if not self.flip:
                surface.blit(self.weapon_image, (self.rect.centerx + 60, self.rect.centery))
            else:
                surface.blit(pygame.transform.flip(self.weapon_image, True, False),
                           (self.rect.centerx - 100, self.rect.centery))

    def update(self, *args, **kwargs):
        moving_left = kwargs.get('moving_left', False)
        moving_right = kwargs.get('moving_right', False)
        self.move(moving_left, moving_right)

    def move(self, moving_left, moving_right):
        if not self.alive:
            return

        dx = 0

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

    def animate_idle(self):
        self.frame_duration = 2500
        scale_range = (0.97, 1.03)
        now = pygame.time.get_ticks()

        cycle_progress = (now % self.frame_duration) / self.frame_duration

        min_scale, max_scale = scale_range
        scale_factor = min_scale + (max_scale - min_scale) * (
            0.5 * (1 + math.sin(2 * math.pi * cycle_progress)))

        original_width, original_height = self.default_image.get_size()
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)

        self.image = pygame.transform.scale(self.default_image, (new_width, new_height))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
